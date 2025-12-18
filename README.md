# 🤖 Assistente Financeiro Inteligente com IA Generativa

![Header](./github-header-banner.png)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![DIO](https://img.shields.io/badge/Bootcamp-DIO%20Bradesco-orange.svg)](https://dio.me)

> Projeto desenvolvido para o **DIO Bootcamp Bradesco - GenAI & Dados**

Uma experiência digital inteligente para relacionamento financeiro, utilizando IA generativa para oferecer interações personalizadas, seguras e contextualizadas.

## 🎯 Sobre o Projeto

Este assistente financeiro integra:
- **IA Generativa** para compreensão de linguagem natural
- **FAQs Inteligentes** com respostas contextualizadas
- **Calculadoras Financeiras** demonstrativas
- **Explicações de Produtos** bancários e investimentos
- **Persistência de Contexto** para conversas continuadas
- **Análise de Dados** para insights personalizados

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **OpenAI GPT** / **Google Gemini** para IA generativa
- **Streamlit** para interface web
- **Pandas** para análise de dados
- **SQLite** para persistência
- **LangChain** para orquestração de LLM
- **Plotly** para visualizações

## 📁 Estrutura do Projeto

```
dio-bootcamp-bradesco-genai-assistente-financeiro/
├── src/
│   ├── chatbot/              # Módulo principal do chatbot
│   ├── calculators/          # Calculadoras financeiras
│   ├── knowledge_base/       # Base de conhecimento e FAQs
│   ├── data_analysis/        # Análise e visualização de dados
│   ├── database/             # Gerenciamento de persistência
│   └── utils/                # Utilitários e helpers
├── data/                     # Dados e datasets
├── docs/                     # Documentação
├── tests/                    # Testes automatizados
├── notebooks/                # Jupyter notebooks
├── app.py                    # Aplicação Streamlit
├── requirements.txt          # Dependências
└── .env.example              # Exemplo de variáveis de ambiente
```

## 🚀 Como Executar

### 1. Clone o Repositório
```bash
git clone https://github.com/celloweb-ai/dio-bootcamp-bradesco-genai-assistente-financeiro.git
cd dio-bootcamp-bradesco-genai-assistente-financeiro
```

### 2. Crie um Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves de API
```

### 5. Execute a Aplicação
```bash
streamlit run app.py
```

Acesse: `http://localhost:8501`

## ✨ Funcionalidades

### 1. 💬 Chatbot Inteligente
- Compreensão de linguagem natural
- Respostas contextualizadas sobre produtos financeiros
- Histórico de conversações persistente

### 2. 🧑‍🏫 FAQs Dinâmicas
- Busca semântica em base de conhecimento
- Respostas adaptadas ao perfil do usuário
- Atualização contínua da base

### 3. 🧮 Calculadoras Financeiras
- Financiamento (SAC, Price, Amort. Constante)
- Investimentos (renda fixa, tesouro, ações)
- Simulações de aposentadoria
- Cálculo de juros compostos

### 4. 📊 Análise de Dados
- Visualizações interativas
- Insights personalizados
- Recomendações baseadas em perfil

### 5. 🔒 Segurança e Privacidade
- Criptografia de dados sensíveis
- Conformidade com LGPD
- Autenticação e autorização

## 📖 Documentação

Documentação completa disponível em: [docs/](docs/)

- [Arquitetura do Sistema](docs/architecture.md)
- [Guia de UX/UI](docs/ux_guidelines.md)
- [API Reference](docs/api_reference.md)
- [Casos de Uso](docs/use_cases.md)

## 🧪 Testes

```bash
pytest tests/ -v
```

## 📈 Roadmap

- [x] Estrutura inicial do projeto
- [x] Implementação do chatbot base
- [x] Calculadoras financeiras
- [x] Sistema de FAQs
- [ ] Integração com APIs bancárias (Open Banking)
- [ ] Módulo de recomendações avançadas
- [ ] App mobile (React Native)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 👥 Autor

**Marcus Vasconcellos**
- GitHub: [@celloweb-ai](https://github.com/celloweb-ai)
- LinkedIn: [marcusvasconcellos](https://www.linkedin.com/in/marcusvasconcellos)

## 📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🎓 Agradecimentos

- [DIO - Digital Innovation One](https://dio.me)
- [Bradesco](https://www.bradesco.com.br)
- Comunidade Open Source

---

**Desenvolvido com ❤️ durante o DIO Bootcamp Bradesco - GenAI & Dados**
