import sqlite3
import os
from datetime import datetime, timedelta

# Assuming the database is in the same directory as this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'stock_data.db')


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def get_stock_data(self, symbol, start_date, end_date):
        self.cursor.execute('''
            SELECT * FROM daily_data
            WHERE symbol = ? AND date BETWEEN ? AND ?
            ORDER BY date
        ''', (symbol, start_date, end_date))
        return self.cursor.fetchall()

    def get_all_symbols(self):
        self.cursor.execute('SELECT symbol FROM stocks')
        return [row[0] for row in self.cursor.fetchall()]

    def get_stock_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM stocks')
        return self.cursor.fetchone()[0]

    def get_data_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM daily_data')
        return self.cursor.fetchone()[0]

    def get_date_range(self):
        self.cursor.execute('SELECT MIN(date), MAX(date) FROM daily_data')
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()


def test_database():
    db = DatabaseManager()

    # Test 1: Check if we have stocks in the database
    stock_count = db.get_stock_count()
    print(f"Total number of stocks: {stock_count}")
    if stock_count == 0:
        print("Error: No stocks found in the database.")
        return

    # Test 2: Check if we have daily data
    data_count = db.get_data_count()
    print(f"Total number of daily data entries: {data_count}")
    if data_count == 0:
        print("Error: No daily data found in the database.")
        return

    # Test 3: Check the date range of our data
    min_date, max_date = db.get_date_range()
    print(f"Data range: from {min_date} to {max_date}")

    # Test 4: Get all symbols and check a few
    all_symbols = db.get_all_symbols()
    print(f"Total unique symbols: {len(all_symbols)}")
    print("First 5 symbols:", all_symbols[:5])

    # Test 5: Check data for a specific stock
    test_symbol = all_symbols[0]  # Let's check the first symbol
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    stock_data = db.get_stock_data(test_symbol, start_date, end_date)
    print(f"\nLast 30 days of data for {test_symbol}:")
    print(f"Number of entries: {len(stock_data)}")
    if stock_data:
        print("First entry:", stock_data[0])
        print("Last entry:", stock_data[-1])

    db.close()


if __name__ == "__main__":
    test_database()