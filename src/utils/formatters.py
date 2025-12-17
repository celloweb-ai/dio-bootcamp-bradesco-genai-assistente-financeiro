"""
Formatadores de dados
Funções para formatação de moeda, percentual, data, etc.
"""

from typing import Optional
from datetime import datetime, date
import locale

# Tenta configurar locale para pt_BR
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass  # Mantém locale padrão


def formatar_moeda(valor: float, simbolo: str = 'R$') -> str:
    """
    Formata valor como moeda brasileira.

    Args:
        valor: Valor a ser formatado
        simbolo: Símbolo da moeda

    Returns:
        String formatada (ex: "R$ 1.234,56")
    """
    try:
        return f"{simbolo} {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return f"{simbolo} {valor:.2f}"


def formatar_percentual(valor: float, casas_decimais: int = 2) -> str:
    """
    Formata valor como percentual.

    Args:
        valor: Valor decimal (ex: 0.125 para 12.5%)
        casas_decimais: Número de casas decimais

    Returns:
        String formatada (ex: "12,5%" ou "12,50%")
    """
    percentual = valor * 100
    return f"{percentual:.{casas_decimais}f}%".replace('.', ',')


def formatar_data(
    data: datetime | date | str,
    formato_saida: str = '%d/%m/%Y',
    formato_entrada: Optional[str] = None
) -> str:
    """
    Formata data.

    Args:
        data: Data a ser formatada
        formato_saida: Formato de saída desejado
        formato_entrada: Formato de entrada (se data for string)

    Returns:
        String formatada
    """
    if isinstance(data, str):
        if formato_entrada:
            data = datetime.strptime(data, formato_entrada)
        else:
            # Tenta adivinhar formato
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
                try:
                    data = datetime.strptime(data, fmt)
                    break
                except ValueError:
                    continue
    
    if isinstance(data, date) and not isinstance(data, datetime):
        data = datetime.combine(data, datetime.min.time())
    
    return data.strftime(formato_saida)


def formatar_cpf(cpf: str) -> str:
    """
    Formata CPF.

    Args:
        cpf: CPF (apenas números)

    Returns:
        String formatada (ex: "123.456.789-00")
    """
    import re
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def formatar_cnpj(cnpj: str) -> str:
    """
    Formata CNPJ.

    Args:
        cnpj: CNPJ (apenas números)

    Returns:
        String formatada (ex: "12.345.678/0001-00")
    """
    import re
    cnpj = re.sub(r'\D', '', cnpj)
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def formatar_telefone(telefone: str) -> str:
    """
    Formata telefone brasileiro.

    Args:
        telefone: Telefone (apenas números)

    Returns:
        String formatada (ex: "(11) 98765-4321" ou "(11) 3456-7890")
    """
    import re
    telefone = re.sub(r'\D', '', telefone)
    
    if len(telefone) == 11:  # Celular
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"
    elif len(telefone) == 10:  # Fixo
        return f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}"
    else:
        return telefone


def formatar_cep(cep: str) -> str:
    """
    Formata CEP.

    Args:
        cep: CEP (apenas números)

    Returns:
        String formatada (ex: "12345-678")
    """
    import re
    cep = re.sub(r'\D', '', cep)
    if len(cep) != 8:
        return cep
    return f"{cep[:5]}-{cep[5:]}"


def formatar_numero(
    numero: float,
    casas_decimais: int = 2,
    separador_milhar: bool = True
) -> str:
    """
    Formata número.

    Args:
        numero: Número a ser formatado
        casas_decimais: Número de casas decimais
        separador_milhar: Se deve usar separador de milhar

    Returns:
        String formatada
    """
    if separador_milhar:
        return f"{numero:,.{casas_decimais}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    else:
        return f"{numero:.{casas_decimais}f}".replace('.', ',')


def formatar_tamanho_arquivo(bytes: int) -> str:
    """
    Formata tamanho de arquivo.

    Args:
        bytes: Tamanho em bytes

    Returns:
        String formatada (ex: "1,5 MB")
    """
    for unidade in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unidade}".replace('.', ',')
        bytes /= 1024.0
    return f"{bytes:.1f} PB".replace('.', ',')