# N8N Workflows - Shopee Affiliate Ops

Este diretório contém workflows prontos para importar no N8N e automatizar todas as operações do sistema.

## 📋 Workflows Disponíveis

### 1. Daily Collect (01_daily_collect.json)
**Horário:** 06:00 BRT  
**Frequência:** Diário

**O que faz:**
- Coleta produtos de cada nicho via API
- Salva no banco de dados
- Envia notificação com resumo

**Endpoints usados:**
```
POST /api/products/collect?nicho=casa&limit=50
POST /api/products/collect?nicho=tech&limit=50
POST /api/products/collect?nicho=pet&limit=50
POST /api/products/collect?nicho=cosmeticos&limit=50
```

---

### 2. Generate Content (02_generate_content.json)
**Horário:** 07:00 BRT  
**Frequência:** Diário

**O que faz:**
- Busca top 10 produtos ranqueados de cada nicho
- Gera conteúdo para cada canal
- Aprova automaticamente conteúdos de grupo

**Endpoints usados:**
```
GET /api/products/top/{nicho}?limit=10
POST /api/content/generate/{produto_id}?canal=grupo&num_variacoes=3
POST /api/content/{conteudo_id}/approve
```

---

### 3. Publish Telegram (03_publish_telegram.json)
**Horário:** A cada 2 horas (08:00, 10:00, 12:00, etc)  
**Frequência:** 10x por dia

**O que faz:**
- Busca conteúdos aprovados pendentes de publicação
- Publica no grupo Telegram do nicho correspondente
- Marca como publicado

**Endpoints usados:**
```
GET /api/content/pending?canal=grupo&nicho={nicho}
(Integração direta com Telegram Bot API)
POST /api/content/{conteudo_id}/mark-published
```

---

### 4. Fetch Analytics (04_fetch_analytics.json)
**Horário:** 23:00 BRT  
**Frequência:** Diário

**O que faz:**
- Busca relatórios do dia da API Shopee
- Atualiza métricas no banco
- Gera relatório resumido
- Envia via Telegram

**Endpoints usados:**
```
GET /api/analytics/summary?days=1
GET /api/analytics/by-canal
GET /api/analytics/by-nicho
```

---

### 5. Alerts Monitor (05_alerts_monitor.json)
**Horário:** Sempre ativo  
**Frequência:** A cada 5 minutos

**O que faz:**
- Monitora health check da API
- Verifica se há erros nos logs
- Envia alertas se algo estiver quebrado

**Endpoints usados:**
```
GET /health
```

---

## 🚀 Como Importar

### Passo 1: Acesse o N8N

```bash
# Se usando Docker Compose:
docker-compose up -d n8n

# Ou inicie manualmente:
n8n start
```

Acesse: http://localhost:5678

### Passo 2: Login

- Usuário: `admin`
- Senha: `change_me_n8n_pass` (configure no docker-compose.yml)

### Passo 3: Importar Workflows

1. Clique no menu hamburguer (☰) no canto superior esquerdo
2. Selecione "Workflows"
3. Clique em "Import from File"
4. Selecione um dos arquivos `.json` desta pasta
5. O workflow será importado
6. Repita para cada arquivo

### Passo 4: Configurar Credenciais

Cada workflow usa HTTP Request para chamar a API local.

**Configure uma vez:**

1. Abra qualquer workflow importado
2. Clique em um nó "HTTP Request"
3. Em "Credentials", clique em "Create New"
4. Configure:
   - **Name:** Shopee Affiliate API
   - **Authentication:** None (API local)
   - **Base URL:** `http://localhost:8000`
5. Salve

Todos os workflows compartilharão essa credencial.

### Passo 5: Ativar Workflows

1. Abra cada workflow
2. Toggle do "Inactive" para "Active" no canto superior direito
3. O workflow começará a executar nos horários programados

---

## 📊 Monitoramento

### Ver Execuções

1. No menu, clique em "Executions"
2. Veja histórico de todas as execuções
3. Clique em qualquer execução para ver detalhes

### Logs

Logs detalhados estão em:
- Logs da API: `logs/` no diretório do projeto
- Logs do N8N: Dashboard de execuções

---

## 🔧 Personalização

### Alterar Horários

Edite o nó "Schedule Trigger" em cada workflow:
- Modo: Cron
- Expression: `0 6 * * *` (06:00 diário)

### Adicionar Mais Canais

No workflow `03_publish_telegram.json`:
1. Duplique o fluxo existente
2. Altere o parâmetro `canal` para `tiktok` ou `reels`
3. Configure integração com Buffer API

### Custom Webhooks

Crie workflows acionados por webhook:
1. Adicione nó "Webhook Trigger"
2. Configure path (ex: `/webhook/new-product`)
3. Use URL gerada para acionar de outras aplicações

---

## 🎯 Exemplo de Workflow Customizado

### Workflow: Auto-Approval de Conteúdo

```json
{
  "nodes": [
    {
      "name": "Schedule Every Hour",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 1}]
        }
      }
    },
    {
      "name": "Get Pending Content",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/api/content/pending",
        "method": "GET"
      }
    },
    {
      "name": "For Each Content",
      "type": "n8n-nodes-base.splitInBatches",
      "parameters": {
        "batchSize": 1
      }
    },
    {
      "name": "Approve",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:8000/api/content/{{$json.id}}/approve",
        "method": "POST"
      }
    }
  ],
  "connections": {
    "Schedule Every Hour": {"main": [[{"node": "Get Pending Content"}]]},
    "Get Pending Content": {"main": [[{"node": "For Each Content"}]]},
    "For Each Content": {"main": [[{"node": "Approve"}]]}
  }
}
```

---

## 🆘 Troubleshooting

### Workflow não executa

- Verifique se está "Active"
- Confira o horário configurado
- Veja logs de erro em "Executions"

### Erro "Connection refused"

- API não está rodando
- Inicie: `uvicorn src.api.main:app --reload`
- Verifique porta 8000 está livre

### Credenciais inválidas

- Re-configure as credenciais HTTP
- Certifique-se que Base URL está correto
- Teste chamando `/health` manualmente

---

## 📚 Recursos

- [N8N Documentation](https://docs.n8n.io)
- [N8N Community](https://community.n8n.io)
- [Workflow Templates](https://n8n.io/workflows)

---

**Pronto para automação total! 🤖⚡**
