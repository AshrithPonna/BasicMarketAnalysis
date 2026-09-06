# Basic Market Analysis 

 Stock Price Tracker

## Installation
```bash
python3 -m pip install yfinance pandas numpy matplotlib
```

## Usage
```bash
python3 stock_tracker.py              # Analyze Apple (default)
python3 stock_tracker.py MSFT         # Analyze Microsoft
python3 stock_tracker.py TSLA         # Analyze Tesla

# Overview
This application takes information from Yahoo Finance and calculations a variety of metrics:
> Average Price (stock price over past year)
> Average Returns (averaging returns)
> Volatility Determinations (fluctuations calculated via std.dev)
> Statistics (
> Daily Gains/Losses (this includes averages)

These are all correlative to stocks; graphs (line) for historical distributions are created.

# Learning Technicalities
> Data manipulations in data frames with panda.
> How to manipulate data frame contents with functions.
> Utilizing matplotlib to create graphs representative of historical data.
> Understanding key financial metrics and their relevance.

# Skills
> Python 3
> yfinance ( stock data)
> pandas (data manipulation)
> numpy (calculations)
> matplotlib (visualization)

Tested and reviewed codebase.
