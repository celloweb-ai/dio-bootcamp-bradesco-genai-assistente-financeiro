# Guia de UX/UI - Assistente Financeiro

## Princípios de Design

### 1. Clareza
- **Linguagem simples**: Evitar jargões financeiros complexos
- **Hierarquia visual**: Informações mais importantes em destaque
- **Feedback imediato**: Resposta rápida a todas as ações

### 2. Confiança
- **Transparência**: Explicar como as informações são usadas
- **Segurança visível**: Indicadores de proteção de dados
- **Consistência**: Padrões mantidos em toda aplicação

### 3. Acessibilidade
- **Contraste adequado**: WCAG 2.1 AA compliance
- **Responsividade**: Adaptação a diferentes telas
- **Navegação por teclado**: Suporte completo

## Paleta de Cores

### Cores Principais
```
Primária (Azul Bradesco):  #CC092F (vermelho institucional)
Secundária (Azul Escuro):  #003B7A
Acento (Verde):            #00A86B (positivo/sucesso)
Alerta (Amarelo):          #FFA500
Erro (Vermelho):           #DC143C
```

### Cores de Suporte
```
Fundo Claro:      #FFFFFF
Fundo Secundário: #F5F5F5
Texto Principal:  #333333
Texto Secundário: #666666
Bordas:           #E0E0E0
```

## Tipografia

### Fontes
```
Principal: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI'
Mono: 'Fira Code', 'Courier New', monospace (para valores)
```

### Hierarquia
```
H1: 32px, Bold (Títulos principais)
H2: 24px, Semibold (Seções)
H3: 20px, Semibold (Subseções)
Body: 16px, Regular (Texto corrente)
Small: 14px, Regular (Legendas)
```

## Componentes

### Chatbot Interface

**Layout**:
```
┌─────────────────────────────────┐
│  🤖 Assistente Financeiro       │
├─────────────────────────────────┤
│                                 │
│  💬 Mensagens do chat           │
│  (scroll vertical)              │
│                                 │
├─────────────────────────────────┤
│  [Digite sua mensagem...]  [>]  │
└─────────────────────────────────┘
```

**Bolhas de Mensagem**:
- **Usuário**: Alinhada à direita, fundo azul claro
- **Assistente**: Alinhada à esquerda, fundo cinza claro
- **Sistema**: Centralizada, itálico, cor neutra

### Calculadoras

**Estrutura**:
1. **Inputs**: Campos claros com labels e placeholders
2. **Botão Calcular**: Destaque, cor primária
3. **Resultados**: Cards separados, fácil leitura
4. **Gráficos**: Visualização complementar

**Exemplo - Financiamento**:
```
┌────────────────────────────────┐
│ Valor do Imóvel:               │
│ [R$ ___________]               │
│                                │
│ Entrada:                       │
│ [R$ ___________]               │
│                                │
│ Prazo (meses):                 │
│ [___]                          │
│                                │
│     [📊 Calcular]              │
└────────────────────────────────┘
```

### Cards de Produtos

```
┌─────────────────────────────┐
│ 💳 Conta Digital            │
├─────────────────────────────┤
│ Zero tarifas mensais        │
│ Cartão sem anuidade         │
│                             │
│ [Saiba mais →]              │
└─────────────────────────────┘
```

## Microinterações

### Loading States
- **Typing indicator**: Três pontos animados
- **Skeleton screens**: Placeholder durante carregamento
- **Progress bars**: Para processos longos

### Feedback Visual
- **Hover**: Mudança sutil de cor/sombra
- **Focus**: Outline azul acessível
- **Success**: Check verde com fade-in
- **Error**: Shake animation + mensagem clara

### Transições
```css
Transição padrão: 200ms ease-in-out
Fade: opacity 300ms
Slide: transform 250ms cubic-bezier(0.4, 0, 0.2, 1)
```

## Mensagens e Tone of Voice

### Características
- **Amigável**: "Olá! Como posso ajudar você hoje?"
- **Profissional**: Sem gírias, mas acessível
- **Empático**: Reconhecer situações do usuário
- **Educativo**: Explicar quando necessário

### Exemplos

❌ **Evitar**:
"Erro 404: Recurso não encontrado"

✅ **Preferir**:
"Ops! Não consegui encontrar essa informação. Que tal reformular sua pergunta?"

❌ **Evitar**:
"Input inválido"

✅ **Preferir**:
"Por favor, insira um valor entre R$ 1.000 e R$ 10.000.000"

## Fluxos de Usuário

### 1. Primeira Interação
```
1. Boas-vindas automáticas
2. Breve explicação do que o assistente faz
3. Sugestões de perguntas iniciais
4. Campo de entrada em foco
```

### 2. Consulta de FAQ
```
1. Usuário digita pergunta
2. Loading indicator (typing...)
3. Resposta estruturada com:
   - Resposta direta
   - Informações complementares
   - Links úteis (se aplicável)
4. "Isso respondeu sua dúvida?" [Sim] [Não]
```

### 3. Uso de Calculadora
```
1. Usuário menciona cálculo
2. Assistente oferece calculadora específica
3. Formulário interativo aparece
4. Validação em tempo real
5. Resultados com visualização
6. Opção de salvar/compartilhar
```

## Responsividade

### Breakpoints
```
Mobile:  < 768px
Tablet:  768px - 1024px
Desktop: > 1024px
```

### Adaptações Mobile
- Menu hambúrguer
- Cards em coluna única
- Botões com altura mínima de 44px
- Font-size base: 16px (evitar zoom no iOS)

## Acessibilidade (WCAG 2.1)

### Checklist
- [ ] Contraste mínimo 4.5:1 para texto
- [ ] Todos os elementos interativos navegáveis por teclado
- [ ] Alt text em todas as imagens
- [ ] Labels em todos os inputs
- [ ] Skip links para navegação
- [ ] ARIA labels onde necessário
- [ ] Focus visível em todos os elementos
- [ ] Sem dependência exclusiva de cor

### Screen Readers
- Ordem lógica de leitura
- Landmarks ARIA (navigation, main, aside)
- Live regions para atualizações dinâmicas

## Animações e Performance

### Princípios
- **Sutileza**: Animações devem ajudar, não distrair
- **Performance**: 60fps, usar transform/opacity
- **Respeitar preferências**: `prefers-reduced-motion`

### Exemplos
```css
/* Respeitar preferência de movimento reduzido */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Testes de Usabilidade

### Métricas
- **Time to First Interaction**: < 3s
- **Response Time**: < 2s para respostas simples
- **Error Rate**: < 5% de erros de usuário
- **Satisfaction Score**: > 4.5/5

### A/B Testing
- Variações de mensagens de boas-vindas
- Posicionamento de CTAs
- Cores de botões principais
- Estrutura de respostas do chatbot

## Recursos de Design

### Ícones
- **Biblioteca**: Lucide Icons / Heroicons
- **Tamanho padrão**: 24x24px
- **Estilo**: Outline (linha)

### Ilustrações
- **Estilo**: Flat, moderno, amigável
- **Paleta**: Consistente com cores da marca
- **Uso**: Estados vazios, onboarding, erros

## Documentação para Desenvolvedores

### Componentes Streamlit Customizados
```python
# Exemplo de componente de chat
import streamlit as st

def chat_message(message, is_user=False):
    alignment = "flex-end" if is_user else "flex-start"
    bg_color = "#E3F2FD" if is_user else "#F5F5F5"
    
    st.markdown(f"""
    <div style="display: flex; justify-content: {alignment};">
        <div style="
            background-color: {bg_color};
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 70%;
            margin: 8px 0;
        ">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)
```

## Manutenção e Evolução

### Design System (futuro)
- Componentização completa
- Storybook para documentação
- Tokens de design (cores, espaçamentos)
- Versionamento semântico

### Feedback dos Usuários
- Coletar feedback após interações
- Análise de heatmaps
- Session recordings
- Pesquisas de satisfação
