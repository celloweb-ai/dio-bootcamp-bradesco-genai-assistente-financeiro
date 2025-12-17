"""
Módulo de Calculadoras Financeiras
Implementa cálculos de financiamento, investimento e planejamento financeiro.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ResultadoFinanciamento:
    """Resultado de simulação de financiamento"""
    valor_financiado: float
    parcelas: List[float]
    total_juros: float
    total_pago: float
    amortizacoes: List[float]
    juros_parcela: List[float]
    saldo_devedor: List[float]


@dataclass
class ResultadoInvestimento:
    """Resultado de simulação de investimento"""
    montante_final: float
    total_investido: float
    total_rendimento: float
    evolucao_mensal: List[Dict[str, float]]


class FinancialCalculators:
    """
    Classe para cálculos financeiros diversos.
    """

    @staticmethod
    def calcular_financiamento_sac(
        valor: float,
        entrada: float,
        prazo: int,
        taxa: float
    ) -> ResultadoFinanciamento:
        """
        Calcula financiamento pelo Sistema SAC (Sistema de Amortização Constante).

        Args:
            valor: Valor total do bem
            entrada: Valor da entrada
            prazo: Prazo em meses
            taxa: Taxa de juros anual em percentual

        Returns:
            ResultadoFinanciamento com detalhes da simulação
        """
        if valor <= 0 or prazo <= 0 or taxa < 0:
            raise ValueError("Valores devem ser positivos")
        
        if entrada >= valor:
            raise ValueError("Entrada não pode ser maior ou igual ao valor total")

        valor_financiado = valor - entrada
        taxa_mensal = taxa / 100 / 12
        amortizacao = valor_financiado / prazo

        parcelas = []
        juros_parcela = []
        saldo_devedor = []
        amortizacoes = []
        saldo_atual = valor_financiado

        for i in range(prazo):
            juros = saldo_atual * taxa_mensal
            parcela = amortizacao + juros
            
            parcelas.append(parcela)
            juros_parcela.append(juros)
            amortizacoes.append(amortizacao)
            saldo_atual -= amortizacao
            saldo_devedor.append(max(0, saldo_atual))

        total_pago = sum(parcelas)
        total_juros = sum(juros_parcela)

        return ResultadoFinanciamento(
            valor_financiado=valor_financiado,
            parcelas=parcelas,
            total_juros=total_juros,
            total_pago=total_pago,
            amortizacoes=amortizacoes,
            juros_parcela=juros_parcela,
            saldo_devedor=saldo_devedor
        )

    @staticmethod
    def calcular_financiamento_price(
        valor: float,
        entrada: float,
        prazo: int,
        taxa: float
    ) -> ResultadoFinanciamento:
        """
        Calcula financiamento pelo Sistema Price (Tabela Price).

        Args:
            valor: Valor total do bem
            entrada: Valor da entrada
            prazo: Prazo em meses
            taxa: Taxa de juros anual em percentual

        Returns:
            ResultadoFinanciamento com detalhes da simulação
        """
        if valor <= 0 or prazo <= 0 or taxa < 0:
            raise ValueError("Valores devem ser positivos")
        
        if entrada >= valor:
            raise ValueError("Entrada não pode ser maior ou igual ao valor total")

        valor_financiado = valor - entrada
        taxa_mensal = taxa / 100 / 12

        # Fórmula da Tabela Price
        if taxa_mensal > 0:
            parcela_fixa = valor_financiado * (
                taxa_mensal * (1 + taxa_mensal) ** prazo
            ) / ((1 + taxa_mensal) ** prazo - 1)
        else:
            parcela_fixa = valor_financiado / prazo

        parcelas = []
        juros_parcela = []
        amortizacoes = []
        saldo_devedor = []
        saldo_atual = valor_financiado

        for i in range(prazo):
            juros = saldo_atual * taxa_mensal
            amortizacao = parcela_fixa - juros
            
            parcelas.append(parcela_fixa)
            juros_parcela.append(juros)
            amortizacoes.append(amortizacao)
            saldo_atual -= amortizacao
            saldo_devedor.append(max(0, saldo_atual))

        total_pago = sum(parcelas)
        total_juros = sum(juros_parcela)

        return ResultadoFinanciamento(
            valor_financiado=valor_financiado,
            parcelas=parcelas,
            total_juros=total_juros,
            total_pago=total_pago,
            amortizacoes=amortizacoes,
            juros_parcela=juros_parcela,
            saldo_devedor=saldo_devedor
        )

    @staticmethod
    def calcular_investimento(
        valor_inicial: float,
        aporte_mensal: float,
        taxa: float,
        prazo: int
    ) -> ResultadoInvestimento:
        """
        Calcula retorno de investimento com aportes mensais.

        Args:
            valor_inicial: Valor inicial investido
            aporte_mensal: Valor de aporte mensal
            taxa: Taxa de rendimento anual em percentual
            prazo: Prazo em meses

        Returns:
            ResultadoInvestimento com projeção
        """
        if valor_inicial < 0 or aporte_mensal < 0 or prazo <= 0:
            raise ValueError("Valores devem ser positivos")

        taxa_mensal = taxa / 100 / 12
        montante = valor_inicial
        total_investido = valor_inicial
        evolucao = []

        # Mês 0
        evolucao.append({
            'mes': 0,
            'aporte': valor_inicial,
            'rendimento': 0,
            'montante': valor_inicial
        })

        for mes in range(1, prazo + 1):
            rendimento = montante * taxa_mensal
            montante = montante + rendimento + aporte_mensal
            total_investido += aporte_mensal

            evolucao.append({
                'mes': mes,
                'aporte': aporte_mensal,
                'rendimento': rendimento,
                'montante': montante
            })

        total_rendimento = montante - total_investido

        return ResultadoInvestimento(
            montante_final=montante,
            total_investido=total_investido,
            total_rendimento=total_rendimento,
            evolucao_mensal=evolucao
        )

    @staticmethod
    def calcular_juros_compostos(
        principal: float,
        taxa: float,
        periodo: int,
        aporte: float = 0
    ) -> float:
        """
        Calcula juros compostos.

        Args:
            principal: Valor principal
            taxa: Taxa de juros (decimal, ex: 0.10 para 10%)
            periodo: Período de aplicação
            aporte: Aporte regular (opcional)

        Returns:
            Montante final
        """
        if aporte == 0:
            return principal * (1 + taxa) ** periodo
        else:
            # Fórmula com aportes regulares
            montante_principal = principal * (1 + taxa) ** periodo
            montante_aportes = aporte * (((1 + taxa) ** periodo - 1) / taxa)
            return montante_principal + montante_aportes

    @staticmethod
    def calcular_aposentadoria(
        idade_atual: int,
        idade_aposentadoria: int,
        renda_desejada: float,
        valor_atual: float = 0,
        taxa_rendimento: float = 8.0,
        taxa_inflacao: float = 4.0,
        expectativa_vida: int = 85
    ) -> Dict:
        """
        Calcula planejamento de aposentadoria.

        Args:
            idade_atual: Idade atual
            idade_aposentadoria: Idade planejada para aposentar
            renda_desejada: Renda mensal desejada na aposentadoria
            valor_atual: Valor já acumulado
            taxa_rendimento: Taxa de rendimento anual esperada
            taxa_inflacao: Taxa de inflação anual esperada
            expectativa_vida: Expectativa de vida

        Returns:
            Dict com análise do planejamento
        """
        if idade_atual >= idade_aposentadoria:
            raise ValueError("Idade de aposentadoria deve ser maior que idade atual")

        anos_ate_aposentar = idade_aposentadoria - idade_atual
        anos_aposentado = expectativa_vida - idade_aposentadoria
        meses_ate_aposentar = anos_ate_aposentar * 12
        meses_aposentado = anos_aposentado * 12

        # Taxa real (descontando inflação)
        taxa_real = ((1 + taxa_rendimento/100) / (1 + taxa_inflacao/100) - 1) * 100
        taxa_real_mensal = taxa_real / 12 / 100

        # Montante necessário para gerar a renda desejada
        montante_necessario = renda_desejada * (
            (1 - (1 + taxa_real_mensal) ** -meses_aposentado) / taxa_real_mensal
        )

        # Aporte mensal necessário
        if taxa_real_mensal > 0:
            valor_futuro_atual = valor_atual * (1 + taxa_real_mensal) ** meses_ate_aposentar
            montante_faltante = montante_necessario - valor_futuro_atual
            
            if montante_faltante > 0:
                aporte_mensal = montante_faltante / (
                    ((1 + taxa_real_mensal) ** meses_ate_aposentar - 1) / taxa_real_mensal
                )
            else:
                aporte_mensal = 0
        else:
            aporte_mensal = (montante_necessario - valor_atual) / meses_ate_aposentar

        return {
            'montante_necessario': montante_necessario,
            'aporte_mensal_necessario': aporte_mensal,
            'anos_ate_aposentar': anos_ate_aposentar,
            'anos_aposentado': anos_aposentado,
            'total_a_investir': aporte_mensal * meses_ate_aposentar + valor_atual,
            'taxa_real': taxa_real
        }

    @staticmethod
    def calcular_valor_presente(
        valor_futuro: float,
        taxa: float,
        periodo: int
    ) -> float:
        """
        Calcula o valor presente de um valor futuro.

        Args:
            valor_futuro: Valor futuro
            taxa: Taxa de desconto (anual em percentual)
            periodo: Período em anos

        Returns:
            Valor presente
        """
        taxa_decimal = taxa / 100
        return valor_futuro / (1 + taxa_decimal) ** periodo

    @staticmethod
    def calcular_valor_futuro(
        valor_presente: float,
        taxa: float,
        periodo: int
    ) -> float:
        """
        Calcula o valor futuro de um valor presente.

        Args:
            valor_presente: Valor presente
            taxa: Taxa de juros (anual em percentual)
            periodo: Período em anos

        Returns:
            Valor futuro
        """
        taxa_decimal = taxa / 100
        return valor_presente * (1 + taxa_decimal) ** periodo

    @staticmethod
    def calcular_tir(
        fluxos: List[float]
    ) -> float:
        """
        Calcula a Taxa Interna de Retorno (TIR).

        Args:
            fluxos: Lista de fluxos de caixa (primeiro deve ser negativo)

        Returns:
            TIR em percentual
        """
        return np.irr(fluxos) * 100

    @staticmethod
    def calcular_vpl(
        fluxos: List[float],
        taxa: float
    ) -> float:
        """
        Calcula o Valor Presente Líquido (VPL).

        Args:
            fluxos: Lista de fluxos de caixa
            taxa: Taxa de desconto (anual em percentual)

        Returns:
            VPL
        """
        taxa_decimal = taxa / 100
        return np.npv(taxa_decimal, fluxos)