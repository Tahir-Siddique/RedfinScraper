from datetime import datetime

from utils.utils import get_owner_by_kane_county


START_DATE = datetime.now().strftime('%d.%m.%Y')
RECEIVER_EMAILS = ['jason@falconmoving.com', "tahircreativedev577@gmail.com"]
EMAIL_FROM = 'Redfin Bot'
SENDER_USERNAME = 'redfin.notifier@gmail.com'
SENDER_PASSWORD = '#redfin.notifier#'
SENDER_APP_PASSWORD = 'ywykrababxcybpjv'
NUMBER_OF_THREADS_PAGES = 20

COUNTIES = [
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
        'region_id': 733,
        'county': 'DuPage County',
        "parcel_url":"https://propertylookup.dupagecounty.gov/search/commonsearch.aspx?mode=parid",
        'min_price': 250000,
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