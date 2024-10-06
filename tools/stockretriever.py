import yfinance as yf
from datetime import datetime, timedelta


def get_current_info(symbols):
    """
    Fetch current information for given stock symbols.

    :param symbols: List of stock symbols
    :return: List of dictionaries containing current stock information
    """
    results = []
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            results.append({
                'symbol': symbol,
                'longName': info.get('longName', 'N/A'),
                'currentPrice': info.get('currentPrice', 'N/A'),
                'marketCap': info.get('marketCap', 'N/A'),
                'peRatio': info.get('trailingPE', 'N/A'),
                'volume': info.get('volume', 'N/A'),
                'averageVolume': info.get('averageVolume', 'N/A'),
                'dividendYield': info.get('dividendYield', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A')
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return results


def get_historical_info(symbol, start_date, end_date):
    """
    Fetch historical stock data for a given symbol and date range.

    :param symbol: Stock symbol
    :param start_date: Start date for historical data
    :param end_date: End date for historical data
    :return: List of dictionaries containing historical stock data
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=end_date)

        return [{
            'Date': index.strftime('%Y-%m-%d'),
            'Open': row['Open'],
            'High': row['High'],
            'Low': row['Low'],
            'Close': row['Close'],
            'Volume': row['Volume']
        } for index, row in hist.iterrows()]
    except Exception as e:
        print(f"Error fetching historical data for {symbol}: {e}")
        return []


if __name__ == "__main__":
    # Test the functions
    symbols = ['AAPL', 'GOOGL']
    print("Current Info:")
    print(get_current_info(symbols))

    print("\nHistorical Info for AAPL (last 7 days):")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=120)
    print(get_historical_info('AAPL', start_date, end_date))