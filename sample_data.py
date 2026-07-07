"""
Sample mock data for WealthPath AI demo.
In production these would come from MyData API / bank open API.
"""

from agents import UserProfile, Transaction

# ── Persona A: 사회초년생 김지수 ──────────────────────────────────────────────
JISOO = UserProfile(
    age=29,
    monthly_income=3_100_000,
    current_assets=2_000_000,
    monthly_fixed_expense=1_800_000,
    goals=["비상금 1,000만원", "주거자금 500만원"],
    retirement_age=63,
    expected_pension=0,
)

JISOO_TRANSACTIONS = [
    Transaction("배달",    420_000),
    Transaction("식비·마트", 380_000),
    Transaction("카페·간식", 190_000),
    Transaction("구독",    96_000),
    Transaction("쇼핑",    340_000),
    Transaction("교통",    120_000),
    Transaction("기타",    254_000),
]

# ── Persona B: 예비은퇴자 박영호 ──────────────────────────────────────────────
YOUNGHOO = UserProfile(
    age=58,
    monthly_income=5_200_000,
    current_assets=120_000_000,
    monthly_fixed_expense=2_300_000,
    goals=["은퇴 후 월 230만원 생활비 확보"],
    retirement_age=63,
    expected_pension=1_490_000,   # 국민연금 92만 + 퇴직연금 57만
)

YOUNGHOO_TRANSACTIONS = [
    Transaction("식비·마트",  580_000),
    Transaction("의료비",     250_000),
    Transaction("보험료",     180_000),
    Transaction("교통",       120_000),
    Transaction("여가·문화",  200_000),
    Transaction("기타",        70_000),
]
