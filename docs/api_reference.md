# API Reference

## Visão Geral

Documentação completa dos módulos, classes e funções do Assistente Financeiro.

## Módulo: Chatbot

### `ChatbotEngine`

Classe principal para gerenciamento do chatbot com IA generativa.

```python
from src.chatbot import ChatbotEngine

chatbot = ChatbotEngine(
    model="gpt-4",
    temperature=0.7,
    max_tokens=500
)
```

#### Métodos

##### `generate_response()`

Gera uma resposta baseada na mensagem do usuário.

**Parâmetros**:
- `message` (str): Mensagem do usuário
- `context` (list, opcional): Histórico de conversação
- `user_profile` (dict, opcional): Perfil do usuário

**Retorna**:
- `dict`: Resposta formatada com texto e metadados

**Exemplo**:
```python
response = chatbot.generate_response(
    message="Como funciona a poupança?",
    context=[
        {"role": "user", "content": "Olá"},
        {"role": "assistant", "content": "Olá! Como posso ajudar?"}
    ]
)

print(response['text'])
print(response['confidence'])  # Score de confiança 0-1
```

---

## Módulo: Calculators

### `LoanCalculator`

Calculadora de financiamentos e empréstimos.

```python
from src.calculators import LoanCalculator

calc = LoanCalculator()
```

#### Métodos

##### `calculate_sac()`

Calcula financiamento pelo Sistema SAC (amortização constante).

**Parâmetros**:
- `principal` (float): Valor financiado
- `annual_rate` (float): Taxa de juros anual (%)
- `months` (int): Prazo em meses

**Retorna**:
- `dict`: Detalhes do financiamento
  - `parcelas` (list): Lista de parcelas
  - `total_juros` (float): Total de juros pagos
  - `total_pago` (float): Total pago

**Exemplo**:
```python
result = calc.calculate_sac(
    principal=300000,  # R$ 300.000
    annual_rate=8.5,   # 8.5% a.a.
    months=360         # 30 anos
)

for i, parcela in enumerate(result['parcelas'][:12]):
    print(f"Mês {i+1}: R$ {parcela['valor']:.2f}")
```

##### `calculate_price()`

Calcula financiamento pelo Sistema Price (parcelas fixas).

**Parâmetros**: Idênticos a `calculate_sac()`

**Retorna**: Estrutura idêntica a `calculate_sac()`

---

### `InvestmentCalculator`

Calculadora de investimentos.

```python
from src.calculators import InvestmentCalculator

invest_calc = InvestmentCalculator()
```

#### Métodos

##### `calculate_compound_interest()`

Calcula juros compostos para investimentos.

**Parâmetros**:
- `initial_amount` (float): Valor inicial
- `monthly_contribution` (float): Aporte mensal
- `annual_rate` (float): Rentabilidade anual (%)
- `months` (int): Período em meses
- `tax_rate` (float, opcional): IR sobre rendimento (%)

**Retorna**:
- `dict`:
  - `final_amount` (float): Montante final
  - `total_invested` (float): Total investido
  - `net_profit` (float): Lucro líquido
  - `monthly_breakdown` (list): Evolução mensal

**Exemplo**:
```python
result = invest_calc.calculate_compound_interest(
    initial_amount=10000,
    monthly_contribution=500,
    annual_rate=12,  # 12% a.a.
    months=60,       # 5 anos
    tax_rate=15      # 15% IR
)

print(f"Montante final: R$ {result['final_amount']:,.2f}")
print(f"Lucro líquido: R$ {result['net_profit']:,.2f}")
```

---

## Módulo: FAQs

### `FAQEngine`

Motor de busca e resposta de perguntas frequentes.

```python
from src.faqs import FAQEngine

faq = FAQEngine(data_path="data/samples/faqs.json")
```

#### Métodos

##### `search()`

Busca semântica por FAQs relevantes.

**Parâmetros**:
- `query` (str): Pergunta do usuário
- `top_k` (int): Número de resultados (padrão: 3)
- `threshold` (float): Score mínimo de relevância (0-1)

**Retorna**:
- `list`: FAQs mais relevantes com scores

**Exemplo**:
```python
results = faq.search(
    query="Como aumentar meu limite?",
    top_k=3,
    threshold=0.7
)

for item in results:
    print(f"Score: {item['score']:.2f}")
    print(f"Q: {item['pergunta']}")
    print(f"A: {item['resposta']}\n")
```

##### `get_by_category()`

Retorna todas FAQs de uma categoria.

**Parâmetros**:
- `category` (str): Nome da categoria

**Retorna**:
- `list`: FAQs da categoria

**Exemplo**:
```python
investment_faqs = faq.get_by_category("investimentos")
```

---

## Módulo: Data Analysis

### `TransactionAnalyzer`

Analisador de transações financeiras.

```python
from src.data_analysis import TransactionAnalyzer

analyzer = TransactionAnalyzer()
```

#### Métodos

##### `load_transactions()`

Carrega transações de um DataFrame ou arquivo.

**Parâmetros**:
- `data` (pd.DataFrame ou str): DataFrame ou caminho do CSV

**Retorna**:
- `bool`: Sucesso da operação

##### `get_monthly_summary()`

Resumo mensal de receitas e despesas.

**Parâmetros**:
- `year` (int): Ano
- `month` (int): Mês

**Retorna**:
- `dict`:
  - `receitas` (float)
  - `despesas` (float)
  - `saldo` (float)
  - `por_categoria` (dict)

**Exemplo**:
```python
analyzer.load_transactions("data/samples/transactions.csv")

summary = analyzer.get_monthly_summary(2024, 1)
print(f"Receitas: R$ {summary['receitas']:.2f}")
print(f"Despesas: R$ {summary['despesas']:.2f}")
print(f"Saldo: R$ {summary['saldo']:.2f}")
```

##### `plot_category_distribution()`

Gera gráfico de pizza com distribuição por categoria.

**Parâmetros**:
- `transaction_type` (str): "credito" ou "debito"

**Retorna**:
- `plotly.graph_objects.Figure`: Gráfico interativo

---

## Módulo: Context Manager

### `ContextManager`

Gerenciador de contexto e histórico de conversação.

```python
from src.context_manager import ContextManager

context = ContextManager(db_path="data/context.db")
```

#### Métodos

##### `add_message()`

Adiciona mensagem ao histórico.

**Parâmetros**:
- `session_id` (str): ID da sessão
- `role` (str): "user" ou "assistant"
- `content` (str): Conteúdo da mensagem
- `metadata` (dict, opcional): Dados adicionais

**Retorna**:
- `int`: ID da mensagem

##### `get_history()`

Recupera histórico de uma sessão.

**Parâmetros**:
- `session_id` (str): ID da sessão
- `limit` (int, opcional): Número de mensagens

**Retorna**:
- `list`: Mensagens ordenadas cronologicamente

**Exemplo**:
```python
# Adicionar mensagens
context.add_message(
    session_id="user123",
    role="user",
    content="Quanto rende a poupança?"
)

context.add_message(
    session_id="user123",
    role="assistant",
    content="A poupança rende 70% da Selic + TR..."
)

# Recuperar histórico
history = context.get_history("user123", limit=10)
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

---

## Utilitários

### `format_currency()`

Formata valores monetários.

```python
from src.utils import format_currency

value = format_currency(1500.50)
print(value)  # "R$ 1.500,50"
```

### `validate_cpf()`

Valida número de CPF.

```python
from src.utils import validate_cpf

is_valid = validate_cpf("123.456.789-00")
print(is_valid)  # True ou False
```

### `calculate_working_days()`

Calcula dias úteis entre duas datas.

```python
from src.utils import calculate_working_days
from datetime import date

days = calculate_working_days(
    start_date=date(2024, 1, 1),
    end_date=date(2024, 12, 31)
)
print(f"Dias úteis: {days}")
```

---

## Exceções

### `ChatbotError`

Erro relacionado ao processamento do chatbot.

### `CalculationError`

Erro em cálculos financeiros.

### `DatabaseError`

Erro de conexão ou operação no banco de dados.

**Exemplo de tratamento**:
```python
from src.exceptions import CalculationError

try:
    result = calc.calculate_sac(principal=-1000, annual_rate=10, months=12)
except CalculationError as e:
    print(f"Erro: {e}")
```

---

## Tipos de Dados

### UserProfile

```python
UserProfile = {
    "id": str,
    "name": str,
    "risk_profile": str,  # "conservador", "moderado", "arrojado"
    "income_range": str,  # "0-2k", "2k-5k", "5k-10k", "10k+"
    "goals": List[str],   # ["aposentadoria", "casa_propria", ...]
    "preferences": dict
}
```

### Transaction

```python
Transaction = {
    "id": int,
    "date": str,          # ISO format "YYYY-MM-DD"
    "description": str,
    "amount": float,
    "category": str,
    "type": str          # "credito" ou "debito"
}
```

---

## Configuração

### Variáveis de Ambiente

```bash
# .env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
DATABASE_URL=sqlite:///data/app.db
DEBUG=True
LOG_LEVEL=INFO
```

### Constantes

```python
# src/config.py

DEFAULT_MODEL = "gpt-4"
MAX_TOKENS = 500
TEMPERATURE = 0.7
SESSION_TIMEOUT = 3600  # segundos
MAX_HISTORY_LENGTH = 50  # mensagens
```

---

## Testes

Todos os módulos possuem testes unitários em `tests/`.

```bash
# Executar todos os testes
pytest

# Testes com coverage
pytest --cov=src tests/

# Teste específico
pytest tests/test_calculators.py::test_calculate_sac
```
