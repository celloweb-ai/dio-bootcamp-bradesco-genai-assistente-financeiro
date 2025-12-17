"""
Analisador de Dados Financeiros
Implementa análise e visualização de dados.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import dataclass


@dataclass
class AnaliseGastos:
    """Resultado de análise de gastos"""
    total_gasto: float
    gastos_por_categoria: Dict[str, float]
    media_mensal: float
    tendencia: str
    periodo_analise: str


class DataAnalyzer:
    """
    Analisador de dados financeiros com visualizações.
    """

    def __init__(self):
        """Inicializa o analisador."""
        self.cores_categorias = {
            'Alimentação': '#FF6B6B',
            'Transporte': '#4ECDC4',
            'Moradia': '#45B7D1',
            'Saúde': '#96CEB4',
            'Educação': '#FFEAA7',
            'Lazer': '#DFE6E9',
            'Outros': '#B2BEC3'
        }

    def analisar_gastos(self, df: pd.DataFrame) -> AnaliseGastos:
        """
        Analisa padrões de gastos.

        Args:
            df: DataFrame com colunas: data, descricao, valor, categoria

        Returns:
            AnaliseGastos com resultados
        """
        if df.empty:
            return AnaliseGastos(
                total_gasto=0,
                gastos_por_categoria={},
                media_mensal=0,
                tendencia="N/A",
                periodo_analise="N/A"
            )

        # Converter data se necessário
        if not pd.api.types.is_datetime64_any_dtype(df['data']):
            df['data'] = pd.to_datetime(df['data'])

        # Total gasto
        total_gasto = df['valor'].sum()

        # Gastos por categoria
        gastos_por_categoria = df.groupby('categoria')['valor'].sum().to_dict()

        # Média mensal
        df['mes'] = df['data'].dt.to_period('M')
        gastos_mensais = df.groupby('mes')['valor'].sum()
        media_mensal = gastos_mensais.mean()

        # Tendência
        if len(gastos_mensais) > 1:
            ultima_diferenca = gastos_mensais.iloc[-1] - gastos_mensais.iloc[-2]
            if ultima_diferenca > 0:
                percentual = (ultima_diferenca / gastos_mensais.iloc[-2]) * 100
                tendencia = f"Aumentando ({percentual:.1f}%)"
            elif ultima_diferenca < 0:
                percentual = abs((ultima_diferenca / gastos_mensais.iloc[-2]) * 100)
                tendencia = f"Diminuindo ({percentual:.1f}%)"
            else:
                tendencia = "Estável"
        else:
            tendencia = "Dados insuficientes"

        # Período de análise
        data_inicio = df['data'].min().strftime('%d/%m/%Y')
        data_fim = df['data'].max().strftime('%d/%m/%Y')
        periodo_analise = f"{data_inicio} a {data_fim}"

        return AnaliseGastos(
            total_gasto=total_gasto,
            gastos_por_categoria=gastos_por_categoria,
            media_mensal=media_mensal,
            tendencia=tendencia,
            periodo_analise=periodo_analise
        )

    def gerar_grafico_pizza(
        self,
        gastos_por_categoria: Dict[str, float],
        titulo: str = "Gastos por Categoria"
    ) -> go.Figure:
        """
        Gera gráfico de pizza para gastos por categoria.

        Args:
            gastos_por_categoria: Dicionário com gastos
            titulo: Título do gráfico

        Returns:
            Figura Plotly
        """
        categorias = list(gastos_por_categoria.keys())
        valores = list(gastos_por_categoria.values())
        
        cores = [self.cores_categorias.get(cat, '#B2BEC3') for cat in categorias]

        fig = go.Figure(data=[go.Pie(
            labels=categorias,
            values=valores,
            hole=0.3,
            marker_colors=cores
        )])

        fig.update_layout(
            title=titulo,
            showlegend=True,
            height=400
        )

        return fig

    def gerar_grafico_evolucao(
        self,
        df: pd.DataFrame,
        periodo: str = 'mensal'
    ) -> go.Figure:
        """
        Gera gráfico de evolução temporal.

        Args:
            df: DataFrame com dados
            periodo: 'diario', 'mensal', 'anual'

        Returns:
            Figura Plotly
        """
        if df.empty:
            return go.Figure()

        # Converter data
        if not pd.api.types.is_datetime64_any_dtype(df['data']):
            df = df.copy()
            df['data'] = pd.to_datetime(df['data'])

        # Agrupar por período
        if periodo == 'diario':
            df['periodo'] = df['data'].dt.date
            titulo = "Evolução Diária"
        elif periodo == 'mensal':
            df['periodo'] = df['data'].dt.to_period('M').astype(str)
            titulo = "Evolução Mensal"
        else:  # anual
            df['periodo'] = df['data'].dt.year
            titulo = "Evolução Anual"

        # Agregar dados
        evolucao = df.groupby('periodo')['valor'].sum().reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=evolucao['periodo'],
            y=evolucao['valor'],
            mode='lines+markers',
            name='Gastos',
            line=dict(color='#CC092F', width=3),
            marker=dict(size=8)
        ))

        fig.update_layout(
            title=titulo,
            xaxis_title='Período',
            yaxis_title='Valor (R$)',
            hovermode='x unified',
            height=400
        )

        return fig

    def gerar_grafico_barras_categorias(
        self,
        df: pd.DataFrame,
        top_n: int = 10
    ) -> go.Figure:
        """
        Gera gráfico de barras com top categorias.

        Args:
            df: DataFrame com dados
            top_n: Número de categorias a exibir

        Returns:
            Figura Plotly
        """
        if df.empty:
            return go.Figure()

        # Agrupar e ordenar
        categorias = df.groupby('categoria')['valor'].sum().sort_values(ascending=False).head(top_n)

        cores = [self.cores_categorias.get(cat, '#B2BEC3') for cat in categorias.index]

        fig = go.Figure(data=[go.Bar(
            x=categorias.index,
            y=categorias.values,
            marker_color=cores
        )])

        fig.update_layout(
            title=f'Top {top_n} Categorias de Gastos',
            xaxis_title='Categoria',
            yaxis_title='Valor (R$)',
            height=400
        )

        return fig

    def gerar_relatorio_completo(self, df: pd.DataFrame) -> Dict:
        """
        Gera relatório completo de análise.

        Args:
            df: DataFrame com dados

        Returns:
            Dicionário com todas as análises e gráficos
        """
        analise = self.analisar_gastos(df)
        
        return {
            'analise': analise,
            'grafico_pizza': self.gerar_grafico_pizza(
                analise.gastos_por_categoria
            ),
            'grafico_evolucao': self.gerar_grafico_evolucao(df),
            'grafico_barras': self.gerar_grafico_barras_categorias(df)
        }

    def detectar_anomalias(self, df: pd.DataFrame, desvios: float = 2.0) -> pd.DataFrame:
        """
        Detecta gastos anômalos.

        Args:
            df: DataFrame com dados
            desvios: Número de desvios padrão para considerar anomalia

        Returns:
            DataFrame com anomalias detectadas
        """
        if df.empty:
            return pd.DataFrame()

        # Calcular média e desvio padrão por categoria
        stats = df.groupby('categoria')['valor'].agg(['mean', 'std']).reset_index()
        
        # Merge com dados originais
        df_com_stats = df.merge(stats, on='categoria')
        
        # Identificar anomalias
        df_com_stats['anomalia'] = (
            np.abs(df_com_stats['valor'] - df_com_stats['mean']) > 
            desvios * df_com_stats['std']
        )
        
        return df_com_stats[df_com_stats['anomalia']]

    def calcular_kpis(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calcula KPIs financeiros.

        Args:
            df: DataFrame com dados

        Returns:
            Dicionário com KPIs
        """
        if df.empty:
            return {}

        return {
            'total_gastos': df['valor'].sum(),
            'media_transacao': df['valor'].mean(),
            'mediana_transacao': df['valor'].median(),
            'maior_transacao': df['valor'].max(),
            'menor_transacao': df['valor'].min(),
            'numero_transacoes': len(df),
            'desvio_padrao': df['valor'].std()
        }

    def __repr__(self) -> str:
        return "DataAnalyzer()"