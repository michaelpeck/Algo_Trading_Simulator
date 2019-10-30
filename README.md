# Algo_Trading_Simulator

Sense bot is an algorithmic trade calculating Python webapp.

It is hosted at www.sensebot.co.

Languages: Python3, Jinja2, HTML5, CSS3, Javascript

Python packages: Pandas, Numpy, yFinance

Libraries: Bootstrap 4, DataTables, Chart.js

Hosting: Linode Linux Server

Database: MongoDB Atlas remote db

*** SUMMARY ***

This is a Python-based webapp that allows users to simulate the performance of an automated trading bot on historical stock data.
It was originally conceptualized as a means to test trading on low-cap stocks that experience high volatility over the short term but low volatility in the long term. This is in order to take advantage of high % increase over short periods with frequent transactions.
Users are able to create accounts to store calculation data or post to the forum, though that is not required in order to use the app.

The app collects the following inputs depending on the desired calculation:

Ticker - NYSE stock ticker
Period - duration of experiment back from time of execution
Interval - of data points (smaller intervals will lead to more accurate results but limit period length)
Length of average - # pf days on which to base a average for moving average and weighted moving average calculations
Account balance - money availible for trading)
Buy point - price at which to buy if funds are availible
Sell point - price at which to sell if stock is owned
Trade cost - broker fee per transaction

The output is the ending balance of the account if the requested trades were executed over the period.

*** PREREQUISITES ***

In order to successfully utilize this platform, users must first research stocks in order to determine effective buy/sell points. Otherwise, it is likely that no trades will be completed.

FOR SMALL CAP STOCKS:

It is recommended that users use a stock scanners to scan for the following daily data:

Price - <$0.01
Volume - >5,000,000
Large difference between high and low

Once stocks are found, users should look at the 1mo, 3mo, 6mo, and 1y charts to ensure that they are steady over the long term.
Users can play around with those numbers and more scanning metrics to see what works best for them.

*** COMPONENTS ***

The following languages are used in the app:

Python3
HTML5
CSS3
Javascript
Jinja2

Python packages:

Pandas - used for data processing
yfinance - used for data retrieval

Storage:

MongoDB Atlas - remote server database

Hosting: 

Linode - Remote Linux Server

*** LIMITATIONS ***

This is not an exact indicator of the preformance of a given stock, it is an estimate.
Data collected from yfinance does not indicated exact transaction data or bid/ask data, it provides a open, close, high, low, and volume data for a given interval. As a result, transactions are made based on an estimate of what shares would have been availible at each price during that interval. 
In order to create conservitive estimates, I indicated that 1/40th of given volume during a period is accessible.
