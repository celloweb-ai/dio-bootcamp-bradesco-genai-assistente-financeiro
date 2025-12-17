# Dados e Datasets

Este diretório contém os dados utilizados pelo assistente financeiro.

## Estrutura

```
data/
├── raw/                  # Dados brutos
├── processed/            # Dados processados
├── external/             # Dados externos (APIs, etc)
├── user_data/            # Dados de usuários (gitignored)
└── samples/              # Dados de exemplo para testes
```

## Segurança

⚠️ **IMPORTANTE**: Nunca commite dados sensíveis ou pessoais!

- Dados de usuários devem estar em `user_data/` (incluído no .gitignore)
- Use sempre dados anonimizados para exemplos
- Respeite a LGPD em todo tratamento de dados

## Datasets Disponíveis

### Samples
- `samples/transactions.csv` - Transações de exemplo
- `samples/products.json` - Catálogo de produtos financeiros
- `samples/faqs.json` - Base de perguntas frequentes

### External
- Cotações de mercado (via API)
- Taxas de juros (Banco Central)
- Índices econômicos
