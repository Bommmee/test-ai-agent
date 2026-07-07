"""
WealthPath AI — Streamlit Demo
--------------------------------
Run: streamlit run app.py
"""

import streamlit as st
from agents import UserProfile, Transaction, WealthPathOrchestrator
from sample_data import (
    JISOO, JISOO_TRANSACTIONS,
    YOUNGHOO, YOUNGHOO_TRANSACTIONS,
)

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WealthPath AI",
    page_icon="💙",
    layout="wide",
)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='color:#0C447C;margin-bottom:2px'>WealthPath AI</h1>
    <p style='color:#5F5E5A;font-size:15px'>
    첫 월급부터 은퇴 후 현금흐름까지 — LifeLong WM AI Agent
    </p>
    """,
    unsafe_allow_html=True,
)
st.divider()

# ─── Mode selection ───────────────────────────────────────────────────────────
mode = st.radio(
    "모드 선택",
    ["🟦 생애 첫 자산관리 (사회초년생)", "🟪 은퇴 현금흐름 점검 (예비은퇴자)"],
    horizontal=True,
)

use_sample = st.toggle("샘플 데이터 사용 (김지수 / 박영호)", value=True)

st.markdown("---")

# ─── Input forms ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

if "사회초년생" in mode:
    with col1:
        st.subheader("기본 정보")
        age     = st.number_input("나이", 19, 45, JISOO.age if use_sample else 28)
        income  = st.number_input("월 소득 (원)", 0, 10_000_000,
                                   JISOO.monthly_income if use_sample else 3_000_000,
                                   step=100_000)
        assets  = st.number_input("현재 자산 (원)", 0, 500_000_000,
                                   JISOO.current_assets if use_sample else 2_000_000,
                                   step=500_000)
        expense = st.number_input("월 고정지출 (원)", 0, 10_000_000,
                                   JISOO.monthly_fixed_expense if use_sample else 1_500_000,
                                   step=100_000)
    with col2:
        st.subheader("목표 설정")
        target  = st.number_input("목표 금액 (원)", 1_000_000, 100_000_000,
                                   30_000_000, step=1_000_000)
        st.markdown("**이번 달 지출 내역**")
        delivery  = st.slider("배달 지출 (원)", 0, 1_000_000,
                               420_000 if use_sample else 300_000, step=10_000)
        cafe      = st.slider("카페·간식 (원)", 0, 500_000,
                               190_000 if use_sample else 100_000, step=10_000)
        subscribe = st.slider("구독 서비스 (원)", 0, 300_000,
                               96_000 if use_sample else 50_000, step=5_000)
        shopping  = st.slider("쇼핑 (원)", 0, 1_000_000,
                               340_000 if use_sample else 200_000, step=10_000)

    user = UserProfile(
        age=age, monthly_income=income,
        current_assets=assets, monthly_fixed_expense=expense,
        goals=["비상금 만들기"],
    )
    transactions = [
        Transaction("배달",    delivery),
        Transaction("카페·간식", cafe),
        Transaction("구독",    subscribe),
        Transaction("쇼핑",    shopping),
        Transaction("식비·마트", 380_000 if use_sample else 300_000),
        Transaction("교통",    120_000),
    ]
    monthly_medical = 0

else:  # 예비은퇴자
    with col1:
        st.subheader("기본 정보")
        age     = st.number_input("나이", 45, 70, YOUNGHOO.age if use_sample else 58)
        assets  = st.number_input("금융자산 (원)", 0, 1_000_000_000,
                                   YOUNGHOO.current_assets if use_sample else 120_000_000,
                                   step=1_000_000)
        pension = st.number_input("예상 월 연금 합계 (원)", 0, 5_000_000,
                                   YOUNGHOO.expected_pension if use_sample else 1_000_000,
                                   step=100_000)
    with col2:
        st.subheader("지출 계획")
        living  = st.number_input("목표 월 생활비 (원)", 500_000, 10_000_000,
                                   YOUNGHOO.monthly_fixed_expense if use_sample else 2_300_000,
                                   step=100_000)
        medical = st.number_input("월 의료비 (원)", 0, 2_000_000,
                                   250_000 if use_sample else 200_000, step=50_000)
        insurance = st.number_input("월 보험료 (원)", 0, 2_000_000,
                                    180_000 if use_sample else 150_000, step=10_000)
        target = 10_000_000   # placeholder, not used in retirement mode

    user = UserProfile(
        age=age, monthly_income=0,
        current_assets=assets,
        monthly_fixed_expense=living,
        goals=["은퇴 후 생활비 확보"],
        expected_pension=pension,
    )
    transactions = YOUNGHOO_TRANSACTIONS if use_sample else []
    monthly_medical = medical + insurance

# ─── Run agents ───────────────────────────────────────────────────────────────
if st.button("🤖 AI 분석 시작하기", type="primary", use_container_width=True):
    with st.spinner("7개 Agent가 순차 실행 중입니다..."):

        orchestrator = WealthPathOrchestrator()
        result = orchestrator.run(
            user, transactions,
            target_amount=target,
            monthly_medical=monthly_medical,
        )

    # ── Agent execution log ─────────────────────────────────────────────
    st.markdown("### 🔄 Agent 실행 로그")
    stage_labels = {1: "JUDGE (판단)", 2: "ACT (행동)", 3: "VERIFY (검증)"}
    log_cols = st.columns(len(result["execution_log"]))
    for i, entry in enumerate(result["execution_log"]):
        with log_cols[i]:
            st.success(
                f"**{entry['agent']}**\n\n"
                f"Stage {entry['stage']} · {stage_labels[entry['stage']]}"
            )

    st.markdown("---")

    # ── Main results ────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("#### 📊 소비 분석")
        spending = result["spending"]
        for cat, amt in spending["category_breakdown"].items():
            warn = " ⚠️" if cat in spending["overspend_warnings"] else ""
            st.markdown(f"**{cat}{warn}**: {amt:,}원")
        st.metric("월 절약 가능 추정", f"{spending['savings_capacity']:,}원")

    with c2:
        if "사회초년생" in mode:
            st.markdown("#### 🎯 목표 달성 시뮬레이터")
            goal = result["goal"]
            st.info(f"💡 {goal['range_nudge']}")
            for scenario, months in goal["scenarios"].items():
                st.markdown(f"**{scenario}**: {months}개월")
            st.success(f"6개월 절약 시 → {goal['physical_equivalent_6m']}")
        else:
            st.markdown("#### 💰 은퇴 현금흐름")
            cf = result["cashflow"]
            st.metric("예상 월 수입", f"{cf['monthly_income']:,}원")
            st.metric("예상 월 지출", f"{cf['monthly_expense']:,}원")
            delta = cf['monthly_shortage']
            color = "normal" if delta >= 0 else "inverse"
            st.metric("월 부족분", f"{abs(delta):,}원",
                      delta="충분" if delta >= 0 else "부족",
                      delta_color=color)
            st.warning(f"리스크 등급: **{cf['risk_level']}**")

    with c3:
        st.markdown("#### 🏦 JB 상품군 비교")
        products = result["products"]
        for p in products["products"]:
            badge = "🥇" if p["suitability"] == "1순위" else \
                    "🥈" if p["suitability"] == "2순위" else \
                    "🥉" if p["suitability"] == "3순위" else "➕"
            st.markdown(
                f"{badge} **{p['name']}**  \n"
                f"안정성: {p['stability']} · 유동성: {p['liquidity']}  \n"
                f"_{p['note']}_"
            )
        st.caption(products["disclaimer"])

    # ── Risk Guard ──────────────────────────────────────────────────────
    st.markdown("---")
    rg = result["risk_guard"]
    if rg["passed"]:
        st.success("✅ Risk Guard 검증 통과 — 모든 항목 정상")
    else:
        st.error("⚠️ Risk Guard 위반 항목 발견")
        for v in rg["violations"]:
            st.warning(v)
    with st.expander("검증 항목 전체 보기"):
        for check in rg["checks_performed"]:
            st.markdown(f"✔ {check}")
        st.caption(rg["note"])

    # ── Wealth Report ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📋 Wealth Report")
    report = result["report"]
    st.code(report["report_text"], language=None)

    st.markdown("#### 다음 액션 3가지")
    for i, action in enumerate(report["next_actions"], 1):
        st.markdown(f"**{i}.** {action}")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "WealthPath AI · JB금융그룹 Fin:AI Challenge 2025 · "
    "본 서비스는 투자권유가 아닌 금융 정보 제공 서비스입니다."
)
