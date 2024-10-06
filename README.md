# Stock Investment Pipeline

This project simulates a stock investment pipeline, mimicking the decision-making process of a financial firm. It includes various agents (CEO, Warren Buffet, Market Research, Analyst, Secretary, and Operator) that interact to make investment decisions based on market data and analysis.


## Project Structure

```
stock_investment_pipeline/
│
├── agents/
│   [Contents as before]
│
├── tools/
│   [Contents as before]
│
├── database/
│   [Contents as before]
│
├── models/
│   [Contents as before]
│
├── utils/
│   [Contents as before]
│
├── office/
│   [Contents as before]
│
├── main.py
├── requirements.txt
└── README.md
```

## Setup and Execution

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/stock_investment_pipeline.git
   cd stock_investment_pipeline
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   ```
   python database/build_database.py
   ```
   This will create and populate the SQLite database with initial stock data.

5. **Run the simulation:**
   ```
   python main.py
   ```

   The `main.py` file is the entry point of the application. It initializes the `OfficeSimulation` class and starts the daily investment cycle.


## Dependencies

The main dependencies for this project include:
- yfinance: For fetching stock data
- pandas: For data manipulation and analysis
- numpy: For numerical operations
- matplotlib: For data visualization
- sqlite3: For database operations (included in Python standard library)
- openai: For AI-powered decision making and analysis

Refer to `requirements.txt` for the complete list of dependencies and their versions.

## Notes

- Ensure you have Python 3.7+ installed on your system.
- The simulation runs continuously by default. You may want to implement a more sophisticated scheduling system for production use.
- Make sure to keep your API keys and sensitive data secure. Consider using environment variables for API keys.

## Future Improvements

- Implement more sophisticated AI models for decision making
- Add real-time data streaming capabilities
- Develop a web interface for monitoring the simulation
- Implement backtesting functionality to evaluate strategy performance
- Enhance error handling and logging mechanisms
- Add unit tests and integration tests for better code reliability

