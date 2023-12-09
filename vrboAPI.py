import requests
import json
import re
import pandas as pd
from datetime import datetime, timedelta 
import os

url = 'https://www.vrbo.com/graphql'

RESULT_FILE = 'output.csv'

headers = {
    'Authority': 'www.vrbo.com',
    'method': 'POST',
    'path': '/graphql',
    'scheme': 'https',
    'Accept': '*/*',
    'Accept-language': 'en-IN,en-US;q=0.9,en-GB;q=0.8,en;q=0.7',
    'Client-info': 'shopping-pwa,unknown,unknown',
    'Content-type': 'application/json',
    'Cookie': 'linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; CRQS=t|9001`s|9001001`l|en_US`c|USD; currency=USD; tpid=v.1,9001; hav=cdd7ef2c-5c31-7956-0389-a6fb945956d2; MC1=GUID=cdd7ef2c5c3179560389a6fb945956d2; DUAID=cdd7ef2c-5c31-7956-0389-a6fb945956d2; ha-device-id=cdd7ef2c-5c31-7956-0389-a6fb945956d2; hav=cdd7ef2c-5c31-7956-0389-a6fb945956d2; _gcl_au=1.1.1693190545.1700249663; _fbp=fb.1.1700249663535.870324860; OptanonAlertBoxClosed=2023-11-17T19:34:26.064Z; OIP=ccpa|1`ts|1700249666; xdid=6ab89a26-43ba-4abe-b40d-048ecc2327fd|1700249669|vrbo.com; s_fid=751AD26A46D5C75E-1D9662A9A4513BE6; QSI_SI_aWQdMdC3KF1RI10_intercept=true; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Nov+20+2023+13%3A52%3A18+GMT%2B0530+(India+Standard+Time)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=927ee8bc-c315-4ab4-8926-05e0060b66c1&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CSPD_BG%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=IN%3BCH&AwaitingReconsent=false; aspp=v.1,0|||||||||||||; _ga=GA1.2.1924316392.1700475768; _cls_v=34d5d705-8236-4e0d-bd5b-fd906e9a8ce9; has=187a9507-5d39-223c-8d87-7de76a43054e; CRQSS=e|1; iEAPID=1; HMS=8bf8de26-61c1-4cf1-ae08-efa11d47d75e; ak_bmsc=7D13FD01E987803074FBA45800017863~000000000000000000000000000000~YAAQiLYRYMHc/jCMAQAAvvetQhbV3Bme23WQXeUU0KKYM0lIW9S9g+d1x+VZkkSGK6BnN4OF21bl73eF7jlHxgfKzxl1Zw9WTsUNuTuSoyFKJ8XtycHtpMv09Mrj7UOaV8G1ujn8Acb1XWjibKAOTbLMvoseZTj66ExPLTBD7hHefDSs5XrEEzqbR3RMvXD6yAEX+y8p1JpE8UleRWno82nC507eoIpUDaQu2EErDKDFOZeUpe/wWRGwR1hs/k1SMsgj9KeEluwaW5qyOnO3EUsUN47BuzLHcwlEKvII2NO+eIZ+414iMYn8GlX+b1SwDBO3ojzSPA4cM9AVRIrfEo3BCbk8EEsn2NWPUt+aEV9Ik87NJ1Se8O4zwEjFzgLyvnD1dBOl0H4=; s_ppn=page.Hotel-Search; s_ppv=%5B%5BB%5D%5D; s_ips=1; AMCVS_C00802BE5330A8350A490D4C%40AdobeOrg=1; AMCV_C00802BE5330A8350A490D4C%40AdobeOrg=1585540135%7CMCIDTS%7C19699%7CMCMID%7C18439981346053663073455550440919209970%7CMCAAMLH-1702530578%7C12%7CMCAAMB-1702530578%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1701932978s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; eg_ppid=65ef152d-c194-4e02-b825-c939df0347dd; session_id=8bf8de26-61c1-4cf1-ae08-efa11d47d75e; page_name=page.Hotel-Search; _uetsid=cd3801a0942611ee99ac9daede2d433e; _uetvid=4f0e6080858011ee8278fbd5e694b689; _tq_id.TV-8181636390-1.1968=7a4c790888da3d81.1700249664.0.1701925792..; __gads=ID=e893818b40669bb9:T=1700249662:RT=1701925795:S=ALNI_MYBch3iFHD3WBdtTQpgQXfEfXtG5Q; __gpi=UID=00000c8cc3054387:T=1700249662:RT=1701925795:S=ALNI_MYAz_nduave3aeFIKks5SuuWmfuDQ; JSESSIONID=ACB94328BC32058C86C9BFA3BC92AB63; QSI_HistorySession=https%3A%2F%2Fwww.vrbo.com%2Fsearch%3Fadults%3D2%26amenities%3D%26children%3D%26d1%3D2023-11-19%26d2%3D2023-11-20%26destination%3D73%2BW%2BMonroe%2BSt%252C%2BChicago%252C%2BIL%2B60603%252C%2BUSA%26endDate%3D2023-12-28%26latLong%3D%26mapBounds%3D%26pwaDialog%3D%26regionId%3D6350699%26semdtl%3D%26sort%3DRECOMMENDED%26startDate%3D2023-12-14%26theme%3D%26userIntent%3D~1701925906262; _dd_s=rum=0&expire=1701926807094; cesc=%7B%22lpe%22%3A%5B%2226230afa-b08b-4ac9-ae3b-2ad5135bc656%22%2C1701925905515%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1701925905515%5D%2C%22lmc%22%3A%5B%22DIRECT.REFERRAL%22%2C1701925905515%5D%2C%22hitNumber%22%3A%5B%224%22%2C1701925905515%5D%2C%22amc%22%3A%5B%22DIRECT.REFERRAL%22%2C1701925905515%5D%2C%22visitNumber%22%3A%5B%2224%22%2C1701925746563%5D%2C%22ape%22%3A%5B%2226230afa-b08b-4ac9-ae3b-2ad5135bc656%22%2C1701925905515%5D%2C%22entryPage%22%3A%5B%22page.Hotel-Search%22%2C1701925905515%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1700249651848%5D%7D; bm_sv=0CD76B20986EAF22F041E36EB8669C21~YAAQhbYRYMOH+DCMAQAAn2SwQhbYcfEfzoCZiwkI93Nc2s6DGNpy3T8hKpb9WFfclGknRUxJC8g1Buz8yZly4qXiUojM3NqKBf+h5PIQfUbtZQlMhrtkMt8aC82qQpm5c3vlDYn33hxT3rUG5UiWpS6WB3CGT/tQEKFJt7As0vG0aGRBLbjx4NJHL8cn8qiphFUL+DEgspuSzL6xsNnkZEOJ77gYNpKDyZwzzMSZnY8N/bwKLeRg9YG5Dclg8hs=~1; s_tp=1728',  # Replace with your actual cookie value
    'Origin': 'https://www.vrbo.com',
    'Referer': 'https://www.vrbo.com/search?adults=2&amenities=&children=&d1=2023-11-19&d2=2023-11-20&destination=73%20W%20Monroe%20St%2C%20Chicago%2C%20IL%2060603%2C%20USA&endDate=2023-12-28&latLong=&mapBounds=&pwaDialog&regionId=6350699&semdtl=&sort=RECOMMENDED&startDate=2023-12-14&theme=&userIntent=',
    'Sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-ch-ua-mobile': '?0',
    'Sec-ch-ua-platform': '"Windows"',
    'Sec-fetch-dest': 'empty',
    'Sec-fetch-mode': 'cors',
    'Sec-fetch-site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-enable-apq': 'true',
    'X-page-id': 'page.Hotel-Search,H,20',
    "Postman-Token": "2bc2c056-17e9-4450-9003-64bc6f85fd5b"
}

payload = {
    'variables': {
        'context': {
            'siteId': 9001001,
            'locale': 'en_US',
            'eapid': 1,
            'currency': 'USD',
            'device': {'type': 'DESKTOP'},
            'identity': {
                'duaid': 'cdd7ef2c-5c31-7956-0389-a6fb945956d2',
                'expUserId': None,
                'tuid': None,
                'authState': 'ANONYMOUS'
            },
            'privacyTrackingState': 'CAN_TRACK',
            'debugContext': {'abacusOverrides': []}
        },
        'criteria': {
            'primary': {
                'dateRange': {
                    'checkInDate': {'day': 14, 'month': 12, 'year': 2023},
                    'checkOutDate': {'day': 28, 'month': 12, 'year': 2023}
                },
                'destination': {
                    'regionName': '73 W Monroe St, Chicago, IL 60603, USA',
                    'regionId': '6350699',
                    'coordinates': None,
                    'pinnedPropertyId': None,
                    'propertyIds': None,
                    'mapBounds': None
                },
                'rooms': [{'adults': 2, 'children': []}]
            },
            'secondary': {
                'counts': [],
                'booleans': [],
                'selections': [
                    {'id': 'sort', 'value': 'RECOMMENDED'},
                    {'id': 'privacyTrackingState', 'value': 'CAN_TRACK'},
                    {'id': 'useRewards', 'value': 'SHOP_WITHOUT_POINTS'},
                    {'id': 'searchId', 'value': 'e02b8748-0503-42a7-9468-a4f8477cae76'}
                ],
                'ranges': []
            }
        },
        'destination': {
            'regionName': None,
            'regionId': None,
            'coordinates': None,
            'pinnedPropertyId': None,
            'propertyIds': None,
            'mapBounds': None
        },
        'shoppingContext': {'multiItem': None},
        'returnPropertyType': False,
        'includeDynamicMap': True
    },
    'operationName': 'LodgingPwaPropertySearch',
    'extensions': {
        'persistedQuery': {
            'sha256Hash': '5247eef59f2303d0d40b7ca21bf547835e8bfb321b26ca802a58c2f4a78697c3',
            'version': 1
        }
    }
}



# response = requests.post(url, json=payload, headers=headers)
# print(response.status_code)
# with open ('opt.text', 'w') as f:
#     f.write(str(response.headers))
# print(response.text)
# print(response.headers)

def dfToJson(df):
    res = df.to_json(orient="records")
    parsed = json.loads(res)
    return parsed

def main(destination="New Delhi",radius=-1, dateRange = None):

    payload['variables']['criteria']['primary']['dateRange'] = dateRange

    checkInDate = dateRange.get('checkInDate')
    checkOutDate = dateRange.get('checkOutDate')

    links=[]
    prices=[]
    distances=[]

    # filename = str(checkInDate['year']) + '-' + str(checkInDate['month']) + '-' + str(checkInDate['day']) + '.json'

    # if os.path.exists(filename):
    #     print("File exists: ", filename)
    #     with open(filename, encoding='utf-8') as f:
    #         data = json.load(f)

    
    if True:
    
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        
        
        

        listings=data['data']['propertySearch']["propertySearchListings"]
        for listing in listings :
            if(listing.get("cardLink") is not None):
                links.append(listing["cardLink"]["resource"]["value"])
            if(listing.get("priceSection") is not None):
                prices.append(listing["priceSection"]["priceSummary"]["options"][0]["displayPrice"]["formatted"])
            if(listing.get("headingSection") is not None):
                distance=listing["headingSection"]["featuredMessages"][0]["text"]
                distance_match = re.search(r'\d+(\.\d+)?', str(distance))
                if distance_match:
                    final_distance = float(distance_match.group())
                    distances.append(final_distance)
        # print(len(links))
        # print(len(prices))
        # print(len(distances))
        dict = {'link':links,'distance':distances,'price':prices}
        df=pd.DataFrame(dict)
        if radius != -1:
            df = df[df['distance'] <= radius]
        df = df.sort_values(by='distance')

        # add a column to the dataframe with the current date
        df['date'] = str(checkInDate['year']) + '-' + str(checkInDate['month']) + '-' + str(checkInDate['day'])
        print(df.head())

        # read output.csv if it exists, and append its data to the dataframe
        df2 = pd.read_csv(RESULT_FILE)
        df = df._append(df2)

        # write the dataframe to output.csv
        df.to_csv(RESULT_FILE, index=False)

        # return 
        return dfToJson(df)


def getDates(destination="New Delhi",radius=-1):
    from datetime import datetime, timedelta

    # Get the current date
    current_date = datetime.now()

    # Loop over the next 365 days
    for i in range(365):
        # Calculate the next date
        next_date = current_date + timedelta(days=i)

        # get current date and next date, and increment both by 1
        checkInDate =  {"day": next_date.day, "month": next_date.month, "year": next_date.year}

        checkOutDate = next_date + timedelta(days=1)
        checkOutDate = {"day": checkOutDate.day, "month": checkOutDate.month, "year": checkOutDate.year}

        dateRange = {"checkInDate": checkInDate, "checkOutDate": checkOutDate}
        # TODO : uncomment this line
        # dateRange = json.dumps(dateRange)
        
        main(destination=destination, radius=radius, dateRange=dateRange)
        print("Done with date: ", next_date)
getDates()