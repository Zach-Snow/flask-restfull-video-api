import requests

BASE = "http://127.0.0.1:5000/"

# data = [
#   {"name": "you have got to be kidding me", "likes": 30, "views": 69000},
#  {"name": "you have to see to believe", "likes": 55, "views": 79000},
#  {"name": "you have to see to believe 2", "likes": 3323, "views": 59000},
# {"name": "you have to see to believe 6", "likes": 3323, "views": 59000}
# ]

# for i in range(len(data)):
#  response = requests.put(BASE + "video/"+ str(i), data[i])
#   print(response.json())

# response = requests.delete(BASE + "video/0")
# print(response)

# input()

response = requests.get(BASE + "videos")
print(response.json())
# input()
# response = requests.get(BASE + "video/3")
# print(response.json())
# input()
#response = requests.delete(BASE + "video/3")
#print(response.json())
#input()
#response = requests.get(BASE + "video/3")
#print(response.json())
