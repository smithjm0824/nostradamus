# Lasso and Shepherd
The first task is data collection. I opted to retrieve historical price info for the stocks 
currently listed in the S&P 500 index. This process is all handled by *lasso.py*.


### Pulling Historical Stock Price (OHLCV)
First, you'll need to create a free account with Tiingo. Tiingo has an excellent API for retrieving 
historical Open-High-Low-Close-Volume data for a huge number of stocks. While there are many other 
services out there, I ended up choosing Tiingo because I wanted to utilize async-await logic, and Tiingo 
offers a very simple-to-use REST API.

You can [learn more and sign up for Tiingo on their website.](https://api.tiingo.com/)

Similar to the other services used in this application, you will need to add the api-key obtained to your 
<i>config.ini</i> file with the following naming convention:

> [TIINGO] <br/>
api_key = <b>YOUR_TIINGO_API_KEY</b> <br/>


### PostgresSQL
Rather than gather this historical data in-memory every time we run the application, it makes sense to persist
the data to a database. I ended up choosing Postgres for this task, and while it'll be easier for you to do the same,
you are free to implement the database of your choice.

For the Postgres implementation, I used the [official Docker image for Postgres](https://hub.docker.com/_/postgres). 

### Stock Technical Indicators:
For the task of calculating technical indicators, I turned to a library created by Rinat Maksutov for this very purpose.

<code>
git clone https://github.com/voice32/stock_market_indicators
</code>

