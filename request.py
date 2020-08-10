import requests,json
 
#print('?')
data = {
    'x':"1.11",
    'y':"200.22"
}
url = 'http://127.0.0.1:5000/2'
 
r = requests.post(url,data=json.dumps(data))
#print('??')
tmp = r.json()
print("编号是："+tmp['bianhao']+","+"坐标是：("+tmp['x']+","+tmp['y']+")")