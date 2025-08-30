import json
import os

conditions = os.path.join(os.path.dirname(__file__), "conditions.json")

with open(conditions, 'r', encoding='utf-8-sig') as file:
    data = json.load(file)

for i in range(len(data)):
    day = data[i]["day"]
    night = data[i]["night"]
    code = data[i]["code"]
    print(f"{code}: {night}")