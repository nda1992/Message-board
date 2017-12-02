import shelve
from datetime import datetime
from flask import Flask,request,render_template,redirect,escape,Markup

application = Flask(__name__)
DATA_FILE = 'guestbook.dat'

def save_data(name,comment,create_at):
    #保存提交的数据
    #通过shelve模块打开数据库文件
    database = shelve.open(DATA_FILE)
    #如果数据库中没有greeting_list，就创建一个表
    if 'greeting_list' not in database:
        greeting_list = []
    else:
        #从数据库中获取数据
        greeting_list = database['greeting_list']
        #将提交的数据添加到表头
    greeting_list.insert(0,{
        'name':name,
        'comment':comment,
        'create_at':create_at,
    })
    #更新数据库
    database['greeting_list'] = greeting_list
    #关闭数据库
    database.close()

def load_data():
    #返回已经提交的数据
    #通过shelve模块打开数据库文件
    database = shelve.open(DATA_FILE)
    #返回greeting_list，如果没有返回空列表
    greeting_list = database.get('greeting_list',[])
    database.close()
    return greeting_list

# save_data('test','test comment',datetime.datetime(2017,11,30,10,0,0))
# load_data()

@application.route('/')
def index():
    '''
    首页
    使用模板显示页面
    :return:
    '''
    greeting_list = load_data()
    return render_template('index.html',greeting_list = greeting_list)
@application.route('/post',methods=['POST'])
def post():
    '''
    用于提交评论的URL
    :return:
    '''
    #获取已经提交的数据
    name = request.form.get('name')  #名字
    comment = request.form.get('comment')  #留言
    create_at = datetime.now()  #获取当前时间
    #保存数据
    save_data(name,comment,create_at)
    #保存后重定向页面
    return redirect('/')
@application.template_filter('nl2br')
def nl2br_filter(s):
    '''
    将换行符置换为br标签的模板过滤器
    :param s:
    :return:
    '''
    return escape(s).replace('\n',Markup('<br>'))
@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    return dt.strftime('%Y/%m/%d %H:%M:%S')
if __name__ =='__main__':
    application.run('127.0.0.1',8000,debug=True)