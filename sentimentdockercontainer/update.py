from flask import Flask, request, Response, abort
import pandas as pd
import numpy as np 
import json 

print("Starting update analysis.")

with open("text6.txt") as f:
    content = f.readlines()
line2 = "Test"
df_items =  pd.read_csv("result.csv")

def RunUpdateAnalysis(text):
    for line in text:
        for item in df_items["name"].unique():
            if item.upper() in line.upper():
                line2 = "Item: " + item +" Line: " + line
                return line2
                print(" ")
                if "DROP-RATE" in line.upper():
    
                    line2 = line+" Drop-rate change"
                elif "INCREASED" in line.upper():
                    if "DROP" in line.upper():
                        line2=item + ": Will probably go down"
                elif "DECREASED" in line.upper():
                    line2=item + ": Will probably go up"
                 

app = Flask(__name__)

@app.route('/run-updatescan', methods=['POST'])
def Start():
	
		
	string = request.data
        
	return string
	
if (__name__ == '__main__'):
	app.run(port=5000)
