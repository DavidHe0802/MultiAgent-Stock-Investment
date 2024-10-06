import datetime
from decimal import Decimal
from typing import List, Dict
from tools.stockretriever import get_current_info


class Portfolio:
    def __init__(self, initial_cash: float = 100000.0):
        self.ledger: List[Dict] = []
        self.cash: Decimal = Decimal(str(initial_cash))
        self.holdings: Dict[str, Dict] = {}

    def _add_transaction(self, transaction_type: str, symbol: str, quantity: int, price: float, date: datetime.date):
        transaction = {
            'date': date,
            'type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'price': Decimal(str(price))
        }
        self.ledger.append(transaction)

        if transaction_type == 'buy':
            if symbol not in self.holdings:
                self.holdings[symbol] = {'quantity': 0, 'cost': Decimal('0')}
            self.holdings[symbol]['quantity'] += quantity
            self.holdings[symbol]['cost'] += Decimal(str(price)) * Decimal(str(quantity))
            self.cash -= Decimal(str(price)) * Decimal(str(quantity))
        elif transaction_type == 'sell':
            self.holdings[symbol]['quantity'] -= quantity
            self.cash += Decimal(str(price)) * Decimal(str(quantity))
            if self.holdings[symbol]['quantity'] == 0:
                del self.holdings[symbol]

    def buy_stock(self, symbol: str, quantity: int, price: float, date: datetime.date = None):
        if date is None:
            date = datetime.date.today()
        total_cost = Decimal(str(price)) * Decimal(str(quantity))
        if total_cost > self.cash:
            raise ValueError("Insufficient funds to complete the purchase.")
        self._add_transaction('buy', symbol, quantity, price, date)

    def sell_stock(self, symbol: str, quantity: int, price: float, date: datetime.date = None):
        if date is None:
            date = datetime.date.today()
        if symbol not in self.holdings or self.holdings[symbol]['quantity'] < quantity:
            raise ValueError("Insufficient stocks to complete the sale.")
        self._add_transaction('sell', symbol, quantity, price, date)

    def get_performance_report(self) -> str:
        current_date = datetime.date.today()
        current_info = get_current_info(list(self.holdings.keys()))
        current_prices = {info['symbol']: Decimal(str(info['currentPrice'])) for info in current_info}

        report = f"Performance Report as of {current_date}\n\n"
        report += f"Available Cash: ${self.cash:.2f}\n\n"
        report += "Stock Performance:\n"

        total_portfolio_value = self.cash
        for symbol, holding in self.holdings.items():
            quantity = holding['quantity']
            cost_basis = holding['cost'] / Decimal(str(quantity))
            current_price = current_prices[symbol]

            total_value = current_price * Decimal(str(quantity))
            total_portfolio_value += total_value

            return_rate = ((current_price - cost_basis) / cost_basis) * 100

            purchase_date = min(t['date'] for t in self.ledger if t['symbol'] == symbol and t['type'] == 'buy')
            days_held = (current_date - purchase_date).days

            report += f"  {symbol}:\n"
            report += f"    Quantity: {quantity}\n"
            report += f"    Cost Basis: ${cost_basis:.2f}\n"
            report += f"    Current Price: ${current_price:.2f}\n"
            report += f"    Total Value: ${total_value:.2f}\n"
            report += f"    Return Rate: {return_rate:.2f}%\n"
            report += f"    Days Held: {days_held}\n\n"

        total_return = ((total_portfolio_value - Decimal('100000')) / Decimal('100000')) * 100
        report += f"Total Portfolio Value: ${total_portfolio_value:.2f}\n"
        report += f"Total Portfolio Return: {total_return:.2f}%\n"

        # Save report to file
        filename = f"portfolio_report_{current_date}.txt"
        with open(filename, 'w') as f:
            f.write(report)

        return report

    def generate_ledger_report(self) -> str:
        """
        Generates a report of all transactions recorded in the ledger, showing details like date, type of transaction,
        symbol, quantity, price, and the remaining cash balance after each transaction.
        :return: A formatted report of the ledger as a string.
        """
        report = f"Ledger Report as of {datetime.date.today()}\n"
        report += "-" * 50 + "\n"
        report += f"{'Date':<12} {'Type':<10} {'Symbol':<8} {'Quantity':<10} {'Price':<10} {'Cash Balance':<15}\n"
        report += "-" * 50 + "\n"

        running_cash = Decimal(str(self.cash))  # Keep track of the running cash balance
        for transaction in self.ledger:
            date = transaction['date'].strftime('%Y-%m-%d')
            t_type = transaction['type']
            symbol = transaction['symbol']
            quantity = transaction['quantity']
            price = transaction['price']

            # Calculate running cash balance after each transaction
            if t_type == 'buy':
                running_cash += price * quantity
            elif t_type == 'sell':
                running_cash -= price * quantity

            report += f"{date:<12} {t_type:<10} {symbol:<8} {quantity:<10} ${price:<10.2f} ${running_cash:<15.2f}\n"

        report += "-" * 50 + "\n"

        # Save report to file
        current_date = datetime.date.today()
        filename = f"ledger_report_{current_date}.txt"
        with open(filename, 'w') as f:
            f.write(report)

        print(f"Ledger report saved as {filename}")
        return report


# Example usage:
if __name__ == "__main__":
    portfolio = Portfolio()

    # Buy some stocks
    portfolio.buy_stock("AAPL", 10, 150.0, datetime.date(2023, 1, 1))
    portfolio.buy_stock("GOOGL", 5, 2500.0, datetime.date(2023, 2, 1))

    # Sell some stocks
    portfolio.sell_stock("AAPL", 5, 160.0, datetime.date(2023, 3, 1))

    # Generate and print performance report
    print(portfolio.get_performance_report())