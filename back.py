from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
import json
 
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ayhtf123@127.0.0.1:3306/yewuyuan"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
def danxiaocheng():
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


if __name__=='__main__':
    app.run(debug=True)