"""Módulo de análise de dados financeiros.

Implementa análise de transações, geração de insights
e visualizações de dados financeiros.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


class FinancialDataAnalyzer:
    """Analisador de dados financeiros com geração de insights."""
    
    def __init__(self):
        """Inicializa o analisador."""
        self.transactions: List[Dict] = []
        
    def load_transactions(self, transactions: List[Dict]):
        """Carrega transações para análise.
        
        Args:
            transactions: Lista de dicionários com transações
                Formato esperado: {'date', 'amount', 'category', 'type', 'description'}
        """
        self.transactions = transactions
        
    def create_sample_data(self, months: int = 6) -> List[Dict]:
        """Cria dados de exemplo para demonstração.
        
        Args:
            months: Número de meses de dados
            
        Returns:
            Lista de transações simuladas
        """
        categories_expense = ['Alimentação', 'Transporte', 'Moradia', 'Saúde', 
                             'Educação', 'Lazer', 'Vestuário', 'Outros']
        categories_income = ['Salário', 'Freelance', 'Investimentos', 'Outros']
        
        transactions = []
        start_date = datetime.now() - timedelta(days=months * 30)
        
        for day in range(months * 30):
            current_date = start_date + timedelta(days=day)
            
            # Receitas (salário no dia 5 de cada mês)
            if current_date.day == 5:
                transactions.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'amount': np.random.uniform(4000, 6000),
                    'category': 'Salário',
                    'type': 'income',
                    'description': 'Salário mensal'
                })
            
            # Despesas aleatórias
            if np.random.random() < 0.3:  # 30% de chance de despesa por dia
                category = np.random.choice(categories_expense)
                amount_range = {
                    'Alimentação': (20, 150),
                    'Transporte': (15, 100),
                    'Moradia': (800, 1500),
                    'Saúde': (50, 300),
                    'Educação': (100, 500),
                    'Lazer': (30, 200),
                    'Vestuário': (50, 300),
                    'Outros': (10, 100)
                }
                
                min_val, max_val = amount_range.get(category, (10, 100))
                
                transactions.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'amount': np.random.uniform(min_val, max_val),
                    'category': category,
                    'type': 'expense',
                    'description': f'Despesa com {category.lower()}'
                })
        
        self.transactions = transactions
        return transactions
    
    def get_summary(self) -> Dict[str, float]:
        """Gera resumo financeiro das transações.
        
        Returns:
            Dicionário com resumo financeiro
        """
        if not self.transactions:
            return {}
        
        df = pd.DataFrame(self.transactions)
        
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expense = df[df['type'] == 'expense']['amount'].sum()
        balance = total_income - total_expense
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'savings_rate': (balance / total_income * 100) if total_income > 0 else 0,
            'transaction_count': len(self.transactions),
            'avg_expense': df[df['type'] == 'expense']['amount'].mean() if len(df[df['type'] == 'expense']) > 0 else 0
        }
    
    def get_expenses_by_category(self) -> Dict[str, float]:
        """Agrupa despesas por categoria.
        
        Returns:
            Dicionário com total por categoria
        """
        if not self.transactions:
            return {}
        
        df = pd.DataFrame(self.transactions)
        expenses = df[df['type'] == 'expense']
        
        return expenses.groupby('category')['amount'].sum().to_dict()
    
    def get_monthly_trend(self) -> Dict[str, List[Dict]]:
        """Analisa tendência mensal de receitas e despesas.
        
        Returns:
            Dicionário com tendências mensais
        """
        if not self.transactions:
            return {}
        
        df = pd.DataFrame(self.transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        monthly = df.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        
        result = []
        for month in monthly.index:
            result.append({
                'month': str(month),
                'income': monthly.loc[month].get('income', 0),
                'expense': monthly.loc[month].get('expense', 0),
                'balance': monthly.loc[month].get('income', 0) - monthly.loc[month].get('expense', 0)
            })
        
        return {'monthly_data': result}
    
    def generate_insights(self) -> List[str]:
        """Gera insights automáticos sobre os dados financeiros.
        
        Returns:
            Lista de insights em linguagem natural
        """
        if not self.transactions:
            return ["Nenhuma transação disponível para análise."]
        
        insights = []
        summary = self.get_summary()
        expenses_by_category = self.get_expenses_by_category()
        
        # Insight sobre taxa de poupança
        savings_rate = summary.get('savings_rate', 0)
        if savings_rate > 20:
            insights.append(f"✅ Excelente! Sua taxa de poupança é de {savings_rate:.1f}%, acima da recomendação de 20%.")
        elif savings_rate > 10:
            insights.append(f"⚠️ Sua taxa de poupança é de {savings_rate:.1f}%. Tente aumentar para pelo menos 20%.")
        else:
            insights.append(f"❌ Atenção! Sua taxa de poupança é de apenas {savings_rate:.1f}%. Revise seus gastos.")
        
        # Insight sobre maior categoria de gasto
        if expenses_by_category:
            top_category = max(expenses_by_category.items(), key=lambda x: x[1])
            percentage = (top_category[1] / summary['total_expense'] * 100)
            insights.append(f"📊 Maior gasto: {top_category[0]} ({percentage:.1f}% do total).")
            
            # Verifica se alguma categoria está muito alta
            if percentage > 40:
                insights.append(f"⚠️ {top_category[0]} representa mais de 40% dos seus gastos. Considere reduzir.")
        
        # Insight sobre média de gastos
        avg_expense = summary.get('avg_expense', 0)
        if avg_expense > 0:
            insights.append(f"💸 Sua despesa média por transação é R$ {avg_expense:.2f}.")
        
        return insights
    
    def export_to_csv(self, filename: str = 'transactions.csv'):
        """Exporta transações para CSV.
        
        Args:
            filename: Nome do arquivo de saída
        """
        if not self.transactions:
            raise ValueError("Nenhuma transação para exportar")
        
        df = pd.DataFrame(self.transactions)
        df.to_csv(filename, index=False, encoding='utf-8')
