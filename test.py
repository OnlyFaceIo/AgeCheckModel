import requests


url = 'http://127.0.0.1:8000/faceinfo'
data = open('tmp.jpg','rb').read()
r = requests.post(url,files={
    "img_file": data
    })
print(r.json())
