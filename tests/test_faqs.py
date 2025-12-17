"""Testes para módulo de FAQs inteligentes."""

import unittest
from src.faqs import IntelligentFAQ


class TestIntelligentFAQ(unittest.TestCase):
    """Testes para sistema de FAQs."""
    
    def setUp(self):
        """Configura ambiente de teste."""
        self.faq = IntelligentFAQ()
    
    def test_search_faq_exact_match(self):
        """Testa busca com correspondência exata."""
        results = self.faq.search_faq("Como abrir uma conta corrente?")
        
        self.assertGreater(len(results), 0)
        self.assertGreater(results[0]['relevance'], 0.5)
    
    def test_search_faq_keywords(self):
        """Testa busca por palavras-chave."""
        results = self.faq.search_faq("investimentos")
        
        self.assertGreater(len(results), 0)
        # Deve encontrar FAQ sobre investimentos
        self.assertIn('Investimento', results[0]['faq']['category'])
    
    def test_get_answer_found(self):
        """Testa obtenção de resposta encontrada."""
        result = self.faq.get_answer("pix")
        
        self.assertTrue(result['found'])
        self.assertIn('answer', result)
        self.assertIn('category', result)
    
    def test_get_answer_not_found(self):
        """Testa comportamento quando resposta não é encontrada."""
        result = self.faq.get_answer("pergunta inexistente xyz123")
        
        self.assertFalse(result['found'])
        self.assertIn('suggestions', result)
    
    def test_list_categories(self):
        """Testa listagem de categorias."""
        categories = self.faq.list_categories()
        
        self.assertIsInstance(categories, list)
        self.assertGreater(len(categories), 0)
    
    def test_get_faqs_by_category(self):
        """Testa obtenção de FAQs por categoria."""
        categories = self.faq.list_categories()
        
        if categories:
            faqs = self.faq.get_faqs_by_category(categories[0])
            self.assertIsInstance(faqs, list)
            
            for faq in faqs:
                self.assertEqual(faq['category'], categories[0])


if __name__ == '__main__':
    unittest.main()
