from office.office_simulation import OfficeSimulation
from models.portfolio import Portfolio
import time

if __name__ == "__main__":
    portfolio = Portfolio()
    office = OfficeSimulation(portfolio)

    while True:
        try:
            daily_report = office.run_daily_cycle()
            print(daily_report)
            # Wait for next day (you might want to implement a proper scheduling mechanism)
            time.sleep(86400)  # Sleep for 24 hours
        except Exception as e:
            print(f"An error occurred: {e}")
            # Implement error handling and reporting here