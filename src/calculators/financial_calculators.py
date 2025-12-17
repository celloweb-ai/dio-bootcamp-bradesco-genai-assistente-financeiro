"""Calculadoras financeiras para diversos cenários."""

import numpy as np
from typing import Dict, List


class FinancingCalculator:
    """Calculadora de financiamentos."""
    
    @staticmethod
    def calculate_sac(principal: float, annual_rate: float, months: int) -> Dict:
        """Calcula financiamento pelo Sistema SAC.
        
        Args:
            principal: Valor principal
            annual_rate: Taxa de juros anual (%)
            months: Número de meses
            
        Returns:
            Dicionário com detalhes do financiamento
        """
        monthly_rate = annual_rate / 100 / 12
        amortization = principal / months
        
        installments = []
        balance = principal
        
        for month in range(1, months + 1):
            interest = balance * monthly_rate
            installment = amortization + interest
            balance -= amortization
            
            installments.append({
                'month': month,
                'installment': installment,
                'amortization': amortization,
                'interest': interest,
                'balance': max(0, balance)
            })
        
        total_paid = sum(i['installment'] for i in installments)
        total_interest = total_paid - principal
        
        return {
            'installments': installments,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'first_installment': installments[0]['installment'],
            'last_installment': installments[-1]['installment']
        }
    
    @staticmethod
    def calculate_price(principal: float, annual_rate: float, months: int) -> Dict:
        """Calcula financiamento pelo Sistema PRICE.
        
        Args:
            principal: Valor principal
            annual_rate: Taxa de juros anual (%)
            months: Número de meses
            
        Returns:
            Dicionário com detalhes do financiamento
        """
        monthly_rate = annual_rate / 100 / 12
        
        # Cálculo da prestação fixa
        installment = principal * (monthly_rate * (1 + monthly_rate) ** months) / \
                     ((1 + monthly_rate) ** months - 1)
        
        installments = []
        balance = principal
        
        for month in range(1, months + 1):
            interest = balance * monthly_rate
            amortization = installment - interest
            balance -= amortization
            
            installments.append({
                'month': month,
                'installment': installment,
                'amortization': amortization,
                'interest': interest,
                'balance': max(0, balance)
            })
        
        total_paid = installment * months
        total_interest = total_paid - principal
        
        return {
            'installments': installments,
            'total_paid': total_paid,
            'total_interest': total_interest,
            'fixed_installment': installment
        }


class InvestmentCalculator:
    """Calculadora de investimentos."""
    
    @staticmethod
    def calculate_compound_interest(principal: float, annual_rate: float, 
                                   years: int, monthly_contribution: float = 0) -> Dict:
        """Calcula juros compostos com aportes mensais.
        
        Args:
            principal: Valor inicial
            annual_rate: Taxa anual (%)
            years: Período em anos
            monthly_contribution: Aporte mensal
            
        Returns:
            Dicionário com projeção do investimento
        """
        monthly_rate = annual_rate / 100 / 12
        months = years * 12
        
        timeline = []
        balance = principal
        
        for month in range(1, months + 1):
            interest = balance * monthly_rate
            balance += interest + monthly_contribution
            
            if month % 12 == 0:  # Registra anualmente
                timeline.append({
                    'year': month // 12,
                    'balance': balance,
                    'total_contributed': principal + (monthly_contribution * month),
                    'total_interest': balance - principal - (monthly_contribution * month)
                })
        
        total_contributed = principal + (monthly_contribution * months)
        total_interest = balance - total_contributed
        
        return {
            'final_balance': balance,
            'total_contributed': total_contributed,
            'total_interest': total_interest,
            'timeline': timeline,
            'return_percentage': (total_interest / total_contributed) * 100
        }


class RetirementCalculator:
    """Calculadora de aposentadoria."""
    
    @staticmethod
    def calculate_retirement_savings(current_age: int, retirement_age: int,
                                    monthly_income_needed: float,
                                    annual_return: float = 6.0,
                                    inflation: float = 3.5) -> Dict:
        """Calcula quanto economizar para aposentadoria.
        
        Args:
            current_age: Idade atual
            retirement_age: Idade de aposentadoria desejada
            monthly_income_needed: Renda mensal necessária (valor atual)
            annual_return: Retorno anual esperado (%)
            inflation: Inflação anual (%)
            
        Returns:
            Dicionário com plano de aposentadoria
        """
        years_to_retirement = retirement_age - current_age
        life_expectancy = 85
        years_in_retirement = life_expectancy - retirement_age
        
        # Ajusta renda pela inflação
        real_return = ((1 + annual_return/100) / (1 + inflation/100) - 1) * 100
        
        # Calcula capital necessário na aposentadoria
        monthly_rate = real_return / 100 / 12
        months_retirement = years_in_retirement * 12
        
        if monthly_rate > 0:
            capital_needed = monthly_income_needed * \
                           ((1 - (1 + monthly_rate) ** -months_retirement) / monthly_rate)
        else:
            capital_needed = monthly_income_needed * months_retirement
        
        # Calcula aporte mensal necessário
        monthly_rate_saving = annual_return / 100 / 12
        months_saving = years_to_retirement * 12
        
        if monthly_rate_saving > 0:
            monthly_saving = capital_needed * monthly_rate_saving / \
                           ((1 + monthly_rate_saving) ** months_saving - 1)
        else:
            monthly_saving = capital_needed / months_saving
        
        return {
            'capital_needed': capital_needed,
            'monthly_saving_required': monthly_saving,
            'total_to_contribute': monthly_saving * months_saving,
            'years_to_retirement': years_to_retirement,
            'years_in_retirement': years_in_retirement
        }
