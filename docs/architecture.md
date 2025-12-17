# Arquitetura do Sistema

## Visão Geral

O Assistente Financeiro Inteligente é construído com uma arquitetura modular que separa responsabilidades e facilita manutenção e escalabilidade.

## Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface (Streamlit)                     │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │   app.py (Main)  │
        └────────┬─────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐   ┌───▼───┐   ┌───▼────┐
│Chatbot│   │  FAQ  │   │Calcul. │
└───┬───┘   └───┬───┘   └───┬────┘
    │           │            │
    └───────┬───┴────────────┘
            │
    ┌───────▼────────┐
    │ Context Manager │
    └───────┬─────────┘
            │
    ┌───────▼──────────┐
    │  Data Analysis   │
    └───────┬──────────┘
            │
    ┌───────▼──────────┐
    │    Database      │
    └──────────────────┘
```

## Módulos Principais

### 1. Chatbot (`src/chatbot/`)
**Responsabilidade**: Processamento de linguagem natural e geração de respostas

- **LLM Integration**: Conexão com OpenAI/Gemini
- **Prompt Engineering**: Templates otimizados
- **Response Parser**: Formatação de saídas

**Tecnologias**:
- LangChain para orquestração
- OpenAI GPT-4 / Google Gemini
- Token management e streaming

### 2. Calculadoras (`src/calculators/`)
**Responsabilidade**: Cálculos financeiros precisos

**Componentes**:
- `loan_calculator.py`: Financiamentos (SAC, Price)
- `investment_calculator.py`: Rentabilidade de investimentos
- `retirement_calculator.py`: Planejamento de aposentadoria

### 3. Base de Conhecimento (`src/knowledge_base/`)
**Responsabilidade**: Gerenciamento de FAQs e documentos

**Funcionalidades**:
- Busca semântica (embeddings)
- Ranking de relevância
- Cache de respostas frequentes

### 4. Análise de Dados (`src/data_analysis/`)
**Responsabilidade**: Insights e visualizações

**Recursos**:
- Análise de transações
- Categorização automática
- Gráficos interativos (Plotly)
- Relatórios personalizados

### 5. Gerenciador de Contexto (`src/context_manager.py`)
**Responsabilidade**: Persistência de conversações

**Características**:
- Histórico de mensagens
- Sessões de usuário
- Memória de curto/longo prazo

### 6. Database (`src/database/`)
**Responsabilidade**: Persistência de dados

**Estrutura**:
- SQLite para desenvolvimento
- Preparado para PostgreSQL em produção
- Migrations automáticas

## Fluxo de Dados

### 1. Requisição do Usuário
```
Usuário → Interface → Chatbot → Context Manager
                         ↓
                    LLM (GPT/Gemini)
                         ↓
                    Knowledge Base ← FAQs
                         ↓
                    Response Parser
                         ↓
                    Interface → Usuário
```

### 2. Cálculo Financeiro
```
Usuário → Interface → Calculator Module
                         ↓
                    Validation
                         ↓
                    Computation
                         ↓
                    Data Analysis (charts)
                         ↓
                    Interface → Usuário
```

## Segurança

### Camadas de Proteção

1. **API Keys**: Variáveis de ambiente (.env)
2. **Dados Sensíveis**: Criptografia AES-256
3. **Input Validation**: Sanitização de entradas
4. **Rate Limiting**: Proteção contra abuso
5. **LGPD Compliance**: Anonimização de dados

## Escalabilidade

### Horizontal Scaling
- Stateless application design
- Session management via Redis (futuro)
- Load balancing ready

### Vertical Scaling
- Caching strategies
- Database indexing
- Async operations

## Tecnologias

| Camada | Tecnologia | Propósito |
|--------|-----------|----------|
| Frontend | Streamlit | Interface web |
| Backend | Python 3.9+ | Lógica de negócio |
| LLM | OpenAI/Gemini | IA Generativa |
| Database | SQLite/PostgreSQL | Persistência |
| Cache | In-memory/Redis | Performance |
| Analytics | Pandas/Plotly | Análise de dados |

## Ambiente de Desenvolvimento

```bash
# Development
Streamlit local server
SQLite database
Debug mode enabled

# Production (futuro)
Gunicorn + Nginx
PostgreSQL
Docker containers
Kubernetes orchestration
```

## Monitoramento

### Métricas (futuro)
- Response time
- Error rate
- User satisfaction
- API usage
- Cost tracking

### Logging
- Structured logging (JSON)
- Error tracking (Sentry)
- Analytics (Google Analytics)

## Roadmap Técnico

- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] Real-time updates (WebSockets)
- [ ] ML models para recomendações
- [ ] Integration com Open Banking
- [ ] Mobile app (React Native)
