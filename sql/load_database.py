import sqlite3
import pandas as pd
from pathlib import Path


# ============================================================
# BANKING DATABASE LOADER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DB_PATH = BASE_DIR / "banking_financial_analysis.db"


# ------------------------------------------------------------
# CONNECT TO DATABASE
# ------------------------------------------------------------

connection = sqlite3.connect(DB_PATH)


# ------------------------------------------------------------
# LOAD CSV FILES
# ------------------------------------------------------------

files = {

    "branches": "branches.csv",

    "customers": "customers.csv",

    "accounts": "accounts.csv",

    "loans": "loans.csv",

    "transactions": "transactions.csv",

    "financials": "financials.csv"
}


for table_name, file_name in files.items():

    file_path = DATA_DIR / file_name

    print(
        f"Loading {file_name}..."
    )

    df = pd.read_csv(
        file_path
    )

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"{table_name}: {len(df):,} rows"
    )


# ------------------------------------------------------------
# CREATE INDEXES
# ------------------------------------------------------------

cursor = connection.cursor()


indexes = [

    """
    CREATE INDEX IF NOT EXISTS
    idx_customer_branch
    ON customers(BranchID)
    """,

    """
    CREATE INDEX IF NOT EXISTS
    idx_account_customer
    ON accounts(CustomerID)
    """,

    """
    CREATE INDEX IF NOT EXISTS
    idx_loan_customer
    ON loans(CustomerID)
    """,

    """
    CREATE INDEX IF NOT EXISTS
    idx_transaction_customer
    ON transactions(CustomerID)
    """,

    """
    CREATE INDEX IF NOT EXISTS
    idx_transaction_branch
    ON transactions(BranchID)
    """,

    """
    CREATE INDEX IF NOT EXISTS
    idx_transaction_date
    ON transactions(Date)
    """,

    """
    CREATE INDEX IF NOT EXISTS
    idx_financial_branch
    ON financials(BranchID)
    """

]


for index_sql in indexes:

    cursor.execute(
        index_sql
    )


connection.commit()


# ------------------------------------------------------------
# VERIFY TABLES
# ------------------------------------------------------------

print()
print("=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """
)

tables = cursor.fetchall()


for table in tables:

    table_name = table[0]

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    count = cursor.fetchone()[0]

    print(
        f"{table_name:<15} {count:,} rows"
    )


# ------------------------------------------------------------
# CLOSE
# ------------------------------------------------------------

connection.close()


print()
print("=" * 60)
print("DATABASE CREATED SUCCESSFULLY")
print("=" * 60)

print()
print(
    f"Database location: {DB_PATH}"
)