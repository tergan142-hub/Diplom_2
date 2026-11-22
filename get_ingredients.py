import requests

response = requests.get("https://stellarburgers.education-services.ru/api/ingredients")
for item in response.json()["data"]:
    print(item["_id"], item["name"])