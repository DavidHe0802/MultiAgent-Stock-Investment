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

## Component Descriptions

### Agents

1. **CEOAgent** (`ceo.py`)
   - Reviews portfolio performance
   - Assigns tasks to other agents
   - Evaluates investment recommendations

2. **WarrenBuffetAgent** (`warren_buffet.py`)
   - Raises market questions based on CEO's tasks
   - Decides which stocks to investigate further
   - Makes final investment decisions based on analysis

3. **MarketResearchAgent** (`MarketResearchAgent.py`)
   - Fetches market information based on Buffet's questions
   - Retrieves stock price history data

4. **AnalystAgent** (`analyst.py`)
   - Analyzes stock price trends
   - Provides analysis reports

5. **SecretaryAgent** (`Secretary.py`)
   - Generates meeting notes summarizing the investment process

6. **OperatorAgent** (`operator.py`)
   - Parses and executes approved investment recommendations

### Tools

- **stock_scraper.py**: Provides functionality to scrape stock data from financial websites

### Database

1. **build_database.py**
   - Creates and populates the SQLite database with stock data

2. **db_manager.py**
   - Manages database operations (querying, updating)

3. **nasdaq_symbols.txt**
   - Contains a list of NASDAQ stock symbols

### Models

- **portfolio.py**: Represents the investment portfolio
  - Tracks cash balance and stock holdings
  - Provides methods for buying and selling stocks
  - Generates performance reports

### Utils

1. **data_processing.py**: Contains utility functions for processing financial data

2. **visualization.py**: Provides functions for visualizing stock data and portfolio performance

### Office

- **office_simulation.py**: Orchestrates the entire investment simulation
  - Initializes all agents
  - Runs the daily investment cycle
  - Generates daily reports

## Workflow

1. The CEO reviews the portfolio performance and assigns tasks.
2. Warren Buffet raises market questions based on these tasks.
3. The Market Research Agent fetches relevant market information.
4. Buffet reviews this information and decides which stock trends to investigate.
5. The Market Research Agent retrieves detailed stock trend data.
6. The Analyst analyzes this data and provides a report.
7. Buffet makes final investment decisions based on all available information.
8. The CEO evaluates these recommendations.
9. The Secretary generates meeting notes summarizing the process.
10. If approved, the Operator executes the investment decisions.
11. The process repeats until a decision is approved or a time limit is reached.
12. A daily report is generated, including all meeting notes and executed trades.

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

