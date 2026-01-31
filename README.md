# 🛍️ Shopee Affiliate Ops — Sistema Completo de Automação

Sistema profissional de automação para operação de afiliados Shopee, focado em consistência, rastreabilidade e compliance.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Stack Tecnológico](#stack-tecnológico)
- [🚀 Passo a Passo para INICIANTES](#-passo-a-passo-para-iniciantes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Nichos e Personas](#nichos-e-personas)
- [Convenção de SubIds](#convenção-de-subids)
- [Pipeline Diário](#pipeline-diário)
- [Endpoints da API](#endpoints-da-api)
- [Workflows N8N](#workflows-n8n)
- [Compliance](#compliance)
- [Troubleshooting](#troubleshooting)

---

## Visão Geral

O Shopee Affiliate Ops é um sistema completo que automatiza todo o ciclo de operação de afiliados:

1. **Coleta** de produtos via API Shopee
2. **Ranking** inteligente usando IA (DeepSeek)
3. **Geração de conteúdo** personalizado com GPT
4. **Criação de vídeos** com Gemini/Veo
5. **Publicação** automática em múltiplos canais
6. **Analytics** e atribuição de conversões

### Canais Suportados (por prioridade)
1. ✅ **TikTok** (3-4 posts/dia)
2. ✅ **Instagram Reels** (2-3 posts/dia)
3. ✅ **Instagram Stories** (5-6 posts/dia)
4. ✅ **Grupo Telegram** (8-10 posts/dia)

---

## Stack Tecnológico

- **Python 3.11+** com FastAPI
- **N8N** para orquestração de workflows
- **LLMs**: 
  - DeepSeek (análise e ranking)
  - GPT-4 (copywriting)
  - Gemini 3.0 Pro (roteiros de vídeo)
- **Banco**: SQLite (dev) / PostgreSQL (produção)
- **Storage**: Cloudflare R2 para vídeos

---

## 🚀 Passo a Passo para INICIANTES

### Pré-requisitos

- macOS, Linux ou Windows com WSL
- Conhecimento básico de terminal/linha de comando

### 1️⃣ Instalar Python no Mac

```bash
# Instale o Homebrew (se ainda não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instale Python 3.11
brew install python@3.11

# Verifique a instalação
python3 --version
```

### 2️⃣ Clonar o Repositório

```bash
# Clone o projeto
git clone https://github.com/taffapereira/shopee-affiliate-ops.git

# Entre no diretório
cd shopee-affiliate-ops
```

### 3️⃣ Criar Ambiente Virtual

```bash
# Crie o ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
# No Mac/Linux:
source venv/bin/activate

# No Windows (PowerShell):
# venv\Scripts\Activate.ps1
```

Você verá `(venv)` no início da linha do terminal quando o ambiente estiver ativado.

### 4️⃣ Instalar Dependências

```bash
# Com o ambiente virtual ativado, instale as dependências
pip install -r requirements.txt

# Aguarde a instalação (pode levar alguns minutos)
```

### 5️⃣ Configurar Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Abra o arquivo .env com seu editor preferido
# Mac:
open -a TextEdit .env

# Ou use nano:
nano .env
```

**Preencha AS SEGUINTES CREDENCIAIS OBRIGATÓRIAS:**

```env
# Shopee Affiliate (obrigatório para funcionar)
SHOPEE_AFFILIATE_API_KEY=seu_api_key_aqui
SHOPEE_AFFILIATE_SECRET=seu_secret_aqui
SHOPEE_PARTNER_ID=seu_partner_id_aqui

# LLM APIs (pelo menos uma é recomendada)
OPENAI_API_KEY=seu_openai_key_aqui

# Telegram (para receber alertas)
TELEGRAM_BOT_TOKEN=seu_telegram_bot_token_aqui
```

**Como obter as credenciais:**

- **Shopee**: Cadastre-se no [Shopee Affiliate](https://affiliate.shopee.com.br)
- **OpenAI**: Crie uma conta em [platform.openai.com](https://platform.openai.com)
- **Telegram Bot**: Fale com [@BotFather](https://t.me/botfather) no Telegram

### 6️⃣ Inicializar o Banco de Dados

```bash
# Execute o script de setup
python scripts/setup_db.py
```

Você deve ver:
```
✅ Banco de dados inicializado com sucesso!
```

### 7️⃣ Testar Conexões de API

```bash
# Teste todas as APIs configuradas
python scripts/test_apis.py
```

Você verá um relatório de quais APIs estão funcionando:
```
✅ Banco de Dados     OK
✅ Shopee API         OK
⚠️  DeepSeek          API Key não configurada
...
```

### 8️⃣ Executar Primeiro Ciclo Completo

```bash
# Execute o primeiro ciclo (coleta + ranking + conteúdo + links)
python scripts/first_run.py
```

Este script vai:
1. Coletar produtos da Shopee
2. Ranquear por score
3. Gerar conteúdo
4. Criar links de afiliado

### 9️⃣ Iniciar o Servidor API

```bash
# Inicie o servidor FastAPI
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: **http://localhost:8000**

Você verá:
```json
{
  "app": "Shopee Affiliate Ops",
  "version": "1.0.0",
  "status": "running"
}
```

Documentação interativa: **http://localhost:8000/docs**

### 🔟 Importar Workflows no N8N (Opcional)

#### Instalar N8N

```bash
# Via Docker (recomendado)
docker-compose up -d n8n

# Ou via npm
npm install -g n8n
n8n start
```

#### Importar Workflows

1. Acesse http://localhost:5678
2. Login: `admin` / `change_me_n8n_pass`
3. Clique em "Workflows" → "Import from File"
4. Selecione os arquivos JSON em `n8n-workflows/`
5. Ative os workflows importados

---

## Estrutura do Projeto

```
shopee-affiliate-ops/
│
├── config/               # Configurações (nichos, canais, constantes)
├── src/
│   ├── api/             # FastAPI endpoints
│   ├── collectors/      # Coleta de produtos da Shopee
│   ├── database/        # Models e repository
│   ├── ranking/         # Algoritmo de pontuação
│   ├── links/           # Geração de links com SubIds
│   ├── content/         # Geração de conteúdo + personas
│   ├── llm/             # Clients LLM (DeepSeek, GPT, Gemini)
│   ├── video/           # Pipeline de vídeo (Veo, TTS, R2)
│   ├── publishers/      # Telegram + Buffer
│   ├── analytics/       # Relatórios e métricas
│   └── utils/           # Logger + alerts
│
├── prompts/             # Prompts prontos por LLM
├── n8n-workflows/       # Workflows importáveis
├── scripts/             # Scripts auxiliares
└── tests/               # Testes automatizados
```

---

## Nichos e Personas

### 1. Casa & Cozinha (`casa`)
**Persona: Cléo Cozinha Prática**
- Mulher 28-45 anos
- Tom: Direto, animado mas sem exagero
- Frase: *"Gente, olha o que eu achei..."*

### 2. Tech & Wearables (`tech`)
**Persona: Léo Tech Acessível**
- Homem 20-35 anos
- Tom: Informativo com humor
- Frase: *"Esse fone custa 1/10 do AirPods..."*

### 3. Mundo Pet (`pet`)
**Persona: Pri e os Peludinhos**
- 25-40 anos
- Tom: Carinhoso, empolgado
- Frase: *"A Luna AMOU isso..."*

### 4. Cosméticos (`cosmeticos`)
**Persona: Tati Beleza Real**
- Mulher 18-35 anos
- Tom: Íntimo, autêntica
- Frase: *"Testei por 2 semanas..."*

---

## Convenção de SubIds

Sistema de rastreamento de conversões por SubIds:

```
subId1 = canal      # tiktok, reels, stories, grupo
subId2 = nicho      # casa, tech, pet, cosmeticos
subId3 = formato    # video15s, video30s, texto, stories
subId4 = campanha   # oferta_dia, top_comissao, achado, flash
subId5 = data       # AAAAMMDD (ex: 20260131)
```

**Exemplo:**
```
tiktok_tech_video30s_oferta_dia_20260131
```

Isso permite saber exatamente:
- Onde o clique aconteceu (TikTok)
- Qual nicho (Tech)
- Tipo de conteúdo (Vídeo 30s)
- Qual campanha (Oferta do Dia)
- Quando (31/01/2026)

---

## Pipeline Diário

```
06:00 → Coleta produtos via API Shopee
06:30 → Ranking com DeepSeek
07:00 → Geração de copy com GPT
07:30 → Geração de vídeos com Gemini/Veo
08:00 → Primeira publicação (Telegram)
12:00 → Publicação meio-dia
18:00 → Publicação tarde
20:00 → Publicação noite
23:00 → Fetch analytics e ajuste de pesos
```

---

## Endpoints da API

### Produtos

```bash
# Coletar produtos
POST /api/products/collect?nicho=tech&limit=50

# Top ranqueados
GET /api/products/top/tech?limit=10

# Rankear produtos
POST /api/products/rank?nicho=tech

# Detalhes de produto
GET /api/products/{produto_id}
```

### Conteúdo

```bash
# Gerar conteúdo
POST /api/content/generate/{produto_id}?canal=tiktok&num_variacoes=5

# Ver conteúdo gerado
GET /api/content/{conteudo_id}

# Aprovar conteúdo
POST /api/content/{conteudo_id}/approve
```

### Links

```bash
# Gerar link de afiliado
POST /api/links/generate/{produto_id}?canal=tiktok&formato=video30s&campanha=oferta_dia

# Detalhes do link
GET /api/links/{link_id}
```

### Analytics

```bash
# Resumo geral
GET /api/analytics/summary?days=7

# Por canal
GET /api/analytics/by-canal?start_date=2026-01-01&end_date=2026-01-31

# Por nicho
GET /api/analytics/by-nicho?start_date=2026-01-01

# Calcular métricas
GET /api/analytics/metrics?impressions=1000&clicks=50&conversions=5&revenue=500
```

---

## Workflows N8N

Os workflows em `n8n-workflows/` automatizam:

1. **`01_daily_collect.json`** - Coleta diária às 06:00
2. **`02_generate_content.json`** - Geração de conteúdo às 07:00
3. **`03_publish_telegram.json`** - Publicação Telegram a cada 2h
4. **`04_fetch_analytics.json`** - Analytics às 23:00
5. **`05_alerts_monitor.json`** - Monitor de alertas (sempre ativo)

### Como usar

1. Importe no N8N
2. Configure as credenciais (HTTP Request → localhost:8000)
3. Ative os workflows
4. Monitore a execução no dashboard

---

## Compliance

### ✅ Regras OBRIGATÓRIAS

1. **Sem Spam** - Apenas em canais próprios
2. **APIs Oficiais** - Respeitar rate limits
3. **Sem Bots de Engajamento** - Crescimento orgânico
4. **Disclaimers** - Sempre incluir "Link de afiliado"
5. **Autenticidade** - Conteúdo genuíno, não enganoso

### ❌ Proibido

- DM em massa
- Comentários automáticos em posts alheios
- Bots de like/follow
- Conteúdo enganoso
- Spam em grupos de terceiros

---

## Troubleshooting

### Erro: "Shopee API não configurada"

Verifique se preencheu corretamente no `.env`:
```env
SHOPEE_AFFILIATE_API_KEY=...
SHOPEE_AFFILIATE_SECRET=...
SHOPEE_PARTNER_ID=...
```

### Erro: "Database connection failed"

Execute novamente:
```bash
python scripts/setup_db.py
```

### Erro: "ModuleNotFoundError"

Certifique-se de que o ambiente virtual está ativado:
```bash
source venv/bin/activate  # Mac/Linux
```

E reinstale as dependências:
```bash
pip install -r requirements.txt
```

### Nenhum produto coletado

- Verifique suas credenciais da Shopee
- Teste a API: `python scripts/test_apis.py`
- Veja os logs em `logs/`

---

## Suporte

- **Issues**: [GitHub Issues](https://github.com/taffapereira/shopee-affiliate-ops/issues)
- **Discussões**: [GitHub Discussions](https://github.com/taffapereira/shopee-affiliate-ops/discussions)

---

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

## Próximos Passos

Após o setup completo:

1. ✅ Configure mais LLMs (DeepSeek, Gemini) para melhor qualidade
2. ✅ Conecte Buffer para agendamento em redes sociais
3. ✅ Configure Cloudflare R2 para hospedar vídeos
4. ✅ Personalize os prompts em `prompts/` para seu estilo
5. ✅ Ajuste os pesos de ranking em `config/constants.py`
6. ✅ Configure webhooks do N8N para automação total

**Bons afiliados! 🚀💰**