# coding:utf8
import sys
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, abort

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from flask_sqlalchemy import SQLAlchemy
from com.util.constant import URL
from com.util.timeHelper import timeHelper
from apscheduler.schedulers.blocking import BlockingScheduler
from com.util import constant

# 全局共享变量
app = Flask(__name__)
app.config.from_object(constant)
db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = 'city'
    cityname = db.Column(db.String(50), primary_key=True)
    introduction = db.Column(db.Text, nullable=True)
    scenic_time_crawl = db.Column(db.Date, nullable=True)
    lat = db.Column(db.String(50), nullable=True)
    lng = db.Column(db.String(50), nullable=True)
    hotel_time_crawl = db.Column(db.Date, nullable=True)
    food_time_crawl = db.Column(db.Date, nullable=True)

    def to_json(self):
        return {
            'cityname': self.cityname,
            'introduction': self.introduction,
            'scenic_time_crawl': self.scenic_time_crawl,
            'lat': self.lat,
            'lng': self.lng,
            'hotel_time_crawl': self.hotel_time_crawl,
            'food_time_crawl': self.food_time_crawl

        }


class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    food_name = db.Column(db.String(50))
    food_link = db.Column(db.Text, nullable=True)
    food_pic = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(50), db.ForeignKey('city.cityname'))

    def to_json(self):
        return {
            'food_name': self.food_name,
            'food_link': self.food_link,
            'food_pic': self.food_pic,
            'city': self.city
        }


class Hotel(db.Model):
    __tablename__ = 'hotel'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hotel_name = db.Column(db.String(25))
    city = db.Column(db.String(255), db.ForeignKey('city.cityname'), nullable=True)
    pic = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    types = db.Column(db.String(4), nullable=True)
    url = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    source = db.Column(db.String(20), nullable=True)

    def to_json(self):
        return {
            'hotel_name': self.hotel_name,
            'city': self.city,
            'pic': self.pic,
            'price': self.price,
            'types': self.types,
            'url': self.url,
            'address': self.address,
            'source': self.source

        }


class Senic_spot(db.Model):
    _tablename__ = 'senic_spot_name'
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    senic_spot_name = db.Column(db.String(50), nullable=True)
    introduction = db.Column(db.String(255), db.ForeignKey('city.cityname'), nullable=True)
    pic = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=True)
    types = db.Column(db.String(4), nullable=True)
    url = db.Column(db.Text, nullable=True)
    levels = db.Column(db.String(20), nullable=True)
    source = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(25), db.ForeignKey('city.cityname'), nullable=True)

    def to_json(self):
        return {
            'senic_spot_name': self.senic_spot_name,
            'introduction': self.introduction,
            'pic': self.pic,
            'price': self.price,
            'types': self.types,
            'url': self.url,
            'levels': self.levels,
            'source': self.source,
            'city': self.city

        }

        # 任务模型


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 名字
    name = db.Column(db.String(50), nullable=False)
    # 创建时间
    time = db.Column(db.DateTime, nullable=False)
    # 定时时间
    run_time = db.Column(db.DateTime, nullable=True)
    # 爬虫任务
    spider_type = db.Column(db.String(10), nullable=False)
    # 状态,0为未执行
    status = db.Column(db.Integer, nullable=True, default=0)
    # 爬虫类型,0是即时爬虫，1是定时爬虫，暂定
    type = db.Column(db.Integer, nullable=True, default=0)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'time': str(self.time),
            'run_time': self.run_time,
            'spider_task': self.spider_type,
            'status': self.status,
            'type': self.type
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account = db.Column(db.String(13), nullable=False)
    password = db.Column(db.String(50), nullable=False)


db.create_all()


# 跳转不同的页面逻辑判断
@app.route('/index/page')
def to_page():
    page = request.args.get('p')
    print page
    if page == '0':
        return render_template('index.html')
    elif page == '1':
        return render_template('now_spilder.html')
    elif page == '2':
        return render_template('frequency_splider.html')
    elif page == '3':
        return render_template('showdata.html')
    elif page == '4':
        return render_template('time_spilder.html')
    elif page == '5':
        return render_template('analy_data.html')
    elif page == '6':
        return render_template('time_analy_data.html')


# 跳转到登陆页面,检测提交方法
@app.route('/login', methods=['GET', 'POST'])
def to_login():
    if session.get('user_id') is not None:
        return render_template('index.html')
    elif request.method == 'GET':
        return render_template('login.html')
    else:
        # 获取前端传过来的用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')
        print username, password
        user = User.query.filter(User.account == username, User.password == password).first()
        if user:
            print user.id
            session['user_id'] = user.id
            return render_template('index.html')
        else:
            print '用户名和密码错误'
            return redirect(url_for('to_login'))


# 注销登录
@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}

    return {}


# 创建不同任务
@app.route(URL + 'addjob', methods=['POST'])
def addjob():
    # 获取是定时爬虫还是一次性爬虫
    spider_type = request.form.get('splider_type')
    # 获取爬虫任务
    spider_task = request.form.get('select_type')
    # 获取爬虫标题
    spider_title = request.form.get('task_name')
    # 时间
    spider_create_time = timeHelper().get_curtime()
    print spider_type + ' ' + spider_task + ' ' + spider_title + ' ' + spider_create_time
    # 根据爬虫类型，存入数据库,1000是一次性爬虫
    if spider_type == '0':
        task = Task(name=spider_title, spider_type=spider_task, time=spider_create_time)
    elif spider_type == '1':
        # 时间
        spider__time = request.form.get('task_time')
        task = Task(name=spider_title, spider_type=spider_task, type=spider_type, time=spider_create_time,
                    run_time=spider__time)
    # 添加爬虫任务
    db.session.add(task)
    db.session.commit()


# 显示任务,可以返回未执行的定时爬虫，一次爬虫
# 和执行完毕的定时爬虫和一次爬虫
@app.route(URL + 'showjob', methods=['get'])
def showjob():
    args = request.args.get('status')
    type = request.args.get('type')
    if type is None:
        type = 0
    print type
    # 默认type=0
    # type代表爬虫种类，args代表状态
    # 查询所有准备就绪的一次性爬虫
    result = Task.query.filter_by(status=args, type=type).all()
    temp = []
    if len(result) == 0:
        dict = {"message": "none"}
        return jsonify(dict)
    else:
        for x in result:
            temp.append(x.to_json())

        return jsonify(temp)


# 获取任务列表
@app.route(URL + 'queue', methods=['GET'])
def showQueue():
    # 简单返回任务的个数
    splider_list = []
    for x in scheduler.get_jobs():
        print '打印队列id-----'
        splider_list.append(x.id)
    dict = {"splider": splider_list}
    return jsonify(dict)


# 移除任务
@app.route(URL + 'pushjob', methods=['GET'])
def pushjob():
    id = request.args.get('id')
    scheduler.remove_job(id)


# 删除任务
@app.route(URL + 'deljob', methods=['GET'])
def deljob():
    id = request.args.get('id')
    print id
    try:
        result = Task.query.filter_by(id=id).first()
        print result.name
        db.session.delete(result)
        db.session.commit()
        # 定义删除成功后返回的命令
        # print '删除id为%s任务成功'%str(args)
        message = {"delmes": "ok"}
        return jsonify(message)

    except Exception as e:
        # print '删除id为%s任务失败'%str(args)
        print e.message
        message = {"delmes": "fail"}
        return jsonify(message)  # 修改任务

# 根据id获取爬虫配置信息
@app.route('/ycx/querybyid', methods=['GET'])
def scan2():
    args = int(request.args.get('id'))
    result = Task.query.filter_by(id=args).first()
    if result:
        return jsonify(result.to_json())
    else:
        dict = {"message": "none"}
        return jsonify(dict)  # 执行任务
@app.route(URL + 'startings', methods=['GET'])
def startjobs():
    from task import Spider_task
    id = request.args.get('id')
    print '获得启动定时任务传过来的id', id
    # 查询数据库，获取爬虫的配置信息
    result = Task.query.filter_by(id=id).first()
    if result:
        # 根据不同类型来即时启动或者定时启动
        # 获得爬虫的任务及启动时间
        print '开始打印result'
        print result
        time = result.run_time
        print time, " ---123"
        if time is not None:
            # 将爬虫添加到任务队列
            scheduler.add_job(func=Spider_task().taks, args=(id,), next_run_time=time, id=id)
            print '任务添加成功'

        else:
            print '-----------'
            scheduler.add_job(func=Spider_task().taks, args=(id,))
            print '任务启动成功'

        # 启动
        scheduler.start()
        return jsonify({"startmess": "ok"})


# 暂停任务弄
@app.route(URL + 'pause', methods=['GET'])
def pausejobs():
    id = request.args.get('id')
    scheduler.pause_job(id)
    return jsonify({"pausetmess": "ok"})


# 停止任务
@app.route(URL + 'stop', methods=['GET'])
def stopjobs():
    id = request.args.get('id')
    scheduler.resume_job(id)
    return jsonify({"stoptmess": "ok"})


# 登录
@app.route(URL + 'login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    app.run(host='0.0.0.0', threaded=True)
