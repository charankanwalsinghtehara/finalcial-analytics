import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Banking Financial Performance Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "analysis_output"


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .dashboard-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .dashboard-subtitle {
        font-size: 15px;
        color: #667085;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 12px;
    }

    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        min-height: 105px;
    }

    .kpi-label {
        color: #667085;
        font-size: 13px;
        margin-bottom: 8px;
    }

    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        color: #101828;
    }

    .insight-card {
        background: white;
        border-left: 4px solid #2563eb;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        border-top: 1px solid #eaecf0;
        border-right: 1px solid #eaecf0;
        border-bottom: 1px solid #eaecf0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HELPERS
# ============================================================

def load_csv(filename):
    path = OUTPUT_DIR / filename

    if not path.exists():
        st.error(
            f"File not found:\n\n{path}\n\n"
            "Run Module 3 first."
        )
        st.stop()

    df = pd.read_csv(path)

    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    return df


def numeric(df, column):
    if column not in df.columns:
        return 0

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).fillna(0)


def money(value):
    if pd.isna(value):
        return "₹0"

    value = float(value)

    if abs(value) >= 1_000_000_000:
        return f"₹{value / 1_000_000_000:.2f}B"

    if abs(value) >= 1_000_000:
        return f"₹{value / 1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"₹{value / 1_000:.2f}K"

    return f"₹{value:,.0f}"


def number(value):
    if pd.isna(value):
        return "0"

    return f"{float(value):,.0f}"


def percentage(value):
    if pd.isna(value):
        return "0.00%"

    return f"{float(value) * 100:.2f}%"


def kpi_card(label, value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOAD DATA
# ============================================================

monthly = load_csv("monthly_financial_model.csv")
annual = load_csv("annual_financial_performance.csv")
branches = load_csv("branch_performance.csv")
loans = load_csv("loan_portfolio_analysis.csv")
risk = load_csv("risk_grade_analysis.csv")
customers = load_csv("customer_segment_analysis.csv")
segment_loans = load_csv("segment_loan_exposure.csv")
transactions = load_csv("transaction_channel_analysis.csv")
kpis = load_csv("banking_kpis.csv")
insights = load_csv("management_insights.csv")


# ============================================================
# CENTRAL COLUMN NORMALIZATION
#
# This is the important fix.
# Module 3 may produce slightly different names.
# We normalize them once here.
# ============================================================

def rename_if_exists(df, aliases, standard_name):

    for alias in aliases:

        if alias in df.columns:

            if standard_name not in df.columns:
                df.rename(
                    columns={alias: standard_name},
                    inplace=True
                )

            return


# ----------------------------
# MONTHLY
# ----------------------------

rename_if_exists(
    monthly,
    [
        "DepositINR",
        "DepositsINR",
        "TotalDepositsINR"
    ],
    "DepositINR"
)

rename_if_exists(
    monthly,
    [
        "AdvanceINR",
        "AdvancesINR",
        "TotalAdvancesINR"
    ],
    "AdvancesINR"
)

rename_if_exists(
    monthly,
    [
        "InterestIncomeINR"
    ],
    "InterestIncomeINR"
)

rename_if_exists(
    monthly,
    [
        "InterestExpenseINR"
    ],
    "InterestExpenseINR"
)

rename_if_exists(
    monthly,
    [
        "FeeIncomeINR"
    ],
    "FeeIncomeINR"
)

rename_if_exists(
    monthly,
    [
        "OperatingExpenseINR",
        "OperatingExpensesINR"
    ],
    "OperatingExpenseINR"
)

rename_if_exists(
    monthly,
    [
        "ProvisionINR",
        "ProvisionExpenseINR"
    ],
    "ProvisionINR"
)

rename_if_exists(
    monthly,
    [
        "NetInterestIncomeINR"
    ],
    "NetInterestIncomeINR"
)

rename_if_exists(
    monthly,
    [
        "TotalIncomeCalculatedINR",
        "TotalIncomeINR"
    ],
    "TotalIncomeCalculatedINR"
)

rename_if_exists(
    monthly,
    [
        "PreProvisionProfitINR"
    ],
    "PreProvisionProfitINR"
)

rename_if_exists(
    monthly,
    [
        "NetProfitCalculatedINR",
        "NetProfitINR"
    ],
    "NetProfitCalculatedINR"
)


# ----------------------------
# ANNUAL
# ----------------------------

rename_if_exists(
    annual,
    [
        "DepositINR",
        "DepositsINR",
        "TotalDepositsINR"
    ],
    "DepositsINR"
)

rename_if_exists(
    annual,
    [
        "AdvanceINR",
        "AdvancesINR",
        "TotalAdvancesINR"
    ],
    "AdvancesINR"
)

rename_if_exists(
    annual,
    [
        "TotalIncomeCalculatedINR",
        "TotalIncomeINR"
    ],
    "TotalIncomeINR"
)

rename_if_exists(
    annual,
    [
        "OperatingExpenseINR",
        "OperatingExpensesINR"
    ],
    "OperatingExpensesINR"
)

rename_if_exists(
    annual,
    [
        "ProvisionExpenseINR",
        "ProvisionINR"
    ],
    "ProvisionINR"
)

rename_if_exists(
    annual,
    [
        "NetProfitCalculatedINR",
        "NetProfitINR"
    ],
    "NetProfitINR"
)


# ----------------------------
# BRANCH
# ----------------------------

rename_if_exists(
    branches,
    [
        "DepositINR",
        "DepositsINR"
    ],
    "DepositINR"
)

rename_if_exists(
    branches,
    [
        "AdvanceINR",
        "AdvancesINR"
    ],
    "AdvancesINR"
)

rename_if_exists(
    branches,
    [
        "TotalIncomeCalculatedINR",
        "TotalIncomeINR"
    ],
    "TotalIncomeINR"
)

rename_if_exists(
    branches,
    [
        "OperatingExpenseINR",
        "OperatingExpensesINR"
    ],
    "OperatingExpenseINR"
)

rename_if_exists(
    branches,
    [
        "NetProfitCalculatedINR",
        "NetProfitINR"
    ],
    "NetProfitINR"
)


# ============================================================
# NUMERIC CONVERSION
# ============================================================

all_numeric = {

    "monthly": [
        "DepositINR",
        "AdvancesINR",
        "InterestIncomeINR",
        "InterestExpenseINR",
        "FeeIncomeINR",
        "OperatingExpenseINR",
        "ProvisionINR",
        "NetInterestIncomeINR",
        "TotalIncomeCalculatedINR",
        "PreProvisionProfitINR",
        "NetProfitCalculatedINR"
    ],

    "annual": [
        "DepositsINR",
        "AdvancesINR",
        "NetInterestIncomeINR",
        "TotalIncomeINR",
        "OperatingExpensesINR",
        "ProvisionINR",
        "NetProfitINR",
        "ProfitMargin",
        "CostToIncomeRatio",
        "LoanToDepositRatio",
        "DepositGrowth",
        "AdvanceGrowth",
        "IncomeGrowth",
        "ProfitGrowth"
    ],

    "branches": [
        "DepositINR",
        "AdvancesINR",
        "InterestIncomeINR",
        "InterestExpenseINR",
        "FeeIncomeINR",
        "OperatingExpenseINR",
        "ProvisionINR",
        "NetInterestIncomeINR",
        "TotalIncomeINR",
        "PreProvisionProfitINR",
        "NetProfitINR",
        "ProfitMargin",
        "CostToIncomeRatio",
        "LoanToDepositRatio"
    ],

    "loans": [
        "LoanCount",
        "LoanAmountINR",
        "OutstandingINR",
        "AverageInterestRatePct",
        "NPALoans",
        "NPA_Ratio",
        "OutstandingShare"
    ],

    "risk": [
        "LoanCount",
        "OutstandingINR",
        "AverageInterestRatePct",
        "NPALoans",
        "NPA_Ratio"
    ],

    "customers": [
        "Customers",
        "AverageIncomeINR",
        "AverageCreditScore"
    ],

    "transactions": [
        "TransactionCount",
        "TransactionValueINR"
    ]
}


for col in all_numeric["monthly"]:
    if col in monthly.columns:
        monthly[col] = pd.to_numeric(
            monthly[col],
            errors="coerce"
        ).fillna(0)

for col in all_numeric["annual"]:
    if col in annual.columns:
        annual[col] = pd.to_numeric(
            annual[col],
            errors="coerce"
        ).fillna(0)

for col in all_numeric["branches"]:
    if col in branches.columns:
        branches[col] = pd.to_numeric(
            branches[col],
            errors="coerce"
        ).fillna(0)

for col in all_numeric["loans"]:
    if col in loans.columns:
        loans[col] = pd.to_numeric(
            loans[col],
            errors="coerce"
        ).fillna(0)

for col in all_numeric["risk"]:
    if col in risk.columns:
        risk[col] = pd.to_numeric(
            risk[col],
            errors="coerce"
        ).fillna(0)

for col in all_numeric["customers"]:
    if col in customers.columns:
        customers[col] = pd.to_numeric(
            customers[col],
            errors="coerce"
        ).fillna(0)

for col in all_numeric["transactions"]:
    if col in transactions.columns:
        transactions[col] = pd.to_numeric(
            transactions[col],
            errors="coerce"
        ).fillna(0)


# ============================================================
# REQUIRED COLUMN SAFETY
# ============================================================

required_monthly = [
    "DepositINR",
    "AdvancesINR",
    "NetInterestIncomeINR",
    "TotalIncomeCalculatedINR",
    "OperatingExpenseINR",
    "NetProfitCalculatedINR"
]

missing_monthly = [
    c for c in required_monthly
    if c not in monthly.columns
]

if missing_monthly:

    st.error(
        "Module 3 output schema is missing these columns:"
    )

    st.code(
        "\n".join(missing_monthly)
    )

    st.write(
        "Actual monthly_financial_model columns:"
    )

    st.code(
        "\n".join(monthly.columns.tolist())
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div style="font-size:24px;font-weight:700;">
        🏦 SecureBank Analytics
    </div>

    <div style="color:#667085;margin-bottom:20px;">
        Financial Performance Intelligence
    </div>
    """,
    unsafe_allow_html=True
)


page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Profitability",
        "Lending & Credit Risk",
        "Deposits & Funding",
        "Branch Performance",
        "Customer & Transactions",
        "Management Insights"
    ]
)


st.sidebar.markdown("---")

st.sidebar.caption(
    "Banking Financial Performance Dashboard"
)

st.sidebar.caption(
    "Data → KPI → Analysis → Insight → Decision"
)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="dashboard-title">'
        'Banking Financial Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Executive management dashboard | '
        'Profitability • Growth • Risk • Efficiency'
        '</div>',
        unsafe_allow_html=True
    )

    deposits = monthly["DepositINR"].sum()

    advances = monthly["AdvancesINR"].sum()

    nii = monthly["NetInterestIncomeINR"].sum()

    total_income = monthly[
        "TotalIncomeCalculatedINR"
    ].sum()

    net_profit = monthly[
        "NetProfitCalculatedINR"
    ].sum()

    operating_expenses = monthly[
        "OperatingExpenseINR"
    ].sum()

    profit_margin = (
        net_profit / total_income
        if total_income
        else 0
    )

    cost_income = (
        operating_expenses / total_income
        if total_income
        else 0
    )

    loan_count = loans["LoanCount"].sum()

    npa_count = loans["NPALoans"].sum()

    npa_ratio = (
        npa_count / loan_count
        if loan_count
        else 0
    )

    cols = st.columns(8)

    values = [
        ("Total Deposits", money(deposits)),
        ("Total Advances", money(advances)),
        ("Net Interest Income", money(nii)),
        ("Total Income", money(total_income)),
        ("Net Profit", money(net_profit)),
        ("Profit Margin", percentage(profit_margin)),
        ("NPA Ratio", percentage(npa_ratio)),
        ("Cost / Income", percentage(cost_income))
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            kpi_card(label, value)

    st.markdown(
        '<div class="section-title">'
        'Financial Performance Trend'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.line(
            monthly,
            x="YearQuarter",
            y="NetProfitCalculatedINR",
            markers=True,
            title="Net Profit Trend",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        available = [
            c for c in [
                "TotalIncomeINR",
                "NetProfitINR"
            ]
            if c in annual.columns
        ]

        if available:

            fig = px.bar(
                annual,
                x="Year",
                y=available,
                barmode="group",
                title="Income vs Net Profit",
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    col1, col2 = st.columns(2)

    with col1:

        if "RiskGrade" in risk.columns:

            fig = px.bar(
                risk.sort_values(
                    "OutstandingINR"
                ),
                x="OutstandingINR",
                y="RiskGrade",
                orientation="h",
                title="Loan Exposure by Risk Grade",
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        if "Region" in branches.columns:

            region = (
                branches
                .groupby(
                    "Region",
                    as_index=False
                )["NetProfitINR"]
                .sum()
                .sort_values(
                    "NetProfitINR",
                    ascending=False
                )
            )

            fig = px.bar(
                region,
                x="Region",
                y="NetProfitINR",
                title="Regional Profitability",
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# PROFITABILITY
# ============================================================

elif page == "Profitability":

    st.markdown(
        '<div class="dashboard-title">'
        'Profitability Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Revenue generation, operating efficiency and profit performance'
        '</div>',
        unsafe_allow_html=True
    )

    nii = monthly["NetInterestIncomeINR"].sum()

    fee_income = (
        monthly["FeeIncomeINR"].sum()
        if "FeeIncomeINR" in monthly.columns
        else 0
    )

    income = monthly[
        "TotalIncomeCalculatedINR"
    ].sum()

    expenses = monthly[
        "OperatingExpenseINR"
    ].sum()

    pre_provision = (
        monthly["PreProvisionProfitINR"].sum()
        if "PreProvisionProfitINR" in monthly.columns
        else 0
    )

    profit = monthly[
        "NetProfitCalculatedINR"
    ].sum()

    cols = st.columns(6)

    values = [
        ("Net Interest Income", money(nii)),
        ("Fee Income", money(fee_income)),
        ("Total Income", money(income)),
        ("Operating Expenses", money(expenses)),
        ("Pre-Provision Profit", money(pre_provision)),
        ("Net Profit", money(profit))
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            kpi_card(label, value)

    fig = px.line(
        monthly,
        x="YearQuarter",
        y=[
            "NetInterestIncomeINR",
            "FeeIncomeINR"
        ],
        markers=True,
        title="Core Revenue Trend",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        cols = [
            c for c in [
                "OperatingExpensesINR",
                "ProvisionINR"
            ]
            if c in annual.columns
        ]

        if cols:

            fig = px.bar(
                annual,
                x="Year",
                y=cols,
                barmode="group",
                title="Expenses and Provisions",
                template="plotly_white"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:

        if "ProfitMargin" in annual.columns:

            fig = px.line(
                annual,
                x="Year",
                y="ProfitMargin",
                markers=True,
                title="Profit Margin Trend",
                template="plotly_white"
            )

            fig.update_yaxes(
                tickformat=".1%"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    if "BranchName" in branches.columns:

        branch_profit = (
            branches[
                [
                    "BranchName",
                    "NetProfitINR"
                ]
            ]
            .sort_values(
                "NetProfitINR",
                ascending=False
            )
            .head(15)
        )

        fig = px.bar(
            branch_profit,
            x="NetProfitINR",
            y="BranchName",
            orientation="h",
            title="Top Branches by Net Profit",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# LENDING & CREDIT RISK
# ============================================================

elif page == "Lending & Credit Risk":

    st.markdown(
        '<div class="dashboard-title">'
        'Lending & Credit Risk'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Loan portfolio composition, credit risk and NPA monitoring'
        '</div>',
        unsafe_allow_html=True
    )

    advances = monthly["AdvancesINR"].sum()

    loan_count = loans["LoanCount"].sum()

    npa_count = loans["NPALoans"].sum()

    npa_ratio = (
        npa_count / loan_count
        if loan_count
        else 0
    )

    npa_outstanding = (
        loans["OutstandingINR"]
        * loans["NPA_Ratio"]
    ).sum()

    outstanding = loans[
        "OutstandingINR"
    ].sum()

    weighted_rate = (
        (
            loans["AverageInterestRatePct"]
            * loans["OutstandingINR"]
        ).sum()
        / outstanding
        if outstanding
        else 0
    )

    cols = st.columns(4)

    values = [
        ("Total Advances", money(advances)),
        ("NPA Ratio", percentage(npa_ratio)),
        ("NPA Outstanding", money(npa_outstanding)),
        ("Weighted Loan Rate", f"{weighted_rate:.2f}%")
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            kpi_card(label, value)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            loans.sort_values(
                "OutstandingINR"
            ),
            x="OutstandingINR",
            y="LoanType",
            orientation="h",
            title="Outstanding Loan Portfolio by Product",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            risk.sort_values(
                "OutstandingINR"
            ),
            x="OutstandingINR",
            y="RiskGrade",
            orientation="h",
            title="Outstanding Exposure by Risk Grade",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            loans.sort_values(
                "NPA_Ratio",
                ascending=False
            ),
            x="LoanType",
            y="NPA_Ratio",
            title="NPA Ratio by Loan Product",
            template="plotly_white"
        )

        fig.update_yaxes(
            tickformat=".1%"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.pie(
            loans,
            names="LoanType",
            values="LoanCount",
            hole=0.45,
            title="Loan Portfolio Mix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# DEPOSITS & FUNDING
# ============================================================

elif page == "Deposits & Funding":

    st.markdown(
        '<div class="dashboard-title">'
        'Deposits & Funding'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Funding base, lending growth and liquidity structure'
        '</div>',
        unsafe_allow_html=True
    )

    deposits = monthly["DepositINR"].sum()

    advances = monthly["AdvancesINR"].sum()

    ldr = (
        advances / deposits
        if deposits
        else 0
    )

    deposit_growth = 0

    if "DepositGrowth" in annual.columns:

        deposit_growth = annual[
            "DepositGrowth"
        ].iloc[-1]

    cols = st.columns(4)

    values = [
        ("Total Deposits", money(deposits)),
        ("Total Advances", money(advances)),
        ("Loan / Deposit Ratio", percentage(ldr)),
        ("Latest Deposit Growth", percentage(deposit_growth))
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            kpi_card(label, value)

    fig = px.line(
        monthly,
        x="YearQuarter",
        y="DepositINR",
        markers=True,
        title="Deposit Growth Trend",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    fig = px.line(
        monthly,
        x="YearQuarter",
        y=[
            "DepositINR",
            "AdvancesINR"
        ],
        markers=True,
        title="Funding vs Lending",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Financial interpretation: compare deposit growth "
        "with advances growth to assess whether lending "
        "expansion is supported by the funding base."
    )


# ============================================================
# BRANCH PERFORMANCE
# ============================================================

elif page == "Branch Performance":

    st.markdown(
        '<div class="dashboard-title">'
        'Branch Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Branch profitability, efficiency and regional performance'
        '</div>',
        unsafe_allow_html=True
    )

    total_branches = branches["BranchID"].nunique()

    average_profit = branches[
        "NetProfitINR"
    ].mean()

    best_branch = branches.loc[
        branches["NetProfitINR"].idxmax()
    ]

    worst_branch = branches.loc[
        branches["NetProfitINR"].idxmin()
    ]

    cols = st.columns(4)

    values = [
        ("Total Branches", number(total_branches)),
        ("Average Branch Profit", money(average_profit)),
        ("Top Branch", str(best_branch.get("BranchName", "N/A"))),
        ("Lowest Branch", str(worst_branch.get("BranchName", "N/A")))
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            kpi_card(label, value)

    fig = px.bar(
        branches.sort_values(
            "NetProfitINR"
        ),
        x="NetProfitINR",
        y="BranchName",
        orientation="h",
        title="Branch Net Profit",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if "Region" in branches.columns:

        region = (
            branches
            .groupby(
                "Region",
                as_index=False
            )["NetProfitINR"]
            .sum()
            .sort_values(
                "NetProfitINR",
                ascending=False
            )
        )

        fig = px.bar(
            region,
            x="Region",
            y="NetProfitINR",
            title="Regional Profitability",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    fig = px.scatter(
        branches,
        x="OperatingExpenseINR",
        y="NetProfitINR",
        hover_name="BranchName",
        size="DepositINR",
        title="Operating Cost vs Net Profit",
        template="plotly_white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        branches.sort_values(
            "NetProfitINR",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CUSTOMER & TRANSACTIONS
# ============================================================

elif page == "Customer & Transactions":

    st.markdown(
        '<div class="dashboard-title">'
        'Customer & Transaction Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Customer segmentation, credit profile and banking channel usage'
        '</div>',
        unsafe_allow_html=True
    )

    total_customers = customers[
        "Customers"
    ].sum()

    avg_income = customers[
        "AverageIncomeINR"
    ].mean()

    avg_credit_score = customers[
        "AverageCreditScore"
    ].mean()

    transaction_volume = transactions[
        "TransactionCount"
    ].sum()

    transaction_value = transactions[
        "TransactionValueINR"
    ].sum()

    cols = st.columns(5)

    values = [
        ("Total Customers", number(total_customers)),
        ("Avg Customer Income", money(avg_income)),
        ("Avg Credit Score", f"{avg_credit_score:.0f}"),
        ("Transaction Volume", number(transaction_volume)),
        ("Transaction Value", money(transaction_value))
    ]

    for col, (label, value) in zip(cols, values):
        with col:
            kpi_card(label, value)

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            customers,
            names="Segment",
            values="Customers",
            hole=0.45,
            title="Customer Segment Mix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            customers.sort_values(
                "AverageIncomeINR"
            ),
            x="AverageIncomeINR",
            y="Segment",
            orientation="h",
            title="Average Income by Customer Segment",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            transactions.sort_values(
                "TransactionValueINR"
            ),
            x="TransactionValueINR",
            y="Channel",
            orientation="h",
            title="Transaction Value by Channel",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.bar(
            transactions.sort_values(
                "TransactionCount"
            ),
            x="TransactionCount",
            y="Channel",
            orientation="h",
            title="Transaction Volume by Channel",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# MANAGEMENT INSIGHTS
# ============================================================

elif page == "Management Insights":

    st.markdown(
        '<div class="dashboard-title">'
        'Management Insights'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-subtitle">'
        'Decision-oriented findings from the banking financial model'
        '</div>',
        unsafe_allow_html=True
    )

    if len(insights) > 0:

        for _, row in insights.iterrows():

            values = [
                str(value)
                for value in row.tolist()
                if pd.notna(value)
            ]

            text_value = " | ".join(values)

            st.markdown(
                f"""
                <div class="insight-card">
                    {text_value}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No management insights were generated."
        )

    st.markdown(
        '<div class="section-title">'
        'Management Framework'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### Growth

        Monitor deposits, advances and income growth.

        ### Profitability

        Evaluate NII, fee income, operating expenses and net profit.

        ### Credit Risk

        Monitor NPA ratio, NPA outstanding and risk-grade concentration.

        ### Efficiency

        Track cost-to-income ratio and branch operating performance.

        ### Customer Strategy

        Compare customer segments by income, credit profile and loan exposure.

        ### Digital Banking

        Monitor transaction migration toward digital channels.

        ### Management Action

        Convert analytical findings into measurable financial decisions.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Banking Financial Performance Dashboard | "
    "Python • SQL • Pandas • Plotly • Streamlit"
)