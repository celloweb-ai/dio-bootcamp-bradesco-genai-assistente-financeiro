"""Gerenciador de FAQs com busca semântica."""

from typing import List, Dict, Optional
import json
import os


class FAQManager:
    """Gerencia perguntas frequentes e busca de respostas."""
    
    def __init__(self, faq_file: Optional[str] = None):
        """Inicializa o gerenciador de FAQs.
        
        Args:
            faq_file: Caminho para arquivo JSON com FAQs
        """
        self.faqs = self._load_faqs(faq_file)
    
    def _load_faqs(self, faq_file: Optional[str] = None) -> List[Dict]:
        """Carrega FAQs de arquivo ou retorna padrão."""
        if faq_file and os.path.exists(faq_file):
            with open(faq_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # FAQs padrão
        return [
            {
                "category": "Conta Corrente",
                "question": "Como abrir uma conta corrente?",
                "answer": "Para abrir uma conta no Bradesco, você precisa ter pelo menos 18 anos e apresentar RG, CPF e comprovante de residência. Pode ser feito pelo app, internet banking ou em uma agência."
            },
            {
                "category": "Cartão de Crédito",
                "question": "Como solicitar um cartão de crédito?",
                "answer": "Você pode solicitar seu cartão pelo app Bradesco, internet banking ou em uma agência. A aprovação depende de análise de crédito."
            },
            {
                "category": "Investimentos",
                "question": "Quais são as opções de investimento?",
                "answer": "O Bradesco oferece diversas opções: Poupança, CDB, Tesouro Direto, Fundos de Investimento, Ações, COE e Previdência Privada."
            },
            {
                "category": "Empréstimos",
                "question": "Como solicitar um empréstimo pessoal?",
                "answer": "Acesse o app ou internet banking, vá em 'Empréstimos' e simule as condições. Você pode contratar direto pelo aplicativo após aprovação."
            },
            {
                "category": "Segurança",
                "question": "Como proteger minha conta?",
                "answer": "Use senhas fortes, ative notificações de transações, nunca compartilhe senhas, use biometria quando disponível e desconfie de mensagens suspeitas."
            }
        ]
    
    def search_faq(self, query: str, limit: int = 3) -> List[Dict]:
        """Busca FAQs relevantes.
        
        Args:
            query: Pergunta do usuário
            limit: Número máximo de resultados
            
        Returns:
            Lista de FAQs relevantes
        """
        # Busca simples por palavras-chave (pode ser melhorada com embeddings)
        query_lower = query.lower()
        results = []
        
        for faq in self.faqs:
            score = 0
            question_lower = faq['question'].lower()
            answer_lower = faq['answer'].lower()
            
            # Pontuação baseada em ocorrências
            for word in query_lower.split():
                if len(word) > 3:  # Ignora palavras muito curtas
                    if word in question_lower:
                        score += 2
                    if word in answer_lower:
                        score += 1
            
            if score > 0:
                results.append({**faq, 'score': score})
        
        # Ordena por pontuação e retorna top N
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Retorna todas as FAQs de uma categoria.
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de FAQs da categoria
        """
        return [faq for faq in self.faqs if faq['category'].lower() == category.lower()]
    
    def get_all_categories(self) -> List[str]:
        """Retorna todas as categorias disponíveis.
        
        Returns:
            Lista de categorias únicas
        """
        return list(set(faq['category'] for faq in self.faqs))
    
    def add_faq(self, category: str, question: str, answer: str) -> None:
        """Adiciona uma nova FAQ.
        
        Args:
            category: Categoria da FAQ
            question: Pergunta
            answer: Resposta
        """
        self.faqs.append({
            'category': category,
            'question': question,
            'answer': answer
        })
