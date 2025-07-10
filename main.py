# Author: Yimin Huang

INITIAL_SAVINGS = 5000
INITIAL_DEBT = 30100
INITIAL_WEALTH = -25100  
ANNUAL_SALARY = 59000
SAVINGS_PERCENT = 0.2
CHECKING_PERCENT = 0.3
TOTAL_PERCENT_AVAILABLE = SAVINGS_PERCENT + CHECKING_PERCENT 
ANNUAL_CONTRIBUTION = ANNUAL_SALARY * TOTAL_PERCENT_AVAILABLE
MONTHLY_RENT = 850
HOUSE_COST = 175000
FL_DOWN_PAYMENT_PERCENT = 0.2
NFL_DOWN_PAYMENT_PERCENT = 0.05
FL_MORTGAGE_INTEREST = 0.045
NFL_MORTGAGE_INTEREST = 0.05 
MORTGAGE_YEARS = 30
SAVINGS_INTEREST_NFL = 0.01 
SAVINGS_INTEREST_FL = 0.07  
DEBT_INTEREST = 0.2
DEBT_MIN_PAYMENT_PERCENT = 0.03
FL_ADDITIONAL_DEBT_PAYMENT = 15
NFL_ADDITIONAL_DEBT_PAYMENT = 1

class Person:
    """
    A class to represent a financially literate and a not finantially literate person
    """
    
    def __init__(self, is_financially_literate):
        """
        Initialize a Person with whether they're financial literacy and accounts.
        Arguments:
            is_financially_literate (bool): Whether the person is financially literate
        """
        self.is_financially_literate = is_financially_literate
        self.savings = INITIAL_SAVINGS
        self.checking = 0
        self.debt = INITIAL_DEBT
        self.loan = 0
        self.has_house = False
        
    def calculate_savings_balance_after_year(self):
        """
        Update the savings account balance after one year based on financial literacy.
        FL person uses mutual funds(7% interest).
        NFL person uses savings account(1% interest).
        """
        if self.is_financially_literate:
            self.savings *= (1 + SAVINGS_INTEREST_FL)
        else:
            self.savings *= (1 + SAVINGS_INTEREST_NFL)
            
    def calculate_debt_balance_after_year(self):
        """
        Calculate the amount of debt after one year of payments.
        FL pays minimum + 15 extra.
        NFL pays minimum + 1 extra.
        Returns: float: Total debt payment made during the year
        """
        total_payment = 0
        
        for _ in range(12):
            if self.debt <= 0:
                break
                
            min_payment = self.debt * DEBT_MIN_PAYMENT_PERCENT
            
            if self.is_financially_literate:
                payment = min_payment + FL_ADDITIONAL_DEBT_PAYMENT
            else:
                payment = min_payment + NFL_ADDITIONAL_DEBT_PAYMENT
      
            if payment > self.debt:
                payment = self.debt
                
            self.debt -= payment
            self.checking -= payment
            total_payment += payment
            
        if self.debt > 0:
            self.debt *= (1 + DEBT_INTEREST)
            
        return total_payment
    
    def subtract_rent_payment_from_checking(self):
        """
        Subtract rent payments from checking account for one year.
        """
        yearly_rent = MONTHLY_RENT * 12
        self.checking -= yearly_rent
        
    def can_afford_down_payment(self):
        """
        Check if the person can afford a down payment on a house.
        
        Returns: bool: True if the person can afford the down payment
        """
        if self.is_financially_literate:
            return self.checking >= HOUSE_COST * FL_DOWN_PAYMENT_PERCENT
        else:
            return self.checking >= HOUSE_COST * NFL_DOWN_PAYMENT_PERCENT
        
    def buy_house(self):
        """
        Buy a house by making a down payment and setting up a loan.
        """
        if self.is_financially_literate:
            down_payment = HOUSE_COST * FL_DOWN_PAYMENT_PERCENT
        else:
            down_payment = HOUSE_COST * NFL_DOWN_PAYMENT_PERCENT
            
        self.checking -= down_payment
        self.loan = HOUSE_COST - down_payment
        self.has_house = True
        
    def subtract_mortgage_payment_from_checking(self):
        """
        Calculate and subtract mortgage payments from checking account for one year.
        """
        if not self.has_house or self.loan <= 0:
            return
        n = MORTGAGE_YEARS * 12  
        if self.is_financially_literate:
            i = FL_MORTGAGE_INTEREST / 12
        else:
            i = NFL_MORTGAGE_INTEREST / 12

        discount_factor = ((1 + i) ** n - 1) / (i * (1 + i) ** n)
        monthly_payment = self.loan / discount_factor
        for _ in range(12):
            if self.loan <= 0:
                break
                
            interest_payment = self.loan * i
            principal_payment = monthly_payment - interest_payment
            if principal_payment > self.loan:
                principal_payment = self.loan
                monthly_payment = principal_payment + interest_payment   
            self.loan -= principal_payment
            self.checking -= monthly_payment
            
    def calculate_wealth(self):
        """
        Calculate the total wealth of the person.
        
        Returns: int: Total wealth (savings + checking - debt - loan)
        """
        wealth = self.savings + self.checking - self.debt - self.loan
        return round(wealth)
        
    def __str__(self):
        """
        Return a string representation of the Person.
        
        Returns: str: String representation
        """
        status = "Financially Literate" if self.is_financially_literate else "Not Financially Literate"
        return (f"{status} Person:\n"
                f"  Savings: ${self.savings:.2f}\n"
                f"  Checking: ${self.checking:.2f}\n"
                f"  Debt: ${self.debt:.2f}\n"
                f"  Loan: ${self.loan:.2f}\n"
                f"  Has House: {self.has_house}\n"
                f"  Total Wealth: ${self.calculate_wealth()}")


class Simulation:
    """
    A class to simulate the financial status of a person over 40 years.
    """
    
    def __init__(self, person):
        """
        Initialize a Simulation with a Person.
        Arguments: person (Person): The person to simulate
        """
        self.person = person
        self.years_in_debt = 0
        self.years_rented = 0
        self.total_debt_paid = 0
        
    def simulate(self, years=40):
        """
        Run the financial simulation for the specified number of years.
        Arguments: years (int): Number of years to simulate  
        Returns: list: Wealth at each year (including initial)
        """
        wealth_history = [self.person.calculate_wealth()]  # Initial wealth
        
        for year in range(1, years + 1):
            savings_contribution = ANNUAL_CONTRIBUTION * SAVINGS_PERCENT / TOTAL_PERCENT_AVAILABLE
            checking_contribution = ANNUAL_CONTRIBUTION * CHECKING_PERCENT / TOTAL_PERCENT_AVAILABLE
            
            self.person.savings += savings_contribution
            self.person.checking += checking_contribution
            self.person.calculate_savings_balance_after_year()
            debt_payment = self.person.calculate_debt_balance_after_year()
            self.total_debt_paid += debt_payment
            if self.person.debt > 0 or self.person.loan > 0:
                self.years_in_debt += 1
            if not self.person.has_house:
                self.years_rented += 1
                self.person.subtract_rent_payment_from_checking()
                if self.person.can_afford_down_payment():
                    self.person.buy_house()
            else:
                self.person.subtract_mortgage_payment_from_checking()
            wealth_history.append(self.person.calculate_wealth())       
        return wealth_history
        
    def __str__(self):
        """
        Return a string representation of the Simulation results.
        Returns: str: String representation
        """
        status = "Financially Literate" if self.person.is_financially_literate else "Not Financially Literate"
        return (f"Simulation Results for {status} Person:\n"
                f"  Years in Debt: {self.years_in_debt}\n"
                f"  Years Rented: {self.years_rented}\n"
                f"  Total Debt Paid: ${self.total_debt_paid:.2f}\n"
                f"  Final Wealth: ${self.person.calculate_wealth()}")


def run_tests():
    """
    Run tests for all methods of the Person and Simulation classes.
    """
    fl_person = Person(True)
    assert fl_person.is_financially_literate == True, "FL person should be financially literate"
    assert fl_person.savings == INITIAL_SAVINGS, "Initial savings should be $5000"
    assert fl_person.debt == INITIAL_DEBT, "Initial debt should be $30100"
    
    nfl_person = Person(False)
    assert nfl_person.is_financially_literate == False, "NFL person should not be financially literate"
    assert nfl_person.checking == 0, "Initial checking should be $0"
    assert nfl_person.has_house == False, "Should not have a house initially"

    test_fl = Person(True)
    test_fl.savings = 10000
    test_fl.calculate_savings_balance_after_year()
    assert round(test_fl.savings, 2) == round(10000 * 1.07, 2), "FL savings should grow at 7%"
    
    test_nfl = Person(False)
    test_nfl.savings = 10000
    test_nfl.calculate_savings_balance_after_year()
    assert round(test_nfl.savings, 2) == round(10000 * 1.01, 2), "NFL savings should grow at 1%"
    
    test_empty = Person(True)
    test_empty.savings = 0
    test_empty.calculate_savings_balance_after_year()
    assert test_empty.savings == 0, "Zero savings should remain zero"
 
    test_fl = Person(True)
    test_fl.debt = 1000
    test_fl.checking = 5000
    payment = test_fl.calculate_debt_balance_after_year()
    assert test_fl.debt < 1000, "Debt should decrease after payments"
    assert payment > 0, "Total payment should be positive"
    assert test_fl.checking < 5000, "Checking should decrease after debt payments"
    
    test_nfl = Person(False)
    test_nfl.debt = 1000
    test_nfl.checking = 5000
    nfl_payment = test_nfl.calculate_debt_balance_after_year()
    assert test_nfl.debt < 1000, "NFL debt should decrease after payments"
    assert payment > nfl_payment, "FL should pay more than NFL"
    
    test_zero_debt = Person(True)
    test_zero_debt.debt = 0
    test_zero_debt.checking = 5000
    zero_payment = test_zero_debt.calculate_debt_balance_after_year()
    assert zero_payment == 0, "Zero debt should result in zero payment"
    assert test_zero_debt.checking == 5000, "Checking should not change with zero debt"

    test_rent = Person(True)
    test_rent.checking = 20000
    test_rent.subtract_rent_payment_from_checking()
    assert test_rent.checking == 20000 - (MONTHLY_RENT * 12), "Rent should be subtracted from checking"
    
    test_rent_zero = Person(False)
    test_rent_zero.checking = 0
    test_rent_zero.subtract_rent_payment_from_checking()
    assert test_rent_zero.checking == -(MONTHLY_RENT * 12), "Rent should still be subtracted even if checking is zero"
    
    test_rent_negative = Person(True)
    test_rent_negative.checking = -5000
    test_rent_negative.subtract_rent_payment_from_checking()
    assert test_rent_negative.checking == -5000 - (MONTHLY_RENT * 12), "Rent should be subtracted even from negative checking"

    test_can_afford_fl = Person(True)
    test_can_afford_fl.checking = HOUSE_COST * FL_DOWN_PAYMENT_PERCENT
    assert test_can_afford_fl.can_afford_down_payment() == True, "FL should afford down payment"
    
    test_cannot_afford_fl = Person(True)
    test_cannot_afford_fl.checking = HOUSE_COST * FL_DOWN_PAYMENT_PERCENT - 1
    assert test_cannot_afford_fl.can_afford_down_payment() == False, "FL should not afford down payment if short by $1"
    
    test_can_afford_nfl = Person(False)
    test_can_afford_nfl.checking = HOUSE_COST * NFL_DOWN_PAYMENT_PERCENT
    assert test_can_afford_nfl.can_afford_down_payment() == True, "NFL should afford down payment"

    test_buy_fl = Person(True)
    test_buy_fl.checking = 50000
    test_buy_fl.buy_house()
    assert test_buy_fl.has_house == True, "FL should have a house after buying"
    assert test_buy_fl.checking == 50000 - (HOUSE_COST * FL_DOWN_PAYMENT_PERCENT), "Down payment should be subtracted"
    assert test_buy_fl.loan == HOUSE_COST - (HOUSE_COST * FL_DOWN_PAYMENT_PERCENT), "Loan should be house cost minus down payment"
    
    test_buy_nfl = Person(False)
    test_buy_nfl.checking = 50000
    test_buy_nfl.buy_house()
    assert test_buy_nfl.has_house == True, "NFL should have a house after buying"
    assert test_buy_nfl.checking == 50000 - (HOUSE_COST * NFL_DOWN_PAYMENT_PERCENT), "Down payment should be subtracted"
    assert test_buy_nfl.loan == HOUSE_COST - (HOUSE_COST * NFL_DOWN_PAYMENT_PERCENT), "Loan should be house cost minus down payment"
    
    test_buy_exact = Person(True)
    test_buy_exact.checking = HOUSE_COST * FL_DOWN_PAYMENT_PERCENT
    test_buy_exact.buy_house()
    assert test_buy_exact.checking == 0, "Checking should be zero if exact down payment amount"

    test_mortgage_fl = Person(True)
    test_mortgage_fl.has_house = True
    test_mortgage_fl.loan = 10000
    test_mortgage_fl.checking = 5000
    test_mortgage_fl.subtract_mortgage_payment_from_checking()
    assert test_mortgage_fl.loan < 10000, "Loan should decrease after payments"
    assert test_mortgage_fl.checking < 5000, "Checking should decrease after mortgage payments"
    
    test_mortgage_nfl = Person(False)
    test_mortgage_nfl.has_house = True
    test_mortgage_nfl.loan = 10000
    test_mortgage_nfl.checking = 5000
    test_mortgage_nfl.subtract_mortgage_payment_from_checking()
    assert test_mortgage_nfl.loan < 10000, "NFL loan should decrease after payments"
    
    test_no_house = Person(True)
    test_no_house.has_house = False
    test_no_house.loan = 10000
    test_no_house.checking = 5000
    test_no_house.subtract_mortgage_payment_from_checking()
    assert test_no_house.loan == 10000, "Loan should not change without a house"
    assert test_no_house.checking == 5000, "Checking should not change without a house"
    
    test_wealth = Person(True)
    test_wealth.savings = 10000
    test_wealth.checking = 5000
    test_wealth.debt = 3000
    test_wealth.loan = 2000
    assert test_wealth.calculate_wealth() == 10000 + 5000 - 3000 - 2000, "Wealth calculation should be correct"
    
    test_wealth_negative = Person(False)
    test_wealth_negative.savings = 1000
    test_wealth_negative.checking = 2000
    test_wealth_negative.debt = 5000
    test_wealth_negative.loan = 10000
    assert test_wealth_negative.calculate_wealth() == 1000 + 2000 - 5000 - 10000, "Negative wealth calculation should be correct"
    
    test_wealth_zero = Person(True)
    test_wealth_zero.savings = 0
    test_wealth_zero.checking = 0
    test_wealth_zero.debt = 0
    test_wealth_zero.loan = 0
    assert test_wealth_zero.calculate_wealth() == 0, "Zero wealth calculation should be correct"
    
    test_sim_fl = Simulation(Person(True))
    assert test_sim_fl.person.is_financially_literate == True, "Simulation should have FL person"
    assert test_sim_fl.years_in_debt == 0, "Initial years in debt should be 0"
    assert test_sim_fl.years_rented == 0, "Initial years rented should be 0"
    
    test_sim_nfl = Simulation(Person(False))
    assert test_sim_nfl.person.is_financially_literate == False, "Simulation should have NFL person"
    assert test_sim_nfl.total_debt_paid == 0, "Initial total debt paid should be 0"
    
    test_sim_one_year = Simulation(Person(True))
    one_year_history = test_sim_one_year.simulate(1)
    assert len(one_year_history) == 2, "History should have initial + 1 year values"
    assert one_year_history[0] == INITIAL_WEALTH, "Initial wealth should match expected value"
    
    test_sim_zero_years = Simulation(Person(False))
    zero_year_history = test_sim_zero_years.simulate(0)
    assert len(zero_year_history) == 1, "History should have only initial value"
    
    test_sim_multiple_years = Simulation(Person(True))
    test_years = 5
    multi_year_history = test_sim_multiple_years.simulate(test_years)
    assert len(multi_year_history) == test_years + 1, "History should have initial + 5 year values"
    
    print("All tests passed!")


def main():
    """
    Main function to run the financial literacy simulation.
    """
    print("Financial Literacy Simulation")
    print("-" * 30)

    fl_person = Person(True)
    nfl_person = Person(False)

    fl_simulation = Simulation(fl_person)
    nfl_simulation = Simulation(nfl_person)

    fl_wealth_history = fl_simulation.simulate()
    nfl_wealth_history = nfl_simulation.simulate()

    print("\nResults after 40 years:")
    print(fl_simulation)
    print()
    print(nfl_simulation)

    debt_difference = nfl_simulation.total_debt_paid - fl_simulation.total_debt_paid
    years_in_debt_difference = nfl_simulation.years_in_debt - fl_simulation.years_in_debt
    wealth_difference = fl_person.calculate_wealth() - nfl_person.calculate_wealth()
    
    print("\nComparison:")
    print(f"NFL paid ${debt_difference:.2f} more in debt than FL")
    print(f"NFL spent {years_in_debt_difference} more years in debt than FL")
    print(f"FL has ${wealth_difference:.2f} more in wealth than NFL after 40 years")

    try:
        import matplotlib.pyplot as plt
        
        years = list(range(41))
        
        plt.figure(figsize=(12, 6))
        plt.plot(years, fl_wealth_history, label="Financially Literate", color="green")
        plt.plot(years, nfl_wealth_history, label="Not Financially Literate", color="red")
        plt.xlabel("Years")
        plt.ylabel("Wealth ($)")
        plt.title("Wealth Comparison Over 40 Years")
        plt.grid(True)
        plt.legend()
        plt.savefig("wealth_comparison.png")
        print("\nWealth comparison graph saved to 'wealth_comparison.png'")
        
    except ImportError:
        print("\nMatplotlib not installed. Skipping visualization.")


if __name__ == "__main__":
    run_tests()

    main()
