import requests,json
import random
import time
 
# def no2():  #第二题接口
#     x = round(random.random()*1000,2)
#     y = round(random.random()*1000,2)
#     print("当前业务员坐标为："+str(x)+","+str(y))
#     data = {
#         'x':str(x),
#         'y':str(y)
#     }
#     url = 'http://127.0.0.1:5000/2'
    
#     r = requests.post(url,data=json.dumps(data))
#     #print('??')
#     tmp = r.json()
#     print("编号是："+tmp['bianhao']+","+"坐标是：("+tmp['x']+","+tmp['y']+")")

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

def no4_1():  #第4题接口
    #print(time.time())
    data = dict()
    #xx = round(random.random()*1000,2)
    #yy = round(random.random()*1000,2)
    print("输入。。。。。。")
    for i in range(15):
        x = round(random.random()*1000,2)#xx
        y = round(random.random()*1000,2)#yy

        print("当前第"+str(i)+"个用户编号为："+str(i)+"坐标为："+str(x)+","+str(y))
        data[str(i)] = {
            'bianhao':str(i),
            'x':str(x),
            'y':str(y)
        }
    url = 'http://127.0.0.1:5000/4_1'
    
    r = requests.post(url,data=json.dumps(data))
    print(r.text)
    return 

def no4_2():  #第4题接口
    #print(time.time())
    data = dict()
    #xx = round(random.random()*1000,2)
    #yy = round(random.random()*1000,2)
    for i in range(10):
        x = round(random.random()*1000,2)#xx
        y = round(random.random()*1000,2)#yy
        print("当前第"+str(i)+"个业务员坐标为："+str(x)+","+str(y))
        data[str(i)] = {
            'x':str(x),
            'y':str(y)
        }
    url = 'http://127.0.0.1:5000/4_2'
    
    r = requests.post(url,data=json.dumps(data))
    #print('??')
    tmp_all = r.json()
    print(tmp_all)
    for i in tmp_all:
        print("第"+str(i)+"个业务员有"+str(len(tmp_all[i]))+"个用户分别是")
        for j in tmp_all[i]:
            tmp = tmp_all[i][j]
            print("编号是："+str(tmp['bianhao'])+"的用户,"+"坐标是：("+str(tmp['x'])+","+str(tmp['y'])+")")
    #print(time.time())

def main():
    no4_1()

    no4_2()


if __name__=="__main__":
    main()