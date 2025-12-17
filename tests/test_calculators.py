"""Testes para módulo de calculadoras financeiras."""

import unittest
from src.calculators import FinancialCalculators


class TestFinancialCalculators(unittest.TestCase):
    """Testes para calculadoras financeiras."""
    
    def test_compound_interest_basic(self):
        """Testa cálculo básico de juros compostos."""
        result = FinancialCalculators.compound_interest(
            principal=1000,
            rate=10,  # 10% ao ano
            time=12,  # 12 meses
            contribution=0
        )
        
        self.assertGreater(result.final_amount, 1000)
        self.assertAlmostEqual(result.total_invested, 1000, places=2)
        self.assertGreater(result.total_interest, 0)
    
    def test_compound_interest_with_contributions(self):
        """Testa juros compostos com aportes mensais."""
        result = FinancialCalculators.compound_interest(
            principal=1000,
            rate=12,
            time=12,
            contribution=100
        )
        
        # Total investido deve ser principal + (11 aportes * 100)
        expected_invested = 1000 + (11 * 100)
        self.assertAlmostEqual(result.total_invested, expected_invested, places=2)
        self.assertGreater(result.final_amount, result.total_invested)
    
    def test_loan_calculator_price(self):
        """Testa calculadora de financiamento PRICE."""
        result = FinancialCalculators.loan_calculator(
            loan_amount=10000,
            annual_rate=12,
            months=12,
            system='PRICE'
        )
        
        self.assertGreater(result.monthly_payment, 0)
        self.assertGreater(result.total_amount, result.loan_amount)
        self.assertEqual(len(result.installments), 12)
    
    def test_loan_calculator_sac(self):
        """Testa calculadora de financiamento SAC."""
        result = FinancialCalculators.loan_calculator(
            loan_amount=10000,
            annual_rate=12,
            months=12,
            system='SAC'
        )
        
        self.assertGreater(result.total_amount, result.loan_amount)
        self.assertEqual(len(result.installments), 12)
        # No SAC, parcelas devem ser decrescentes
        self.assertGreater(
            result.installments[0]['payment'],
            result.installments[-1]['payment']
        )
    
    def test_retirement_calculator(self):
        """Testa calculadora de aposentadoria."""
        result = FinancialCalculators.retirement_calculator(
            current_age=30,
            retirement_age=65,
            monthly_contribution=500,
            expected_return=8,
            current_savings=10000
        )
        
        self.assertEqual(result['years_until_retirement'], 35)
        self.assertGreater(result['retirement_fund'], result['total_contributions'])
        self.assertGreater(result['estimated_monthly_income'], 0)
    
    def test_compare_investments(self):
        """Testa comparação de investimentos."""
        investments = [
            {'name': 'Poupança', 'rate': 6},
            {'name': 'CDB', 'rate': 10},
            {'name': 'Tesouro Direto', 'rate': 12}
        ]
        
        results = FinancialCalculators.compare_investments(
            amount=10000,
            time_months=12,
            investments=investments
        )
        
        self.assertEqual(len(results), 3)
        # Deve estar ordenado por retorno (maior primeiro)
        self.assertGreaterEqual(
            results[0]['final_amount'],
            results[1]['final_amount']
        )
    
    def test_invalid_inputs(self):
        """Testa validação de entradas inválidas."""
        with self.assertRaises(ValueError):
            FinancialCalculators.compound_interest(
                principal=-1000,  # Negativo
                rate=10,
                time=12
            )
        
        with self.assertRaises(ValueError):
            FinancialCalculators.loan_calculator(
                loan_amount=0,  # Zero
                annual_rate=12,
                months=12
            )


if __name__ == '__main__':
    unittest.main()
