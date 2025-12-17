"""
Gerenciador de Base de Conhecimento e FAQs
Implementa busca semântica e gerenciamento de perguntas frequentes.
"""

import json
import pickle
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
import numpy as np
from pathlib import Path


@dataclass
class FAQ:
    """Representa uma FAQ"""
    id: int
    pergunta: str
    resposta: str
    categoria: str
    tags: List[str]
    relevancia: float = 0.0


class FAQManager:
    """
    Gerenciador de Base de Conhecimento com busca semântica.
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Inicializa o gerenciador de FAQs.

        Args:
            data_path: Caminho para arquivo de dados das FAQs
        """
        self.data_path = data_path or "data/faqs.json"
        self.faqs: List[FAQ] = []
        self.embeddings = None
        self._carregar_faqs()

    def _carregar_faqs(self) -> None:
        """
        Carrega FAQs do arquivo de dados.
        """
        try:
            path = Path(self.data_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.faqs = [
                        FAQ(**faq) if isinstance(faq, dict) else faq
                        for faq in data
                    ]
            else:
                self._criar_faqs_exemplo()
        except Exception as e:
            print(f"Erro ao carregar FAQs: {e}")
            self._criar_faqs_exemplo()

    def _criar_faqs_exemplo(self) -> None:
        """
        Cria FAQs de exemplo para inicialização.
        """
        self.faqs = [
            FAQ(
                id=1,
                pergunta="Como funciona o Pix?",
                resposta="O Pix é um meio de pagamento instantâneo criado pelo Banco Central. Permite transferências 24/7 em até 10 segundos, usando chaves como CPF, telefone, email ou chave aleatória.",
                categoria="Pagamentos",
                tags=["pix", "transferência", "pagamento"]
            ),
            FAQ(
                id=2,
                pergunta="Qual é a taxa de juros da poupança?",
                resposta="A poupança rende 70% da taxa Selic quando esta estiver acima de 8,5% ao ano, mais TR (Taxa Referencial). Quando a Selic estiver igual ou abaixo de 8,5% ao ano, a poupança rende 0,5% ao mês mais TR.",
                categoria="Investimentos",
                tags=["poupança", "rendimento", "taxa"]
            ),
            FAQ(
                id=3,
                pergunta="Como aumentar o limite do cartão de crédito?",
                resposta="Para solicitar aumento de limite: 1) Acesse o app do banco, 2) Vá em Cartões, 3) Selecione 'Aumentar limite', 4) Informe o valor desejado. A análise é automática e leva até 24h.",
                categoria="Cartões",
                tags=["cartão", "limite", "crédito"]
            ),
            FAQ(
                id=4,
                pergunta="O que é Tesouro Direto?",
                resposta="Tesouro Direto é um programa do Tesouro Nacional para venda de títulos públicos a pessoas físicas pela internet. É um investimento seguro, com rentabilidade garantida e aplicação mínima de R$ 30.",
                categoria="Investimentos",
                tags=["tesouro direto", "investimento", "títulos públicos"]
            ),
            FAQ(
                id=5,
                pergunta="Como cancelar um cartão de crédito?",
                resposta="Para cancelar: 1) Quite todas as faturas pendentes, 2) Entre em contato com o banco pelo app, telefone ou agência, 3) Solicite o cancelamento, 4) Guarde o protocolo. O cartão será cancelado em até 5 dias úteis.",
                categoria="Cartões",
                tags=["cartão", "cancelamento"]
            )
        ]

    def salvar_faqs(self) -> None:
        """
        Salva FAQs no arquivo de dados.
        """
        try:
            path = Path(self.data_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                data = [asdict(faq) for faq in self.faqs]
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar FAQs: {e}")

    def buscar(self, pergunta: str, top_k: int = 3) -> List[Dict]:
        """
        Busca FAQs relevantes usando busca por palavras-chave.
        Para busca semântica real, seria necessário integrar embeddings.

        Args:
            pergunta: Pergunta do usuário
            top_k: Número de resultados

        Returns:
            Lista de FAQs relevantes
        """
        if not self.faqs:
            return []

        # Busca simples por palavras-chave
        pergunta_lower = pergunta.lower()
        palavras = set(pergunta_lower.split())

        # Calcula score de relevância
        for faq in self.faqs:
            score = 0
            faq_texto = f"{faq.pergunta} {faq.resposta} {' '.join(faq.tags)}".lower()
            
            # Conta palavras em comum
            for palavra in palavras:
                if len(palavra) > 2:  # Ignora palavras muito curtas
                    score += faq_texto.count(palavra)
            
            faq.relevancia = score

        # Ordena por relevância
        faqs_ordenadas = sorted(
            self.faqs,
            key=lambda x: x.relevancia,
            reverse=True
        )

        # Retorna top_k resultados com relevância > 0
        resultados = [
            {
                'id': faq.id,
                'pergunta': faq.pergunta,
                'resposta': faq.resposta,
                'categoria': faq.categoria,
                'tags': faq.tags,
                'score': faq.relevancia
            }
            for faq in faqs_ordenadas[:top_k]
            if faq.relevancia > 0
        ]

        return resultados

    def adicionar_faq(
        self,
        pergunta: str,
        resposta: str,
        categoria: str,
        tags: Optional[List[str]] = None
    ) -> FAQ:
        """
        Adiciona nova FAQ à base.

        Args:
            pergunta: Pergunta
            resposta: Resposta
            categoria: Categoria da FAQ
            tags: Lista de tags (opcional)

        Returns:
            FAQ criada
        """
        novo_id = max([faq.id for faq in self.faqs], default=0) + 1
        
        nova_faq = FAQ(
            id=novo_id,
            pergunta=pergunta,
            resposta=resposta,
            categoria=categoria,
            tags=tags or []
        )
        
        self.faqs.append(nova_faq)
        self.salvar_faqs()
        
        return nova_faq

    def atualizar_faq(
        self,
        faq_id: int,
        pergunta: Optional[str] = None,
        resposta: Optional[str] = None,
        categoria: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[FAQ]:
        """
        Atualiza FAQ existente.

        Args:
            faq_id: ID da FAQ
            pergunta: Nova pergunta (opcional)
            resposta: Nova resposta (opcional)
            categoria: Nova categoria (opcional)
            tags: Novas tags (opcional)

        Returns:
            FAQ atualizada ou None se não encontrada
        """
        for faq in self.faqs:
            if faq.id == faq_id:
                if pergunta:
                    faq.pergunta = pergunta
                if resposta:
                    faq.resposta = resposta
                if categoria:
                    faq.categoria = categoria
                if tags:
                    faq.tags = tags
                
                self.salvar_faqs()
                return faq
        
        return None

    def remover_faq(self, faq_id: int) -> bool:
        """
        Remove FAQ da base.

        Args:
            faq_id: ID da FAQ

        Returns:
            True se removida, False se não encontrada
        """
        for i, faq in enumerate(self.faqs):
            if faq.id == faq_id:
                self.faqs.pop(i)
                self.salvar_faqs()
                return True
        
        return False

    def listar_categorias(self) -> List[str]:
        """
        Lista todas as categorias disponíveis.

        Returns:
            Lista de categorias únicas
        """
        return list(set(faq.categoria for faq in self.faqs))

    def buscar_por_categoria(self, categoria: str) -> List[FAQ]:
        """
        Busca FAQs por categoria.

        Args:
            categoria: Nome da categoria

        Returns:
            Lista de FAQs da categoria
        """
        return [faq for faq in self.faqs if faq.categoria == categoria]

    def obter_faq(self, faq_id: int) -> Optional[FAQ]:
        """
        Obtém FAQ específica por ID.

        Args:
            faq_id: ID da FAQ

        Returns:
            FAQ ou None se não encontrada
        """
        for faq in self.faqs:
            if faq.id == faq_id:
                return faq
        return None

    def __len__(self) -> int:
        """Retorna o número de FAQs."""
        return len(self.faqs)

    def __repr__(self) -> str:
        return f"FAQManager(faqs={len(self.faqs)}, categorias={len(self.listar_categorias())})"