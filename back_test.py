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
import pymysql
from tqdm import tqdm


#multithread global var
res_all = dict()


 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ayhtf123@127.0.0.1:3306/yewuyuan"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 200

db = SQLAlchemy(app)

#业务员类改为用户类，建立用户表
class yonghu(db.Model):
    __tablename__ = "yonghu"
    id = db.Column(db.Integer,primary_key=True)
    bianhao = db.Column(db.String(10))
    x = db.Column(db.DECIMAL(10,2))
    y = db.Column(db.DECIMAL(10,2))

    #如果一个类继承自object那么重写__str__方法即可, 如果是继承自db.Model那么需要重写__repr__方法
    def __repr__(self):
        return "<yonghu:%s,%s,%s>"%(self.bianhao,self.x,self.y)


@app.route('/4_1',methods = ["POST"])
def NO41():
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
            print("还没用户表")
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

@app.route('/4_2',methods = ["POST"])
def NO42():
    if  not request.data:   #检测是否有数据
        return ('fail')
    res_all4 = {}
    pos = request.data.decode('utf-8')
    ywy_1 = json.loads(pos)
    yh_1 = yonghu.query.all()

    # print(ywy)
    # print(yh)
    #把格式都变成list[id(用户：编号),x,y] int,float float
    # ywy : {'0': {'x': '141.73', 'y': '359.96'}
    # yonghu: <yonghu:8,573.00,188.44>

    ywy = []
    for i in ywy_1:
        ywy.append([int(i),float(ywy_1[i]['x']),float(ywy_1[i]['y'])])

    yh = []
    for i in yh_1:
        yh.append([int(i.bianhao),float(i.x),float(i.y)])

    #print(ywy)
    #print(yh)
    yh_point   = [[0,0] for _ in range(len(yh))]
    yh_bianhao = [None]*len(yh)
    ywy_point  = [[0,0]for _ in range(len(ywy))]
    ywy_bianhao= [None]*len(ywy)


    #[1, 777.43, 989.85]
    for i in range(len(yh)):
        yh_point[i] = yh[i][1:]
        yh_bianhao[i] = yh[i][0]

    for i in range(len(ywy)):
        ywy_point[i] = ywy[i][1:]
        ywy_bianhao[i] = ywy[i][0]
    
    
    print('载入numpy')



    #获得距离矩阵
    dis = cdist(ywy_point,yh_point,metric='euclidean')

    dis_i_j = [0 ]*150

    for i in range(len(dis)):
        for j in range(len(dis[0])):
            dis_i_j[i*len(dis[0])+j] = [dis[i][j],i,j]
    dis_i_j.sort()
        
    naive = defaultdict(list)

    # 先把业务员每人分配一个用户进行服务
    ywy_set = set([i for i in range(10)])
    yh_set = set([i for i in range(15)])
    
    #print('?',len(dis_i_j))

    while ywy_set:
        dd = dis_i_j.pop(0)
        if dd[1] in ywy_set and dd[2] in yh_set:
            naive[dd[1]].append(dd[2])
            ywy_set.remove(dd[1])
            yh_set.remove(dd[2])
    
    
    dis_i_j = [0 ]*150
    for i in range(len(dis)):
        for j in range(len(dis[0])):
            dis_i_j[i*len(dis[0])+j] = [dis[i][j],i,j]
    dis_i_j.sort()
        
    ywy_set = set([i for i in range(10)])
    
    while yh_set:
        dd = dis_i_j.pop(0)
        if dd[1] in ywy_set and dd[2] in yh_set:
            naive[dd[1]].append(dd[2])
            ywy_set.remove(dd[1])
            yh_set.remove(dd[2])

    #print(naive)        
    #print(yh_set)


    #输出对应关系
    for i in naive:
        for jj,j in enumerate(naive[i]):
            #print(jj,j)
            if jj == 0:
                res_all4[ywy_bianhao[i]] = {}
                res_all4[ywy_bianhao[i]][jj] = {'bianhao':yh_bianhao[j],'x':yh_point[j][0],'y':yh_point[j][1]}
            else:
                res_all4[ywy_bianhao[i]][jj] = {'bianhao':yh_bianhao[j],'x':yh_point[j][0],'y':yh_point[j][1]}

    #print("res_all4",res_all4)
    
    return jsonify(res_all4)
   





if __name__=='__main__':
    app.run(debug=True)