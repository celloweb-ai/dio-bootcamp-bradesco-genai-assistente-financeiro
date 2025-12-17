# 📂 Dados

Diretório para armazenamento de datasets e arquivos de dados.

## Estrutura

```
data/
├── raw/              # Dados brutos
├── processed/        # Dados processados
├── samples/          # Dados de exemplo
└── exports/          # Exportações
```

## Tipos de Dados

### FAQs
- Perguntas e respostas sobre produtos financeiros
- Formato: JSON, CSV

### Transações (Exemplos)
- Dados de exemplo para testes
- Formato: CSV, Parquet

### Embeddings
- Vetores para busca semântica
- Formato: NPY, Pickle

## Segurança

⚠️ **IMPORTANTE**: 
- Não commitar dados sensíveis
- Usar .gitignore para dados reais
- Apenas dados de exemplo/mock no repositório

## Exemplos de Uso

```python
import pandas as pd

# Carregar dados de exemplo
df = pd.read_csv('data/samples/transacoes_exemplo.csv')
```