import requests
import base64
import asyncio
import time
client_secret = "f".join(["4e835e0801374","e5a3313755b1","bb4c9"])
client_id = "f".join(["67926443640b4e89904","41669069e61c"])

# headers = {
#     "Authorization": "Bearer my_access_token"
# }

# response = requests.get("https://api.example.com/data", headers=headers)
currentAccessToken = ""
timeGotten = 0
async def getToken():
    response = requests.post('https://accounts.spotify.com/api/token',
    params={
      'grant_type': 'client_credentials',
    },
    headers= {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': 'Basic ' + (base64.b64encode((client_id + ':' + client_secret).encode('utf-8')).decode('utf-8')),
    })

    token = response.json()["access_token"]
    global timeGotten,currentAccessToken
    timeGotten = time.time()
    currentAccessToken = token
async def getCurrentToken():
    if time.time()-timeGotten > 3000:
        await getToken()
    return currentAccessToken
async def getSong(songTitle,artist):
    response = requests.get('https://api.spotify.com/v1/search',
    params={
      'q': f'track:{songTitle} artist:{artist}',
      'type': "track",
      "limit":1,
      "offset":0
    },
    headers= {
      'Authorization': ('Bearer ' + await getCurrentToken()),
    })
    if response.status_code != 200:
        print(response)
        return {}
    result = response.json()
    return result
async def getAlbum(albumTitle,artist):
    response = requests.get('https://api.spotify.com/v1/search',
    params={
      'q': f'album:{albumTitle} artist:{artist}',
      'type': "album",
      "limit":1,
      "offset":0
    },
    headers= {
      'Authorization': ('Bearer ' + await getCurrentToken()),
    })
    if response.status_code != 200:
        print(response)
        return {}
    result = response.json()
    return result