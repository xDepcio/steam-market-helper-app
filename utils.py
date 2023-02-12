from seleniumwire.utils import decode
import json


def scrape_reqs_for_graphs(driver, item_id):
    for request in driver.requests:
        if request.response:
            body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))

                            #   f"https://steamcommunity.com/market/itemordershistogram?country=PL&language=polish&currency=6&item_nameid=176293907&two_factor=0"
            if request.url == f"https://steamcommunity.com/market/itemordershistogram?country=PL&language=polish&currency=6&item_nameid={item_id}&two_factor=0":
                str_body = str(body)
                str_body = str_body[1:]

                str_charts = str_body.split('buy_order_graph')[1]
                buy_part, sell_part = str_charts.split('sell_order_graph')

                entires_buy = buy_part.split('],[')
                entires_buy_foramtted = []
                accum = 0
                for entry in entires_buy:
                    price, amount = entry.split(',')[:2]
                    price = price.strip('":[')
                    price = float(price)
                    amount = int(amount)
                    amount = amount - accum
                    accum += amount

                    entires_buy_foramtted.append([price, amount])

                entires_sell = sell_part.split('],[')
                entires_sell_foramtted = []
                accum = 0
                for entry in entires_sell:
                    price, amount = entry.split(',')[:2]
                    price = price.strip('":[')
                    price = float(price)
                    amount = int(amount)
                    amount = amount - accum
                    accum += amount

                    entires_sell_foramtted.append([price, amount])

                return entires_sell_foramtted, entires_buy_foramtted


def scrape_reqs_for_inv_cards(driver):
    for request in driver.requests:
        if request.response:
            body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))

            if request.url == f"https://steamcommunity.com/inventory/76561198462126877/753/6?l=polish&count=75":
                str_body = str(body)
                str_body = str_body[1:]

                str_body = str_body.split('],"descriptions":')[1]
                str_body = str_body.split(',"more_items":')[0]

                hashes = str_body.split('type":"')[1:]
                data = [hash_.split('","market_fee_app')[0] for hash_ in hashes]
                new_data = [entry for entry in data if 'Karta kolekcjonerska' in entry]

                hashes_names = [ele.split('hash_name":"')[1] for ele in new_data]

                urls = [
                    f"https://steamcommunity.com/market/listings/753/{ele}" for ele in hashes_names
                ]

                print(hashes_names)
                print(urls)
                with open('data.txt', 'w') as fh:
                    fh.write(str_body)
                return urls


def load_urls(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['links']


def get_sell_price(sell_arr, ignore_prev_count):
    total_prev = 0
    for price, amount in sell_arr:
        total_prev += amount
        if total_prev >= ignore_prev_count:
            return price
