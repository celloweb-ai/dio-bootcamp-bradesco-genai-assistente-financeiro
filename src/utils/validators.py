"""
Validadores de dados
Funções para validação de CPF, email, telefone, etc.
"""

import re
from typing import Optional


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF.

    Args:
        cpf: CPF a ser validado (com ou sem pontuação)

    Returns:
        True se válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cpf = re.sub(r'\D', '', cpf)

    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Valida primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if int(cpf[9]) != digito1:
        return False

    # Valida segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if int(cpf[10]) != digito2:
        return False

    return True


def validar_cnpj(cnpj: str) -> bool:
    """
    Valida CNPJ.

    Args:
        cnpj: CNPJ a ser validado (com ou sem pontuação)

    Returns:
        True se válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cnpj = re.sub(r'\D', '', cnpj)

    # Verifica se tem 14 dígitos
    if len(cnpj) != 14:
        return False

    # Verifica se todos os dígitos são iguais
    if cnpj == cnpj[0] * 14:
        return False

    # Valida primeiro dígito verificador
    multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores1[i] for i in range(12))
    digito1 = 11 - (soma % 11)
    digito1 = 0 if digito1 >= 10 else digito1
    if int(cnpj[12]) != digito1:
        return False

    # Valida segundo dígito verificador
    multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * multiplicadores2[i] for i in range(13))
    digito2 = 11 - (soma % 11)
    digito2 = 0 if digito2 >= 10 else digito2
    if int(cnpj[13]) != digito2:
        return False

    return True


def validar_email(email: str) -> bool:
    """
    Valida email.

    Args:
        email: Email a ser validado

    Returns:
        True se válido, False caso contrário
    """
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))


def validar_telefone(telefone: str) -> bool:
    """
    Valida telefone brasileiro (celular ou fixo).

    Args:
        telefone: Telefone a ser validado (com ou sem pontuação)

    Returns:
        True se válido, False caso contrário
    """
    # Remove caracteres não numéricos
    telefone = re.sub(r'\D', '', telefone)

    # Verifica se tem 10 ou 11 dígitos (com DDD)
    if len(telefone) not in [10, 11]:
        return False

    # Verifica DDD válido (11 a 99)
    ddd = int(telefone[:2])
    if ddd < 11 or ddd > 99:
        return False

    # Se tem 11 dígitos, o terceiro deve ser 9 (celular)
    if len(telefone) == 11 and telefone[2] != '9':
        return False

    return True


def validar_cep(cep: str) -> bool:
    """
    Valida CEP.

    Args:
        cep: CEP a ser validado (com ou sem pontuação)

    Returns:
        True se válido, False caso contrário
    """
    # Remove caracteres não numéricos
    cep = re.sub(r'\D', '', cep)

    # Verifica se tem 8 dígitos
    return len(cep) == 8


def validar_valor_monetario(valor: str) -> bool:
    """
    Valida formato de valor monetário.

    Args:
        valor: Valor a ser validado (ex: "1.234,56" ou "1234.56")

    Returns:
        True se válido, False caso contrário
    """
    # Aceita formatos: 1234.56, 1.234,56, 1234,56
    padrao = r'^\d{1,3}(\.\d{3})*(,\d{2})?$|^\d+(\.\d{2})?$'
    return bool(re.match(padrao, valor))


def validar_data(data: str, formato: str = '%d/%m/%Y') -> bool:
    """
    Valida formato de data.

    Args:
        data: Data a ser validada
        formato: Formato esperado (padrão: dd/mm/yyyy)

    Returns:
        True se válido, False caso contrário
    """
    from datetime import datetime
    try:
        datetime.strptime(data, formato)
        return True
    except ValueError:
        return False