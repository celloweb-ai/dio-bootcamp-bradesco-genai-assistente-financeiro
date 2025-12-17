"""
Gerenciador de Banco de Dados
Implementa persistência de dados usando SQLite.
"""

import sqlite3
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
import pickle


class DatabaseManager:
    """
    Gerenciador de banco de dados SQLite para persistência.
    """

    def __init__(self, db_path: str = "data/assistente.db"):
        """
        Inicializa o gerenciador de banco de dados.

        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self._criar_banco()

    def _criar_banco(self) -> None:
        """
        Cria as tabelas do banco de dados se não existirem.
        """
        # Garante que o diretório existe
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                nome TEXT,
                email TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tabela de conversas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                session_id TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                role TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)

        # Tabela de preferências
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                preferencias_json TEXT,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)

        # Tabela de simulações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS simulacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                tipo TEXT NOT NULL,
                parametros_json TEXT NOT NULL,
                resultado_json TEXT NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES usuarios(user_id)
            )
        """)

        # Tabela de feedback
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                conversa_id INTEGER,
                rating INTEGER,
                comentario TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversa_id) REFERENCES conversas(id)
            )
        """)

        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """Retorna uma conexão com o banco."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # Métodos para Usuários

    def criar_usuario(
        self,
        user_id: str,
        nome: Optional[str] = None,
        email: Optional[str] = None
    ) -> bool:
        """
        Cria novo usuário.

        Args:
            user_id: ID único do usuário
            nome: Nome do usuário
            email: Email do usuário

        Returns:
            True se criado, False se já existe
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuarios (user_id, nome, email) VALUES (?, ?, ?)",
                (user_id, nome, email)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def obter_usuario(self, user_id: str) -> Optional[Dict]:
        """
        Obtém dados do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dicionário com dados do usuário ou None
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None

    # Métodos para Conversas

    def salvar_mensagem(
        self,
        user_id: str,
        session_id: str,
        mensagem: str,
        role: str
    ) -> int:
        """
        Salva mensagem da conversa.

        Args:
            user_id: ID do usuário
            session_id: ID da sessão
            mensagem: Conteúdo da mensagem
            role: 'user' ou 'assistant'

        Returns:
            ID da mensagem salva
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO conversas (user_id, session_id, mensagem, role) 
               VALUES (?, ?, ?, ?)""",
            (user_id, session_id, mensagem, role)
        )
        mensagem_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return mensagem_id

    def obter_historico(
        self,
        user_id: str,
        session_id: Optional[str] = None,
        limite: int = 50
    ) -> List[Dict]:
        """
        Obtém histórico de conversações.

        Args:
            user_id: ID do usuário
            session_id: ID da sessão (opcional, pega todas se None)
            limite: Número máximo de mensagens

        Returns:
            Lista de mensagens
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute(
                """SELECT * FROM conversas 
                   WHERE user_id = ? AND session_id = ? 
                   ORDER BY timestamp DESC LIMIT ?""",
                (user_id, session_id, limite)
            )
        else:
            cursor.execute(
                """SELECT * FROM conversas 
                   WHERE user_id = ? 
                   ORDER BY timestamp DESC LIMIT ?""",
                (user_id, limite)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in reversed(rows)]

    def limpar_historico(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> int:
        """
        Limpa histórico de conversações.

        Args:
            user_id: ID do usuário
            session_id: ID da sessão (opcional, limpa todas se None)

        Returns:
            Número de mensagens removidas
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute(
                "DELETE FROM conversas WHERE user_id = ? AND session_id = ?",
                (user_id, session_id)
            )
        else:
            cursor.execute(
                "DELETE FROM conversas WHERE user_id = ?",
                (user_id,)
            )
        
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted

    # Métodos para Preferências

    def salvar_preferencias(
        self,
        user_id: str,
        preferencias: Dict[str, Any]
    ) -> None:
        """
        Salva preferências do usuário.

        Args:
            user_id: ID do usuário
            preferencias: Dicionário com preferências
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        preferencias_json = json.dumps(preferencias, ensure_ascii=False)
        
        cursor.execute(
            """INSERT OR REPLACE INTO preferencias (user_id, preferencias_json, atualizado_em)
               VALUES (?, ?, CURRENT_TIMESTAMP)""",
            (user_id, preferencias_json)
        )
        
        conn.commit()
        conn.close()

    def obter_preferencias(self, user_id: str) -> Dict[str, Any]:
        """
        Obtém preferências do usuário.

        Args:
            user_id: ID do usuário

        Returns:
            Dicionário com preferências
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT preferencias_json FROM preferencias WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row and row['preferencias_json']:
            return json.loads(row['preferencias_json'])
        return {}

    # Métodos para Simulações

    def salvar_simulacao(
        self,
        user_id: str,
        tipo: str,
        parametros: Dict,
        resultado: Dict
    ) -> int:
        """
        Salva simulação financeira.

        Args:
            user_id: ID do usuário
            tipo: Tipo de simulação (ex: 'financiamento', 'investimento')
            parametros: Parâmetros da simulação
            resultado: Resultado da simulação

        Returns:
            ID da simulação salva
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        parametros_json = json.dumps(parametros, ensure_ascii=False)
        resultado_json = json.dumps(resultado, ensure_ascii=False, default=str)
        
        cursor.execute(
            """INSERT INTO simulacoes (user_id, tipo, parametros_json, resultado_json)
               VALUES (?, ?, ?, ?)""",
            (user_id, tipo, parametros_json, resultado_json)
        )
        
        simulacao_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return simulacao_id

    def obter_simulacoes(
        self,
        user_id: str,
        tipo: Optional[str] = None,
        limite: int = 10
    ) -> List[Dict]:
        """
        Obtém simulações do usuário.

        Args:
            user_id: ID do usuário
            tipo: Tipo de simulação (opcional)
            limite: Número máximo de resultados

        Returns:
            Lista de simulações
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        if tipo:
            cursor.execute(
                """SELECT * FROM simulacoes 
                   WHERE user_id = ? AND tipo = ? 
                   ORDER BY criado_em DESC LIMIT ?""",
                (user_id, tipo, limite)
            )
        else:
            cursor.execute(
                """SELECT * FROM simulacoes 
                   WHERE user_id = ? 
                   ORDER BY criado_em DESC LIMIT ?""",
                (user_id, limite)
            )
        
        rows = cursor.fetchall()
        conn.close()
        
        simulacoes = []
        for row in rows:
            sim = dict(row)
            sim['parametros'] = json.loads(sim['parametros_json'])
            sim['resultado'] = json.loads(sim['resultado_json'])
            del sim['parametros_json']
            del sim['resultado_json']
            simulacoes.append(sim)
        
        return simulacoes

    # Métodos para Feedback

    def salvar_feedback(
        self,
        user_id: str,
        conversa_id: Optional[int],
        rating: int,
        comentario: Optional[str] = None
    ) -> int:
        """
        Salva feedback do usuário.

        Args:
            user_id: ID do usuário
            conversa_id: ID da conversa avaliada
            rating: Nota (1-5)
            comentario: Comentário opcional

        Returns:
            ID do feedback salvo
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO feedback (user_id, conversa_id, rating, comentario)
               VALUES (?, ?, ?, ?)""",
            (user_id, conversa_id, rating, comentario)
        )
        feedback_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return feedback_id

    def obter_estatisticas_feedback(self) -> Dict:
        """
        Obtém estatísticas de feedback.

        Returns:
            Dicionário com estatísticas
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT 
                   COUNT(*) as total,
                   AVG(rating) as media,
                   MIN(rating) as minimo,
                   MAX(rating) as maximo
               FROM feedback"""
        )
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}

    def fechar(self) -> None:
        """
        Fecha conexões (cleanup).
        """
        pass  # SQLite fecha automaticamente

    def __repr__(self) -> str:
        return f"DatabaseManager(db_path='{self.db_path}')"