import requests,json
import random
 
#print('?')
x = round(random.random()*1000,2)
y = round(random.random()*1000,2)
print("当前业务员坐标为："+str(x)+","+str(y))
data = {
    'x':str(x),
    'y':str(y)
}
url = 'http://127.0.0.1:5000/2'
 
r = requests.post(url,data=json.dumps(data))
#print('??')
tmp = r.json()
print("编号是："+tmp['bianhao']+","+"坐标是：("+tmp['x']+","+tmp['y']+")")