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