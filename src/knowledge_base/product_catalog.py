"""Catálogo de produtos e serviços financeiros."""

from typing import List, Dict, Optional


class ProductCatalog:
    """Catálogo de produtos financeiros do Bradesco."""
    
    def __init__(self):
        """Inicializa o catálogo de produtos."""
        self.products = self._load_products()
    
    def _load_products(self) -> List[Dict]:
        """Carrega catálogo de produtos."""
        return [
            {
                "id": "cc_prime",
                "name": "Conta Corrente Prime",
                "category": "Conta Corrente",
                "description": "Conta completa com benefícios exclusivos e tarifas diferenciadas.",
                "features": [
                    "Cartão de crédito sem anuidade",
                    "Transferências ilimitadas",
                    "Assessoria financeira",
                    "Seguros inclusos"
                ],
                "target_audience": "Alta renda"
            },
            {
                "id": "poupanca",
                "name": "Poupança Bradesco",
                "category": "Investimentos",
                "description": "Investimento seguro com liquidez diária e rendimento mensal.",
                "features": [
                    "Sem taxa de administração",
                    "Liquidez diária",
                    "Rendimento mensal",
                    "Garantia do FGC até R$ 250.000"
                ],
                "target_audience": "Conservador"
            },
            {
                "id": "cdb",
                "name": "CDB Bradesco",
                "category": "Investimentos",
                "description": "Certificado de Depósito Bancário com rentabilidade atrativa.",
                "features": [
                    "Rentabilidade acima da poupança",
                    "Diferentes prazos de vencimento",
                    "Garantia do FGC",
                    "Opções de liquidez"
                ],
                "target_audience": "Moderado"
            },
            {
                "id": "credito_pessoal",
                "name": "Crédito Pessoal",
                "category": "Empréstimos",
                "description": "Empréstimo com taxas competitivas e prazos flexíveis.",
                "features": [
                    "Até 60 meses para pagar",
                    "Taxas competitivas",
                    "Aprovação rápida",
                    "Crédito de até R$ 50.000"
                ],
                "target_audience": "Geral"
            },
            {
                "id": "consorcio",
                "name": "Consórcio Bradesco",
                "category": "Financiamentos",
                "description": "Planejamento para aquisição de bens sem juros.",
                "features": [
                    "Sem juros",
                    "Taxas de administração reduzidas",
                    "Diversos segmentos (imóveis, veículos, serviços)",
                    "Flexibilidade de prazos"
                ],
                "target_audience": "Planejador"
            }
        ]
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """Obtém produto por ID.
        
        Args:
            product_id: ID do produto
            
        Returns:
            Dicionário com dados do produto ou None
        """
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Obtém produtos por categoria.
        
        Args:
            category: Nome da categoria
            
        Returns:
            Lista de produtos da categoria
        """
        return [p for p in self.products if p['category'].lower() == category.lower()]
    
    def search_products(self, query: str) -> List[Dict]:
        """Busca produtos por termo.
        
        Args:
            query: Termo de busca
            
        Returns:
            Lista de produtos encontrados
        """
        query_lower = query.lower()
        results = []
        
        for product in self.products:
            if (query_lower in product['name'].lower() or 
                query_lower in product['description'].lower() or
                query_lower in product['category'].lower()):
                results.append(product)
        
        return results
    
    def get_all_categories(self) -> List[str]:
        """Retorna todas as categorias de produtos.
        
        Returns:
            Lista de categorias únicas
        """
        return list(set(p['category'] for p in self.products))
