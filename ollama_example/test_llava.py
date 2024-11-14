import base64
import json
import requests

url = "http://192.168.1.185:11434/api/generate"
image_path = "image.jpg"
image = open(image_path, "rb").read()
image = base64.b64encode(image).decode("utf-8")
data = json.dumps(
    {
        "prompt":"Please describe the image.",
        "model":"llava-llama3",
        "stream":False,
        "images":[image],
    }
)
res = requests.post(url, data=data)
print("res", res.json())
print("res", res.json()["response"])
