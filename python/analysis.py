import pandas as pd
import numpy as np
from pathlib import Path



BASE_DIR = Path(r"D:\Banking_Financial_Performance_Dashboard")
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "analysis_output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("=" * 70)
print("BANKING FINANCIAL PERFORMANCE ANALYSIS")
print("=" * 70)

branches = pd.read_csv(DATA_DIR / "branches.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")
accounts = pd.read_csv(DATA_DIR / "accounts.csv")
loans = pd.read_csv(DATA_DIR / "loans.csv")
transactions = pd.read_csv(DATA_DIR / "transactions.csv")
financials = pd.read_csv(DATA_DIR / "financials.csv")


print("\nData loaded successfully.")

print(f"Branches      : {len(branches):,}")
print(f"Customers     : {len(customers):,}")
print(f"Accounts      : {len(accounts):,}")
print(f"Loans         : {len(loans):,}")
print(f"Transactions  : {len(transactions):,}")
print(f"Financials    : {len(financials):,}")


# ============================================================
# 2. CLEAN COLUMN NAMES
# ============================================================

def clean_columns(df):
    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    return df


branches = clean_columns(branches)
customers = clean_columns(customers)
accounts = clean_columns(accounts)
loans = clean_columns(loans)
transactions = clean_columns(transactions)
financials = clean_columns(financials)


# ============================================================
# 3. HELPER FUNCTIONS
# ============================================================

def convert_numeric(df, columns):

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


def find_column(df, candidates):

    lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for candidate in candidates:

        key = candidate.strip().lower()

        if key in lookup:
            return lookup[key]

    return None


# ============================================================
# 4. NORMALIZE CUSTOMER SEGMENT
# ============================================================

segment_column = find_column(
    customers,
    [
        "Segment",
        "CustomerSegment",
        "Customer Segment",
        "Customer_Segment",
        "SegmentName",
        "CustomerType",
        "Customer Type"
    ]
)


if segment_column is not None:

    customers["Segment"] = (
        customers[segment_column]
        .astype(str)
        .str.strip()
    )

else:

    print("\nWARNING: Customer segment column was not found.")

    print(
        "Available customer columns:"
    )

    print(
        list(customers.columns)
    )

    print(
        "\nCreating Segment using AnnualIncomeINR fallback."
    )

    if "AnnualIncomeINR" not in customers.columns:

        raise KeyError(
            "Customer segment could not be found and "
            "AnnualIncomeINR is also missing."
        )

    customers["AnnualIncomeINR"] = pd.to_numeric(
        customers["AnnualIncomeINR"],
        errors="coerce"
    )

    customers["Segment"] = np.select(
        [
            customers["AnnualIncomeINR"] < 500000,
            customers["AnnualIncomeINR"] < 1000000,
            customers["AnnualIncomeINR"] < 2500000
        ],
        [
            "Retail",
            "Mass Affluent",
            "Affluent"
        ],
        default="SME"
    )


customers["Segment"] = (
    customers["Segment"]
    .replace(
        {
            "nan": "Unknown",
            "None": "Unknown",
            "": "Unknown"
        }
    )
)


print(
    f"\nCustomer Segment Column: {segment_column}"
    if segment_column is not None
    else "\nCustomer Segment Column: Derived"
)

print(
    "Customer Segments:"
)

print(
    customers["Segment"]
    .value_counts(dropna=False)
    .to_string()
)


# ============================================================
# 5. NUMERIC CONVERSION
# ============================================================

financials = convert_numeric(
    financials,
    [
        "DepositsINR",
        "AdvancesINR",
        "InterestIncomeINR",
        "InterestExpenseINR",
        "FeeIncomeINR",
        "OtherIncomeINR",
        "OperatingExpenseINR",
        "ProvisionINR",
        "NetInterestIncomeINR",
        "TotalIncomeINR",
        "PreProvisionProfitINR",
        "NetProfitINR"
    ]
)


loans = convert_numeric(
    loans,
    [
        "LoanAmountINR",
        "InterestRatePct",
        "TenureMonths",
        "OutstandingINR",
        "NPAFlag"
    ]
)


customers = convert_numeric(
    customers,
    [
        "AnnualIncomeINR",
        "CreditScore",
        "Age"
    ]
)


accounts = convert_numeric(
    accounts,
    [
        "BalanceINR"
    ]
)


transactions = convert_numeric(
    transactions,
    [
        "AmountINR",
        "NetCashFlowINR"
    ]
)


# ============================================================
# 6. DATE CONVERSION
# ============================================================

if "Month" in financials.columns:

    financials["Month"] = pd.to_datetime(
        financials["Month"],
        errors="coerce"
    )


if "Date" in transactions.columns:

    transactions["Date"] = pd.to_datetime(
        transactions["Date"],
        errors="coerce"
    )


if "OriginationDate" in loans.columns:

    loans["OriginationDate"] = pd.to_datetime(
        loans["OriginationDate"],
        errors="coerce"
    )


if "OpenDate" in accounts.columns:

    accounts["OpenDate"] = pd.to_datetime(
        accounts["OpenDate"],
        errors="coerce"
    )


if "CustomerSince" in customers.columns:

    customers["CustomerSince"] = pd.to_datetime(
        customers["CustomerSince"],
        errors="coerce"
    )


# ============================================================
# 7. CLEAN NPA FLAG
# ============================================================

loans["NPAFlag"] = pd.to_numeric(
    loans["NPAFlag"],
    errors="coerce"
).fillna(0)

loans["NPAFlag"] = (
    loans["NPAFlag"]
    .clip(0, 1)
    .astype(int)
)


# ============================================================
# 8. FINANCIAL MODEL
# ============================================================

financials["NetInterestIncomeINR"] = (
    financials["InterestIncomeINR"]
    - financials["InterestExpenseINR"]
)


financials["TotalIncomeCalculatedINR"] = (
    financials["InterestIncomeINR"]
    + financials["FeeIncomeINR"]
    + financials["OtherIncomeINR"]
)


financials["PreProvisionProfitINR"] = (
    financials["TotalIncomeCalculatedINR"]
    - financials["OperatingExpenseINR"]
)


financials["NetProfitCalculatedINR"] = (
    financials["PreProvisionProfitINR"]
    - financials["ProvisionINR"]
)


# ============================================================
# 9. FINANCIAL RATIOS
# ============================================================

financials["ProfitMargin"] = np.where(
    financials["TotalIncomeCalculatedINR"] != 0,
    financials["NetProfitCalculatedINR"]
    / financials["TotalIncomeCalculatedINR"],
    0
)


financials["CostToIncomeRatio"] = np.where(
    financials["TotalIncomeCalculatedINR"] != 0,
    financials["OperatingExpenseINR"]
    / financials["TotalIncomeCalculatedINR"],
    0
)


financials["LoanToDepositRatio"] = np.where(
    financials["DepositsINR"] != 0,
    financials["AdvancesINR"]
    / financials["DepositsINR"],
    0
)


# ============================================================
# 10. TIME DIMENSIONS
# ============================================================

financials["Year"] = (
    financials["Month"]
    .dt.year
)


financials["Quarter"] = (
    "Q"
    + financials["Month"]
    .dt.quarter
    .astype(str)
)


financials["YearQuarter"] = (
    financials["Year"].astype(str)
    + "-"
    + financials["Quarter"]
)


financials["MonthName"] = (
    financials["Month"]
    .dt.strftime("%b")
)


financials["MonthNumber"] = (
    financials["Month"]
    .dt.month
)


# ============================================================
# 11. ANNUAL FINANCIAL PERFORMANCE
# ============================================================

annual = (
    financials
    .groupby("Year")
    .agg(
        DepositsINR=("DepositsINR", "sum"),
        AdvancesINR=("AdvancesINR", "sum"),
        InterestIncomeINR=("InterestIncomeINR", "sum"),
        InterestExpenseINR=("InterestExpenseINR", "sum"),
        FeeIncomeINR=("FeeIncomeINR", "sum"),
        OtherIncomeINR=("OtherIncomeINR", "sum"),
        OperatingExpenseINR=("OperatingExpenseINR", "sum"),
        ProvisionINR=("ProvisionINR", "sum"),
        NetProfitINR=("NetProfitCalculatedINR", "sum")
    )
    .reset_index()
)


annual["NetInterestIncomeINR"] = (
    annual["InterestIncomeINR"]
    - annual["InterestExpenseINR"]
)


annual["TotalIncomeINR"] = (
    annual["InterestIncomeINR"]
    + annual["FeeIncomeINR"]
    + annual["OtherIncomeINR"]
)


annual["PreProvisionProfitINR"] = (
    annual["TotalIncomeINR"]
    - annual["OperatingExpenseINR"]
)


annual["ProfitMargin"] = np.where(
    annual["TotalIncomeINR"] != 0,
    annual["NetProfitINR"]
    / annual["TotalIncomeINR"],
    0
)


annual["CostToIncomeRatio"] = np.where(
    annual["TotalIncomeINR"] != 0,
    annual["OperatingExpenseINR"]
    / annual["TotalIncomeINR"],
    0
)


annual["LoanToDepositRatio"] = np.where(
    annual["DepositsINR"] != 0,
    annual["AdvancesINR"]
    / annual["DepositsINR"],
    0
)


# ============================================================
# 12. GROWTH ANALYSIS
# ============================================================

annual["DepositGrowth"] = (
    annual["DepositsINR"]
    .pct_change()
)


annual["AdvanceGrowth"] = (
    annual["AdvancesINR"]
    .pct_change()
)


annual["IncomeGrowth"] = (
    annual["TotalIncomeINR"]
    .pct_change()
)


annual["ProfitGrowth"] = (
    annual["NetProfitINR"]
    .pct_change()
)


# ============================================================
# 13. LOAN PORTFOLIO
# ============================================================

loan_summary = (
    loans
    .groupby("LoanType")
    .agg(
        LoanCount=("LoanID", "count"),
        LoanAmountINR=("LoanAmountINR", "sum"),
        OutstandingINR=("OutstandingINR", "sum"),
        AverageInterestRatePct=("InterestRatePct", "mean"),
        NPALoans=("NPAFlag", "sum")
    )
    .reset_index()
)


loan_summary["LoanCount"] = pd.to_numeric(
    loan_summary["LoanCount"],
    errors="coerce"
).fillna(0)


loan_summary["NPALoans"] = pd.to_numeric(
    loan_summary["NPALoans"],
    errors="coerce"
).fillna(0)


loan_summary["NPA_Ratio"] = np.where(
    loan_summary["LoanCount"] > 0,
    loan_summary["NPALoans"]
    / loan_summary["LoanCount"],
    0
)


total_outstanding = (
    loan_summary["OutstandingINR"]
    .sum()
)


loan_summary["OutstandingShare"] = np.where(
    total_outstanding > 0,
    loan_summary["OutstandingINR"]
    / total_outstanding,
    0
)


# ============================================================
# 14. RISK GRADE
# ============================================================

risk_summary = (
    loans
    .groupby("RiskGrade")
    .agg(
        LoanCount=("LoanID", "count"),
        OutstandingINR=("OutstandingINR", "sum"),
        AverageInterestRatePct=("InterestRatePct", "mean"),
        NPALoans=("NPAFlag", "sum")
    )
    .reset_index()
)


risk_summary["LoanCount"] = pd.to_numeric(
    risk_summary["LoanCount"],
    errors="coerce"
).fillna(0)


risk_summary["NPALoans"] = pd.to_numeric(
    risk_summary["NPALoans"],
    errors="coerce"
).fillna(0)


risk_summary["NPA_Ratio"] = np.where(
    risk_summary["LoanCount"] > 0,
    risk_summary["NPALoans"]
    / risk_summary["LoanCount"],
    0
)


# ============================================================
# 15. BRANCH PERFORMANCE
# ============================================================

branch_financials = (
    financials
    .groupby("BranchID")
    .agg(
        DepositsINR=("DepositsINR", "sum"),
        AdvancesINR=("AdvancesINR", "sum"),
        InterestIncomeINR=("InterestIncomeINR", "sum"),
        InterestExpenseINR=("InterestExpenseINR", "sum"),
        FeeIncomeINR=("FeeIncomeINR", "sum"),
        OtherIncomeINR=("OtherIncomeINR", "sum"),
        OperatingExpenseINR=("OperatingExpenseINR", "sum"),
        ProvisionINR=("ProvisionINR", "sum"),
        NetProfitINR=("NetProfitCalculatedINR", "sum")
    )
    .reset_index()
)


branch_columns = [
    "BranchID",
    "BranchName",
    "Region",
    "City"
]


branch_financials = branch_financials.merge(
    branches[branch_columns],
    on="BranchID",
    how="left"
)


branch_financials["NetInterestIncomeINR"] = (
    branch_financials["InterestIncomeINR"]
    - branch_financials["InterestExpenseINR"]
)


branch_financials["TotalIncomeINR"] = (
    branch_financials["InterestIncomeINR"]
    + branch_financials["FeeIncomeINR"]
    + branch_financials["OtherIncomeINR"]
)


branch_financials["ProfitMargin"] = np.where(
    branch_financials["TotalIncomeINR"] != 0,
    branch_financials["NetProfitINR"]
    / branch_financials["TotalIncomeINR"],
    0
)


branch_financials["CostToIncomeRatio"] = np.where(
    branch_financials["TotalIncomeINR"] != 0,
    branch_financials["OperatingExpenseINR"]
    / branch_financials["TotalIncomeINR"],
    0
)


branch_financials["LoanToDepositRatio"] = np.where(
    branch_financials["DepositsINR"] != 0,
    branch_financials["AdvancesINR"]
    / branch_financials["DepositsINR"],
    0
)


# ============================================================
# 16. BRANCH RANKING
# ============================================================

branch_financials["ProfitRank"] = (
    branch_financials["NetProfitINR"]
    .rank(
        ascending=False,
        method="min"
    )
    .astype(int)
)


branch_financials["PerformanceCategory"] = np.select(
    [
        branch_financials["ProfitMargin"] >= 0.30,
        branch_financials["ProfitMargin"] >= 0.20,
        branch_financials["ProfitMargin"] >= 0.10
    ],
    [
        "High Performer",
        "Stable Performer",
        "Watchlist"
    ],
    default="Underperformer"
)


# ============================================================
# 17. CUSTOMER SEGMENT ANALYSIS
# ============================================================

customer_summary = (
    customers
    .groupby("Segment")
    .agg(
        Customers=("CustomerID", "count"),
        AverageIncomeINR=("AnnualIncomeINR", "mean"),
        AverageCreditScore=("CreditScore", "mean")
    )
    .reset_index()
)


# ============================================================
# 18. CUSTOMER LOAN EXPOSURE
# ============================================================

customer_loan_data = (
    customers[
        [
            "CustomerID",
            "Segment"
        ]
    ]
    .merge(
        loans[
            [
                "CustomerID",
                "OutstandingINR",
                "NPAFlag"
            ]
        ],
        on="CustomerID",
        how="left"
    )
)


customer_loan_data["OutstandingINR"] = (
    pd.to_numeric(
        customer_loan_data["OutstandingINR"],
        errors="coerce"
    )
    .fillna(0)
)


customer_loan_data["NPAFlag"] = (
    pd.to_numeric(
        customer_loan_data["NPAFlag"],
        errors="coerce"
    )
    .fillna(0)
)


segment_loan_summary = (
    customer_loan_data
    .groupby("Segment")
    .agg(
        Customers=("CustomerID", "nunique"),
        LoanOutstandingINR=("OutstandingINR", "sum"),
        NPALoans=("NPAFlag", "sum")
    )
    .reset_index()
)


segment_loan_summary["Customers"] = pd.to_numeric(
    segment_loan_summary["Customers"],
    errors="coerce"
).fillna(0)


segment_loan_summary["NPALoans"] = pd.to_numeric(
    segment_loan_summary["NPALoans"],
    errors="coerce"
).fillna(0)


segment_loan_summary["NPA_Ratio"] = np.where(
    segment_loan_summary["Customers"] > 0,
    segment_loan_summary["NPALoans"]
    / segment_loan_summary["Customers"],
    0
)


customer_summary = customer_summary.merge(
    segment_loan_summary,
    on="Segment",
    how="left"
)


# ============================================================
# 19. TRANSACTION ANALYSIS
# ============================================================

completed_transactions = transactions[
    transactions["Status"].astype(str).str.strip().str.lower()
    == "completed"
].copy()


transaction_summary = (
    completed_transactions
    .groupby("Channel")
    .agg(
        TransactionCount=("TransactionID", "count"),
        TransactionValueINR=("AmountINR", "sum"),
        AverageTransactionINR=("AmountINR", "mean")
    )
    .reset_index()
)


transaction_summary["DigitalFlag"] = np.where(
    transaction_summary["Channel"].isin(
        [
            "Mobile App",
            "Internet Banking",
            "UPI"
        ]
    ),
    "Digital",
    "Traditional"
)


# ============================================================
# 20. DIGITAL BANKING
# ============================================================

digital_transactions = completed_transactions[
    completed_transactions["Channel"].isin(
        [
            "Mobile App",
            "Internet Banking",
            "UPI"
        ]
    )
]


traditional_transactions = completed_transactions[
    ~completed_transactions["Channel"].isin(
        [
            "Mobile App",
            "Internet Banking",
            "UPI"
        ]
    )
]


digital_value = digital_transactions[
    "AmountINR"
].sum()


traditional_value = traditional_transactions[
    "AmountINR"
].sum()


total_transaction_value = (
    digital_value
    + traditional_value
)


digital_adoption = (
    digital_value / total_transaction_value
    if total_transaction_value != 0
    else 0
)


# ============================================================
# 21. NPA MODEL
# ============================================================

total_loans = len(loans)


npa_loans = loans[
    "NPAFlag"
].sum()


npa_ratio = (
    npa_loans / total_loans
    if total_loans != 0
    else 0
)


npa_outstanding = loans.loc[
    loans["NPAFlag"] == 1,
    "OutstandingINR"
].sum()


# ============================================================
# 22. MANAGEMENT KPI CALCULATIONS
# ============================================================

total_deposits = financials[
    "DepositsINR"
].sum()


total_advances = financials[
    "AdvancesINR"
].sum()


interest_income = financials[
    "InterestIncomeINR"
].sum()


interest_expense = financials[
    "InterestExpenseINR"
].sum()


net_interest_income = (
    interest_income
    - interest_expense
)


fee_income = financials[
    "FeeIncomeINR"
].sum()


other_income = financials[
    "OtherIncomeINR"
].sum()


total_income = (
    interest_income
    + fee_income
    + other_income
)


operating_expenses = financials[
    "OperatingExpenseINR"
].sum()


provision_expense = financials[
    "ProvisionINR"
].sum()


pre_provision_profit = (
    total_income
    - operating_expenses
)


net_profit = (
    pre_provision_profit
    - provision_expense
)


profit_margin = (
    net_profit / total_income
    if total_income != 0
    else 0
)


cost_to_income = (
    operating_expenses / total_income
    if total_income != 0
    else 0
)


loan_to_deposit = (
    total_advances / total_deposits
    if total_deposits != 0
    else 0
)


# ============================================================
# 23. KPI TABLE
# ============================================================

kpis = {
    "Total Customers": len(customers),
    "Total Accounts": len(accounts),
    "Total Loans": len(loans),
    "Total Deposits": total_deposits,
    "Total Advances": total_advances,
    "Interest Income": interest_income,
    "Interest Expense": interest_expense,
    "Net Interest Income": net_interest_income,
    "Fee Income": fee_income,
    "Other Income": other_income,
    "Total Income": total_income,
    "Operating Expenses": operating_expenses,
    "Provision Expense": provision_expense,
    "Pre-Provision Profit": pre_provision_profit,
    "Net Profit": net_profit,
    "Profit Margin": profit_margin,
    "Cost to Income Ratio": cost_to_income,
    "Loan to Deposit Ratio": loan_to_deposit,
    "NPA Ratio": npa_ratio,
    "NPA Outstanding": npa_outstanding,
    "Digital Transaction Adoption": digital_adoption
}


kpi_df = pd.DataFrame(
    list(kpis.items()),
    columns=[
        "KPI",
        "Value"
    ]
)


# ============================================================
# 24. MANAGEMENT INSIGHTS
# ============================================================

top_branch = (
    branch_financials
    .sort_values(
        "NetProfitINR",
        ascending=False
    )
    .iloc[0]
)


bottom_branch = (
    branch_financials
    .sort_values(
        "NetProfitINR",
        ascending=True
    )
    .iloc[0]
)


highest_npa_loan_type = (
    loan_summary
    .sort_values(
        "NPA_Ratio",
        ascending=False
    )
    .iloc[0]
)


largest_loan_type = (
    loan_summary
    .sort_values(
        "OutstandingINR",
        ascending=False
    )
    .iloc[0]
)


highest_risk_grade = (
    risk_summary
    .sort_values(
        "NPA_Ratio",
        ascending=False
    )
    .iloc[0]
)


# ============================================================
# 25. EXPORT FILES
# ============================================================

annual.to_csv(
    OUTPUT_DIR / "annual_financial_performance.csv",
    index=False
)


loan_summary.to_csv(
    OUTPUT_DIR / "loan_portfolio_analysis.csv",
    index=False
)


risk_summary.to_csv(
    OUTPUT_DIR / "risk_grade_analysis.csv",
    index=False
)


branch_financials.to_csv(
    OUTPUT_DIR / "branch_performance.csv",
    index=False
)


customer_summary.to_csv(
    OUTPUT_DIR / "customer_segment_analysis.csv",
    index=False
)


segment_loan_summary.to_csv(
    OUTPUT_DIR / "segment_loan_exposure.csv",
    index=False
)


transaction_summary.to_csv(
    OUTPUT_DIR / "transaction_channel_analysis.csv",
    index=False
)


financials.to_csv(
    OUTPUT_DIR / "monthly_financial_model.csv",
    index=False
)


kpi_df.to_csv(
    OUTPUT_DIR / "banking_kpis.csv",
    index=False
)


# ============================================================
# 26. MANAGEMENT INSIGHTS EXPORT
# ============================================================

insights = pd.DataFrame(
    {
        "Metric": [
            "Most Profitable Branch",
            "Least Profitable Branch",
            "Highest NPA Loan Type",
            "Largest Loan Portfolio",
            "Highest Risk Grade"
        ],
        "Result": [
            top_branch["BranchName"],
            bottom_branch["BranchName"],
            highest_npa_loan_type["LoanType"],
            largest_loan_type["LoanType"],
            highest_risk_grade["RiskGrade"]
        ]
    }
)


insights.to_csv(
    OUTPUT_DIR / "management_insights.csv",
    index=False
)


# ============================================================
# 27. CONSOLE REPORT
# ============================================================

print("\n")
print("=" * 70)
print("BANKING KPI SUMMARY")
print("=" * 70)


print(
    f"Total Customers       : {len(customers):,}"
)


print(
    f"Total Accounts        : {len(accounts):,}"
)


print(
    f"Total Loans           : {len(loans):,}"
)


print(
    f"Total Deposits        : "
    f"₹{total_deposits / 10000000:,.2f} Cr"
)


print(
    f"Total Advances        : "
    f"₹{total_advances / 10000000:,.2f} Cr"
)


print(
    f"Interest Income       : "
    f"₹{interest_income / 10000000:,.2f} Cr"
)


print(
    f"Interest Expense      : "
    f"₹{interest_expense / 10000000:,.2f} Cr"
)


print(
    f"Net Interest Income   : "
    f"₹{net_interest_income / 10000000:,.2f} Cr"
)


print(
    f"Fee Income            : "
    f"₹{fee_income / 10000000:,.2f} Cr"
)


print(
    f"Total Income          : "
    f"₹{total_income / 10000000:,.2f} Cr"
)


print(
    f"Operating Expenses    : "
    f"₹{operating_expenses / 10000000:,.2f} Cr"
)


print(
    f"Provision Expense     : "
    f"₹{provision_expense / 10000000:,.2f} Cr"
)


print(
    f"Pre-Provision Profit  : "
    f"₹{pre_provision_profit / 10000000:,.2f} Cr"
)


print(
    f"Net Profit            : "
    f"₹{net_profit / 10000000:,.2f} Cr"
)


print(
    f"Profit Margin         : "
    f"{profit_margin * 100:.2f}%"
)


print(
    f"Cost-to-Income        : "
    f"{cost_to_income * 100:.2f}%"
)


print(
    f"Loan-to-Deposit       : "
    f"{loan_to_deposit * 100:.2f}%"
)


print(
    f"NPA Ratio             : "
    f"{npa_ratio * 100:.2f}%"
)


print(
    f"NPA Outstanding       : "
    f"₹{npa_outstanding / 10000000:,.2f} Cr"
)


print(
    f"Digital Adoption      : "
    f"{digital_adoption * 100:.2f}%"
)


# ============================================================
# 28. MANAGEMENT INSIGHTS
# ============================================================

print("\n")
print("=" * 70)
print("MANAGEMENT INSIGHTS")
print("=" * 70)


print(
    f"\nMost Profitable Branch : "
    f"{top_branch['BranchName']}"
)


print(
    f"Least Profitable Branch: "
    f"{bottom_branch['BranchName']}"
)


print(
    f"Highest NPA Loan Type  : "
    f"{highest_npa_loan_type['LoanType']}"
)


print(
    f"Largest Loan Portfolio : "
    f"{largest_loan_type['LoanType']}"
)


print(
    f"Highest Risk Grade     : "
    f"{highest_risk_grade['RiskGrade']}"
)


# ============================================================
# 29. TOP 5 BRANCHES
# ============================================================

print("\n")
print("=" * 70)
print("TOP 5 BRANCHES BY PROFIT")
print("=" * 70)


top_5 = (
    branch_financials[
        [
            "BranchName",
            "Region",
            "NetProfitINR",
            "ProfitMargin",
            "CostToIncomeRatio"
        ]
    ]
    .sort_values(
        "NetProfitINR",
        ascending=False
    )
    .head(5)
)


print(
    top_5.to_string(index=False)
)


# ============================================================
# 30. BOTTOM 5 BRANCHES
# ============================================================

print("\n")
print("=" * 70)
print("BOTTOM 5 BRANCHES BY PROFIT")
print("=" * 70)


bottom_5 = (
    branch_financials[
        [
            "BranchName",
            "Region",
            "NetProfitINR",
            "ProfitMargin",
            "CostToIncomeRatio"
        ]
    ]
    .sort_values(
        "NetProfitINR",
        ascending=True
    )
    .head(5)
)


print(
    bottom_5.to_string(index=False)
)


# ============================================================
# 31. OUTPUT LOCATION
# ============================================================

print("\n")
print("=" * 70)
print("MODULE 3 COMPLETE")
print("=" * 70)


print(
    f"\nAnalysis files created in:\n"
    f"{OUTPUT_DIR}"
)


print("\nGenerated files:")


for file in sorted(
    OUTPUT_DIR.glob("*.csv")
):

    print(
        f"  - {file.name}"
    )


print("\n")