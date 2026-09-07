import uuid
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

user_agent = "android.zepeto_global/3.25.100 (android; U; Android OS 7.1.2 / API-25 (NRD90M/G9550ZHU1AQEE); id-ID; occ-ID; samsung SM-G988N)"
x_zepeto_duid = str(uuid.uuid4())
session = requests.Session()

find_url = "https://gw-napi.zepeto.io/FriendNicknameSearchWithFeedInfo"
keyword = input("ID ZPT: ")
payload = json.dumps({
    "size": 30,
    "cursor": "",
    "place": "home",
    "keyword": keyword
})
headers = {
    'Content-Type':
    'application/json',
    'Authorization':
    'Bearer 9LdQ88iIkoFDRo21xhFY/hQyZuzINjjBcu2oda8LvZeG39S+uiAkIfH0J6g+hcTPgE5bgn1lq7J5qMihaeq9cXxypXsDPqaJwsxRr2tidAw=\\1\\bS4qM83NhdSmhxT8M8rgBj3zBjPzEQ7XEm36'
}
response = session.request("POST", find_url, headers=headers, data=payload)

jsondata = response.json()

if 'result' in jsondata:
  result = jsondata['result'][0]
  user_id = result['userId']
  # print(user_id)


def follow_request(user_id):
  x_zepeto_duid = str(uuid.uuid4())
  device_id = str(uuid.uuid4())

  b_url = "https://gw-napi.zepeto.io/DeviceAuthenticationRequest"
  payload = {"deviceId": device_id}
  headers = {
      "X-Zepeto-Duid": x_zepeto_duid,
      "User-Agent": user_agent,
      "Content-Type": "application/json",
      "Accept-Language": "application/json; charset=utf-8",
      "Content-Length": "51",
  }
  response = session.post(b_url, headers=headers, data=json.dumps(payload))
  if response.status_code != 200:
    raise Exception("Device authentication failed")

  json_data = json.loads(response.text)
  auth_token = json_data.get("authToken")

  if not auth_token:
    # Retry up to max_attempts times if authToken is not received
    max_attempts = 5
    for _ in range(max_attempts):
      response = session.post(b_url, headers=headers, data=json.dumps(payload))
      if response.status_code != 200:
        raise Exception("Device authentication failed")

      json_data = json.loads(response.text)
      auth_token = json_data.get("authToken")

      if auth_token:
        break
    else:
      raise Exception("Failed to receive authToken after multiple attempts")

  accusr_url = 'https://gw-napi.zepeto.io/AccountUser_v5'
  payload = {
      'creatorAllItemsVersion': '_',
      'creatorHotItemGroupId': '_',
      'creatorHotItemsVersion': '_',
      'creatorNewItemsVersion': '_',
      'params': {
          'appVersion': '3.33.000',
          'itemVersion': '_',
          'language': '_',
          'platform': '_'
      },
      'timeZone': 'Asia/Jakarta'
  }
  headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent': user_agent,
      "X-Zepeto-Duid": x_zepeto_duid,
      "Authorization": "Bearer " + auth_token,
  }

  response = session.post(accusr_url, headers=headers, json=payload)
  if response.status_code == 200:
    modified_response = response.json()
    modified_response["isOfficialAccount"] = "true"
    modified_response["officialAccountType"] = "EVENT"
    modified_response["isGreeter"] = "true"
  else:
    print("Gagal menerima respons dari gw-napi.zepeto.io")

  savep_url = 'https://gw-napi.zepeto.io/SaveProfileRequest_v2'
  payload = {
      "job": "𝗯𝘂𝘀𝘆",
      "name": "𝗡𝗔 𝗦𝗧𝗢𝗥𝗘",
      "nationality": "",
      "statusMessage": "𝗻𝗮 𝘀𝘁𝗼𝗿𝗲"
  }
  headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent': user_agent,
      "X-Zepeto-Duid": x_zepeto_duid,
      "Authorization": "Bearer " + auth_token,
  }

  response = session.post(savep_url, headers=headers, json=payload)
  print(response.text)

  zepeto_codes = [
      'ZPT221', 'ZPT222', 'ZPT223', 'ZPT225', 'ZPT226', 'ZPT227', 'ZPT228',
      'ZPT229', 'ZPT230'
  ]
  random_zpt_code = random.choice(zepeto_codes)

  savepp_url = 'https://gw-napi.zepeto.io/CopyCharacterByHashcode'
  payload = {'hashCode': random_zpt_code, 'characterId': ''}
  headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent': user_agent,
      "X-Zepeto-Duid": x_zepeto_duid,
      "Authorization": "Bearer " + auth_token,
  }

  response = session.post(savepp_url, headers=headers, json=payload)

  c_url = 'https://gw-napi.zepeto.io/FollowRequest_v2'
  payload = {'followUserId': user_id}
  headers = {
      'Content-Type': 'application/json; charset=utf-8',
      'User-Agent': user_agent,
      "X-Zepeto-Duid": x_zepeto_duid,
      "Authorization": "Bearer " + auth_token,
  }

  response = session.post(c_url, headers=headers, json=payload)

  if response.status_code != 200:
    raise Exception("Follow request failed")

  print(response.text)


# Menggunakan ThreadPoolExecutor untuk memanggil fungsi follow_request dengan beberapa ID pengguna

user_id = user_id
jumlah_follow_request𝟬

success_count = 0
max_attempts = 10

# Proses 1
executor_1 = ThreadPoolExecutor(max_workers=100)
future_to_user_id_1 = {
    executor_1.submit(follow_request, user_id): user_id
    for _ in range(jumlah_follow_request)
} 100

# Gabungkan semua proses menjadi 1 array
all_futures = {**future_to_user_id_1}

# Collect results from all the executors
for future in as_completed(all_futures):
  try:
    future.result()
    success_count += 1
  except Exception as e:
    print(f"Error: {e}")
  finally:
    # Tembahkan delay proses 2 detik
    time.sleep(2)

print(f"Successful follow requests: {success_count}/{jumlah_follow_request}")
  
