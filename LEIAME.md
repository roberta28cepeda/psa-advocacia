# PSA Advocacia v2 — Sistema Jurídico Completo

## Instalação (primeira vez)

```bash
# 1. Entrar na pasta
cd psa_app_v2

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Iniciar
python server.py
```

Acesse: **http://localhost:8000**

---

## O que há de novo nesta versão

### Agenda & Prazos
- Calendário mensal interativo com todos os eventos
- Vista diária: clique em qualquer dia para ver o que acontece
- Lista "próximos 30 dias" com indicador de urgência
- Criação de prazos, audiências, reuniões e diligências
- Cores personalizadas por evento
- Notificação configurável (X dias antes)

### Notificações
- Sininho no topo com badge vermelho quando há pendências
- Painel lateral com todos os alertas de prazos urgentes (≤7 dias)
- Tarefas com prazo nos próximos 3 dias também geram alertas

### Nova tarefa direto do processo
- Botão "+ Tarefa" em cada linha da tabela de processos
- O processo já fica pré-selecionado no formulário
- Também disponível no detalhe do processo

### Demandas
- Acompanhamento de demandas complexas com etapas
- Barra de progresso automática conforme etapas são concluídas
- Clique em cada etapa para marcar como feita
- Status automático: vira "Concluída" quando todas as etapas são feitas

### Detalhe do processo (melhorado)
- Mostra prazos e audiências do processo
- Mostra tarefas vinculadas
- Mostra andamentos
- Botão "+ Nova tarefa" direto no detalhe
- Botão "+ Novo prazo" direto no detalhe

---

## Backup

O arquivo `database.json` contém todos os seus dados. Faça cópias regulares.

---

## CNJ / DataJud — Tribunais suportados
TJRJ (8.19), TJSP (8.26), TJMG (8.13), TJRS (8.21), TJDFT (8.07),
TRF1 (4.01), TRF2 (4.02), TRF3 (4.03), TRF4 (4.04), TRF5 (4.05), TST (5.01)
