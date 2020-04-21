import requests

url = 'http://127.0.0.1:5000/accounts/login/'
data = {"username":"siuweide", "password":123456}
res = requests.post(url, data=data).cookies

cookie = requests.utils.dict_from_cookiejar(res)
cookie = 'sessionid=' + cookie['sessionid']
cookies = {'Cookie': cookie}
url2 = 'http://127.0.0.1:5000/api/get_event_list/'

res2 = requests.get(url2,headers=cookies).text
print(res2)