from flask import Flask, request, Response
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import json

print("Starting update analysis.")

with open("Text6.txt") as f:
    content = f.readlines()
line2 = "Test"
df_items = pd.read_csv("result.csv")


def run_update_analysis():
    response = requests.post('http://192.168.27.170/graphql', json={'query': '''
    {
    updates {
        id
        title
        date
        content
    }
    }
    '''})

    last_update = json.loads(response.text)["data"]["updates"][0]
    items = []
    for line in last_update['content'].splitlines():
        for item in df_items["name"].unique():
            if item.upper() in line.upper():
                item_change = ''
                if "DROP-RATE" in line.upper():
                    item_change = "drop-rate change"
                elif "INCREASED" in line.upper():
                    if "DROP" in line.upper():
                        item_change = "price decrease"
                elif "DECREASED" in line.upper():
                    if "DROP" in line.upper():
                        item_change = "price increase"

                items.append({'item_name': str(
                    item), 'line': str(line), 'change': item_change})
    return items


app = Flask(__name__)


@app.route('/run-updatescan', methods=['POST'])
def Start():
    return json.dumps(run_update_analysis())


if (__name__ == '__main__'):
    app.run(port=5000)
