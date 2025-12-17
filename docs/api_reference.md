# 📡 Referência da API

## Visão Geral

Documentação completa das funções e módulos do Assistente Financeiro.

## Módulos

### Chatbot

#### `ChatBot`

Classe principal para interação com IA generativa.

```python
from src.chatbot import ChatBot

chatbot = ChatBot(api_key="sua_chave_api")
```

##### Métodos

**`chat(message: str, context: dict = None) -> str`**

Processa uma mensagem e retorna resposta.

**Parâmetros:**
- `message` (str): Mensagem do usuário
- `context` (dict, opcional): Contexto da conversação

**Retorna:**
- `str`: Resposta gerada pela IA

**Exemplo:**
```python
resposta = chatbot.chat(
    message="Quanto rende R$ 10.000 na poupança?",
    context={"user_id": "123", "session_id": "abc"}
)
print(resposta)
```

**`reset_conversation() -> None`**

Reseta o histórico de conversação.

**Exemplo:**
```python
chatbot.reset_conversation()
```

---

### Calculators

#### `FinancialCalculators`

Calculadoras financeiras diversas.

```python
from src.calculators import FinancialCalculators

calc = FinancialCalculators()
```

##### Métodos

**`calcular_financiamento_sac(valor: float, entrada: float, prazo: int, taxa: float) -> dict`**

Calcula financiamento pelo sistema SAC.

**Parâmetros:**
- `valor` (float): Valor total do bem
- `entrada` (float): Valor da entrada
- `prazo` (int): Prazo em meses
- `taxa` (float): Taxa de juros anual (%)

**Retorna:**
- `dict`: Dados da simulação
  - `valor_financiado` (float)
  - `parcelas` (list): Lista de parcelas
  - `total_juros` (float)
  - `total_pago` (float)

**Exemplo:**
```python
resultado = calc.calcular_financiamento_sac(
    valor=200000,
    entrada=20000,
    prazo=180,
    taxa=9.5
)

print(f"Primeira parcela: R$ {resultado['parcelas'][0]:.2f}")
print(f"Total de juros: R$ {resultado['total_juros']:.2f}")
```

**`calcular_investimento(valor_inicial: float, aporte_mensal: float, taxa: float, prazo: int) -> dict`**

Calcula retorno de investimento com aportes.

**Parâmetros:**
- `valor_inicial` (float): Valor inicial investido
- `aporte_mensal` (float): Valor de aporte mensal
- `taxa` (float): Taxa de rendimento anual (%)
- `prazo` (int): Prazo em meses

**Retorna:**
- `dict`: Projeção do investimento
  - `montante_final` (float)
  - `total_investido` (float)
  - `total_rendimento` (float)
  - `evolucao_mensal` (list)

**Exemplo:**
```python
investimento = calc.calcular_investimento(
    valor_inicial=10000,
    aporte_mensal=500,
    taxa=12.5,
    prazo=60
)

print(f"Montante final: R$ {investimento['montante_final']:.2f}")
```

---

### Knowledge Base (FAQs)

#### `FAQManager`

Gerenciador de base de conhecimento.

```python
from src.faqs import FAQManager

faq = FAQManager()
```

##### Métodos

**`buscar(pergunta: str, top_k: int = 3) -> list`**

Busca semântica em FAQs.

**Parâmetros:**
- `pergunta` (str): Pergunta do usuário
- `top_k` (int): Número de resultados

**Retorna:**
- `list`: Lista de dicionários com FAQs relevantes

**Exemplo:**
```python
resultados = faq.buscar("Como funciona o Pix?", top_k=3)

for item in resultados:
    print(f"Pergunta: {item['pergunta']}")
    print(f"Resposta: {item['resposta']}")
    print(f"Score: {item['score']}")
    print("---")
```

**`adicionar_faq(pergunta: str, resposta: str, categoria: str) -> None`**

Adiciona nova FAQ à base.

**Parâmetros:**
- `pergunta` (str): Pergunta
- `resposta` (str): Resposta
- `categoria` (str): Categoria da FAQ

**Exemplo:**
```python
faq.adicionar_faq(
    pergunta="O que é Open Banking?",
    resposta="Open Banking é um sistema que permite...",
    categoria="Serviços Bancários"
)
```

---

### Data Analysis

#### `DataAnalyzer`

Análise e visualização de dados financeiros.

```python
from src.data_analysis import DataAnalyzer
import pandas as pd

analyzer = DataAnalyzer()
```

##### Métodos

**`analisar_gastos(df: pd.DataFrame) -> dict`**

Analisa padrões de gastos.

**Parâmetros:**
- `df` (pd.DataFrame): DataFrame com transações
  - Colunas: `data`, `descricao`, `valor`, `categoria`

**Retorna:**
- `dict`: Análise dos gastos
  - `total_gasto` (float)
  - `gastos_por_categoria` (dict)
  - `media_mensal` (float)
  - `tendencia` (str)

**Exemplo:**
```python
df = pd.DataFrame({
    'data': ['2024-01-01', '2024-01-15'],
    'descricao': ['Supermercado', 'Restaurante'],
    'valor': [350.00, 120.00],
    'categoria': ['Alimentação', 'Alimentação']
})

analise = analyzer.analisar_gastos(df)
print(analise)
```

**`gerar_grafico_evolucao(df: pd.DataFrame, periodo: str = 'mensal') -> plotly.graph_objs.Figure`**

Gera gráfico de evolução.

**Parâmetros:**
- `df` (pd.DataFrame): DataFrame com dados
- `periodo` (str): 'diario', 'mensal', 'anual'

**Retorna:**
- `plotly.graph_objs.Figure`: Gráfico interativo

**Exemplo:**
```python
import streamlit as st

fig = analyzer.gerar_grafico_evolucao(df, periodo='mensal')
st.plotly_chart(fig)
```

---

### Context Manager

#### `ContextManager`

Gerencia contexto de conversações.

```python
from src.context_manager import ContextManager

context = ContextManager()
```

##### Métodos

**`adicionar_mensagem(user_id: str, message: str, role: str) -> None`**

Adiciona mensagem ao contexto.

**Parâmetros:**
- `user_id` (str): ID do usuário
- `message` (str): Conteúdo da mensagem
- `role` (str): 'user' ou 'assistant'

**Exemplo:**
```python
context.adicionar_mensagem(
    user_id="user123",
    message="Quanto tenho na poupança?",
    role="user"
)
```

**`obter_historico(user_id: str, limite: int = 10) -> list`**

Obtém histórico de mensagens.

**Parâmetros:**
- `user_id` (str): ID do usuário
- `limite` (int): Número de mensagens

**Retorna:**
- `list`: Lista de mensagens

**Exemplo:**
```python
historico = context.obter_historico("user123", limite=5)
for msg in historico:
    print(f"{msg['role']}: {msg['message']}")
```

---

### Database

#### `DatabaseManager`

Gerenciamento de banco de dados.

```python
from src.database import DatabaseManager

db = DatabaseManager()
```

##### Métodos

**`salvar_conversa(user_id: str, messages: list) -> None`**

Salva conversação no banco.

**`carregar_conversa(user_id: str) -> list`**

Carrega conversação do banco.

**`salvar_preferencias(user_id: str, preferencias: dict) -> None`**

Salva preferências do usuário.

---

### Utils

#### Validators

```python
from src.utils.validators import validar_cpf, validar_email

# Validar CPF
if validar_cpf("123.456.789-00"):
    print("CPF válido")

# Validar email
if validar_email("usuario@example.com"):
    print("Email válido")
```

#### Formatters

```python
from src.utils.formatters import formatar_moeda, formatar_percentual

# Formatar moeda
print(formatar_moeda(1234.56))  # "R$ 1.234,56"

# Formatar percentual
print(formatar_percentual(0.125))  # "12,5%"
```

---

## Tratamento de Erros

Todas as funções podem lançar exceções. Sempre use try/except:

```python
try:
    resultado = calc.calcular_financiamento_sac(
        valor=200000,
        entrada=20000,
        prazo=180,
        taxa=9.5
    )
except ValueError as e:
    print(f"Erro de validação: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

## Variáveis de Ambiente

```bash
# .env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
DATABASE_URL=sqlite:///assistente.db
LOG_LEVEL=INFO
```

## Logging

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Operação realizada com sucesso")
logger.error("Erro ao processar solicitação")
```