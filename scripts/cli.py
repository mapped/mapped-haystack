import requests
from pdb import set_trace as bp


hostname = "http://localhost:5000/haystack"


query = """ver:"3.0"
filter,limit
"temp and air",1000
"""

res = requests.post(hostname + "/read", data=query)
print(res)
output = res.text

with open('test.txt', 'w') as fp:
    fp.write(res.text)
