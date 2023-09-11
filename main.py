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
            break
            print('\t[-] Processed : %s / %s' %
                  ((i+1)*max_concurrent_requests, len(properties)), end='\r')
        print("County Completed", end='\r')
        print("ITEMS:",items)
        send_mail(scraper.generate_sheet(county, items, county['county']))
        break
        

main()