# WealthPath AI 💙
## A Multi-Agent Life-Cycle Asset Management Coach

> **첫 월급부터 은퇴 후 현금흐름까지, 생애 전반의 금융 불안을 관리하는 LifeLong WM AI Agent**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Problem

Most financial apps show data — balances, charts, transactions — but fail to tell users **what to do right now**.

- **Young adults (19–34):** earn income but struggle to form saving habits; can't connect daily spending to long-term goals
- **Pre-retirees (50–64):** hold assets but can't easily calculate whether post-retirement monthly cashflow will be sufficient
- **Elderly (65+):** face digital barriers and heightened fraud risk

WealthPath AI addresses this gap by orchestrating 7 specialized agents that **judge, act, and verify** — moving beyond dashboards to deliver actionable, life-stage-aware financial guidance.

---

## Why Agents?

A single LLM prompt cannot reliably:
- **Validate** user inputs and agent outputs (schema errors break downstream logic)
- **Calculate** numbers accurately (hallucination risk)
- **Enforce** compliance rules (investment-solicitation guardrails)

By decomposing the workflow into 7 agents with clear roles, WealthPath AI achieves:

| Concern | Agent Solution |
|---|---|
| Numeric accuracy | Goal·Cashflow Agents call TypeScript-equivalent **Tool functions** — LLM never generates raw numbers |
| Output consistency | Every agent returns **JSON Schema / Structured Output** — not free text |
| Input safety | **Zod Schema** validation on all user inputs before any agent runs |
| Compliance | **Risk Guard Agent** scans all outputs for forbidden phrases and individual stock recommendations |

---

## Architecture

```
User Input
    │
    ▼  Zod Schema validation
┌─────────────────────────────────────┐
│         Agent Orchestrator          │
│  (Multi-Agent Workflow Controller)  │
└────────────┬────────────────────────┘
             │
    ┌────────▼──────────┐   STAGE 1: JUDGE (Perceive)
    │  Profile Agent    │── life stage · risk capacity · priority
    │  Spending Agent   │── category totals · overspend warnings
    │  Cashflow Agent   │── retirement deficit · risk level
    └────────┬──────────┘
             │  Structured Output passed downstream
    ┌────────▼──────────┐   STAGE 2: ACT
    │  Goal Agent       │── saving scenarios · physical equivalent
    │  Product Agent    │── JB product 2×2 matrix
    │  Report Agent     │── Wealth Report + next actions
    └────────┬──────────┘
             │
    ┌────────▼──────────┐   STAGE 3: VERIFY
    │  RiskGuard Agent  │── compliance · hallucination · solicitation check
    └───────────────────┘
             │
    Wealth Report + AI Chat
```

---

## Key Concepts Applied (Kaggle Course)

| Concept | Where |
|---|---|
| **Multi-Agent System** | 7-agent orchestrator in `agents.py` |
| **Structured Output / JSON Schema** | Every agent returns typed dict; LLM prompt uses JSON Schema |
| **Tool Calling** | `_calc_months_to_goal()`, `_calc_retirement_cashflow()`, `_physical_equivalent()` |
| **Security / Guardrail** | `RiskGuardAgent` — compliance-aware validator |
| **Deployability** | Streamlit app, `requirements.txt`, `.env.example` |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/wealthpath-ai-agent.git
cd wealthpath-ai-agent

# 2. Install
pip install -r requirements.txt

# 3. Run (no API key needed for mock demo)
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Project Structure

```
wealthpath-ai-agent/
├── app.py              # Streamlit UI + agent orchestration trigger
├── agents.py           # 7 Agent classes + Orchestrator + Tool functions
├── sample_data.py      # Mock personas (김지수 / 박영호)
├── requirements.txt
├── .env.example        # API key template (no secrets committed)
└── README.md
```

### agents.py — What each agent does

| Agent | Stage | Role | Key output fields |
|---|---|---|---|
| `ProfileAgent` | JUDGE | Life-stage classification | `life_stage`, `risk_capacity`, `priority` |
| `SpendingAgent` | JUDGE | Transaction categorisation + overspend detection | `category_breakdown`, `overspend_warnings` |
| `CashflowAgent` | JUDGE | Retirement cashflow deficit calculation | `monthly_shortage`, `risk_level` |
| `GoalAgent` | ACT | Saving scenarios + physical equivalent | `scenarios`, `physical_equivalent_6m` |
| `ProductAgent` | ACT | JB Financial product 2×2 matrix | `products`, `disclaimer` |
| `RiskGuardAgent` | VERIFY | Compliance + hallucination guardrail | `passed`, `violations` |
| `ReportAgent` | ACT | Final Wealth Report assembly | `report_text`, `next_actions` |

---

## Two Demo Scenarios

**Scenario A — 사회초년생 김지수 (29)**
- Monthly income: 3,100,000 KRW · Assets: 6,500,000 KRW
- Goal: Build 10M KRW emergency fund
- Result: Spending Agent flags delivery over-spend → Goal Agent calculates 22→17 month shortcut → Product Agent recommends 목돈만들기 product group

**Scenario B — 예비은퇴자 박영호 (58)**
- Financial assets: 120,000,000 KRW · Expected pension: 1,490,000 KRW/month
- Goal: 2,300,000 KRW/month post-retirement living expense
- Result: Cashflow Agent calculates 460,000 KRW/month deficit → risk level "주의" → Product Agent recommends retirement-tier products

---

## Design Decisions

**LLM generates explanations only — never numbers.**
All calculations (goal timelines, retirement deficits, physical equivalents) are handled by pure Python Tool functions. This prevents hallucination on financial figures.

**Risk Guard as a separate agent (not a prompt filter).**
Embedding compliance rules inside the LLM prompt is fragile. A dedicated `RiskGuardAgent` that inspects structured outputs is more reliable and auditable.

**Zod Schema → Python dataclasses for MVP.**
In production (Next.js), Zod Schema validates user input and agent outputs. In this Python prototype, `dataclasses` with type hints serve the same structural role.

---

## Future Work

| Phase | Features |
|---|---|
| **본선 (July)** | Real CSV upload · JB product RAG DB · PDF report download · Slow Banking UI |
| **PoC** | JB전북/광주은행 app integration · Guardian alert mock |
| **Production** | MyData API · anomaly detection · family WM · B2B Financial Wellness |

---

## Theoretical Foundation

- **Merton (1969)** Life-cycle portfolio selection — consumption and investment ratios change dynamically with life stage
- **Bodie-Merton-Samuelson (1992)** Human capital model — asset allocation shifts as labor income flexibility declines
- **통계청 국민이전계정** — surplus entry at ~age 28, deficit from retirement; validates our two MVP scenarios
- **Behavioral economics / Nudge theory** — Range-type saving nudges ("주 1~2회 줄이면 월 4~8만원") outperform precise targets for behavior change

---

## License

MIT License — see [LICENSE](LICENSE)

---

*Built as a capstone project for Kaggle's 5-Day AI Agents: Intensive Vibe Coding Course with Google (June 2026).*  
*Service concept originally developed for JB Financial Group Fin:AI Challenge 2025.*
