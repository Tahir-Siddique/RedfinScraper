

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import random
import smtplib
import time
from bs4 import BeautifulSoup

import requests



url = "https://www.redfin.com"


def get_owner_by_lake_county(item):
    
    from utils.constants import PROXIES
    headers = {
        'user-agent': 'Redfin Android 458.0.1',
    }
    item["owner_name"] = "Not found"
    item["parcel_no"] = "Not found"
    
    
    proxy = PROXIES[random.randint(0, len(PROXIES)-1)]
    
    try:
        cookies = {
            'ASP.NET_SessionId': 'cuzcolz2rvkllwyjawaoc3uv',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-PK,en-US;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            # 'Cookie': 'ASP.NET_SessionId=cuzcolz2rvkllwyjawaoc3uv',
            'Origin': 'https://tax.lakecountyil.gov',
            'Referer': 'https://tax.lakecountyil.gov/search/CommonSearch.aspx?mode=REALPROP',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'mode': 'REALPROP',
        }

        data = {
            'ScriptManager1_TSM': ';;AjaxControlToolkit, Version=4.1.50731.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:f8fb2a65-e23a-483b-b20e-6db6ef539a22:ea597d4b:b25378d2;Telerik.Web.UI, Version=2020.2.512.45, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:88f9a2dc-9cbf-434f-a243-cf2dd9f642dc:16e4e7cd:33715776:58366029:f7645509:24ee1bba:f46195d3:c128760b:19620875:874f8ea2:b2e06756:92fe8ea0:fa31b949:4877f69a:490a9d4e',
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': '0278B551',
            '__EVENTVALIDATION': 'X1Zjl5LV3VkZV87oKYAt+M5VXPCV7iuW95ASLlXIjKA76SEybHqNv79/YOSpGNVp23o7Y3aGJT3m9e5yz13/TSe4ZivY9y7sGQesiGzSAZIJv0CmnmEvpzUQ7KV+09zcWDlbHG0/tXQL0BG8LVDwY+Vp3DnIrTjgMD3UvwT5vofLTSYH6zB9DXeT47qbL+HNiPrhSl6ki/eq7b2Pwr4ekCv7IBXIDKwJnwI8ncLDWL06jEzNxtKBooOrwxlYUabL+NqRyPCKOwW5Yu34F25vXSnXSy3t5JyZToO3gFM2RksLpMIlVvfMU5DskmAo86YKjBrM/uIwcaILVC0CfbbDgHl1Bsw3deLQFLoxrTyMoKU=',
            'PageNum': '1',
            'SortBy': 'PARID',
            'SortDir': ' asc',
            'PageSize': '15',
            'hdAction': 'Search',
            'hdIndex': '3',
            'sIndex': '-1',
            'hdListType': 'PA',
            'hdJur': '',
            'hdSelectAllChecked': 'false',
            'inpParid': '',
            'inpOwner1': '',
            'inpOwner2': '',
            'inpNo': item.get("addressInfo").get("formattedStreetLine").split(" ")[0], # House Nuumber
            'inpDir': '',
            'inpStreet': item.get("addressInfo").get("formattedStreetLine").split(" ")[-2],
            'inpBookPage': '',
            'inpSuf': item.get("addressInfo").get("formattedStreetLine").split(" ")[-1], # Suffix
            'inpAltid': '',
            'inpUnit': '',
            'inpZip1': item.get("addressInfo").get("city"), # City
            'inpZip': str(item.get("addressInfo").get("zip")), # Zipcode
            'searchClt$hdSelSuf': '',
            'searchClt$hdSelDir': '',
            'hdTaxYear': '',
            'inpTaxyr': '0',
            'selSortBy': 'PARID',
            'selSortDir': ' asc',
            'selPageSize': '15',
            'searchOptions$hdBeta': '',
            'btSearch': '',
            'RadWindow_NavigateUrl_ClientState': '',
            'mode': 'REALPROP',
            'mask': '',
            'param1': '',
            'searchimmediate': '',
        }

        response = requests.post(
            'https://tax.lakecountyil.gov/search/CommonSearch.aspx',
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        item["owner_name"] = soup.find("tr", {"id": "datalet_header_row"}).find("table").find_all("tr")[3].find("td").getText()
    except:
        pass
    return item



def get_owner_by_kane_county(item):
    
    from utils.constants import PROXIES
    headers = {
        'user-agent': 'Redfin Android 458.0.1',
    }
    item["owner_name"] = "Not found"
    item["parcel_no"] = "Not found"
    
    try:
        proxy = PROXIES[random.randint(0, len(PROXIES)-1)]
        response = requests.get(url + item.get("url"), headers=headers, proxies=proxy, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, features="html.parser")
            elems = soup.find_all("div", {"class": "amenity-group"})
            parcelNumber = "Parcel Number"
            for elem in elems:
                elem.getText(strip=True)
                for li in elem.find("ul").find_all("li"):
                    if parcelNumber in li.getText(strip=True):
                        item["parcel_no"] = li.getText(strip=True).split(":")[1].strip()
            
            try:
                response = requests.get('https://kaneil.devnetwedge.com/parcel/view/'+parcelNumber, headers=headers, allow_redirects=True, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                owner_name = soup.find("table").find("tr").find_all("td")[2].find_all("div")[1].getText().strip()
                item["owner_name"] = owner_name
                item["parcel_no"] = parcelNumber
                item.pop("get_owner")
                return item
            except Exception as e:
                print(f"Error while getting owner details with proxy {proxy.get('http')}: {str(e)}")
        else:
            print(f"Request failed for {url + item.get('url')}: {proxy.get('http')} - Status Code: {response.status_code}. Trying again")
    except Exception as e:
        print(f"Unable to process", url + item.get("url"))
    
    return item

def send_mail(file_name):
    # Create a multipart message
    msg = MIMEMultipart()
    body_part = MIMEText(
        "Hi,\nPlease find the attached RedfinScrapper file.\n\n", 'plain')
    msg['Subject'] = "RedfinScrapper File"
    msg['From'] = "automationscripts@falconmoving.com"
    msg['To'] = "jason@falconmoving.com"

    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary
    print(file_name)
    with open(file_name, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(
            file.read(), Name="Redfin.csv"))
    
    # open a connection to the server
    smtp_obj = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    # Login to the server
    smtp_obj.login(msg['From'], "Falcon100!!")

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    time.sleep(2)
    smtp_obj.sendmail(
        msg['From'], "tahirsiddique52740@gmail.com", msg.as_string())
    smtp_obj.quit()