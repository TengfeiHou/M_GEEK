import requests,json
import random
import time
 
def no2():  #第二题接口
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

# def no3():  #第三题接口
#     #print(time.time())
#     data = dict()
#     #xx = round(random.random()*1000,2)
#     #yy = round(random.random()*1000,2)
#     for i in range(100):
#         x = round(random.random()*1000,2)#xx
#         y = round(random.random()*1000,2)#yy
#         print("当前第"+str(i)+"个业务员坐标为："+str(x)+","+str(y))
#         data[str(i)] = {
#             'x':str(x),
#             'y':str(y)
#         }
#     url = 'http://127.0.0.1:5000/3'
    
#     r = requests.post(url,data=json.dumps(data))
#     #print('??')
#     tmp_all = r.json()
#     print(tmp_all)
#     for i in range(100):
#         tmp = tmp_all[str(i)]
#         print("第"+str(i)+"个业务员需要去找编号是："+tmp['bianhao']+"的用户,"+"坐标是：("+str(tmp['x'])+","+str(tmp['y'])+")")
#     #print(time.time())

def main():
    no2()

if __name__=="__main__":
    main()