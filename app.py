"""Aplicativo principal - Assistente Financeiro Inteligente.

Interface web com Streamlit integrando todos os módulos:
- Chatbot com IA generativa
- Sistema de FAQs
- Calculadoras financeiras
- Análise de dados
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Importa módulos
from src.chatbot import FinancialChatbot
from src.faqs import IntelligentFAQ
from src.calculators import FinancialCalculators
from src.data_analysis import FinancialDataAnalyzer
from src.context_manager import ConversationContext

# Configuração da página
st.set_page_config(
    page_title="Assistente Financeiro Bradesco",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #CC0000;
        text-align: center;
        padding: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #E8F4F8;
    }
    .assistant-message {
        background-color: #F5F5F5;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização de estado
if 'context' not in st.session_state:
    st.session_state.context = ConversationContext()
if 'faq_system' not in st.session_state:
    st.session_state.faq_system = IntelligentFAQ()
if 'data_analyzer' not in st.session_state:
    st.session_state.data_analyzer = FinancialDataAnalyzer()

# Sidebar
with st.sidebar:
    st.image("https://logodownload.org/wp-content/uploads/2014/05/bradesco-logo-0.png", width=200)
    st.markdown("---")
    
    page = st.selectbox(
        "Navegação",
        ["🏠 Início", "💬 Chat IA", "❓ FAQs", "📊 Calculadoras", "📊 Análise de Dados"]
    )
    
    st.markdown("---")
    st.markdown("### 🛡️ Segurança")
    st.info("Este é um ambiente seguro. Nunca compartilhe senhas ou dados sensíveis.")
    
    st.markdown("---")
    st.markdown("### 📞 Contato")
    st.markdown("""
    **Central de Atendimento:**
    - 4004-0022 (capitais)
    - 0800-570-0022 (demais localidades)
    - 24 horas, 7 dias por semana
    """)

# Página Inicial
if page == "🏠 Início":
    st.markdown('<div class="main-header">💰 Assistente Financeiro Inteligente</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Sua jornada para saúde financeira começa aqui</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🤖 Chat com IA")
        st.write("Converse com nosso assistente inteligente para tirar dúvidas e receber orientações personalizadas.")
        st.markdown("**Recursos:**")
        st.markdown("- Processamento de linguagem natural")
        st.markdown("- Respostas contextualizadas")
        st.markdown("- Memória de conversação")
    
    with col2:
        st.markdown("### 📊 Calculadoras")
        st.write("Ferramentas para planejamento financeiro e simulações.")
        st.markdown("**Disponíveis:**")
        st.markdown("- Juros compostos")
        st.markdown("- Financiamentos")
        st.markdown("- Aposentadoria")
    
    with col3:
        st.markdown("### 📈 Análise de Dados")
        st.write("Visualize e analise seus gastos para tomar decisões melhores.")
        st.markdown("**Funcionalidades:**")
        st.markdown("- Análise de gastos")
        st.markdown("- Insights automáticos")
        st.markdown("- Visualizações")
    
    st.markdown("---")
    st.info("💡 **Dica:** Use o menu lateral para navegar entre as funcionalidades!")

# Página Chat IA
elif page == "💬 Chat IA":
    st.markdown('<div class="main-header">🤖 Chat com Assistente IA</div>', unsafe_allow_html=True)
    
    # Verifica se API key está configurada
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'sua_chave_api_aqui':
        st.error("⚠️ API Key da OpenAI não configurada!")
        st.info("""
        Para usar o chat com IA:
        1. Crie uma conta em https://platform.openai.com/
        2. Gere uma API key
        3. Configure no arquivo .env: OPENAI_API_KEY=sua_chave
        """)
        st.stop()
    
    try:
        if 'chatbot' not in st.session_state:
            st.session_state.chatbot = FinancialChatbot(api_key)
        
        # Exibe histórico
        for msg in st.session_state.chatbot.get_context():
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Digite sua mensagem..."):
            # Exibe mensagem do usuário
            with st.chat_message("user"):
                st.write(prompt)
            
            # Obtém resposta
            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    response = st.session_state.chatbot.chat(prompt)
                    st.write(response)
        
        # Botões de controle
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Limpar Chat"):
                st.session_state.chatbot.clear_context()
                st.rerun()
    
    except Exception as e:
        st.error(f"Erro ao inicializar chatbot: {str(e)}")
        st.info("Verifique se a API key da OpenAI está correta e válida.")

# Página FAQs
elif page == "❓ FAQs":
    st.markdown('<div class="main-header">❓ Perguntas Frequentes</div>', unsafe_allow_html=True)
    
    # Busca
    query = st.text_input("🔍 Buscar pergunta:", placeholder="Ex: Como abrir uma conta?")
    
    if query:
        result = st.session_state.faq_system.get_answer(query)
        
        if result['found']:
            st.success(f"**{result['category']}**")
            st.markdown(f"### {result['question']}")
            st.markdown(result['answer'])
            st.markdown(f"*Relevância: {result['relevance']*100:.0f}%*")
            
            if result.get('related'):
                st.markdown("---")
                st.markdown("**Perguntas relacionadas:**")
                for q in result['related']:
                    st.markdown(f"- {q}")
        else:
            st.warning(result['message'])
            st.markdown("**Sugestões:**")
            for q in result['suggestions']:
                st.markdown(f"- {q}")
    
    # Categorias
    st.markdown("---")
    st.markdown("### 📂 Navegar por Categoria")
    
    categories = st.session_state.faq_system.list_categories()
    selected_category = st.selectbox("Selecione uma categoria:", ["Todas"] + categories)
    
    if selected_category != "Todas":
        faqs = st.session_state.faq_system.get_faqs_by_category(selected_category)
        for faq in faqs:
            with st.expander(faq['question']):
                st.markdown(faq['answer'])

# Página Calculadoras
elif page == "📊 Calculadoras":
    st.markdown('<div class="main-header">📊 Calculadoras Financeiras</div>', unsafe_allow_html=True)
    
    calc_type = st.selectbox(
        "Escolha a calculadora:",
        ["Juros Compostos", "Financiamento", "Aposentadoria", "Comparar Investimentos"]
    )
    
    st.markdown("---")
    
    if calc_type == "Juros Compostos":
        st.markdown("### 💵 Calculadora de Juros Compostos")
        
        col1, col2 = st.columns(2)
        with col1:
            principal = st.number_input("Valor Inicial (R$)", min_value=0.0, value=1000.0, step=100.0)
            rate = st.number_input("Taxa de Juros (% ao ano)", min_value=0.0, value=10.0, step=0.5)
        with col2:
            time = st.number_input("Período (meses)", min_value=1, value=12, step=1)
            contribution = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=100.0, step=50.0)
        
        if st.button("Calcular"):
            result = FinancialCalculators.compound_interest(principal, rate, time, contribution)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Valor Final", f"R$ {result.final_amount:,.2f}")
            with col2:
                st.metric("Total Investido", f"R$ {result.total_invested:,.2f}")
            with col3:
                st.metric("Juros Ganhos", f"R$ {result.total_interest:,.2f}")
            
            st.markdown("---")
            st.markdown("### 📈 Evolução do Investimento")
            
            import pandas as pd
            df = pd.DataFrame(result.monthly_breakdown)
            st.line_chart(df.set_index('month')['balance'])
    
    elif calc_type == "Financiamento":
        st.markdown("### 🏠 Calculadora de Financiamento")
        
        col1, col2 = st.columns(2)
        with col1:
            loan_amount = st.number_input("Valor do Empréstimo (R$)", min_value=1000.0, value=100000.0, step=1000.0)
            annual_rate = st.number_input("Taxa de Juros (% ao ano)", min_value=0.0, value=12.0, step=0.5)
        with col2:
            months = st.number_input("Prazo (meses)", min_value=1, value=36, step=1)
            system = st.selectbox("Sistema de Amortização", ["PRICE", "SAC"])
        
        if st.button("Calcular Financiamento"):
            result = FinancialCalculators.loan_calculator(loan_amount, annual_rate, months, system)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Parcela Média", f"R$ {result.monthly_payment:,.2f}")
            with col2:
                st.metric("Total a Pagar", f"R$ {result.total_amount:,.2f}")
            with col3:
                st.metric("Total de Juros", f"R$ {result.total_interest:,.2f}")
            
            st.markdown("---")
            st.markdown("### 📄 Tabela de Parcelas (primeiras 12)")
            
            import pandas as pd
            df = pd.DataFrame(result.installments[:12])
            st.dataframe(df.style.format({
                'payment': 'R$ {:,.2f}',
                'principal': 'R$ {:,.2f}',
                'interest': 'R$ {:,.2f}',
                'balance': 'R$ {:,.2f}'
            }))
    
    elif calc_type == "Aposentadoria":
        st.markdown("### 👴 Planejamento de Aposentadoria")
        
        col1, col2 = st.columns(2)
        with col1:
            current_age = st.number_input("Idade Atual", min_value=18, max_value=100, value=30)
            retirement_age = st.number_input("Idade de Aposentadoria", min_value=current_age+1, max_value=100, value=65)
            monthly_contribution = st.number_input("Contribuição Mensal (R$)", min_value=0.0, value=500.0, step=50.0)
        with col2:
            expected_return = st.number_input("Retorno Esperado (% ao ano)", min_value=0.0, value=8.0, step=0.5)
            current_savings = st.number_input("Patrimônio Atual (R$)", min_value=0.0, value=10000.0, step=1000.0)
        
        if st.button("Calcular Aposentadoria"):
            result = FinancialCalculators.retirement_calculator(
                current_age, retirement_age, monthly_contribution, expected_return, current_savings
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Reserva na Aposentadoria", f"R$ {result['retirement_fund']:,.2f}")
                st.metric("Anos até Aposentar", f"{result['years_until_retirement']} anos")
            with col2:
                st.metric("Renda Mensal Estimada", f"R$ {result['estimated_monthly_income']:,.2f}")
                st.metric("Retorno Total", f"{result['total_return_percentage']:.1f}%")
            
            st.info("💡 A renda mensal é estimada usando a regra dos 4% (saque anual seguro).")

# Página Análise de Dados
elif page == "📊 Análise de Dados":
    st.markdown('<div class="main-header">📈 Análise de Dados Financeiros</div>', unsafe_allow_html=True)
    
    # Gera dados de exemplo
    if st.button("🎲 Gerar Dados de Exemplo"):
        st.session_state.data_analyzer.create_sample_data(months=6)
        st.success("✅ Dados de exemplo gerados!")
    
    if st.session_state.data_analyzer.transactions:
        # Resumo
        summary = st.session_state.data_analyzer.get_summary()
        
        st.markdown("### 📊 Resumo Financeiro")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Receitas", f"R$ {summary['total_income']:,.2f}")
        with col2:
            st.metric("Despesas", f"R$ {summary['total_expense']:,.2f}")
        with col3:
            st.metric("Saldo", f"R$ {summary['balance']:,.2f}")
        with col4:
            st.metric("Taxa de Poupança", f"{summary['savings_rate']:.1f}%")
        
        # Insights
        st.markdown("---")
        st.markdown("### 💡 Insights Automáticos")
        insights = st.session_state.data_analyzer.generate_insights()
        for insight in insights:
            st.markdown(insight)
        
        # Gastos por categoria
        st.markdown("---")
        st.markdown("### 📊 Gastos por Categoria")
        expenses = st.session_state.data_analyzer.get_expenses_by_category()
        
        import pandas as pd
        df_expenses = pd.DataFrame(list(expenses.items()), columns=['Categoria', 'Valor'])
        df_expenses = df_expenses.sort_values('Valor', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.bar_chart(df_expenses.set_index('Categoria'))
        with col2:
            st.dataframe(df_expenses.style.format({'Valor': 'R$ {:,.2f}'}))
        
        # Exportar
        st.markdown("---")
        if st.button("💾 Exportar para CSV"):
            st.session_state.data_analyzer.export_to_csv('transactions_export.csv')
            st.success("✅ Arquivo 'transactions_export.csv' criado!")
    else:
        st.info("📊 Clique em 'Gerar Dados de Exemplo' para começar a análise!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>💻 Desenvolvido para o <strong>DIO Bootcamp Bradesco - GenAI & Dados</strong></p>
    <p>🔒 Este é um projeto educacional. Para operações reais, use os canais oficiais do Bradesco.</p>
</div>
""", unsafe_allow_html=True)
