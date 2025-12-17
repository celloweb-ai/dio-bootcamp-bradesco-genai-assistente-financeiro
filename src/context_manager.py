"""Gerenciador de contexto conversacional.

Mantém histórico e contexto das interações do usuário
para proporcionar experiência personalizada.
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class ConversationContext:
    """Gerencia contexto e histórico de conversações."""
    
    def __init__(self, user_id: Optional[str] = None):
        """Inicializa gerenciador de contexto.
        
        Args:
            user_id: Identificador único do usuário
        """
        self.user_id = user_id or "default_user"
        self.session_start = datetime.now()
        self.conversation_history: List[Dict] = []
        self.user_preferences: Dict = {}
        self.context_data: Dict = {}
        
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Adiciona mensagem ao histórico.
        
        Args:
            role: Papel (user/assistant/system)
            content: Conteúdo da mensagem
            metadata: Metadados adicionais
        """
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.conversation_history.append(message)
    
    def get_recent_messages(self, count: int = 10) -> List[Dict]:
        """Retorna mensagens recentes.
        
        Args:
            count: Número de mensagens a retornar
            
        Returns:
            Lista com mensagens mais recentes
        """
        return self.conversation_history[-count:]
    
    def set_preference(self, key: str, value: any):
        """Define preferência do usuário.
        
        Args:
            key: Chave da preferência
            value: Valor da preferência
        """
        self.user_preferences[key] = value
    
    def get_preference(self, key: str, default: any = None) -> any:
        """Obtém preferência do usuário.
        
        Args:
            key: Chave da preferência
            default: Valor padrão se não encontrado
            
        Returns:
            Valor da preferência
        """
        return self.user_preferences.get(key, default)
    
    def update_context(self, key: str, value: any):
        """Atualiza dado de contexto.
        
        Args:
            key: Chave do contexto
            value: Valor a armazenar
        """
        self.context_data[key] = value
    
    def get_context(self, key: str, default: any = None) -> any:
        """Obtém dado de contexto.
        
        Args:
            key: Chave do contexto
            default: Valor padrão
            
        Returns:
            Valor do contexto
        """
        return self.context_data.get(key, default)
    
    def clear_history(self):
        """Limpa histórico de conversação."""
        self.conversation_history = []
    
    def get_session_duration(self) -> float:
        """Retorna duração da sessão em minutos."""
        duration = datetime.now() - self.session_start
        return duration.total_seconds() / 60
    
    def save_to_file(self, directory: str = 'data/sessions'):
        """Salva contexto em arquivo.
        
        Args:
            directory: Diretório para salvar
        """
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        filename = f"{directory}/{self.user_id}_{self.session_start.strftime('%Y%m%d_%H%M%S')}.json"
        
        data = {
            'user_id': self.user_id,
            'session_start': self.session_start.isoformat(),
            'conversation_history': self.conversation_history,
            'user_preferences': self.user_preferences,
            'context_data': self.context_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'ConversationContext':
        """Carrega contexto de arquivo.
        
        Args:
            filepath: Caminho do arquivo
            
        Returns:
            Instância de ConversationContext
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        context = cls(user_id=data['user_id'])
        context.session_start = datetime.fromisoformat(data['session_start'])
        context.conversation_history = data['conversation_history']
        context.user_preferences = data['user_preferences']
        context.context_data = data['context_data']
        
        return context
    
    def get_summary(self) -> Dict:
        """Gera resumo da sessão.
        
        Returns:
            Dicionário com estatísticas da sessão
        """
        user_messages = [m for m in self.conversation_history if m['role'] == 'user']
        assistant_messages = [m for m in self.conversation_history if m['role'] == 'assistant']
        
        return {
            'user_id': self.user_id,
            'session_duration_minutes': self.get_session_duration(),
            'total_messages': len(self.conversation_history),
            'user_messages': len(user_messages),
            'assistant_messages': len(assistant_messages),
            'preferences_set': len(self.user_preferences),
            'context_items': len(self.context_data)
        }
