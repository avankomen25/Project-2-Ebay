# eBay Scraper
 
## What it does
`ebay-dl.py` is a command line tool that scrapes eBay search results and saves the data as a JSON or CSV file. For a given search term, it downloads a default of 10 pages of results and extracts the following information for each item:
 
- **name** — the item's title
- **price** — the price in cents (integer)
- **status** — condition of the item (e.g. Brand New, Pre-owned)
- **shipping** — shipping cost in cents (0 if free)
- **free_returns** — whether the item has free returns (boolean)
- **items_sold** — number of items sold (integer)
 
## How to run it
 
You can also specify how many pages of results to scrape (default is 10) by adding `--num_pages='number'`:
 
```
python3 ebay-dl.py laptop --num_pages=5
```
 
Generate JSON files:
 
```
python3 ebay-dl.py laptop --num_pages=10
```
 
```
python3 ebay-dl.py hammer --num_pages=10
```
 
```
python3 ebay-dl.py 'stuffed animal' --num_pages=10
```
 
Generate CSV files by adding `--csv` :
 
```
python3 ebay-dl.py laptop --num_pages=10 --csv
```
 
```
python3 ebay-dl.py hammer --num_pages=10 --csv
```
 
```
python3 ebay-dl.py 'stuffed animal' --num_pages=10 --csv
```
 
## Course Project Link
[Course Project](https://github.com/mikeizbicki/cmc-csci040/tree/2026spring/project_02_webscraping)