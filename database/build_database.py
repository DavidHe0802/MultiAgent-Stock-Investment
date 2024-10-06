import sqlite3
import os
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import stockretriever
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Assuming the script is in the same directory as the database folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'stock_data.db')
SYMBOLS_FILE_PATH = os.path.join(BASE_DIR, 'nasdaq_symbols.txt')


class DatabaseBuilder:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS stocks (
                symbol TEXT PRIMARY KEY,
                company_name TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_data (
                date TEXT,
                symbol TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (date, symbol),
                FOREIGN KEY (symbol) REFERENCES stocks(symbol)
            )
        ''')
        self.conn.commit()

    def get_nasdaq_symbols(self):
        with open(SYMBOLS_FILE_PATH, 'r') as file:
            return [line.strip() for line in file if line.strip()]

    def populate_database(self):
        symbols = self.get_nasdaq_symbols()
        total_symbols = len(symbols)

        BATCH_SIZE = 100
        for index, symbol in enumerate(symbols, 1):
            try:
                logging.info(f"Processing {symbol} ({index}/{total_symbols})")

                # Fetch current info to get company name
                try:
                    current_info = stockretriever.get_current_info([symbol])[0]
                    company_name = current_info.get('longName', 'Unknown')
                except (json.JSONDecodeError, IndexError) as e:
                    logging.error(f"Error processing {symbol}: {str(e)}. Skipping this symbol.")
                    continue
                except Exception as e:
                    logging.error(f"Unexpected error processing {symbol}: {str(e)}. Skipping this symbol.")
                    continue

                # Insert or update stock info
                self.cursor.execute('INSERT OR REPLACE INTO stocks VALUES (?, ?)',
                                    (symbol, company_name))

                # Fetch historical data (last 5 years)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=365 * 5)
                try:
                    historical_data = stockretriever.get_historical_info(symbol, start_date, end_date)
                except json.JSONDecodeError:
                    logging.error(f"Invalid JSON response for historical data of {symbol}. Skipping historical data.")
                    continue

                if not historical_data:
                    logging.error(f"No historical data available for {symbol}. Skipping historical data.")
                    continue

                # Insert historical data
                self.cursor.executemany('''
                    INSERT OR REPLACE INTO daily_data VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', [(data['Date'], symbol, data['Open'], data['High'], data['Low'], data['Close'], data['Volume'])
                      for data in historical_data])

                # Commit after each stock to save progress
                if index % BATCH_SIZE == 0:
                    self.conn.commit()
                    logging.info(f"Committed batch of {BATCH_SIZE} symbols")

            except Exception as e:
                logging.error(f"Unexpected error processing {symbol}: {e}")
                continue

        logging.info("Database population completed.")

    def update_database(self):
        symbols = self.get_nasdaq_symbols()
        total_symbols = len(symbols)

        for index, symbol in enumerate(symbols, 1):
            try:
                logging.info(f"Updating {symbol} ({index}/{total_symbols})")

                # Get the most recent date for this symbol
                self.cursor.execute('SELECT MAX(date) FROM daily_data WHERE symbol = ?', (symbol,))
                last_date = self.cursor.fetchone()[0]

                if last_date:
                    start_date = datetime.strptime(last_date, '%Y-%m-%d') + timedelta(days=1)
                    end_date = datetime.now()

                    if start_date < end_date:
                        new_data = stockretriever.get_historical_info(symbol, start_date, end_date)

                        self.cursor.executemany('''
                            INSERT OR REPLACE INTO daily_data VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', [(data['Date'], symbol, data['Open'], data['High'], data['Low'], data['Close'],
                               data['Volume'])
                              for data in new_data])

                        self.conn.commit()
                else:
                    logging.info(f"No existing data for {symbol}. Skipping update.")

            except Exception as e:
                logging.error(f"Error updating {symbol}: {e}")

        logging.info("Database update completed.")

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db_builder = DatabaseBuilder()
    db_builder.create_tables()
    db_builder.populate_database()
    db_builder.update_database()
    db_builder.close()