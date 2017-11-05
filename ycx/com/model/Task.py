# coding:utf8
from untitled2 import db


# 任务模型
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #名字
    name = db.Column(db.String(50), nullable=False)
    #创建时间
    time = db.Column(db.DateTime, nullable=False)
    #定时时间
    run_time=db.Column(db.DateTime,nullable=True)
    #爬虫任务
    spider_type=db.Column(db.String(10),nullable=False)
    #状态,0为未执行
    status=db.Column(db.Integer,nullable=True,default=0)
    #爬虫类型,0是即时爬虫，1是定时爬虫，暂定
    type=db.Column(db.Integer,nullable=True,default=0)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': str(self.time),
            'run_time': self.run_time,
            'spider_task': self.spider_type,
            'status': self.status,
            'type':self.type
        }