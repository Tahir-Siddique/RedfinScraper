

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import json
import smtplib
import time
from bs4 import BeautifulSoup

import requests


def get_owner_by_kane_county(item):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    }
    # print()
    # print(item.get("url"))
    
    response = requests.get("https://www.redfin.com"+item.get("url"), headers=headers)
    
    # async with session.get(url="https://www.redfin.com"+item.get("url"), headers=headers) as res:
        
        # html = await res.text()
        # soup = BeautifulSoup(html, features="html.parser")
    soup = BeautifulSoup(response.text, features="html.parser")
    elems = soup.find_all("div", {"class":"amenity-group"})
    parcelNumber = "Parcel Number"
    for elem in elems:
        elem.getText(strip=True)
        for li in elem.find("ul").find_all("li"):
            if parcelNumber in li.getText(strip=True):

                parcelNumber = li.getText(strip=True).split(":")[1].strip()
    if "Parcel Number" not in parcelNumber:
        response = requests.get('https://kaneil.devnetwedge.com/parcel/view/'+parcelNumber, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")
        try:
            owner_name = soup.find("table").find("tr").find_all("td")[2].find_all("div")[1].getText().strip()
            # print(owner_name)
            item["owner_name"] = owner_name
            item["parcel_no"] = parcelNumber
            item.pop("get_owner")
            return item
        except:
            item["owner_name"] = "Not found"
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