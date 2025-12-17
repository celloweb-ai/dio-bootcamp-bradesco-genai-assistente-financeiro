"""Testes para módulo de análise de dados."""

import unittest
from src.data_analysis import FinancialDataAnalyzer


class TestFinancialDataAnalyzer(unittest.TestCase):
    """Testes para analisador de dados financeiros."""
    
    def setUp(self):
        """Configura ambiente de teste."""
        self.analyzer = FinancialDataAnalyzer()
    
    def test_create_sample_data(self):
        """Testa criação de dados de exemplo."""
        transactions = self.analyzer.create_sample_data(months=3)
        
        self.assertIsInstance(transactions, list)
        self.assertGreater(len(transactions), 0)
        
        # Verifica estrutura das transações
        for transaction in transactions[:5]:  # Verifica primeiras 5
            self.assertIn('date', transaction)
            self.assertIn('amount', transaction)
            self.assertIn('category', transaction)
            self.assertIn('type', transaction)
    
    def test_get_summary(self):
        """Testa geração de resumo financeiro."""
        self.analyzer.create_sample_data(months=3)
        summary = self.analyzer.get_summary()
        
        self.assertIn('total_income', summary)
        self.assertIn('total_expense', summary)
        self.assertIn('balance', summary)
        self.assertIn('savings_rate', summary)
        
        self.assertGreaterEqual(summary['total_income'], 0)
        self.assertGreaterEqual(summary['total_expense'], 0)
    
    def test_get_expenses_by_category(self):
        """Testa agrupamento de despesas por categoria."""
        self.analyzer.create_sample_data(months=3)
        expenses = self.analyzer.get_expenses_by_category()
        
        self.assertIsInstance(expenses, dict)
        self.assertGreater(len(expenses), 0)
        
        # Verifica se valores são positivos
        for category, amount in expenses.items():
            self.assertGreater(amount, 0)
    
    def test_generate_insights(self):
        """Testa geração de insights."""
        self.analyzer.create_sample_data(months=3)
        insights = self.analyzer.generate_insights()
        
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
        
        # Verifica se insights são strings
        for insight in insights:
            self.assertIsInstance(insight, str)
    
    def test_empty_data(self):
        """Testa comportamento com dados vazios."""
        summary = self.analyzer.get_summary()
        self.assertEqual(summary, {})
        
        expenses = self.analyzer.get_expenses_by_category()
        self.assertEqual(expenses, {})


if __name__ == '__main__':
    unittest.main()
