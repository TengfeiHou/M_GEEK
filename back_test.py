"""
查询

"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#1.设置数据库的配置信息
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:ayhtf123@127.0.0.1:3306/yewuyuan"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#2.创建SQLalchemy对象,关联app
db = SQLAlchemy(app)

#3.编写模型类
#角色(一方)
class yewuyuan(db.Model):
    __tablename__ = "yewuyuan"
    id = db.Column(db.Integer,primary_key=True)
    bianhao = db.Column(db.String(10))
    x = db.Column(db.DECIMAL(10,2))
    y = db.Column(db.DECIMAL(10,2))

    #如果一个类继承自object那么重写__str__方法即可, 如果是继承自db.Model那么需要重写__repr__方法
    def __repr__(self):
        return "<yewuyuan:%s,%s,%s>"%(self.bianhao,self.x,self.y)

@app.route('/')
def hello_world():

    return "helloworld"

if __name__ == '__main__':

    tmp = yewuyuan.query.filter(yewuyuan.x< 10,yewuyuan.x>9 ,yewuyuan.y<200 ,yewuyuan.y>199).all()
    print(tmp[0],tmp[0].x)
    app.run(debug=True)