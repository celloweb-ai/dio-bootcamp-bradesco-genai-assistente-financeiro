"""Implementação do chatbot financeiro inteligente."""

import os
from typing import Dict, List, Optional
from openai import OpenAI
import google.generativeai as genai


class FinancialChatbot:
    """Chatbot financeiro com IA generativa."""
    
    def __init__(self, provider: str = "openai"):
        """Inicializa o chatbot.
        
        Args:
            provider: Provedor de IA ('openai' ou 'gemini')
        """
        self.provider = provider
        self.conversation_history = []
        
        if provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        elif provider == "gemini":
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            self.model = genai.GenerativeModel('gemini-pro')
    
    def get_response(self, user_message: str, context: Optional[Dict] = None) -> str:
        """Obtém resposta do chatbot.
        
        Args:
            user_message: Mensagem do usuário
            context: Contexto adicional da conversa
            
        Returns:
            Resposta do chatbot
        """
        system_prompt = self._build_system_prompt(context)
        
        if self.provider == "openai":
            return self._get_openai_response(user_message, system_prompt)
        else:
            return self._get_gemini_response(user_message, system_prompt)
    
    def _build_system_prompt(self, context: Optional[Dict] = None) -> str:
        """Constrói o prompt do sistema."""
        base_prompt = """Você é um assistente financeiro inteligente do Bradesco.
        Seu objetivo é ajudar clientes com dúvidas sobre produtos bancários,
        investimentos, financiamentos e serviços financeiros em geral.
        
        Seja profissional, educado e forneça informações precisas.
        Quando apropriado, sugira produtos e serviços relevantes."""
        
        if context:
            base_prompt += f"\n\nContexto adicional: {context}"
        
        return base_prompt
    
    def _get_openai_response(self, message: str, system_prompt: str) -> str:
        """Obtém resposta do OpenAI."""
        messages = [
            {"role": "system", "content": system_prompt},
            *self.conversation_history,
            {"role": "user", "content": message}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        
        # Atualiza histórico
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def _get_gemini_response(self, message: str, system_prompt: str) -> str:
        """Obtém resposta do Gemini."""
        full_prompt = f"{system_prompt}\n\nUsuário: {message}"
        response = self.model.generate_content(full_prompt)
        
        assistant_message = response.text
        
        # Atualiza histórico
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})
        
        return assistant_message
    
    def clear_history(self):
        """Limpa o histórico de conversação."""
        self.conversation_history = []
