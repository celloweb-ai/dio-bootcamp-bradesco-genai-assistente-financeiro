"""Módulo de base de conhecimento e FAQs.

Este módulo gerencia a base de conhecimento do assistente,
incluindo FAQs, documentação de produtos e busca semântica.
"""

from .faq_manager import FAQManager
from .product_catalog import ProductCatalog

__all__ = ['FAQManager', 'ProductCatalog']
