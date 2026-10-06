

-- Total Customers
SELECT
    COUNT(*) AS TotalCustomers
FROM customers;


-- Customer Segmentation
SELECT
    Segment,
    COUNT(*) AS CustomerCount
FROM customers
GROUP BY Segment
ORDER BY CustomerCount DESC;


-- Customers by Region
SELECT
    b.Region,
    COUNT(DISTINCT c.CustomerID) AS Customers
FROM customers c
JOIN branches b
    ON c.BranchID = b.BranchID
GROUP BY b.Region
ORDER BY Customers DESC;


-- ============================================================
-- 2. DEPOSIT ANALYSIS
-- ============================================================

-- Total Deposits
SELECT
    ROUND(SUM(DepositsINR) / 10000000.0, 2) AS TotalDeposits_Crore
FROM financials;


-- Deposits by Region
SELECT
    b.Region,
    ROUND(SUM(f.DepositsINR) / 10000000.0, 2) AS Deposits_Crore
FROM financials f
JOIN branches b
    ON f.BranchID = b.BranchID
GROUP BY b.Region
ORDER BY Deposits_Crore DESC;


-- Deposits by Branch
SELECT
    b.BranchName,
    b.Region,
    ROUND(SUM(f.DepositsINR) / 10000000.0, 2) AS Deposits_Crore
FROM financials f
JOIN branches b
    ON f.BranchID = b.BranchID
GROUP BY b.BranchID, b.BranchName, b.Region
ORDER BY Deposits_Crore DESC;


-- ============================================================
-- 3. ADVANCES / LOAN ANALYSIS
-- ============================================================

-- Total Advances
SELECT
    ROUND(SUM(AdvancesINR) / 10000000.0, 2) AS TotalAdvances_Crore
FROM financials;


-- Advances by Region
SELECT
    b.Region,
    ROUND(SUM(f.AdvancesINR) / 10000000.0, 2) AS Advances_Crore
FROM financials f
JOIN branches b
    ON f.BranchID = b.BranchID
GROUP BY b.Region
ORDER BY Advances_Crore DESC;


-- Loan Portfolio by Type
SELECT
    LoanType,
    COUNT(*) AS LoanCount,
    ROUND(SUM(LoanAmountINR) / 10000000.0, 2) AS LoanAmount_Crore,
    ROUND(SUM(OutstandingINR) / 10000000.0, 2) AS Outstanding_Crore
FROM loans
GROUP BY LoanType
ORDER BY Outstanding_Crore DESC;


-- ============================================================
-- 4. NET INTEREST INCOME
-- ============================================================

SELECT
    ROUND(SUM(InterestIncomeINR) / 10000000.0, 2)
        AS InterestIncome_Crore,

    ROUND(SUM(InterestExpenseINR) / 10000000.0, 2)
        AS InterestExpense_Crore,

    ROUND(
        (SUM(InterestIncomeINR) - SUM(InterestExpenseINR))
        / 10000000.0,
        2
    ) AS NetInterestIncome_Crore
FROM financials;


-- ============================================================
-- 5. TOTAL INCOME
-- ============================================================

SELECT
    ROUND(SUM(InterestIncomeINR) / 10000000.0, 2)
        AS InterestIncome_Crore,

    ROUND(SUM(FeeIncomeINR) / 10000000.0, 2)
        AS FeeIncome_Crore,

    ROUND(SUM(OtherIncomeINR) / 10000000.0, 2)
        AS OtherIncome_Crore,

    ROUND(SUM(TotalIncomeINR) / 10000000.0, 2)
        AS TotalIncome_Crore
FROM financials;


-- ============================================================
-- 6. PROFITABILITY
-- ============================================================

SELECT
    ROUND(SUM(TotalIncomeINR) / 10000000.0, 2)
        AS TotalIncome_Crore,

    ROUND(SUM(OperatingExpenseINR) / 10000000.0, 2)
        AS OperatingExpense_Crore,

    ROUND(SUM(ProvisionExpenseINR) / 10000000.0, 2)
        AS Provision_Crore,

    ROUND(SUM(NetProfitINR) / 10000000.0, 2)
        AS NetProfit_Crore
FROM financials;


-- Profit Margin
SELECT
    ROUND(
        SUM(NetProfitINR) * 100.0 /
        NULLIF(SUM(TotalIncomeINR), 0),
        2
    ) AS ProfitMargin_Percent
FROM financials;


-- ============================================================
-- 7. COST TO INCOME RATIO
-- ============================================================

SELECT
    ROUND(
        SUM(OperatingExpenseINR) * 100.0 /
        NULLIF(SUM(TotalIncomeINR), 0),
        2
    ) AS CostToIncomeRatio_Percent
FROM financials;


-- ============================================================
-- 8. LOAN TO DEPOSIT RATIO
-- ============================================================

SELECT
    ROUND(
        SUM(AdvancesINR) * 100.0 /
        NULLIF(SUM(DepositsINR), 0),
        2
    ) AS LoanToDepositRatio_Percent
FROM financials;


-- ============================================================
-- 9. YEARLY FINANCIAL PERFORMANCE
-- ============================================================

SELECT
    SUBSTR(Month, 1, 4) AS Year,

    ROUND(SUM(DepositsINR) / 10000000.0, 2)
        AS Deposits_Crore,

    ROUND(SUM(AdvancesINR) / 10000000.0, 2)
        AS Advances_Crore,

    ROUND(SUM(TotalIncomeINR) / 10000000.0, 2)
        AS TotalIncome_Crore,

    ROUND(SUM(NetProfitINR) / 10000000.0, 2)
        AS NetProfit_Crore

FROM financials
GROUP BY SUBSTR(Month, 1, 4)
ORDER BY Year;


-- ============================================================
-- 10. YEARLY PROFIT GROWTH
-- ============================================================

WITH yearly_profit AS (

    SELECT
        SUBSTR(Month, 1, 4) AS Year,
        SUM(NetProfitINR) AS NetProfit
    FROM financials
    GROUP BY SUBSTR(Month, 1, 4)

)

SELECT
    Year,

    ROUND(NetProfit / 10000000.0, 2)
        AS NetProfit_Crore,

    ROUND(
        (NetProfit -
        LAG(NetProfit) OVER (ORDER BY Year))
        * 100.0 /
        NULLIF(
            LAG(NetProfit) OVER (ORDER BY Year),
            0
        ),
        2
    ) AS ProfitGrowth_Percent

FROM yearly_profit
ORDER BY Year;


-- ============================================================
-- 11. REGIONAL PROFITABILITY
-- ============================================================

SELECT
    b.Region,

    ROUND(SUM(f.TotalIncomeINR) / 10000000.0, 2)
        AS TotalIncome_Crore,

    ROUND(SUM(f.OperatingExpenseINR) / 10000000.0, 2)
        AS OperatingExpense_Crore,

    ROUND(SUM(f.NetProfitINR) / 10000000.0, 2)
        AS NetProfit_Crore,

    ROUND(
        SUM(f.NetProfitINR) * 100.0 /
        NULLIF(SUM(f.TotalIncomeINR), 0),
        2
    ) AS ProfitMargin_Percent

FROM financials f

JOIN branches b
    ON f.BranchID = b.BranchID

GROUP BY b.Region

ORDER BY NetProfit_Crore DESC;


-- ============================================================
-- 12. BRANCH PROFITABILITY
-- ============================================================

SELECT
    b.BranchID,
    b.BranchName,
    b.Region,

    ROUND(SUM(f.DepositsINR) / 10000000.0, 2)
        AS Deposits_Crore,

    ROUND(SUM(f.AdvancesINR) / 10000000.0, 2)
        AS Advances_Crore,

    ROUND(SUM(f.TotalIncomeINR) / 10000000.0, 2)
        AS TotalIncome_Crore,

    ROUND(SUM(f.NetProfitINR) / 10000000.0, 2)
        AS NetProfit_Crore,

    ROUND(
        SUM(f.NetProfitINR) * 100.0 /
        NULLIF(SUM(f.TotalIncomeINR), 0),
        2
    ) AS ProfitMargin_Percent

FROM financials f

JOIN branches b
    ON f.BranchID = b.BranchID

GROUP BY
    b.BranchID,
    b.BranchName,
    b.Region

ORDER BY NetProfit_Crore DESC;


-- ============================================================
-- 13. BRANCH COST EFFICIENCY
-- ============================================================

SELECT
    b.BranchName,
    b.Region,

    ROUND(
        SUM(f.OperatingExpenseINR) / 10000000.0,
        2
    ) AS OperatingExpense_Crore,

    ROUND(
        SUM(f.TotalIncomeINR) / 10000000.0,
        2
    ) AS TotalIncome_Crore,

    ROUND(
        SUM(f.OperatingExpenseINR) * 100.0 /
        NULLIF(SUM(f.TotalIncomeINR), 0),
        2
    ) AS CostToIncomeRatio_Percent

FROM financials f

JOIN branches b
    ON f.BranchID = b.BranchID

GROUP BY
    b.BranchID,
    b.BranchName,
    b.Region

ORDER BY CostToIncomeRatio_Percent ASC;


-- ============================================================
-- 14. NPA ANALYSIS
-- ============================================================

-- Overall NPA Ratio
SELECT
    COUNT(*) AS TotalLoans,

    SUM(
        CASE
            WHEN NPAFlag = 1 THEN 1
            ELSE 0
        END
    ) AS NPALoans,

    ROUND(
        SUM(
            CASE
                WHEN NPAFlag = 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS NPA_Ratio_Percent

FROM loans;


-- NPA by Loan Type
SELECT
    LoanType,

    COUNT(*) AS TotalLoans,

    SUM(
        CASE
            WHEN NPAFlag = 1 THEN 1
            ELSE 0
        END
    ) AS NPALoans,

    ROUND(
        SUM(
            CASE
                WHEN NPAFlag = 1 THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS NPA_Ratio_Percent,

    ROUND(
        SUM(
            CASE
                WHEN NPAFlag = 1
                THEN OutstandingINR
                ELSE 0
            END
        ) / 10000000.0,
        2
    ) AS NPA_Outstanding_Crore

FROM loans

GROUP BY LoanType

ORDER BY NPA_Ratio_Percent DESC;


-- ============================================================
-- 15. RISK GRADE ANALYSIS
-- ============================================================

SELECT
    RiskGrade,

    COUNT(*) AS LoanCount,

    ROUND(
        SUM(OutstandingINR) / 10000000.0,
        2
    ) AS Outstanding_Crore,

    ROUND(
        AVG(InterestRate),
        2
    ) AS AverageInterestRate,

    ROUND(
        AVG(
            CASE
                WHEN NPAFlag = 1 THEN 1.0
                ELSE 0.0
            END
        ) * 100,
        2
    ) AS NPA_Ratio_Percent

FROM loans

GROUP BY RiskGrade

ORDER BY NPA_Ratio_Percent DESC;


-- ============================================================
-- 16. CREDIT SCORE VS NPA
-- ============================================================

SELECT
    CASE
        WHEN c.CreditScore < 600 THEN 'Below 600'
        WHEN c.CreditScore < 700 THEN '600-699'
        WHEN c.CreditScore < 800 THEN '700-799'
        ELSE '800+'
    END AS CreditScoreBand,

    COUNT(DISTINCT c.CustomerID) AS Customers,

    COUNT(l.LoanID) AS Loans,

    SUM(
        CASE
            WHEN l.NPAFlag = 1 THEN 1
            ELSE 0
        END
    ) AS NPALoans,

    ROUND(
        SUM(
            CASE
                WHEN l.NPAFlag = 1 THEN 1
                ELSE 0
            END
        ) * 100.0 /
        NULLIF(COUNT(l.LoanID), 0),
        2
    ) AS NPA_Ratio_Percent

FROM customers c

LEFT JOIN loans l
    ON c.CustomerID = l.CustomerID

GROUP BY CreditScoreBand

ORDER BY CreditScoreBand;


-- ============================================================
-- 17. TRANSACTION ANALYSIS
-- ============================================================

SELECT
    TransactionType,

    COUNT(*) AS TransactionCount,

    ROUND(
        SUM(AmountINR) / 10000000.0,
        2
    ) AS TransactionValue_Crore

FROM transactions

WHERE Status = 'Completed'

GROUP BY TransactionType

ORDER BY TransactionValue_Crore DESC;


-- ============================================================
-- 18. TRANSACTION CHANNEL ANALYSIS
-- ============================================================

SELECT
    Channel,

    COUNT(*) AS TransactionCount,

    ROUND(
        SUM(AmountINR) / 10000000.0,
        2
    ) AS TransactionValue_Crore,

    ROUND(
        AVG(AmountINR),
        2
    ) AS AverageTransaction_INR

FROM transactions

WHERE Status = 'Completed'

GROUP BY Channel

ORDER BY TransactionCount DESC;


-- ============================================================
-- 19. DIGITAL VS TRADITIONAL BANKING
-- ============================================================

SELECT

    CASE
        WHEN Channel IN ('Mobile App', 'Internet Banking', 'UPI')
            THEN 'Digital'

        ELSE 'Traditional'
    END AS BankingType,

    COUNT(*) AS TransactionCount,

    ROUND(
        SUM(AmountINR) / 10000000.0,
        2
    ) AS TransactionValue_Crore

FROM transactions

WHERE Status = 'Completed'

GROUP BY BankingType;


-- ============================================================
-- 20. CUSTOMER SEGMENT ANALYSIS
-- ============================================================

SELECT

    c.Segment,

    COUNT(DISTINCT c.CustomerID) AS Customers,

    COUNT(DISTINCT l.LoanID) AS Loans,

    ROUND(
        SUM(l.OutstandingINR) / 10000000.0,
        2
    ) AS LoanOutstanding_Crore,

    ROUND(
        AVG(c.CreditScore),
        2
    ) AS AverageCreditScore

FROM customers c

LEFT JOIN loans l
    ON c.CustomerID = l.CustomerID

GROUP BY c.Segment

ORDER BY LoanOutstanding_Crore DESC;


-- ============================================================
-- 21. TOP 10 BRANCHES
-- ============================================================

SELECT
    b.BranchName,
    b.Region,

    ROUND(
        SUM(f.NetProfitINR) / 10000000.0,
        2
    ) AS NetProfit_Crore

FROM financials f

JOIN branches b
    ON f.BranchID = b.BranchID

GROUP BY
    b.BranchID,
    b.BranchName,
    b.Region

ORDER BY NetProfit_Crore DESC

LIMIT 10;


-- ============================================================
-- 22. BOTTOM 10 BRANCHES
-- ============================================================

SELECT
    b.BranchName,
    b.Region,

    ROUND(
        SUM(f.NetProfitINR) / 10000000.0,
        2
    ) AS NetProfit_Crore

FROM financials f

JOIN branches b
    ON f.BranchID = b.BranchID

GROUP BY
    b.BranchID,
    b.BranchName,
    b.Region

ORDER BY NetProfit_Crore ASC

LIMIT 10;


-- ============================================================
-- 23. HIGH DEPOSIT BUT LOW PROFIT BRANCHES
-- ============================================================

WITH branch_metrics AS (

    SELECT
        BranchID,

        SUM(DepositsINR) AS Deposits,

        SUM(NetProfitINR) AS NetProfit

    FROM financials

    GROUP BY BranchID
),

averages AS (

    SELECT
        AVG(Deposits) AS AvgDeposits,
        AVG(NetProfit) AS AvgProfit

    FROM branch_metrics
)

SELECT

    b.BranchName,
    b.Region,

    ROUND(
        bm.Deposits / 10000000.0,
        2
    ) AS Deposits_Crore,

    ROUND(
        bm.NetProfit / 10000000.0,
        2
    ) AS NetProfit_Crore

FROM branch_metrics bm

JOIN branches b
    ON bm.BranchID = b.BranchID

CROSS JOIN averages a

WHERE
    bm.Deposits > a.AvgDeposits
    AND bm.NetProfit < a.AvgProfit

ORDER BY bm.Deposits DESC;


-- ============================================================
-- 24. HIGH RISK LOAN PORTFOLIO
-- ============================================================

SELECT

    LoanType,
    RiskGrade,

    COUNT(*) AS LoanCount,

    ROUND(
        SUM(OutstandingINR) / 10000000.0,
        2
    ) AS Outstanding_Crore,

    ROUND(
        AVG(InterestRate),
        2
    ) AS AverageInterestRate,

    ROUND(
        AVG(
            CASE
                WHEN NPAFlag = 1 THEN 1.0
                ELSE 0.0
            END
        ) * 100,
        2
    ) AS NPA_Ratio_Percent

FROM loans

GROUP BY
    LoanType,
    RiskGrade

ORDER BY NPA_Ratio_Percent DESC;


-- ============================================================
-- 25. MONTHLY FINANCIAL PERFORMANCE
-- ============================================================

SELECT

    Month,

    ROUND(
        SUM(DepositsINR) / 10000000.0,
        2
    ) AS Deposits_Crore,

    ROUND(
        SUM(AdvancesINR) / 10000000.0,
        2
    ) AS Advances_Crore,

    ROUND(
        SUM(TotalIncomeINR) / 10000000.0,
        2
    ) AS TotalIncome_Crore,

    ROUND(
        SUM(NetProfitINR) / 10000000.0,
        2
    ) AS NetProfit_Crore

FROM financials

GROUP BY Month

ORDER BY Month;

