# 📚 Casos de Uso

## Visão Geral

Documentação dos principais casos de uso do Assistente Financeiro.

---

## 1. Consulta de Saldo e Extrato

### Descrição
Usuário consulta saldo da conta e movimentações recentes.

### Atores
- Usuário (Cliente do banco)
- Assistente Financeiro

### Pré-condições
- Usuário autenticado
- Conta bancária ativa

### Fluxo Principal

1. Usuário pergunta: "Qual é meu saldo?"
2. Assistente identifica intenção de consulta de saldo
3. Sistema recupera saldo da conta
4. Assistente responde: "Seu saldo atual é R$ 5.432,18"
5. Usuário solicita: "Mostre meu extrato dos últimos 7 dias"
6. Sistema recupera movimentações
7. Assistente apresenta lista formatada de transações

### Fluxos Alternativos

**A1: Conta com saldo negativo**
- Sistema detecta saldo negativo
- Assistente alerta sobre uso de limite
- Oferece orientações sobre regularização

**A2: Múltiplas contas**
- Assistente pergunta qual conta consultar
- Usuário especifica (conta corrente/poupança)
- Continua fluxo normal

### Pós-condições
- Informação exibida ao usuário
- Conversação registrada no histórico

---

## 2. Simulação de Financiamento Imobiliário

### Descrição
Usuário simula financiamento de imóvel.

### Atores
- Usuário potencial comprador
- Assistente Financeiro

### Pré-condições
- Nenhuma

### Fluxo Principal

1. Usuário: "Quero financiar um imóvel de R$ 300.000"
2. Assistente coleta informações:
   - "Qual o valor de entrada que você possui?"
   - "Em quanto tempo pretende pagar?"
3. Usuário fornece: "R$ 50.000 de entrada, em 20 anos"
4. Sistema calcula simulação (SAC e Price)
5. Assistente apresenta:
   - Valor financiado
   - Parcela inicial e final (SAC)
   - Parcela fixa (Price)
   - Total de juros
   - Gráfico de evolução das parcelas
6. Usuário analisa opções
7. Assistente oferece agendar contato com gerente

### Fluxos Alternativos

**A1: Entrada insuficiente**
- Sistema detecta entrada < 20%
- Assistente informa requisito mínimo
- Sugere ajustar valores

**A2: Prazo muito longo**
- Assistente alerta sobre custo total elevado
- Sugere simular prazos menores

### Pós-condições
- Simulação salva no histórico
- Usuário informado sobre próximos passos

---

## 3. Recomendação de Investimentos

### Descrição
Usuário busca recomendações de investimento.

### Atores
- Usuário investidor
- Assistente Financeiro

### Pré-condições
- Usuário autenticado
- Perfil de investidor preenchido

### Fluxo Principal

1. Usuário: "Onde posso investir R$ 10.000?"
2. Assistente verifica perfil de investidor
3. Sistema analisa:
   - Perfil de risco (conservador/moderado/arrojado)
   - Objetivo (reserva/aposentadoria/objetivo específico)
   - Prazo
4. Assistente apresenta recomendações:
   - Poupança: X% do valor
   - Tesouro Direto: Y% do valor
   - Fundos: Z% do valor
5. Explica cada opção:
   - Rentabilidade esperada
   - Risco
   - Liquidez
   - Tributação
6. Usuário escolhe opção
7. Assistente orienta sobre como investir

### Fluxos Alternativos

**A1: Perfil não preenchido**
- Assistente oferece questionário de perfil
- Usuário responde questões
- Sistema define perfil
- Continua fluxo normal

**A2: Valor muito baixo**
- Assistente informa sobre valor mínimo
- Sugere iniciar com poupança ou tesouro

### Pós-condições
- Recomendações registradas
- Usuário orientado

---

## 4. Consulta de FAQ sobre Produtos

### Descrição
Usuário tira dúvidas sobre produtos bancários.

### Atores
- Usuário
- Assistente Financeiro

### Pré-condições
- Nenhuma

### Fluxo Principal

1. Usuário: "Como funciona o Pix?"
2. Sistema busca semanticamente na base de conhecimento
3. Encontra FAQs relevantes
4. Assistente responde:
   - Explicação clara sobre Pix
   - Como usar
   - Limites
   - Segurança
5. Oferece perguntas relacionadas:
   - "Como aumentar limite do Pix?"
   - "Pix tem custo?"
   - "Como fazer Pix agendado?"

### Fluxos Alternativos

**A1: Pergunta não encontrada**
- Assistente admite não saber
- Oferece transferir para atendente humano
- Registra pergunta para futura inclusão

**A2: Múltiplas interpretações**
- Assistente pede esclarecimento
- Usuário especifica
- Continua fluxo normal

### Pós-condições
- Dúvida esclarecida
- Feedback coletado

---

## 5. Análise de Gastos Mensais

### Descrição
Usuário analisa padrões de gastos.

### Atores
- Usuário
- Assistente Financeiro

### Pré-condições
- Usuário autenticado
- Histórico de transações disponível

### Fluxo Principal

1. Usuário: "Quanto gastei este mês?"
2. Sistema analisa transações do mês
3. Assistente apresenta:
   - Total gasto
   - Gastos por categoria (gráfico pizza)
   - Comparação com mês anterior
   - Tendência (aumentando/diminuindo)
4. Usuário: "Onde mais gastei?"
5. Sistema identifica top 3 categorias
6. Assistente mostra detalhamento:
   - Alimentação: R$ 1.200
   - Transporte: R$ 800
   - Lazer: R$ 600
7. Oferece insights:
   - "Seus gastos com alimentação aumentaram 15%"
   - "Sugiro revisar assinaturas de streaming"

### Fluxos Alternativos

**A1: Primeiro mês**
- Não há histórico para comparação
- Assistente apresenta apenas dados atuais
- Incentiva continuar usando para análises futuras

**A2: Gasto anômalo detectado**
- Sistema identifica transação atipicamente alta
- Assistente questiona se está correto
- Oferece categorizar corretamente

### Pós-condições
- Análise exibida
- Insights registrados
- Metas financeiras sugeridas

---

## 6. Planejamento de Aposentadoria

### Descrição
Usuário planeja aposentadoria com assistência.

### Atores
- Usuário
- Assistente Financeiro

### Pré-condições
- Nenhuma

### Fluxo Principal

1. Usuário: "Quero planejar minha aposentadoria"
2. Assistente coleta informações:
   - Idade atual
   - Idade planejada para aposentadoria
   - Renda mensal desejada na aposentadoria
   - Valor atual disponível para investir
   - Capacidade de aporte mensal
3. Sistema calcula:
   - Montante necessário
   - Plano de aportes
   - Rentabilidade necessária
4. Assistente apresenta:
   - Plano de investimento
   - Gráfico de evolução patrimonial
   - Simulações com diferentes cenários
5. Oferece produtos adequados:
   - Previdência privada
   - Tesouro IPCA+
   - Fundos de longo prazo

### Fluxos Alternativos

**A1: Meta inviável**
- Sistema detecta impossibilidade
- Assistente explica a situação
- Sugere ajustes:
  - Aumentar aportes
  - Estender prazo
  - Reduzir expectativa de renda

### Pós-condições
- Plano criado
- Metas estabelecidas
- Acompanhamento agendado

---

## 7. Transferência e Pagamentos

### Descrição
Usuário realiza transferências via assistente.

### Atores
- Usuário
- Assistente Financeiro
- Sistema Bancário

### Pré-condições
- Usuário autenticado
- Saldo disponível

### Fluxo Principal

1. Usuário: "Quero fazer um Pix de R$ 100 para João"
2. Assistente:
   - Verifica contatos salvos
   - Encontra "João Silva"
3. Confirma: "Transferir R$ 100,00 para João Silva (chave: 123.456.789-00)?"
4. Usuário confirma
5. Sistema solicita autenticação (senha/biometria)
6. Transferência processada
7. Assistente confirma: "Transferência realizada com sucesso!"
8. Exibe comprovante

### Fluxos Alternativos

**A1: Saldo insuficiente**
- Sistema detecta saldo insuficiente
- Assistente informa
- Oferece ver limite disponível

**A2: Contato não encontrado**
- Assistente pede chave Pix
- Usuário fornece
- Valida chave
- Continua fluxo normal

**A3: Falha na autenticação**
- Tentativa inválida
- Oferece tentar novamente
- Após 3 tentativas, bloqueia temporariamente

### Pós-condições
- Transferência concluída
- Comprovante disponível
- Saldo atualizado

---

## 8. Atendimento Escalonado

### Descrição
Transferência para atendente humano quando necessário.

### Atores
- Usuário
- Assistente Financeiro
- Atendente Humano

### Pré-condições
- Usuário em conversa com assistente

### Fluxo Principal

1. Assistente não consegue resolver demanda
2. Oferece: "Gostaria de falar com um atendente?"
3. Usuário aceita
4. Sistema:
   - Salva contexto da conversação
   - Verifica disponibilidade de atendentes
5. Assistente: "Transferindo para atendente. Tempo estimado: 2 minutos"
6. Conecta com atendente humano
7. Atendente recebe histórico da conversa
8. Continua atendimento

### Fluxos Alternativos

**A1: Fora do horário**
- Informa horário de atendimento
- Oferece deixar mensagem
- Oferece agendar retorno

**A2: Fila cheia**
- Informa posição na fila
- Oferece callback
- Usuário escolhe aguardar ou receber ligação

### Pós-condições
- Atendimento registrado
- Feedback coletado
- IA aprende com a interação

---

## Matriz de Priorização

| Caso de Uso | Complexidade | Valor | Prioridade |
|-------------|--------------|-------|------------|
| FAQ | Baixa | Alto | Alta |
| Simulação Financiamento | Média | Alto | Alta |
| Análise Gastos | Média | Alto | Alta |
| Consulta Saldo | Baixa | Médio | Média |
| Recomendação Investimentos | Alta | Alto | Média |
| Planejamento Aposentadoria | Alta | Médio | Média |
| Transferências | Alta | Alto | Baixa* |
| Atendimento Escalonado | Média | Alto | Alta |

*Baixa prioridade devido a questões de segurança e regulatórias