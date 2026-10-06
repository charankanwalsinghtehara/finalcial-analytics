import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# BANKING FINANCIAL PERFORMANCE DATA GENERATOR

# ============================================================

np.random.seed(42)

# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 1. BRANCH DATA
# ------------------------------------------------------------

branches = [
    ("B001", "Delhi Main", "Delhi", "North", "Metro"),
    ("B002", "Ludhiana Main", "Ludhiana", "North", "Urban"),
    ("B003", "Chandigarh Main", "Chandigarh", "North", "Urban"),
    ("B004", "Jaipur Main", "Jaipur", "North", "Urban"),
    ("B005", "Lucknow Main", "Lucknow", "North", "Urban"),

    ("B006", "Mumbai Main", "Mumbai", "West", "Metro"),
    ("B007", "Pune Main", "Pune", "West", "Metro"),
    ("B008", "Ahmedabad Main", "Ahmedabad", "West", "Metro"),
    ("B009", "Surat Main", "Surat", "West", "Urban"),

    ("B010", "Bangalore Main", "Bangalore", "South", "Metro"),
    ("B011", "Chennai Main", "Chennai", "South", "Metro"),
    ("B012", "Hyderabad Main", "Hyderabad", "South", "Metro"),
    ("B013", "Kochi Main", "Kochi", "South", "Urban"),

    ("B014", "Kolkata Main", "Kolkata", "East", "Metro"),
    ("B015", "Bhubaneswar Main", "Bhubaneswar", "East", "Urban"),
    ("B016", "Patna Main", "Patna", "East", "Urban"),
    ("B017", "Guwahati Main", "Guwahati", "East", "Urban"),

    ("B018", "Bhopal Main", "Bhopal", "Central", "Urban"),
    ("B019", "Indore Main", "Indore", "Central", "Urban"),
    ("B020", "Nagpur Main", "Nagpur", "Central", "Urban")
]

branches_df = pd.DataFrame(
    branches,
    columns=[
        "BranchID",
        "BranchName",
        "City",
        "Region",
        "BranchType"
    ]
)

branches_df["OpenedYear"] = np.random.randint(
    2010,
    2021,
    len(branches_df)
)

branches_df.to_csv(
    DATA_DIR / "branches.csv",
    index=False
)

print("Branches created:", len(branches_df))


# ------------------------------------------------------------
# 2. CUSTOMER DATA
# ------------------------------------------------------------

NUM_CUSTOMERS = 10000

customer_ids = [
    f"C{i:06d}"
    for i in range(1, NUM_CUSTOMERS + 1)
]

customer_segments = np.random.choice(
    [
        "Retail",
        "Mass Affluent",
        "Affluent",
        "SME"
    ],
    NUM_CUSTOMERS,
    p=[0.50, 0.25, 0.15, 0.10]
)

ages = np.clip(
    np.random.normal(
        39,
        11,
        NUM_CUSTOMERS
    ).round(),
    18,
    75
).astype(int)

annual_income = np.exp(
    np.random.normal(
        np.log(600000),
        0.65,
        NUM_CUSTOMERS
    )
)

annual_income = np.clip(
    annual_income,
    180000,
    10000000
).round().astype(int)

employment = np.random.choice(
    [
        "Salaried",
        "Self-Employed",
        "Business",
        "Retired"
    ],
    NUM_CUSTOMERS,
    p=[0.55, 0.18, 0.22, 0.05]
)

gender = np.random.choice(
    [
        "Male",
        "Female",
        "Other"
    ],
    NUM_CUSTOMERS,
    p=[0.52, 0.46, 0.02]
)

branch_ids = np.random.choice(
    branches_df["BranchID"],
    NUM_CUSTOMERS
)

customer_since = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            "2015-01-01",
            "2023-12-31"
        ),
        NUM_CUSTOMERS
    )
)

credit_score = np.clip(
    np.random.normal(
        720,
        70,
        NUM_CUSTOMERS
    ).round(),
    300,
    900
).astype(int)

customers_df = pd.DataFrame({
    "CustomerID": customer_ids,
    "CustomerSegment": customer_segments,
    "Age": ages,
    "AnnualIncomeINR": annual_income,
    "EmploymentType": employment,
    "Gender": gender,
    "BranchID": branch_ids,
    "CustomerSince": customer_since,
    "CreditScore": credit_score
})

customers_df.to_csv(
    DATA_DIR / "customers.csv",
    index=False
)

print("Customers created:", len(customers_df))


# ------------------------------------------------------------
# 3. ACCOUNT DATA
# ------------------------------------------------------------

account_types = [
    "Savings",
    "Current",
    "Salary",
    "Fixed Deposit"
]

account_rows = []

account_counter = 1

for customer_id in customer_ids:

    number_of_accounts = np.random.choice(
        [1, 2, 3],
        p=[0.70, 0.25, 0.05]
    )

    for _ in range(number_of_accounts):

        account_type = np.random.choice(
            account_types,
            p=[0.50, 0.15, 0.20, 0.15]
        )

        if account_type == "Fixed Deposit":

            balance = np.random.lognormal(
                mean=12,
                sigma=0.8
            )

        else:

            balance = np.random.lognormal(
                mean=10,
                sigma=0.9
            )

        balance = max(
            1000,
            balance
        )

        open_date = pd.Timestamp(
            np.random.choice(
                pd.date_range(
                    "2018-01-01",
                    "2025-06-30"
                )
            )
        )

        status = np.random.choice(
            [
                "Active",
                "Dormant"
            ],
            p=[0.96, 0.04]
        )

        account_rows.append([
            f"A{account_counter:07d}",
            customer_id,
            account_type,
            round(balance, 2),
            open_date,
            status
        ])

        account_counter += 1


accounts_df = pd.DataFrame(
    account_rows,
    columns=[
        "AccountID",
        "CustomerID",
        "AccountType",
        "CurrentBalanceINR",
        "OpenDate",
        "AccountStatus"
    ]
)

accounts_df.to_csv(
    DATA_DIR / "accounts.csv",
    index=False
)

print("Accounts created:", len(accounts_df))


# ------------------------------------------------------------
# 4. LOAN DATA
# ------------------------------------------------------------

NUM_LOANS = 7000

loan_customers = np.random.choice(
    customer_ids,
    NUM_LOANS
)

loan_types = np.random.choice(
    [
        "Home Loan",
        "Personal Loan",
        "Auto Loan",
        "Business Loan",
        "Education Loan"
    ],
    NUM_LOANS,
    p=[
        0.24,
        0.28,
        0.18,
        0.18,
        0.12
    ]
)

loan_amounts = np.exp(
    np.random.normal(
        np.log(700000),
        1.0,
        NUM_LOANS
    )
)

loan_amounts = np.clip(
    loan_amounts,
    50000,
    15000000
)

interest_rates = np.random.uniform(
    7.2,
    16.5,
    NUM_LOANS
).round(2)

origination_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            "2021-01-01",
            "2025-12-31"
        ),
        NUM_LOANS
    )
)

tenures = np.random.choice(
    [
        24,
        36,
        48,
        60,
        84,
        120,
        180,
        240
    ],
    NUM_LOANS
)

outstanding = (
    loan_amounts *
    np.random.uniform(
        0.20,
        0.98,
        NUM_LOANS
    )
)

# ------------------------------------------------------------
# CREDIT RISK
# ------------------------------------------------------------

npa_probability = (
    0.04
    + np.where(
        interest_rates > 12,
        0.05,
        0
    )
    + np.where(
        loan_amounts > 3000000,
        0.03,
        0
    )
)

npa_probability = np.clip(
    npa_probability,
    0,
    0.25
)

npa = np.random.random(
    NUM_LOANS
) < npa_probability

npa_flag = np.where(
    npa,
    "NPA",
    "Standard"
)

risk_grade = []

for is_npa in npa:

    if is_npa:

        risk_grade.append(
            np.random.choice(
                ["D", "E"]
            )
        )

    else:

        risk_grade.append(
            np.random.choice(
                ["A", "B", "C"],
                p=[0.45, 0.40, 0.15]
            )
        )


loans_df = pd.DataFrame({

    "LoanID": [
        f"L{i:07d}"
        for i in range(1, NUM_LOANS + 1)
    ],

    "CustomerID": loan_customers,

    "LoanType": loan_types,

    "LoanAmountINR":
        loan_amounts.round().astype(int),

    "InterestRatePct":
        interest_rates,

    "OriginationDate":
        origination_dates,

    "TenureMonths":
        tenures,

    "OutstandingINR":
        outstanding.round().astype(int),

    "NPAFlag":
        npa_flag,

    "RiskGrade":
        risk_grade
})

loans_df.to_csv(
    DATA_DIR / "loans.csv",
    index=False
)

print("Loans created:", len(loans_df))


# ------------------------------------------------------------
# 5. TRANSACTION DATA
# ------------------------------------------------------------

NUM_TRANSACTIONS = 100000

transaction_ids = [
    f"T{i:08d}"
    for i in range(
        1,
        NUM_TRANSACTIONS + 1
    )
]

transaction_dates = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            "2023-01-01",
            "2025-12-31"
        ),
        NUM_TRANSACTIONS
    )
)

transaction_types = np.random.choice(

    [
        "Deposit",
        "Withdrawal",
        "Transfer In",
        "Transfer Out",
        "Interest Credit",
        "Fee",
        "Loan EMI"
    ],

    NUM_TRANSACTIONS,

    p=[
        0.25,
        0.18,
        0.14,
        0.14,
        0.08,
        0.08,
        0.13
    ]
)

transaction_amounts = np.exp(
    np.random.normal(
        np.log(8500),
        1.15,
        NUM_TRANSACTIONS
    )
)

transaction_amounts = np.clip(
    transaction_amounts,
    100,
    500000
)

negative_types = [
    "Withdrawal",
    "Transfer Out",
    "Fee",
    "Loan EMI"
]

net_cash_flow = np.where(
    np.isin(
        transaction_types,
        negative_types
    ),
    -transaction_amounts,
    transaction_amounts
)

transaction_customer = np.random.choice(
    customer_ids,
    NUM_TRANSACTIONS
)

transaction_branch = np.random.choice(
    branches_df["BranchID"],
    NUM_TRANSACTIONS
)

channels = np.random.choice(

    [
        "Branch",
        "ATM",
        "Mobile App",
        "Internet Banking",
        "UPI"
    ],

    NUM_TRANSACTIONS,

    p=[
        0.18,
        0.20,
        0.25,
        0.17,
        0.20
    ]
)

transaction_status = np.random.choice(

    [
        "Completed",
        "Failed",
        "Reversed"
    ],

    NUM_TRANSACTIONS,

    p=[
        0.965,
        0.025,
        0.010
    ]
)

transactions_df = pd.DataFrame({

    "TransactionID":
        transaction_ids,

    "Date":
        transaction_dates,

    "CustomerID":
        transaction_customer,

    "BranchID":
        transaction_branch,

    "TransactionType":
        transaction_types,

    "AmountINR":
        transaction_amounts.round(2),

    "NetCashFlowINR":
        net_cash_flow.round(2),

    "Channel":
        channels,

    "Status":
        transaction_status
})

transactions_df.to_csv(
    DATA_DIR / "transactions.csv",
    index=False
)

print(
    "Transactions created:",
    len(transactions_df)
)


# ------------------------------------------------------------
# 6. MONTHLY BANK FINANCIALS
# ------------------------------------------------------------

months = pd.date_range(
    "2023-01-01",
    "2025-12-01",
    freq="MS"
)

financial_rows = []

for month in months:

    for branch_id in branches_df["BranchID"]:

        # Branch scale
        branch_scale = np.random.uniform(
            0.8,
            1.3
        )

        # Seasonal effect
        seasonal_factor = (
            1
            + 0.05 *
            np.sin(
                (month.month - 1)
                / 12
                * 2
                * np.pi
            )
        )

        deposits = (
            np.random.uniform(
                8_000_000,
                25_000_000
            )
            * branch_scale
            * seasonal_factor
        )

        advances = (
            np.random.uniform(
                6_000_000,
                20_000_000
            )
            * branch_scale
            * seasonal_factor
        )

        interest_income = (
            advances
            * np.random.uniform(
                0.075,
                0.115
            )
        )

        interest_expense = (
            deposits
            * np.random.uniform(
                0.025,
                0.055
            )
        )

        fee_income = (
            deposits
            * np.random.uniform(
                0.004,
                0.012
            )
        )

        other_income = (
            deposits
            * np.random.uniform(
                0.002,
                0.006
            )
        )

        operating_expense = (
            deposits
            * np.random.uniform(
                0.035,
                0.065
            )
        )

        provision = (
            advances
            * np.random.uniform(
                0.003,
                0.012
            )
        )

        net_interest_income = (
            interest_income
            - interest_expense
        )

        total_income = (
            interest_income
            + fee_income
            + other_income
        )

        pre_provision_profit = (
            total_income
            - interest_expense
            - operating_expense
        )

        net_profit = (
            pre_provision_profit
            - provision
        )

        financial_rows.append([

            month,
            branch_id,

            round(
                deposits,
                2
            ),

            round(
                advances,
                2
            ),

            round(
                interest_income,
                2
            ),

            round(
                interest_expense,
                2
            ),

            round(
                fee_income,
                2
            ),

            round(
                other_income,
                2
            ),

            round(
                operating_expense,
                2
            ),

            round(
                provision,
                2
            ),

            round(
                net_interest_income,
                2
            ),

            round(
                total_income,
                2
            ),

            round(
                pre_provision_profit,
                2
            ),

            round(
                net_profit,
                2
            )
        ])


financials_df = pd.DataFrame(

    financial_rows,

    columns=[

        "Month",
        "BranchID",
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

financials_df.to_csv(
    DATA_DIR / "financials.csv",
    index=False
)

print(
    "Financial records created:",
    len(financials_df)
)


# ------------------------------------------------------------
# COMPLETE
# ------------------------------------------------------------

print()
print("=" * 60)
print("BANKING DATA GENERATION COMPLETE")
print("=" * 60)

print()
print("Files created:")

for file in DATA_DIR.glob("*.csv"):

    print(
        f" - {file.name}"
    )

print()
print("Data location:")
print(DATA_DIR)