import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/clubs/920379/activities"

payload = {
    'client_id': "115482",
    'client_secret': '072cec1efffcbea77b4624dc81131860263249b5',
    'refresh_token': 'ba1dd4536f3d6b2a66cbffe16a51c46c51289a08',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + '8fb54422c4dcca968b40da4f55f4f23245c89d07'}
param = {'id':920379, 'per_page': 100, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset)
