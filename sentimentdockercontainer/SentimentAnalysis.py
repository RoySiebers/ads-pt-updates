from flask import Flask, request, Response
import pandas as pd
import numpy as np 
import json 

print("Starting update analysis.")

with open("text6.txt") as f:
    content = f.readlines()

df_items =  pd.read_csv("result.csv")

def RunUpdateAnalysis(text):
    for line in text:
        for item in df_items["name"].unique():
            if item.upper() in line.upper():
                print("Item: " + item +" Line: " + line)
                print(" ")
                if "DROP-RATE" in line.upper():
    
                    print(line+" Drop-rate change" )
                elif "INCREASED" in line.upper():
                    if "DROP" in line.upper():
                        print(item + ": Will probably go down") 
                elif "DECREASED" in line.upper():
                    print(item + ": Will probably go up")

app = Flask(__name__)

@app.route('/run-updatescan', methods=['POST'])
def Start():
	if not request.get_json():
		abort(400)
		
	string = np.array(request.get_string())
	
	return Response(json.dumps(RunUpdateAnalysis(string)), mimetype='application/json')
	
if (__name__ == '__main__'):
	app.run(port=5000)
