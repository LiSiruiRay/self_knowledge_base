# Author: ray
# Date: 8/21/24
# Description:
import json
import os

import requests
from pyzotero import zotero

import logging

logging.basicConfig(level=logging.DEBUG)


def get_data_from_api(base, params):
    try:
        # Send a GET request to the API
        response = requests.get(base, params=params)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

current_path = os.getcwd()
buffered = os.path.exists(current_path + 'buffered_zh.json')
if not buffered:
    logging.info(f"not buffered, started querying")
    collection_id = 695507497
    offset = 0
    limit = 10

    base = f"https://www.zhihu.com/api/v4/collections/{collection_id}/items"
    params = {"offset": offset, "limit": limit}
    # response = requests.get(base, params=params)
    # result = get_data_from_api(base=base, params=params)
    # print(f"test: {result['paging']}")
    is_end = False

    collection_list = []
    logging.info(f"started getting collection_list")
    counter = 1
    while not is_end:
        data = get_data_from_api(base=base, params=params)
        is_end = data['paging']['is_end']
        collection_list.extend(data['data'])
        base = data['paging']['next']
        params = None
        counter += 1
        logging.info(f"finished getting collection_list {counter}")

    logging.info(f"finished getting collection_list : {collection_list}")
    logging.info(f"started buffering")

    with open(current_path + 'buffered_zh.json', 'w') as f:
        json.dump(collection_list, f, indent=4)
else:
    logging.info(f"buffered requests result, reading from buffered_zh.json")
    with open(current_path + 'buffered_zh.json', 'r') as f:
        collection_list = json.load(f)

l_id = "14848999"
library_type = 'user'
api_key = 'Xiv5ApgC6SnUgx5R0so7a99L'
zot = zotero.Zotero(l_id, library_type, api_key)
collections = ['7PCC75HY']
language = "Chinese"
websiteType = "zhihu"
items = []
logging.info(f"started getting items")
for i, collection in enumerate(collection_list):

    content = collection["content"]
    url = content['url']
    logging.debug(f"{i}th collection, {content['type']}")
    if content["type"] == "answer":
        title = content["question"]["title"]
        abs = content["excerpt"]
    elif content["type"] == "article":
        title = content["title"]
        abs = content["excerpt_title"]
    elif content["type"] == "pin":
        title = 'pin'
        abs = content["excerpt_title"]
    else:
        title = content["title"]
        abs = title

    author_name = content["author"]["name"]

    temp = zot.item_template(itemtype='webpage')
    temp['url'] = url
    temp['title'] = title
    temp['creators'][0]['lastName'] = author_name
    temp['abstractNote'] = abs
    temp['collections'] = collections
    temp['language'] = language
    items.append(temp)
logging.info(f"finished getting items : {items}")

logging.info(f"started injecting items...")
resp = zot.create_items(items)
logging.info(resp)
# title = 'test title'
# temp = zot.item_template(itemtype = 'webpage')
# temp['url'] = each_url
# temp['title'] = title
# temp['creators'][0]['lastName'] = "test_name"
# temp['abstractNote'] = "tset_abs_note"
# temp['collections'] = collections
# temp['language'] = language
#
# resp = zot.create_items([temp])
#
# print(resp)
