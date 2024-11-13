import json
import requests
from pprint import pprint
 
prompt = """
your job is to convert input to a specific output.
Here's some examples:
example1:
    input:戴著帽子的人
    output:[person[hat]]
example2:
    input: 穿著背心的人
    output:[person[vest]]
please convert input `{context}` to specific output
only reply the output
"""
url = 'http://192.168.1.168:11434/api/chat'
json_data = json.dumps({
  "model": "qwen2.5:32b",
  "stream":False,
  "messages": [
    {
      "role": "user",
      "content": prompt.format(context="戴著帽子又穿著背心的人")
    }
  ]
})
response = requests.post(url, data=json_data)
pprint(response.json())