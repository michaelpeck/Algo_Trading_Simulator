# Algo_Trading_Simulator
 Algorithmic trading webapp

*** SUMMARY ***

This is a Python-based webapp that allows users to simulate the performance of an automated trading bot on historical stock data.
The intentioned use-case is extremely low-cap stocks that experience high volatility over the short term but low volatility in the long term. This is in order to take advantage of high % increase over short periods with frequent transactions.
While the algorithm is oriented towards the behavior of small-cap stocks, the simulator should still work for more expensive stocks with lesser accuracy.
Users are able to create accounts that store simulation entry data, though that is not required in order to use the app.

The app collects:

Ticker - NYSE stock ticker
Period - duration of experiment back from time of execution
Interval - of data points (smaller intervals will lead to more accurate results but limit period length)
Account balance - money availible for trading)
Buy point - price at which to buy if funds are availible
Sell point - price at which to sell if stock is owned

The output is the ending balance of the account if respective trades were executed.

*** PREREQUISITES ***

In order to successfully utilize this platform, users must first research stocks in order to determine effective buy/sell points. Otherwise, it is likely that no trades will be completed.

In order to do this it is recommended that users use a stock scanners to scan for the following daily data:

Price - <$0.01
Volume - >5,000,000
Large difference between high and low

Once stocks are found, users should look at the 1mo, 3mo, 6mo, and 1y charts to ensure that they are steady over the long term.
Users can play around with those numbers and more scanning metrics to see what works best for them

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

*** LIMITATIONS ***

This is not an exact indicator of the preformance of a given stock, it is an estimate.
Data collected from yfinance does not indicated exact transaction data or bid/ask data, it provides a open, close, high, low, and volume data for a given interval. As a result, transactions are made based on an estimate of what shares would have been availible at each price during that interval. 
In order to create conservitive estimates, I indicated that 1/5th of the volume occured at the low and 1/2 occured at the high. 
This decision was made based on the nature of the specific goal of this bot, as volume at below-average prices is often  significantly lower than volume at average-above average prices.
