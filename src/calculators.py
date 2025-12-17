"""Módulo de calculadoras financeiras.

Implementa cálculos demonstrativos para educação financeira
incluindo juros compostos, investimentos e financiamentos.
"""

from typing import Dict, List, Tuple
import math
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class InvestmentResult:
    """Resultado de cálculo de investimento."""
    initial_amount: float
    monthly_contribution: float
    interest_rate: float
    months: int
    final_amount: float
    total_invested: float
    total_interest: float
    monthly_breakdown: List[Dict[str, float]]


@dataclass
class LoanResult:
    """Resultado de cálculo de financiamento."""
    loan_amount: float
    interest_rate: float
    months: int
    monthly_payment: float
    total_amount: float
    total_interest: float
    installments: List[Dict[str, float]]


class FinancialCalculators:
    """Coleção de calculadoras financeiras."""
    
    @staticmethod
    def compound_interest(
        principal: float,
        rate: float,
        time: int,
        contribution: float = 0,
        frequency: str = 'monthly'
    ) -> InvestmentResult:
        """Calcula juros compostos com aportes periódicos.
        
        Args:
            principal: Valor inicial
            rate: Taxa de juros (% ao ano)
            time: Período em meses
            contribution: Aporte mensal
            frequency: Frequência dos aportes
            
        Returns:
            InvestmentResult com detalhes do investimento
        """
        if principal < 0 or rate < 0 or time < 0 or contribution < 0:
            raise ValueError("Valores devem ser positivos")
        
        # Converte taxa anual para mensal
        monthly_rate = rate / 100 / 12
        
        monthly_breakdown = []
        current_amount = principal
        total_invested = principal
        
        for month in range(1, time + 1):
            # Aplica juros
            interest = current_amount * monthly_rate
            current_amount += interest
            
            # Adiciona aporte
            if month < time:  # Não adiciona aporte no último mês
                current_amount += contribution
                total_invested += contribution
            
            monthly_breakdown.append({
                'month': month,
                'contribution': contribution if month < time else 0,
                'interest': interest,
                'balance': current_amount
            })
        
        total_interest = current_amount - total_invested
        
        return InvestmentResult(
            initial_amount=principal,
            monthly_contribution=contribution,
            interest_rate=rate,
            months=time,
            final_amount=current_amount,
            total_invested=total_invested,
            total_interest=total_interest,
            monthly_breakdown=monthly_breakdown
        )
    
    @staticmethod
    def loan_calculator(
        loan_amount: float,
        annual_rate: float,
        months: int,
        system: str = 'PRICE'
    ) -> LoanResult:
        """Calcula parcelas de financiamento.
        
        Args:
            loan_amount: Valor do empréstimo
            annual_rate: Taxa de juros anual (%)
            months: Número de parcelas
            system: Sistema de amortização ('PRICE' ou 'SAC')
            
        Returns:
            LoanResult com detalhes do financiamento
        """
        if loan_amount <= 0 or annual_rate < 0 or months <= 0:
            raise ValueError("Parâmetros inválidos")
        
        monthly_rate = annual_rate / 100 / 12
        
        if system.upper() == 'PRICE':
            return FinancialCalculators._calculate_price(
                loan_amount, monthly_rate, months
            )
        elif system.upper() == 'SAC':
            return FinancialCalculators._calculate_sac(
                loan_amount, monthly_rate, months
            )
        else:
            raise ValueError("Sistema deve ser 'PRICE' ou 'SAC'")
    
    @staticmethod
    def _calculate_price(
        loan_amount: float,
        monthly_rate: float,
        months: int
    ) -> LoanResult:
        """Calcula financiamento pelo sistema PRICE (parcelas fixas)."""
        # Fórmula: PMT = PV * (i * (1+i)^n) / ((1+i)^n - 1)
        if monthly_rate == 0:
            monthly_payment = loan_amount / months
        else:
            factor = (1 + monthly_rate) ** months
            monthly_payment = loan_amount * (monthly_rate * factor) / (factor - 1)
        
        installments = []
        balance = loan_amount
        
        for month in range(1, months + 1):
            interest = balance * monthly_rate
            principal = monthly_payment - interest
            balance -= principal
            
            installments.append({
                'installment': month,
                'payment': monthly_payment,
                'principal': principal,
                'interest': interest,
                'balance': max(0, balance)  # Evita valores negativos por arredondamento
            })
        
        total_amount = monthly_payment * months
        total_interest = total_amount - loan_amount
        
        return LoanResult(
            loan_amount=loan_amount,
            interest_rate=monthly_rate * 12 * 100,
            months=months,
            monthly_payment=monthly_payment,
            total_amount=total_amount,
            total_interest=total_interest,
            installments=installments
        )
    
    @staticmethod
    def _calculate_sac(
        loan_amount: float,
        monthly_rate: float,
        months: int
    ) -> LoanResult:
        """Calcula financiamento pelo sistema SAC (amortização constante)."""
        amortization = loan_amount / months
        installments = []
        balance = loan_amount
        total_paid = 0
        
        for month in range(1, months + 1):
            interest = balance * monthly_rate
            payment = amortization + interest
            balance -= amortization
            total_paid += payment
            
            installments.append({
                'installment': month,
                'payment': payment,
                'principal': amortization,
                'interest': interest,
                'balance': max(0, balance)
            })
        
        total_interest = total_paid - loan_amount
        avg_payment = total_paid / months
        
        return LoanResult(
            loan_amount=loan_amount,
            interest_rate=monthly_rate * 12 * 100,
            months=months,
            monthly_payment=avg_payment,  # Média das parcelas
            total_amount=total_paid,
            total_interest=total_interest,
            installments=installments
        )
    
    @staticmethod
    def retirement_calculator(
        current_age: int,
        retirement_age: int,
        monthly_contribution: float,
        expected_return: float,
        current_savings: float = 0
    ) -> Dict[str, float]:
        """Calcula reserva para aposentadoria.
        
        Args:
            current_age: Idade atual
            retirement_age: Idade de aposentadoria desejada
            monthly_contribution: Contribuição mensal
            expected_return: Retorno esperado (% ao ano)
            current_savings: Patrimônio atual
            
        Returns:
            Dicionário com projeções de aposentadoria
        """
        if retirement_age <= current_age:
            raise ValueError("Idade de aposentadoria deve ser maior que idade atual")
        
        months_until_retirement = (retirement_age - current_age) * 12
        
        result = FinancialCalculators.compound_interest(
            principal=current_savings,
            rate=expected_return,
            time=months_until_retirement,
            contribution=monthly_contribution
        )
        
        # Calcula renda mensal possível (4% rule)
        monthly_income = result.final_amount * 0.04 / 12
        
        return {
            'years_until_retirement': retirement_age - current_age,
            'total_contributions': result.total_invested,
            'investment_growth': result.total_interest,
            'retirement_fund': result.final_amount,
            'estimated_monthly_income': monthly_income,
            'total_return_percentage': (result.total_interest / result.total_invested * 100) if result.total_invested > 0 else 0
        }
    
    @staticmethod
    def compare_investments(
        amount: float,
        time_months: int,
        investments: List[Dict[str, any]]
    ) -> List[Dict[str, any]]:
        """Compara diferentes opções de investimento.
        
        Args:
            amount: Valor a investir
            time_months: Período em meses
            investments: Lista de investimentos com 'name' e 'rate'
            
        Returns:
            Lista com resultados comparativos
        """
        results = []
        
        for inv in investments:
            result = FinancialCalculators.compound_interest(
                principal=amount,
                rate=inv['rate'],
                time=time_months
            )
            
            results.append({
                'name': inv['name'],
                'rate': inv['rate'],
                'final_amount': result.final_amount,
                'total_return': result.total_interest,
                'return_percentage': (result.total_interest / amount * 100)
            })
        
        # Ordena por retorno
        results.sort(key=lambda x: x['final_amount'], reverse=True)
        return results
