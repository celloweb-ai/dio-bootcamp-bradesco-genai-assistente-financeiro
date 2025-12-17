# 🎨 Guia de UX/UI

## Princípios de Design

### 1. Simplicidade
- Interface limpa e intuitiva
- Fluxos diretos e sem fricção
- Hierarquia visual clara

### 2. Acessibilidade
- Contraste adequado (WCAG 2.1)
- Tamanhos de fonte legíveis
- Navegação por teclado
- Compatibilidade com leitores de tela

### 3. Personalização
- Experiência adaptada ao perfil do usuário
- Preferências de visualização
- Histórico contextualizado

### 4. Confiança
- Transparência nas recomendações
- Explicabilidade das decisões da IA
- Segurança visível

## Paleta de Cores

### Cores Principais
```css
/* Primária - Bradesco */
--primary: #CC092F;
--primary-light: #E63946;
--primary-dark: #A50725;

/* Secundária */
--secondary: #2C3E50;
--secondary-light: #34495E;
--secondary-dark: #1A252F;

/* Neutras */
--gray-100: #F8F9FA;
--gray-200: #E9ECEF;
--gray-300: #DEE2E6;
--gray-400: #CED4DA;
--gray-500: #ADB5BD;
--gray-600: #6C757D;
--gray-700: #495057;
--gray-800: #343A40;
--gray-900: #212529;

/* Feedback */
--success: #28A745;
--warning: #FFC107;
--error: #DC3545;
--info: #17A2B8;
```

## Tipografia

### Fontes
```css
/* Principal */
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monoespaçada (código/números) */
font-family: 'JetBrains Mono', 'Courier New', monospace;
```

### Hierarquia
- **H1**: 32px / 2rem - Títulos principais
- **H2**: 24px / 1.5rem - Seções
- **H3**: 20px / 1.25rem - Subseções
- **Body**: 16px / 1rem - Texto padrão
- **Small**: 14px / 0.875rem - Legendas

## Componentes

### Chat Interface

#### Mensagens do Usuário
```
┌────────────────────────────────┐
│ Quanto rende R$ 10.000 na    │ ◄─ Alinhado à direita
│ poupança?                      │    Fundo: primary-light
└────────────────────────────────┘    Texto: branco
```

#### Mensagens do Assistente
```
┌────────────────────────────────┐
│ 🤖 Com a taxa Selic atual...   │ ◄─ Alinhado à esquerda
│                                │    Fundo: gray-100
└────────────────────────────────┘    Texto: gray-900
```

### Calculadoras

#### Layout
```
┌─────────────────────────────────────┐
│ 📊 Simulador de Financiamento       │
├─────────────────────────────────────┤
│ Valor do Imóvel:     [R$ ______]   │
│ Entrada:             [R$ ______]   │
│ Prazo:               [___ meses]   │
│ Taxa de Juros:       [____ % a.a.] │
├─────────────────────────────────────┤
│           [Calcular]                │
└─────────────────────────────────────┘
```

#### Resultado
```
┌─────────────────────────────────────┐
│ Resultado da Simulação              │
├─────────────────────────────────────┤
│ Valor Financiado:    R$ 180.000,00 │
│ Parcela Mensal:      R$ 1.245,67   │
│ Total a Pagar:       R$ 224.220,60 │
│ Juros Total:         R$ 44.220,60  │
└─────────────────────────────────────┘
```

### Gráficos

#### Estilo
- **Cores**: Paleta consistente
- **Interatividade**: Tooltip, zoom, pan
- **Responsividade**: Adapta ao tamanho da tela
- **Acessibilidade**: Legendas claras

## Estados de Interação

### Botões

#### Estados
- **Default**: Cor primária, sombra sutil
- **Hover**: Cor mais escura, sombra elevada
- **Active**: Cor mais escura, sem sombra
- **Disabled**: Cinza, sem interação
- **Loading**: Spinner animado

#### Exemplo CSS
```css
.button {
  background: var(--primary);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  transition: all 0.2s;
}

.button:hover {
  background: var(--primary-dark);
  box-shadow: 0 4px 12px rgba(204, 9, 47, 0.3);
}
```

### Inputs

#### Estados
- **Default**: Borda cinza
- **Focus**: Borda primária, sombra
- **Error**: Borda vermelha, mensagem de erro
- **Success**: Borda verde, ícone de check
- **Disabled**: Fundo cinza claro

## Feedback ao Usuário

### Mensagens de Sucesso
```
✅ Simulação realizada com sucesso!
```

### Mensagens de Erro
```
❌ Não foi possível processar sua solicitação. Tente novamente.
```

### Mensagens de Aviso
```
⚠️ Os valores são apenas simulações e não constituem oferta.
```

### Mensagens Informativas
```
ℹ️ Esta operação pode levar alguns segundos...
```

## Loading States

### Skeleton Screen
Para listas e cards:
```
┌────────────────────┐
│ ▓▓▓▓▓▓▓▓          │
│ ▓▓▓▓▓▓▓▓▓▓▓▓      │
│ ▓▓▓▓▓▓            │
└────────────────────┘
```

### Spinner
Para operações rápidas:
```
  ⟳  Processando...
```

## Responsividade

### Breakpoints
```css
/* Mobile */
@media (max-width: 768px) { ... }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { ... }

/* Desktop */
@media (min-width: 1025px) { ... }
```

### Adaptações Mobile
- Menu hamburger
- Cards empilhados
- Inputs full-width
- Botões expansivos

## Animações

### Princípios
- **Duração**: 200-300ms para interações
- **Easing**: ease-in-out para naturalidade
- **Propósito**: Guiar atenção, não distrair

### Exemplos
```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide up */
@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
```

## Boas Práticas

### ✅ Fazer
- Usar ícones consistentes
- Fornecer feedback imediato
- Validar inputs em tempo real
- Mostrar progresso em operações longas
- Usar linguagem clara e objetiva

### ❌ Evitar
- Animações excessivas
- Cores que não atendem contraste
- Jargões técnicos sem explicação
- Formulários muito longos
- Pop-ups intrusivos

## Checklist de Acessibilidade

- [ ] Contraste mínimo 4.5:1 para texto
- [ ] Navegação por teclado funcional
- [ ] Labels em todos os inputs
- [ ] Alt text em imagens
- [ ] ARIA labels em componentes complexos
- [ ] Foco visível em elementos interativos
- [ ] Sem dependência exclusiva de cor para informação
- [ ] Testado com leitores de tela

## Testes de Usabilidade

### Métricas
- **Task Success Rate**: Taxa de conclusão de tarefas
- **Time on Task**: Tempo para completar tarefas
- **Error Rate**: Frequência de erros
- **Satisfaction**: NPS, CSAT

### Ferramentas
- Google Lighthouse (Performance, Accessibility)
- WAVE (Web Accessibility Evaluation Tool)
- Hotjar (Heatmaps, Session Recordings)