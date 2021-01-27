import pandas as pd
import requests
from lxml import html
import time

table_MN = pd.read_html(
    'https://sheet2site-staging.herokuapp.com/api/v3/index.php?key=1ataJJQSe-DMwHk5QY7vgjWB-YkXy_aFNEBnO24Juvm8&g=1&e=1&e=1')

df = table_MN[0]
x = df.head()

# Create a new dataframe
data = pd.DataFrame()

# Create a new column called 'spac_tickers' set equal to df['SPAC NAME / Ticker']
data['spac_tickers'] = df['SPAC Name / Ticker']

# Grab the last 6 chars
data = data['spac_tickers'].str[-6:]

# Clean the strings for each row
data = data.str.replace('(', '')
data = data.str.replace(')', '')
data = data.str.replace(' ', '')

# Write the data to a nice csv
data.to_csv('data')

tickers = list(data)
urls = []

for ticker in tickers:
    base_url_part1 = "https://sec.report/Ticker/"
    base_url_part2 = ticker.lower()
    fullurl = base_url_part1 + base_url_part2
    urls.append(fullurl)

headers = {
  "Referer": "https://sec.report/",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

# Get Response, build tree, scrape for CIK
endpoints = ['https://sec.report/Ticker/paac', 'https://sec.report/Ticker/cciv', 'https://sec.report/Ticker/mosc']

# # Example run using 3 tickers
for endpoint in urls:
    raw = str(requests.get(endpoint, headers=headers).content.decode("latin1"))
    tree = html.fromstring(raw)
    cik = tree.xpath('/html/body/div/div/h2[1]/text()')
    ticker = tree.xpath('/html/body/div/div/h2[2]/text()')
    ticker = ticker[0].split(' ')[1]
    cik = cik[0].split(' ')[2]
    print(f"Ticker: {ticker}, cik: {cik}")
    time.sleep(2)