from datetime import datetime

from utils.utils import get_owner_by_kane_county, get_owner_by_lake_county


START_DATE = datetime.now().strftime('%d.%m.%Y')
RECEIVER_EMAILS = ['jason@falconmoving.com', "tahircreativedev577@gmail.com"]
EMAIL_FROM = 'Redfin Bot'
SENDER_USERNAME = 'redfin.notifier@gmail.com'
SENDER_PASSWORD = '#redfin.notifier#'
SENDER_APP_PASSWORD = 'ywykrababxcybpjv'
NUMBER_OF_THREADS_PAGES = 20

COUNTIES = [
    {
        'region_type': 5,
        'region_id': 733,
        'county': 'DuPage County',
        "parcel_url":"https://propertylookup.dupagecounty.gov/search/commonsearch.aspx?mode=parid",
        'min_price': 250000,
    },
    {
        'region_type': 5,  # type: County
        'region_id': 760,
        'county': 'Lake County',
        'min_price': 250000,
        "get_owner": get_owner_by_lake_county
    },
    {
        'region_type': 5,  # type: County
        'region_id': 756,
        'county': 'Kane County',
        'min_price': 250000,
        "get_owner": get_owner_by_kane_county
    },
    {
        'region_type': 5,  # County type
        'region_id': 727,
        'county': 'Cook County',
        "parce_url": "https://www.cookcountypropertyinfo.com/",
        'min_price': 250000,
        'city_price': {
            'others_price': 500000,  # Min price for cities which are not whitelisted
            'cities': ['Bartlett',
                       'Wayne',
                       'South Elgin',
                       'Elgin',
                       'South Barrington',
                       'Barrington Hills',
                       'Sutton',
                       'Barrington',
                       'Inverness',
                       'Palatine',
                       'Rolling Meadows',
                       'Arlington Heights',
                       'Mt Prospect',
                       'Schaumburg',
                       'Hanover Park',
                       'Streamwood',
                       'Keeneyville',
                       'Roselle',
                       'Medinah',
                       'Bloomingdale',
                       'Itasca',
                       'Elk Grove Village',
                       'Bensenville',
                       'Deer Park',
                       'Kildeer',
                       'Buffalo Grove',
                       'Long Grove', ]
        }
    },
    {
        'region_type': 5,
        'region_id': 767,
        'county': 'McHenry County',
        "parcel_url": "https://mchenryil.devnetwedge.com/",
        'min_price': 250000,
    },
    {
        'region_type': 5,
        'region_id': 810,
        'county': 'Will County',
        'min_price': 750000,
    },
    {
        'region_type': 5,
        'region_id': 757,
        'county': 'Kankakee County',
        'parcel_url': "http://treasurer.k3county.net/",
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 749,
        'county': 'Iroquois County',
        "parcel_url": "https://iroquoisil.devnetwedge.com/",
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 743,
        'county': 'Grundy County',
        "parcel_url": "https://grundyil.devnetwedge.com/",
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 764,
        'county': 'Livingston County',
        "parcel_url": "https://livingstonil.devnetwedge.com/",
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 761,
        'county': 'LaSalle County',
        "parcel_url": "http://propertytaxonline.org/LaSalle/Inquiry.aspx", #not important
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 730,
        'county': 'DeKalb County',
        'min_price': 750000,
    },
    {
        'region_type': 5,
        'region_id': 715,
        'county': 'Boone County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 3192,
        'county': 'Kenosha County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 3214,
        'county': 'Racine County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 3227,
        'county': 'Walworth County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 858,
        'county': 'Lake County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 869,
        'county': 'Newton County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 877,
        'county': 'Porter County',
        'min_price': 1000000,
    },
    {
        'region_type': 5,
        'region_id': 850,
        'county': 'Jasper County',
        'min_price': 1000000,
    },
]
EXCLUDED_PROP_TYPES = ['Vacant Land']

PROXIES = [
    {"ip": "145.239.85.58", "port": 9300, "type": "socks5"},
    {"ip": "46.4.96.137", "port": 1080, "type": "socks5"},
    {"ip": "47.91.88.100", "port": 1080, "type": "socks5"},
    {"ip": "45.77.56.114", "port": 30205, "type": "socks5"},
    {"ip": "82.196.11.105", "port": 1080, "type": "socks5"},
    {"ip": "51.254.69.243", "port": 3128, "type": "http"},
    {"ip": "178.62.193.19", "port": 1080, "type": "socks5"},
    {"ip": "188.226.141.127", "port": 1080, "type": "socks5"},
    {"ip": "217.23.6.40", "port": 1080, "type": "socks5"},
    {"ip": "185.153.198.226", "port": 32498, "type": "socks5"},
    {"ip": "81.171.24.199", "port": 3128, "type": "http"},
    {"ip": "5.189.224.84", "port": 10000, "type": "socks5"},
    {"ip": "108.61.175.7", "port": 31802, "type": "socks5"},
    {"ip": "176.31.200.104", "port": 3128, "type": "http"},
    {"ip": "83.77.118.53", "port": 17171, "type": "http"},
    {"ip": "173.192.21.89", "port": 80, "type": "http"},
    {"ip": "163.172.182.164", "port": 3128, "type": "http"},
    {"ip": "163.172.168.124", "port": 3128, "type": "http"},
    {"ip": "164.68.105.235", "port": 3128, "type": "http"},
    {"ip": "5.199.171.227", "port": 3128, "type": "http"},
    {"ip": "93.171.164.251", "port": 8080, "type": "http"},
    {"ip": "212.112.97.27", "port": 3128, "type": "http"},
    {"ip": "51.68.207.81", "port": 80, "type": "http"},
    {"ip": "91.211.245.176", "port": 8080, "type": "http"},
    {"ip": "84.201.254.47", "port": 3128, "type": "http"},
    {"ip": "95.156.82.35", "port": 3128, "type": "http"},
    {"ip": "185.118.141.254", "port": 808, "type": "http"},
    {"ip": "164.68.98.169", "port": 9300, "type": "socks5"},
    {"ip": "217.113.122.142", "port": 3128, "type": "http"},
    {"ip": "188.100.212.208", "port": 21129, "type": "http"},
    {"ip": "83.77.118.53", "port": 17171, "type": "http"},
    {"ip": "83.79.50.233", "port": 64527, "type": "http"},
]