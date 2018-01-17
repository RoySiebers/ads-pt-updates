import json
import requests
import pandas as pd
from flask import Flask

print("Starting update analysis.")


def run_update_analysis():
    items_response = requests.post('http://192.168.27.170/graphql', json={'query': '''
    {
        items {
            id
            name
        }
    }
    '''})

    updates_response = requests.post('http://192.168.27.170/graphql', json={'query': '''
    {
    updates {
        id
        title
        date
        content
    }
    }
    '''})

    item_names = [item for item in json.loads(
        items_response.text)["data"]["items"]]

    removable_items = ["poison", "fur", "pot", "gin",
                       "weeds", "casket", "hair"]

    last_update = json.loads(updates_response.text)["data"]["updates"][0]
    items = []
    for line in last_update['content'].splitlines():
        for item in item_names:
            if item["name"].upper() in line.upper():
                item_change = ''
                if "DROP-RATE" in line.upper():
                    item_change = "drop-rate change"
                elif "INCREASED" in line.upper():
                    if "DROP" in line.upper():
                        item_change = "price decrease"
                elif "DECREASED" in line.upper():
                    if "DROP" in line.upper():
                        item_change = "price increase"
                items.append({'item_id': item["id"], 'item_name': str(
                    item["name"]), 'line': str(line), 'change': item_change})

    for removable_item in removable_items:
        for final_item in items:
            if removable_item.upper() in final_item["item_name"].upper():
                items.remove(final_item)

    return items


app = Flask(__name__)


@app.route('/', methods=['POST'])
def Start():
    return json.dumps(run_update_analysis())


if (__name__ == '__main__'):
    app.run(host='0.0.0.0', port=5002)
