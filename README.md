# 📈 Pipeline de Monitoramento de Ações da B3

Pipeline de dados que extrai cotações de ações da B3 de hora em hora, valida a qualidade dos dados, armazena o histórico em PostgreSQL e gera um gráfico atualizado automaticamente — orquestrado com Apache Airflow.

Projeto pessoal construído para praticar engenharia de dados na prática: orquestração, tratamento de erros rastreável e decisões de design de pipeline, não apenas extração simples de API.

---

## 🧱 Arquitetura

```
Trigger horário (Airflow)
        │
        ▼
┌─────────────────┐
│  busca_api.py    │  Extrai cotações de 3 tickers em uma única chamada à brapi.dev
└────────┬─────────┘
         ▼
┌─────────────────┐
│  validacao.py    │  Separa dados válidos de dados incompletos
└────────┬─────────┘
         ├──► ações válidas ──────┐
         └──► erros encontrados ──┤
                                  ▼
                       ┌─────────────────────┐
                       │  carga_postgres.py   │  Grava no Postgres (tabela acoes / tabela_erros)
                       └──────────┬───────────┘
                                  ▼
                       ┌─────────────────────┐
                       │  gerar_grafico.py    │  Lê o histórico e atualiza o gráfico
                       └─────────────────────┘
```

Cada etapa vive em um arquivo próprio dentro de `include/`, com responsabilidade única. A DAG (`dags/`) apenas orquestra a ordem de execução — a lógica de negócio fica isolada e testável separadamente.

---

## ⚙️ Stack

| Camada | Tecnologia |
|---|---|
| Orquestração | Apache Airflow (via Astro CLI) |
| Linguagem | Python |
| Banco de dados | PostgreSQL |
| Fonte de dados | [brapi.dev](https://brapi.dev) (API pública B3) |
| Ambiente | Docker |

---

## 📊 Ativos monitorados

`PETR4` · `VALE3` · `MGLU3` — coleta a cada 1 hora.

---

## ✅ Regra de validação de dados

Nem todo campo ausente tem o mesmo peso. Os dados são avaliados em dois níveis:

- **Campos indispensáveis** (`symbol`, `regularMarketPrice`): se estiverem ausentes, a ação inteira é descartada e um erro é registrado. Sem eles, o registro não tem utilidade analítica.
- **Campos desejáveis** (nome da empresa, moeda, máxima/mínima do dia, variação): se ausentes, o campo entra como `NULL`, mas o restante do dado válido não é perdido.

Essa abordagem evita dois extremos: inserir dados incompletos demais para serem confiáveis, ou descartar um registro inteiro por causa de um único campo secundário.

---

## 🚨 Tratamento de erros

Toda falha — seja na chamada à API ou na validação dos dados — gera um registro em uma tabela de erros dedicada, com:

- Código do erro
- Mensagem descritiva
- Task/etapa de origem
- Horário da ocorrência

Isso garante rastreabilidade completa: nenhuma falha é "silenciosa".

---

## 🗄️ Modelo de dados

**`acoes`**

| Coluna | Tipo |
|---|---|
| id | SERIAL PRIMARY KEY |
| symbol_empresa | VARCHAR(10) |
| nome_da_empresa | VARCHAR(50) |
| moeda | VARCHAR(4) |
| preco_regular | DECIMAL(7,2) |
| preco_mais_alto | DECIMAL(7,2) |
| preco_mais_baixo | DECIMAL(7,2) |
| variacao_de_preco | DECIMAL(7,2) |
| percentual_variacao_de_preco | DECIMAL(7,2) |
| hora_coleta | TIMESTAMP |

Restrição `UNIQUE (symbol_empresa, hora_coleta)` garante idempotência — a mesma ação não é inserida duas vezes na mesma hora.

**`tabela_erros`**

| Coluna | Tipo |
|---|---|
| id | SERIAL PRIMARY KEY |
| codigo_erro | VARCHAR(5) |
| mensagem_erro | TEXT |
| task_origem | VARCHAR(30) |
| hora_erro | TIMESTAMP |

---

## 📂 Estrutura do projeto

```
├── dags/                    # Definição da DAG (orquestração)
├── include/
│   ├── busca_api.py         # Extração — chamada à brapi.dev
│   ├── validacao.py         # Validação e organização dos dados
│   ├── carga_postgres.py    # Inserção no PostgreSQL
│   └── gerar_grafico.py     # Geração do gráfico
├── codigo_tabela_acoes.sql
├── codigo_tabela_erro.sql
├── requirements.txt
├── .env                     # Credenciais (não versionado)
└── README.md
```

---

## 🚧 Status do projeto

- [x] Modelagem do banco de dados
- [x] Extração da API
- [x] Validação em dois níveis
- [ ] Carga no PostgreSQL
- [ ] Geração do gráfico
- [ ] DAG final orquestrando o pipeline completo

Projeto em desenvolvimento ativo.

---
👩‍💻 Autora

Eva Gabriela — Graduada em Tecnologia em Banco de Dados (PUC Minas)

## 👩‍💻 Autora

**Eva Gabriela** — Graduada em Tecnologia em Banco de Dados (PUC Minas)
