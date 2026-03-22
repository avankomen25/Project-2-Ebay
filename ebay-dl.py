import argparse
import requests
from bs4 import BeautifulSoup
import random
import json



def parse_itemssold(text):
    '''
    Takes input as string and returns number of items sold as specified in the string
    
    >>> parse_itemssold('38 sold')
    38
    >>> parse_itemssold('14 watchers')
    0
    >>> parse_itemssold('Almost gone')
    0
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char 
    if 'sold' in text:
        return int(numbers)
    else:
        return 0

def parse_price(text):
    '''
    >>> parse_price('$52.95')
    5295
    >>> parse_price('$1,590.00')
    159000
    >>> parse_price('$54.99 to $79.99')
    5499
    '''
    numbers = ''
    for char in text:
        if char in '1234567890':
            numbers += char
    if '$' in text:
        return int(numbers[:-2]) * 100 + int(numbers[-2:])
    else:
        return None

def parse_shipping(text):
    '''
    >>> parse_shipping('Free delivery')
    0
    >>> parse_shipping('+$5.30 delivery')
    530
    >>> parse_shipping('Buy It Now')
    None
    '''
    if 'Free delivery' in text or 'Free international shipping' in text:
        return 0
    elif 'delivery' in text and '$' in text:
        numbers = ''
        for char in text:
            if char in '1234567890':
                numbers += char
        return int(numbers[:-2]) * 100 + int(numbers[-2:])
    else:
        return None

if __name__ == '__main__':

    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/137.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
    ]

    # gets command line arguments
    parser = argparse.ArgumentParser(description = 'Download information from ebay and convert to JSON.')
    parser.add_argument('search_term')
    parser.add_argument('--num_pages', default=10)
    parser.add_argument('--csv', action='store_true')
    args = parser.parse_args()
    print('args.search_term=', args.search_term) 

    # list of all items found on all ebay pages
    items = []

    # loop over ebay pages
    for page_number in range(1,int(args.num_pages) + 1):
        
        # builds url
        url = 'https://www.ebay.com/sch/i.html?_nkw=' 
        url += args.search_term 
        url += '&_sacat=0&_from=R40&_pgn='
        url += str(page_number)
        url += '&rt=nc'
        print('url=', url)

        random.shuffle(user_agent_list)
        user_agent = user_agent_list[0]

        headers = {
            "User-Agent": user_agent
        }

        # downloads  html
        r = requests.get(url, headers = headers)
        status = r.status_code
        print('status=', status)
        html = r.text
        #print('html=', html[:500])

        # processes html
        soup = BeautifulSoup(html, 'html.parser')
        
        

        tags_items = soup.select('.s-card') 
        #print('len(tags_items)=', len(tags_items))
        #print('html snippet=', r.text[:500])
        for tag_item in tags_items:
            # print('tag_item=', tag_item) 
            
            # extract names
            tags_name = tag_item.select('.s-card__title')
            name = None
            for tag in tags_name:
                name = tag.text

            if name:
                name = name.replace('Opens in a new window or tab', '').strip()

            if name == 'Shop on eBay':
                continue

            # print('attribute spans:', [tag.get_text(strip=True) for tag in tag_item.select('.s-card__attribute-row span')])

            # extract free returns
            freereturns = False
            tags_freereturns = tag_item.select('.s-card__attribute-row span')
            for tag in tags_freereturns:
                if 'Free returns' in tag.get_text():
                    freereturns = True
                
            items_sold = None
            tags_itemssold = tag_item.select('.s-card__attribute-row span')
            for tag in tags_itemssold:
                if 'sold' in tag.get_text(strip=True):
                    items_sold = parse_itemssold(tag.text)

            price = None
            tags_price = tag_item.select('.s-card__attribute-row span')
            for tag in tags_price:
                if '$' in tag.get_text(strip=True):
                    price = parse_price(tag.get_text(strip=True))
                    break


            status = None
            tags_status = tag_item.select('.s-card__subtitle span')
            for tag in tags_status:
                status = tag.get_text(strip=True)

            if status:
                status = status.replace('\u2013', '-')

            shipping = None
            tags_shipping = tag_item.select('.s-card__attribute-row span')
            for tag in tags_shipping:
                result = parse_shipping(tag.get_text(strip=True))
                if result is not None:
                    shipping = result

            # append per item
            item = {
                'name': name,
                'free_returns': freereturns,
                'items_sold': items_sold,
                'price': price,
                'status': status,
                'shipping': shipping
            }
            items.append(item)

        print('len(tags_items)=', len(tags_items))

    print('len(items)=', len(items))

    # for item in items:
        # print('item=', item)

    # makes json file or csv file
    if args.csv:
        import csv
        filename = args.search_term.replace(' ', '_') + '.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'price', 'status', 'shipping', 'free_returns', 'items_sold'])
            writer.writeheader()
            writer.writerows(items)
    else:
        filename = args.search_term.replace(' ', '_') + '.json'
        with open(filename, 'w', encoding='ascii') as f:
            f.write(json.dumps(items))