# financial-literacy-simulator
Overview

This project models the long‑term financial outcomes of two hypothetical individuals—one who is financially literate (FL) and one who is not (NFL). It tracks savings, checking, debt, housing decisions, and overall wealth over 40 years to illustrate how everyday financial choices compound over time.


Key Features:
Person class – Encapsulates the financial behavior of an FL or NFL individual, including savings growth, debt repayment, rent, and mortgage.
Simulation class – Runs year‑by‑year projections, logging wealth, years in debt, and total debt paid.
Unit tests – Comprehensive test suite (run_tests) validates every public method.
Visualization – Generates wealth_comparison.png, a line chart showing wealth trajectories for FL vs NFL.


How It Works:
Annual Contributions – Each year, the individual allocates a fixed percentage of salary to savings and checking.
Savings Growth – FL invests in mutual funds (7 % annual return); NFL uses a standard savings account (1 %).
Debt Repayment – Both pay at least the minimum each month. FL makes larger extra payments.
Housing Decision – Once the down payment threshold is met, the person buys a house and begins mortgage payments.
Wealth Calculation – Wealth = savings + checking – debt – mortgage balance.


Requirements:
Python 3.8 or newer
matplotlib (optional, for the chart)


Install dependencies (only if you want the graph):
pip install matplotlib


Running the Simulation:
python finance_simulation.py
The script first runs run_tests() – you’ll see “All tests passed!” if everything is correct.
It then prints a summary comparison and (optionally) saves the wealth chart.

Customizing Parameters:
All simulation constants (salary, interest rates, rent, etc.) are defined at the top of finance_simulation.py. Change them to explore different scenarios—for example:
ANNUAL_SALARY = 75000      # try a higher income
SAVINGS_INTEREST_FL = 0.08 # assume better fund performance

Sample Output:
Financial Literacy Simulation
------------------------------

Results after 40 years:
Simulation Results for Financially Literate Person:
  Years in Debt: 5
  Years Rented: 3
  Total Debt Paid: $43,812.00
  Final Wealth: $728,951

Simulation Results for Not Financially Literate Person:
  Years in Debt: 15
  Years Rented: 10
  Total Debt Paid: $60,437.00
  Final Wealth: $192,367

Comparison:
NFL paid $16,625.00 more in debt than FL
NFL spent 10 more years in debt than FL
FL has $536,584.00 more in wealth than NFL after 40 years
Wealth comparison graph saved to 'wealth_comparison.png'

(Values will differ if you adjust parameters.)
