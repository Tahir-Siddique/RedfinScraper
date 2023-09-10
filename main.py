from redfin_scraper import RedfinScrapper
from utils.constants import COUNTIES, NUMBER_OF_THREADS_PAGES
from utils.utils import send_mail
import threading

def main():
    
    scraper = RedfinScrapper()
    print('[-] Total Counties : %s' % (len(COUNTIES)))
    for county in COUNTIES:
        print('\n[-] Scraping : %s' % (county['county']))
        properties = scraper.get_properties(county)
        max_concurrent_requests = 50
        items = []
        
        chunks = [properties[i:i + max_concurrent_requests] for i in range(0, len(properties), max_concurrent_requests)]
        
        threads = []
        for i, chunk in enumerate(chunks):
            thread = threading.Thread(target=lambda: items.extend(scraper.batch_items(chunk)))
            threads.append(thread)
            thread.start()
            thread.join()
            print('\t[-] Processed : %s / %s' %
                  ((i+1)*max_concurrent_requests, len(properties)), end='\r')
        
        send_mail(scraper.generate_sheet(county, items, county['county']))
        
        


    #     # print(properties)
    #     i = 0
    #     items_queue = Queue()
    #     items = []
    #     while True:
    #         try:
    #             asyncio.run()
    #             while not items_queue.empty():
    #                 items.append(items_queue.get())
    #         except Exception as e:
    #             message = '[asyncio-handle_batch] %s' % str(e)
    #             # sendMessage(message=message)
    #             print(message)
    #         if i >= len(properties):
    #             break
    #         i += NUMBER_OF_THREADS_PAGES
    #     send_mail(scraper.generate_sheet(county, items, county['county']))
    #     break
    # print('[-] All Done.')
    


main()
