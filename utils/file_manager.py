"""
=================================================
GERENCIADOR DE ARQUIVOS
=================================================

Este módulo centraliza todas as operações de arquivo
do sistema, incluindo carregamento, salvamento e
backup de dados em formato JSON.

=================================================
"""

import json
import os
import shutil
from datetime import datetime
from tkinter import messagebox
from core.config import config


class FileManager:
    """
    Gerenciador centralizado de arquivos.
    
    Responsável por todas as operações de I/O do sistema,
    incluindo backup automático e recuperação de dados.
    """
    
    def __init__(self):
        """Inicializa o gerenciador de arquivos."""
        self.backup_dir = "backups"
        self.ensure_directories()
    
    def ensure_directories(self):
        """
        Garante que todos os diretórios necessários existem.
        """
        directories = [config.DATA_DIR, self.backup_dir]
        
        for directory in directories:
            if directory and not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except Exception as e:
                    print(f"Erro ao criar diretório {directory}: {e}")
    
    def load_json_data(self, filename, default_data=None):
        """
        Carrega dados de um arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo
            default_data: Dados padrão se arquivo não existir
            
        Returns:
            Dados carregados ou dados padrão
        """
        if default_data is None:
            default_data = {}
        
        filepath = config.get_file_path(filename)
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✓ Dados carregados de {filename}")
                    return data
            else:
                print(f"⚠ Arquivo {filename} não existe, criando com dados padrão")
                self.save_json_data(filename, default_data)
                return default_data
                
        except json.JSONDecodeError as e:
            print(f"✗ Erro JSON em {filename}: {e}")
            messagebox.showerror(
                "Erro de Dados", 
                f"Arquivo {filename} corrompido.\n"
                f"Verificando backup..."
            )
            return self.restore_from_backup(filename, default_data)
            
        except Exception as e:
            print(f"✗ Erro ao carregar {filename}: {e}")
            messagebox.showerror(
                "Erro de Arquivo", 
                f"Erro ao carregar {filename}: {str(e)}"
            )
            return default_data
    
    def save_json_data(self, filename, data):
        """
        Salva dados em um arquivo JSON.
        
        Args:
            filename (str): Nome do arquivo
            data: Dados para salvar
            
        Returns:
            bool: True se salvamento bem-sucedido
        """
        filepath = config.get_file_path(filename)
        
        try:
            # Criar backup antes de salvar
            if os.path.exists(filepath):
                self.create_backup(filename)
            
            # Salvar dados
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Dados salvos em {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Erro ao salvar {filename}: {e}")
            messagebox.showerror(
                "Erro de Salvamento", 
                f"Erro ao salvar {filename}: {str(e)}"
            )
            return False
    
    def create_backup(self, filename):
        """
        Cria backup de um arquivo.
        
        Args:
            filename (str): Nome do arquivo para backup
        """
        try:
            source = config.get_file_path(filename)
            if not os.path.exists(source):
                return
            
            # Nome do backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.splitext(filename)[0]}_{timestamp}.json"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Copiar arquivo
            shutil.copy2(source, backup_path)
            print(f"✓ Backup criado: {backup_name}")
            
            # Limpar backups antigos (manter apenas 5 mais recentes)
            self.cleanup_old_backups(filename)
            
        except Exception as e:
            print(f"⚠ Erro ao criar backup de {filename}: {e}")
    
    def cleanup_old_backups(self, filename, keep_count=5):
        """
        Remove backups antigos, mantendo apenas os mais recentes.
        
        Args:
            filename (str): Nome base do arquivo
            keep_count (int): Número de backups para manter
        """
        try:
            base_name = os.path.splitext(filename)[0]
            backup_files = []
            
            # Listar backups do arquivo
            for file in os.listdir(self.backup_dir):
                if file.startswith(base_name + "_") and file.endswith(".json"):
                    filepath = os.path.join(self.backup_dir, file)
                    mtime = os.path.getmtime(filepath)
                    backup_files.append((filepath, mtime))
            
            # Ordenar por data (mais recentes primeiro)
            backup_files.sort(key=lambda x: x[1], reverse=True)
            
            # Remover backups excedentes
            for filepath, _ in backup_files[keep_count:]:
                os.remove(filepath)
                print(f"✓ Backup antigo removido: {os.path.basename(filepath)}")
                
        except Exception as e:
            print(f"⚠ Erro ao limpar backups: {e}")
    
    def restore_from_backup(self, filename, default_data):
        """
        Restaura arquivo de backup mais recente.
        
        Args:
            filename (str): Nome do arquivo
            default_data: Dados padrão se não houver backup
            
        Returns:
            Dados restaurados ou dados padrão
        """
        try:
            base_name = os.path.splitext(filename)[0]
            backup_files = []
            
            # Listar backups disponíveis
            if os.path.exists(self.backup_dir):
                for file in os.listdir(self.backup_dir):
                    if file.startswith(base_name + "_") and file.endswith(".json"):
                        filepath = os.path.join(self.backup_dir, file)
                        mtime = os.path.getmtime(filepath)
                        backup_files.append((filepath, mtime))
            
            if backup_files:
                # Pegar backup mais recente
                latest_backup = max(backup_files, key=lambda x: x[1])[0]
                
                with open(latest_backup, 'r', encoding='utf-8') as f:
                    restored_data = json.load(f)
                
                # Restaurar arquivo principal
                self.save_json_data(filename, restored_data)
                
                messagebox.showinfo(
                    "Backup Restaurado", 
                    f"Arquivo {filename} foi restaurado do backup:\n"
                    f"{os.path.basename(latest_backup)}"
                )
                
                return restored_data
            else:
                messagebox.showwarning(
                    "Sem Backup", 
                    f"Não há backup disponível para {filename}.\n"
                    "Usando dados padrão."
                )
                return default_data
                
        except Exception as e:
            print(f"✗ Erro ao restaurar backup: {e}")
            messagebox.showerror(
                "Erro de Restauração", 
                f"Erro ao restaurar backup: {str(e)}\n"
                "Usando dados padrão."
            )
            return default_data
    
    def export_data(self, export_path):
        """
        Exporta todos os dados do sistema.
        
        Args:
            export_path (str): Caminho para exportação
            
        Returns:
            bool: True se exportação bem-sucedida
        """
        try:
            export_data = {
                'export_date': datetime.now().isoformat(),
                'app_version': config.APP_VERSION,
                'data': {}
            }
            
            # Coletar todos os dados
            files = [
                config.USUARIOS_FILE,
                config.CLIENTES_FILE,
                config.CORTES_FILE,
                config.AGENDAMENTOS_FILE
            ]
            
            for filename in files:
                filepath = config.get_file_path(filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        export_data['data'][filename] = json.load(f)
            
            # Salvar exportação
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            messagebox.showinfo(
                "Exportação Concluída", 
                f"Dados exportados com sucesso para:\n{export_path}"
            )
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Erro de Exportação", 
                f"Erro ao exportar dados: {str(e)}"
            )
            return False
    
    def import_data(self, import_path):
        """
        Importa dados de arquivo de exportação.
        
        Args:
            import_path (str): Caminho do arquivo de importação
            
        Returns:
            bool: True se importação bem-sucedida
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            # Validar estrutura
            if 'data' not in imported_data:
                raise ValueError("Formato de arquivo inválido")
            
            # Criar backup antes de importar
            for filename in imported_data['data'].keys():
                if os.path.exists(config.get_file_path(filename)):
                    self.create_backup(filename)
            
            # Importar dados
            for filename, data in imported_data['data'].items():
                self.save_json_data(filename, data)
            
            messagebox.showinfo(
                "Importação Concluída", 
                f"Dados importados com sucesso!\n"
                f"Data da exportação: {imported_data.get('export_date', 'N/A')}\n"
                f"Versão: {imported_data.get('app_version', 'N/A')}"
            )
            return True
            
        except Exception as e:
            messagebox.showerror(
                "Erro de Importação", 
                f"Erro ao importar dados: {str(e)}"
            )
            return False
    
    def get_file_info(self, filename):
        """
        Obtém informações sobre um arquivo.
        
        Args:
            filename (str): Nome do arquivo
            
        Returns:
            dict: Informações do arquivo
        """
        filepath = config.get_file_path(filename)
        
        try:
            if os.path.exists(filepath):
                stat = os.stat(filepath)
                return {
                    'exists': True,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'created': datetime.fromtimestamp(stat.st_ctime)
                }
            else:
                return {'exists': False}
        except Exception as e:
            return {'exists': False, 'error': str(e)}


# =================================================
# INSTÂNCIA GLOBAL DO GERENCIADOR DE ARQUIVOS
# =================================================
file_manager = FileManager()
