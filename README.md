# Stock Price Tracker & Analysis Tool

A beginner-friendly Python project that downloads one year of daily stock data,
calculates basic price and return statistics, prints a summary report, and saves
a line chart. The default ticker is Apple (`AAPL`), but the script also accepts a
ticker as a command-line argument.

## How to Run

### 1. Install the required libraries

From this project folder, run:

```bash
python3 -m pip install yfinance pandas numpy matplotlib
```

If your computer uses `python` rather than `python3`, use `python -m pip` and
`python stock_tracker.py` instead.

### 2. Run the analysis

Use the default Apple ticker:

```bash
python3 stock_tracker.py
```

Or provide another ticker, such as Microsoft or Tesla:

```bash
python3 stock_tracker.py MSFT
python3 stock_tracker.py TSLA
```

The script needs an internet connection because `yfinance` retrieves current
historical data from Yahoo Finance. It prints a report in the terminal and
saves a chart such as `AAPL_stock_analysis.png` in this folder.

## Complete Script

The complete, copy-paste-ready script is [stock_tracker.py](stock_tracker.py).
It contains thorough comments, input validation, a formatted report, and the
chart code. Open that file to view or copy the full implementation.

## Key Financial Concepts

### Closing price

The closing price is the stock's last traded price for a trading day. We use it
as one consistent daily value for the analysis.

### Daily return

A daily return is the percentage change from one closing price to the next:

```text
daily return = (today's close - yesterday's close) / yesterday's close
```

For example, moving from $100 to $103 gives a 3% return. Returns are useful
because percentages make price changes easier to compare across stocks with
different prices.

### Average daily return

This is the mean of all daily returns in the period. A positive result means the
average daily movement was upward, but it does not guarantee that the stock will
rise in the future.

### Volatility

Volatility describes how much returns vary. This project uses the standard
deviation of daily returns as a simple volatility measure. A larger value means
the stock's daily movements were less consistent and generally involved more
risk. Volatility measures movement, not whether the price moved up or down.

### Highest and lowest closing prices

These are the largest and smallest daily closing prices in the one-year sample.
They describe the historical range, not a prediction or a guaranteed trading
price.

## Expected Output Example

The dates and values change whenever the script downloads new data. A typical
report looks like this:

```text
====================================================
STOCK PRICE ANALYSIS: AAPL
====================================================
Period: 2025-09-05 to 2026-09-04
Trading days: 251
----------------------------------------------------
Average closing price: $215.42
Volatility (daily return std. dev.): 1.48%
Highest closing price: $241.10
Lowest closing price: $169.21
Average daily return: 0.08%
Daily returns calculated: 250
====================================================

Chart saved to: AAPL_stock_analysis.png
```

These values are illustrative only and are not investment advice.

## Next Steps

- Add a histogram of daily returns with `plt.hist()`.
- Let the user enter a start date, end date, and ticker interactively.
- Compare several stocks on one chart or compare their returns.
- Add a benchmark such as the S&P 500 (`^GSPC`).
- Calculate cumulative return, maximum drawdown, and a moving average.
- Save the downloaded data and metrics to CSV for later analysis.
- Add tests for the calculations using a small, fixed pandas Series.
- Build a notebook or dashboard so the results are easier to explore.

## Important Reminder

Historical performance does not predict future results. This project is for
learning data analysis, not for making investment decisions.