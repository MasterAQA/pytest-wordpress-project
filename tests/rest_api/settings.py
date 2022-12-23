import base64
from random import randint, choice

import names
import pytest
import requests

app_name = "qatesting"
app_pass = "kVWydHZs@p)RX^^NBQ"
credentials = app_name + ":" + app_pass
token = base64.b64encode(credentials.encode())
root_url = "http://wpfolder/wp-json/wp/v2"
headers = {"Authorization": "Basic " + token.decode("utf-8")}

from woocommerce import API


wcapi = API(
    url="http://wpfolder",  # Your store URL
    consumer_key="ck_2829e1ef831f3ab512c2307abccf8baef4fe7164",  # Your consumer key
    consumer_secret="cs_8ec45935a5e8f86d0b4c4569b57c31c9e5b206c3",  # Your consumer secret
    wp_api=True,  # Enable the WP REST API integration
    version="wc/v3",  # WooCommerce WP REST API version
)

wcapi_fail = API(
    url="http://wpfolder",  # Your store URL
    consumer_key="ck_2829e1ef831f3ab512c2307abccf8baef4fe71",  # Your consumer key
    consumer_secret="cs_8ec45935a5e8f86d0b4c4569b57c31c9e06c3",  # Your consumer secret
    wp_api=True,  # Enable the WP REST API integration
    version="wc/v3",  # WooCommerce WP REST API version
)
