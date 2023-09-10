from asyncio import Queue, gather
import asyncio
from redfin_scraper import RedfinScrapper
from utils.constants import COUNTIES, NUMBER_OF_THREADS_PAGES
from utils.utils import send_mail

async def process_county(county, scraper):
    print('\n[-] Scraping : %s' % (county['county']))
    properties = scraper.get_properties(county)
    items = []
    i = 0
    while i < len(properties):
        try:
            async with Queue() as items_queue:
                await scraper.batch_items(
                    items_queue, properties[i:min(i+NUMBER_OF_THREADS_PAGES, len(properties))])
                while not items_queue.empty():
                    items.append(items_queue.get())
        except Exception as e:
            message = '[asyncio-handle_batch] %s' % str(e)
            # sendMessage(message=message)
            print(message)
        print('\t[-] Processed : %s / %s' %
              (i, len(properties)), end='\r')
        i += NUMBER_OF_THREADS_PAGES
    send_mail(scraper.generate_sheet(county, items, county['county']))

async def main():
    scraper = RedfinScrapper()
    print('[-] Total Counties : %s' % (len(COUNTIES)))
    
    tasks = [process_county(county, scraper) for county in COUNTIES]
    await gather(*tasks)
    print('[-] All Done.')

if __name__ == "__main__":
    asyncio.run(main())
