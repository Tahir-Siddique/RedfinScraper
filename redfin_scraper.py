import asyncio
import csv
import datetime
import json
import os
import re
from sys import platform
import selectors
import threading
import time
import aiohttp
from bs4 import BeautifulSoup
from dateutil import parser
import pandas

import pytz
import requests

from utils.constants import EXCLUDED_PROP_TYPES, START_DATE


class RedfinScrapper:
    def __init__(self) -> None:
        # platform specific asyncio policy
        if platform == "darwin":
            # OS X
            selector = selectors.SelectSelector()
            loop = asyncio.SelectorEventLoop(selector)
            asyncio.set_event_loop(loop)
        elif platform == "win32":
            # Windows...
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        
    def convert_utc_to_tz_date(self, date, tz):
        if tz is None:
            return '-'
        _tz = pytz.timezone(tz)
        return _tz.normalize(date.astimezone(_tz))



    def get_sale_history(self, item):
        if "get_owner" in item:
            return item["get_owner"](item)
        item["owner_name"] = "Not found"
        item.pop("get_owner")
        return item
        
        # try:
        #     headers = {'user-agent': 'Redfin Android 458.0.1'}
        #     url = 'https://www.redfin.com/stingray/mobile/api/v2/home/details/belowTheFold?propertyId=%s&listingId=%s&accessLevel=1&android-app-version-code=853' % (
        #         item['propertyId'], item['listingId'])
        #     async with session.get(url=url, headers=headers) as res:
        #         html = await res.text()
        #         data = json.loads(re.sub(r'\{\}&&', '', html))
        #         if data['payload'].get('propertyHistoryInfo') is None:
        #             return
        #         events = data['payload']['propertyHistoryInfo']['events']
        #         if len(events) == 0:
        #             return
        #         eventDescription = events[0].get('eventDescription')
        #         if eventDescription is None or re.search(r'sold|delisted|price changed', eventDescription.lower()) is not None:
        #             return
        #         item['status'] = '%s / %s' % (events[0].get('eventDescription') or '-', events[0].get('mlsDescription') or '-') if len(
        #             events) > 0 else '-'
        #         item['status_date'] = self.convert_utc_to_tz_date(datetime.fromtimestamp(
        #             events[0]['eventDate']/1000, tz=pytz.timezone(data['payload']['publicRecordsInfo']['basicInfo']['displayTimeZone'])), item['timezone']) if len(
        #             events) > 0 else '-'
        #         item['propertyTypeName'] = data['payload']['publicRecordsInfo']['basicInfo'].get(
        #             'propertyTypeName') or '-'
        #         items_queue.put(item)
        # except Exception as e:
        #     if retry < 10:
        #         time.sleep(1)
        #         await self.get_sale_history(items_queue, session, item, retry+1)



    def batch_items(self, items):
        threads = []
        results = []
        
        for item in items:
            thread = threading.Thread(target=lambda: results.append(self.get_sale_history(item)))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return results


    def convert_utc_to_tz_string(self, string_date, tz):
        if string_date is None or tz is None:
            return '-'
        _tz = pytz.timezone(tz)
        date = parser.parse(string_date)
        return _tz.normalize(date.astimezone(_tz))

    
    def get_parcel_and_owner(self, url):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        response = requests.get('https://www.redfin.com'+url, headers=headers)
        soup = BeautifulSoup(response.text, features="html.parser")
        elems = soup.find_all("div", {"class":"amenity-group"})
        parcelNumber = "Parcel Number"
        for elem in elems:
            elem.getText(strip=True)
            for li in elem.find("ul").find_all("li"):
                if parcelNumber in li.getText(strip=True):

                    parcelNumber = li.getText(strip=True).split(":")[1].strip()
        resp = {}
        if "Parcel Number" not in parcelNumber:
            response = requests.get('https://kaneil.devnetwedge.com/parcel/view/'+parcelNumber, headers=headers, allow_redirects=True)
            print(response)
            soup = BeautifulSoup(response.text, "html.parser")
            owner_name = soup.find("table").find("tr").find_all("td")[2].find_all("div")[1].getText().strip()
            
            resp["name"] = "Owner"
            return {"parcel_no": parcelNumber, "owner_name": owner_name}
        return None
    
    def get_properties(self, place):
        headers = {
            'user-agent': 'Redfin Android 458.0.1',
        }
        limit = 2000
        offset = 0
        eeror_count = 0
        out = []
        while True:
            try:
                params = {'min_stories': '1',
                        'max_markers': '250',
                        'lat_q_threshold': '0.2',
                        'num_beds': '',
                        'ord': 'days-on-redfin-asc',
                        'min_listing_approx_size': '',
                        'max_year_built': '',
                        'region_type': place['region_type'],
                        'pkg': '-',
                        'max_listing_approx_size': '',
                        'max_parcel_size': '',
                        'min_price_per_sqft': '',
                        'sf': '1,2,3,5,6,7',
                        'min_parcel_size': '',
                        'num_homes': str(limit),
                        'max_price_per_sqft': '',
                        'supported_virtualtour_sources': '0,1,2',
                        'max_num_beds': '',
                        'max_monthly_payment': '',
                        'start': str(offset),
                        'region_id': place['region_id'],
                        'long_q_threshold': '0.2',
                        'al': '1',
                        'min_monthly_payment': '',
                        'uipt': '1,2,3,4,5,6,7,8',
                        'min_year_built': '',
                        'max_stories': '',
                        'min_markers': '30',
                        'max_price': '',
                        'min_price': str(place.get('min_price')) or '',
                        'time_on_market_range': '-',
                        'v': '6',
                        'status': '131',
                        'android-app-version-code': '853', }
                data = dict(params)
                req = requests.get(
                    'https://www.redfin.com/stingray/mobile/v1/gis-proto-mobile', headers=headers, params=params)
                req_json = req.json()
                json.dump(req_json, open("data.json", "w"))
                
                _tm = [{
                    'propertyId': _property['homeData']['propertyId'],
                    'listingId':_property['homeData'].get('listingId') or '',
                    'beds':_property['homeData'].get('beds') or 0,
                    'baths':int(_property['homeData'].get('baths') or 0),
                    'priceInfo':_property['homeData'].get('priceInfo').get('amount') or None,
                    'sqftInfo':_property['homeData'].get('sqftInfo').get('amount') or None,
                    'listingAddedDate': self.convert_utc_to_tz_string(_property['homeData'].get('daysOnMarket').get('listingAddedDate'), _property['homeData'].get('timezone')) or '-',
                    'yearBuilt':_property['homeData'].get('yearBuilt').get('yearBuilt') or '-',
                    'lotSize':_property['homeData'].get('lotSize').get('amount') or '-',
                    'addressInfo':_property['homeData'].get('addressInfo') or None,
                    'url':_property['homeData']['url'],
                    'get_owner': None if "get_owner" not in place else place["get_owner"],
                    'mlsId':_property['homeData'].get('mlsId') or '-',
                    'hoaDues':_property['homeData']['hoaDues'].get('amount') or '-',
                    'timezone':_property['homeData'].get('timezone') or '-'
                } for _property in req_json['homes']]
                out += _tm
                print('\t[-] Pulled : %s' % (len(out)), end='\r')
                if len(_tm) == 0:
                    break
                offset += limit
            except ConnectionError:
                if eeror_count < 5:
                    eeror_count += 1
                    time.sleep(10)
                else:
                    print('[get_properties:%s:%s:exit_county] %s' %
                        (place['name'], offset, str(e)), flush=True)
                    break
            except Exception as e:
                if eeror_count < 5:
                    eeror_count += 1
                else:
                    message = '[get_properties:%s:%s:offset_skip] %s' % (
                        place['name'], offset, str(e))
                    print(message, flush=True)
                    # Skip current offset if error_count >= 5
                    offset += limit
                    eeror_count = 0
        return out


    def generate_sheet(self, county, data, county_name):
        def is_city_allowed(county, row):
            if county.get('city_price') is None:
                return True
            if row.get('addressInfo') is None or row['addressInfo'].get('city') is None or row.get('priceInfo') is None:
                return True
            return (row['addressInfo']['city'] if row['addressInfo'] is not None else '-') in county['city_price'].get('cities') \
                or (float(row.get('priceInfo')) >= county['city_price']['others_price'])
        try:
            filename = 'Redfin %s.csv' % START_DATE
            pd = pandas.DataFrame(data)
            pd.to_csv(filename)

            # data = list(
            #     sorted(data, key=lambda row: str(row['status_date']), reverse=True))
            # headers = ["MLS#", "Owner Name", "Parcel No." 
            #         #    "Property Type",
            #             "Address", "City", "State", "ZIP", "Location", "County", "Price", "BEDS", "BATHS",
            #         "SQUARE FEET", "$/SQUARE FEET", "LOT SIZE", "HOA/MONTH", "YEAR BUILT", 'TIMEZONE', "LISTING ADDED DATE", 'STATUS', 'URL']
            # if not os.path.isfile(filename):
            #     with open(filename, 'w', newline='', encoding="utf-8") as f:
            #         writer = csv.DictWriter(f, fieldnames=headers)
            #         writer.writeheader()
            #         writer = csv.writer(
            #             f, delimiter=',', quoting=csv.QUOTE_ALL)
            # with open(filename, 'a', newline='', encoding="utf-8") as f:
            #     writer = csv.writer(
            #         f, delimiter=',', quoting=csv.QUOTE_ALL, doublequote=False)
            #     for row in data:
            #         if not is_city_allowed(county, row):
            #             continue
            #         # if row['propertyTypeName'].lower() in list(map(str.lower, EXCLUDED_PROP_TYPES)):
            #         #     continue
            #         generated_row = [
            #             row['mlsId'],
            #             row['owner_name'],
            #             row['parcel_no'],
            #             # row['propertyTypeName'],
            #             row['addressInfo']['formattedStreetLine'] if row['addressInfo'] is not None and row['addressInfo'].get(
            #                 'formattedStreetLine') is not None else '-',
            #             row['addressInfo']['city'] if row['addressInfo'] is not None and row['addressInfo'].get(
            #                 'city') is not None else '-',
            #             row['addressInfo']['state'] if row['addressInfo'] is not None and row['addressInfo'].get(
            #                 'state') else '-',
            #             str(row['addressInfo']['zip']
            #                 if row['addressInfo'] is not None and row['addressInfo'].get(
            #                 'zip') else '-'),
            #             row['addressInfo']['location'] if row['addressInfo'] is not None and row['addressInfo'].get(
            #                 'location') is not None else '-',
            #             county_name,
            #             row.get('priceInfo') or '-',
            #             str(row['beds']),
            #             str(row['baths']),
            #             row['sqftInfo'] or '-',
            #             round(float(row['priceInfo'])/float(row['sqftInfo'])
            #                 ) if row['sqftInfo'] is not None and row['priceInfo'] is not None and float(row['sqftInfo']) > 0 else '-',
            #             str(row['lotSize']),
            #             str(row['hoaDues']),
            #             str(row['yearBuilt']),
            #             row['timezone'],
            #             str(row['listingAddedDate']),
            #             row['status'],
            #             # str(row['status_date']),
            #             str(row['url'])
            #         ]
            #         writer.writerow(generated_row)
            return filename
        except Exception as e:
            message = '[generate_sheet:%s] %s' % (county_name, str(e))
            print(message, flush=True)
