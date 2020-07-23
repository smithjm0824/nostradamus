import asyncio
import time
import psycopg2
import pandas as pd
import aiohttp
import configparser
from sqlalchemy import create_engine


config = configparser.ConfigParser()
config.read('../config.ini')

table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
symbols = table[0]['Symbol'].unique()

postgres_user = config['POSTGRES']['user']
postgres_pw = config['POSTGRES']['password']
host = config['POSTGRES']['host']
port = config['POSTGRES']['port']
postgres_db = config['POSTGRES']['database']
connection = psycopg2.connect(user=postgres_user, password=postgres_pw, host=host, port=port, database=postgres_db)
cursor = connection.cursor()
query = "select distinct(symbol) from historical_stock"
cursor.execute(query)
stored_symbols = cursor.fetchall()

stored_symbols = [x[0] for x in stored_symbols]
symbols = list(set(symbols) - set(stored_symbols))

base_url = "https://api.tiingo.com/tiingo/daily"
token = config['TIINGO']['api_key']
headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + token
        }
start_date = "2000-1-1"
end_date = "2020-7-20"

conn_string = config['POSTGRES']['connection_string']
engine = create_engine(conn_string, echo=False)

query = "select count(*) from historical_stock"
cursor.execute(query)
total_record_count = cursor.fetchone()[0]


async def fetch_data(index, symbol, session, url, header):
    print("Start " + str(index) + ": " + time.strftime('%X'))
    async with session.get(url, headers=header) as response:
        print("End " + str(index) + ": " + time.strftime('%X'))
        page = await response.json()
        df = pd.DataFrame.from_records(page, index=[i for i in range(len(page))])
        df['symbol'] = symbol
        global total_record_count
        total_record_count += df['symbol'].count()
        if 'open' not in df.columns:
            print(page)

        df[['symbol', 'open', 'close', 'low', 'high', 'volume', 'date']].to_sql('historical_stock', engine,
                                                                                if_exists="append", index=False)


async def main():
    session = aiohttp.ClientSession()

    tasks = []
    for index, symbol in enumerate(symbols):
        symbol = symbol.replace(".", "-")
        sub_url = "/{0}/prices?startDate={1}&endDate={2}&resampleFreq=daily".format(symbol, start_date, end_date)
        url = base_url + sub_url
        tasks.append(asyncio.ensure_future(fetch_data(index, symbol, session, url, headers)))

    await asyncio.gather(*tasks)

    await session.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

query = "select count(*) from historical_stock"
cursor.execute(query)
stored_counts = cursor.fetchone()[0]
assert(stored_counts == total_record_count)
