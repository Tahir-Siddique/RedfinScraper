

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
    
    for proxy in random.sample(PROXIES, len(PROXIES)):
        proxy_url = f"{proxy['type']}://{proxy['ip']}:{proxy['port']}"
        try:
            response = requests.get(url + item.get("url"), headers=headers, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features="html.parser")
                elems = soup.find_all("div", {"class": "amenity-group"})
                parcelNumber = "Parcel Number"
                for elem in elems:
                    elem.getText(strip=True)
                    for li in elem.find("ul").find_all("li"):
                        if parcelNumber in li.getText(strip=True):
                            item["parcel_no"] = li.getText(strip=True).split(":")[1].strip()
                
                # if "Parcel Number" not in parcelNumber:
                #     try:
                #         response = requests.get('https://kaneil.devnetwedge.com/parcel/view/'+parcelNumber, headers=headers, allow_redirects=True, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
                #         soup = BeautifulSoup(response.text, "html.parser")
                #         owner_name = soup.find("table").find("tr").find_all("td")[2].find_all("div")[1].getText().strip()
                #         item["owner_name"] = owner_name
                #         item["parcel_no"] = parcelNumber
                #         item.pop("get_owner")
                #         return item
                #     except Exception as e:
                #         print(f"Error while getting owner details with proxy {proxy_url}: {str(e)}")
                # else:
                #     print(f"Parcel Number not found with proxy {proxy_url}")
                item.pop("get_owner")
                return item
            else:
                print(f"Request failed with proxy {proxy_url} - Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error while making request with proxy {proxy_url}: {str(e)}")
    
    return item



def get_owner_by_kane_county(item):
    
    from utils.constants import PROXIES
    headers = {
        'user-agent': 'Redfin Android 458.0.1',
    }
    item["owner_name"] = "Not found"
    item["parcel_no"] = "Not found"
    
    for proxy in random.sample(PROXIES, len(PROXIES)):
        proxy_url = f"{proxy['type']}://{proxy['ip']}:{proxy['port']}"
        try:
            response = requests.get(url + item.get("url"), headers=headers, proxies={"http": proxy_url, "https": proxy_url}, timeout=5)
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
                    print(f"Error while getting owner details with proxy {proxy_url}: {str(e)}")
            else:
                print(f"Request failed with proxy {proxy_url} - Status Code: {response.status_code}")
        except Exception as e:
            print(f"Error while making request with proxy {proxy_url}: {str(e)}")
    
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