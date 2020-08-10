from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import json
import threading
import time
import numpy as np
from scipy.spatial.distance import cdist
from collections import defaultdict
import gc


#multithread global var
res_all = dict()


 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ayhtf123@127.0.0.1:3306/yewuyuan"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 200

db = SQLAlchemy(app)

#业务员类
class yewuyuan(db.Model):
    __tablename__ = "yewuyuan"
    id = db.Column(db.Integer,primary_key=True)
    bianhao = db.Column(db.String(10))
    x = db.Column(db.DECIMAL(10,2))
    y = db.Column(db.DECIMAL(10,2))

    #如果一个类继承自object那么重写__str__方法即可, 如果是继承自db.Model那么需要重写__repr__方法
    def __repr__(self):
        return "<yewuyuan:%s,%s,%s>"%(self.bianhao,self.x,self.y)


@app.route('/2',methods = ["POST"])
def danxiancheng():
    if  not request.data:   #检测是否有数据
        return ('fail')
    pos = request.data.decode('utf-8')
    pos_json = json.loads(pos)
    # print('!!',pos_json)
    # print(pos_json['x'])
    # print(pos_json['y'])
    x = pos_json['x']
    y = pos_json['y']
    

    tmp = []
    eps = 1
    while not tmp:
        
        x1 = str(float(x)+eps)
        x2 = str(float(x)-eps)
        y1 = str(float(y)+eps)
        y2 = str(float(y)-eps)
        print("finding.....")
        tmp = yewuyuan.query.filter(yewuyuan.x < x1,\
                                    yewuyuan.x > x2 ,\
                                    yewuyuan.y < y1,\
                                    yewuyuan.y > y2).all()
        eps*=10
    distance = [0]*len(tmp)
    for i in range(len(distance)):
        distance[i] = (float(tmp[i].x)-float(x))**2+(float(tmp[i].y)-float(y))**2
    index = distance.index(min(distance))

    res = dict()
    res['bianhao'] = tmp[index].bianhao
    res['x'] = str(tmp[index].x)
    res['y'] = str(tmp[index].y)    
    #print('???????/',res)
    return jsonify(res)


@app.route('/3',methods = ["POST"])
def duoxiancheng():
    if  not request.data:   #检测是否有数据
        return ('fail')
    pos = request.data.decode('utf-8')
    pos_json = json.loads(pos)
    N = 100
    # 聚类
    k = 50000 #距离
    zuobiao = [[0,0]for _ in range(N)]
    point  = set([i for i in range(N)])
    juli = [[0]*N for _ in range(N)]
    julei = []
    minn = 20000000
    minn_index = [-1,-1]
    for i in range(N):
        zuobiao[i] = [float(pos_json[str(i)]['x']),float(pos_json[str(i)]['y'])]
    for i in range(len(zuobiao)-1):
        for j in range(i+1,len(zuobiao)):
            juli[i][j] = (zuobiao[i][0]-zuobiao[j][0])**2+(zuobiao[i][1]-zuobiao[j][1])**2
            if   juli[i][j] < minn:
                minn_index = [i,j]
                minn = juli[i][j]
    julei = [set(minn_index)]
    point.remove(minn_index[0])
    point.remove(minn_index[1])
    while point:
        tmp = point.pop()
        ok = 1
        for julei1 in julei:
            okk=1
            for jj in julei1:
                a = min(jj,tmp)
                b = max(jj,tmp)
                if juli[a][b]>k:
                    okk = 0
                    break
            if okk == 1:
                ok= 0
                julei1.add(tmp)
                break
            else:
                continue
        if ok == 1:
            julei.append(set([tmp]))
    print("有多少类",len(julei))

    #得到每个聚类的边界，进行表的搜索和储存
    julei_bianjie = []
    for i in julei:
        x_min = 100000
        y_min = 100000
        x_max = -1
        y_max = -1
        for j in i :
            x_min = min(x_min,zuobiao[j][0])
            x_max = max(x_max,zuobiao[j][0])
            y_min = min(y_min,zuobiao[j][1])
            y_max = max(y_max,zuobiao[j][1])
        julei_bianjie.append([x_min,y_min,x_max,y_max])
    #print(julei_bianjie)
    

    ## 对其中一个聚类进行候选节点搜索
    def jujulei(index):
        tmp = []
        eps = 1
        while len(tmp)<len(julei[index]):
            x1 = julei_bianjie[index][0]-eps
            y1 = julei_bianjie[index][1]-eps
            x2 = julei_bianjie[index][2]+eps
            y2 = julei_bianjie[index][3]+eps

            print("finding")
            tic = time.time()
            tmp = yewuyuan.query.filter(yewuyuan.x > x1,\
                                        yewuyuan.x < x2 ,\
                                        yewuyuan.y > y1,\
                                        yewuyuan.y < y2).all()
            eps*=10
        #print(len(tmp),tmp[0])
        print(time.time()-tic)
        
        #找到候选点之后 利用矩阵进行距离计算


        fujin_point   = [[0,0] for _ in range(len(tmp))]
        fujin_bianhao = [None]*len(tmp)
        mubiao_point  = [[0,0]for _ in range(len(julei[index]))]
        mubiao_bianhao= [None]*len(julei[index])

        for i,ii in enumerate(tmp):
            fujin_point[i] = [float(ii.x),float(ii.y)]
            fujin_bianhao[i] = ii.bianhao

        for i,ii in enumerate(julei[index]):
            mubiao_point[i] = [zuobiao[ii][0],zuobiao[ii][1]]
            mubiao_bianhao[i] = ii
        #print('载入numpy')



        #获得距离矩阵
        dis = cdist(mubiao_point,fujin_point,metric='euclidean')
        pipei1 = defaultdict(list) 
        pipei2 = defaultdict(list) 


        # 或者距离最小的对应
        dis_min = dis.argmin(axis =1 )
        #print(len(dis_min),dis_min)
        for i in range(len(dis_min)):
            pipei1[i].append(dis_min[i])
            pipei2[dis_min[i]].append(i)
        #print("pipei1",pipei1)
        #print("pipei2",pipei2)


        #解决冲突
        chongtu = []
        done = dict()

        #把合适的都挑出来 剩下冲突集合们
        for i in pipei2:
            if len(pipei2[i]) == 1:
                done[pipei2[i][0]] = i
                #print(type(i))
                dis[::,i] = 1000000000
            else:
                print("zouna????????????/")
                chongtu.append([i,pipei2[i]])

        #print("chongtu",chongtu)
        while  chongtu:     #冲突集合
            
            i,chongtus = chongtu.pop() #处理其中集合
            #print("chongtussssssssssss",chongtus)

            while chongtus:
                ct = chongtus.pop() #拿出冲突节点
                done[ct] = dis[ct].argmin()
                dis[::,done[ct]]= 1000000000
        del dis
        gc.collect()
        global res_all
        for i in done:
            res_all[mubiao_bianhao[i]] = {'bianhao':fujin_bianhao[done[i]],'x':fujin_point[done[i]][0],'y':fujin_point[done[i]][1]}
    
 
    t = []
    for i in range(len(julei)):        

        t.append(threading.Thread(target=jujulei,name=i,args=(i,)))

    for i in range(len(julei)):         
        t[i].start()
    for i in range(len(julei)):         
        t[i].join()
    #print(res_all)
    return jsonify(res_all)

@app.route('/4_1',methods = ["POST"])
def danxiancheng():
    if  not request.data:   #检测是否有数据
        return ('fail')
    
    pos = request.data.decode('utf-8')
    pos_json = json.loads(pos)
    #print(pos_json)
    try :
        connc = pymysql.Connect(
            user = 'root',
            password='ayhtf123',
            database = 'yewuyuan',
            charset = 'utf8'
        )
        
        cur = connc.cursor()
        try:
            cur.execute("drop table yonghu;")
        except:
            print("还没用户表表")
            pass

        cur.execute("create table yonghu(id int primary key not null  auto_increment,bianhao char(10) not null , x decimal(10,2) not null,y decimal(10,2) not null);")
        
        sql = "insert into yonghu values (%s,%s,%s,%s)"
        for i in pos_json:
        
            b = ['0',pos_json[i]['bianhao'],pos_json[i]['x'],pos_json[i]['y']]
            #print(b)
    

            cur.execute(sql,b)
            
        connc.commit()
    except Exception as e:
        print(e)
        connc.rollback()
    finally :
        cur.close()
        connc.close()
    print('done')
    return "用户登记成功"

if __name__=='__main__':
    app.run(debug=True)