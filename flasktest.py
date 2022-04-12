"""
flask
"""
import json

"""
python轻量级web框架
"""

import flask
from flask import *
from datetime import timedelta
#数据库
import pymysql

#创建flask程序
app = Flask(__name__,
            static_url_path='/static', #静态文件路径
            static_folder='static',
            template_folder='templates' #模板文件
            )

#配置加密字符串
app.config['SECRET_KEY']="key123"
#设置7天有效
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
#参数传递
@app.route('/get',methods=['GET'])
def a_page():
    user_name=request.args.get('uname')
    user_pass=request.args.get('upass')
    return 'this is a page %s ---------%s hahaha'%(user_name,user_pass)
    pass
# @app.route('/abc/<user_id>/<int:user_pass>')
# def a_page(user_id,user_pass):
#     return 'this is a page %s ---------%s hahaha'%(user_id,user_pass)
#     pass
@app.route('/post',methods=['POST'])
def b_page():
    user_name=request.form.get('uname')
    user_pass=request.form.get('upass')
    return 'this is a page %s ---------%s hahaha'%(user_name,user_pass)
    pass

#装饰器,关联路由
@app.route('/')
def index():
    return 'haha'
    pass

"""
参数传入,获取参数
request.method 获取请求类型
.headers 获得请求头
.path 获得路径
.full_path 获得完整请求
.baseurl
.url
.user_agent.platform
"""

"""
接口
"""
@app.route('/abc')
def c_page():
    #定义一个字典
    json_dict = {
        "name":"xiaoli",
        "age":"18",
        "score":"100"
    }
    #把字典转化为json字符串
    result = json.dumps(json_dict)
    #json转化为字典
    dict1=json.loads('{"age":"18", "name": "xiaoli", "score":"100"}')
    print(dict1["name"])
    return 'x'
    pass

#重定向
@app.route('/redirect')
def d_page():
    #站外重定向
    # return flask.redirect('http://www.baidu.com')

    #站内
    return flask.redirect(flask.url_for('test_page'))

    return 'x'
    pass

@app.route('/test')
def test1_page():
    #状态码会显示404,但是内容会照常显示
    return 'hello,this is test1',404
    pass

#404重定向
@app.errorhandler(404)
def page_not_found(e):
    return '你出错了',404
    pass

#url别名
@app.route('/woshihenchangdemingzi',endpoint='test2')
def test2_page():
    return 'hello,this is test2'
    pass
@app.route('/bieming')
def bieming_page():
    return flask.redirect(flask.url_for('test2'))
    pass

#异常
@app.route('/err')
def err_page():
    #主动抛出异常
    flask.abort(404)
    return 'err'
    pass

#html返回
@app.route('/html')
def html_page():
    return Response('<h1>haha nihao</h1>'
                    '<br><hr>'
                    '<h2>abc</h2>',200)
    pass

#模板,父类子类继承
@app.route('/mode')
def mode_page():
    return flask.render_template('zi1.html')
    pass

"""
jinja2模板
渲染

互动
{{x}}存放变量
{%...%}控制代码块
{#...#}注释
"""
#模板传参
@app.route('/cc/<id>')
def chuancan_page(id):
    #python参数进来都是string类型
    m_int = int(id)+20
    m_str = 'hahanihao'
    m_list = ['xm','xh','xl']
    # vip = 1
    # user_id = request.cookies.get('user_id')
    # vip = request.cookies.get('vip')
    user_id = session['user_id']
    vip = session['vip']
    return flask.render_template('tempa.html',mint=m_int,mstr=m_str,mlist=m_list,vip=vip,user_id=user_id)
    pass

#控制代码块




#过滤器
@app.template_filter('dore')
def do_reserver(li):
    temp = list(li)
    temp.reverse()
    return temp

"""
cookie
"""
@app.route('/cookie')
def cookie_page():
    response = flask.make_response('success')
    #设置cookie
    response.set_cookie('user_id','10',max_age=50)
    response.set_cookie('vip','0',max_age=50)
    return response
    pass

"""
session
"""
@app.route('/session')
def session_page():
    response = flask.make_response('success')
    #设置session
    session['user_id']='20'
    session['vip']='1'
    return response



#cookie登出
@app.route('/logoutcookie')
def logout_cookie():
    response = flask.make_response('exit')
    response.delete_cookie('user_id')
    response.delete_cookie('vip')
    return response
    pass
#session登出
@app.route('/logoutsession')
def logout_session():
    session.pop('user_id',None)
    session.pop('vip',None)
    #第二种方法
    # session['user_id']=False
    #session全清!
    session.clear()

    return 'logout'
    pass

#表单处理
@app.route('/test1')
def test1():
    return render_template('test1.html')
    pass
@app.route('/chuli',methods=['POST'])
def chuli():
    if request.method=='POST':
        username = request.form.get('uname')
        password = request.form.get('passwd')
        print('用户名提交了'+username+'密码提交了'+password)

    #打开数据库
    db = pymysql.connect(host='localhost',user='root',password='root',db='test')
    #创建游标对象
    cursor = db.cursor()
    #sql语句
    sql = 'select * from table1'
    #执行
    cursor.execute(sql)
    #确认
    db.commit()
    list1 = []
    # for i in range(3):
    #     data = cursor.fetchone()
    #     #取出来的是元组,可以转化为列表
    #     li=list(data)
    #     list1.append(li)
    #     # list1+=li
    # print(list1)
    # print(list1[1][1])
    # print('---------')
    #如果刚开始不知道数据库具体信息
    for temp in cursor.fetchall():
        print(temp)
        dict = {'name':temp[1],'pass':temp[2]}
        list1.append(dict)
    print(list1)

    # #增删改 把语句写里面就行
    # sql="""
    # INSERT INTO table1(username,password)VALUES('xw','3456789')
    # """
    # try:
    #     #执行sql
    #     cursor.execute(sql)
    #     #确认
    #     db.commit()
    # except:
    #     #执行失败就回滚
    #     db.rollback()

    db.close()

    result = json.dumps(list1,sort_keys=True,ensure_ascii=False)
    return render_template('chuli.html',list1=list1)
    # return result
    pass



if __name__ == '__main__':
    #不建议这么写
    #app.add_url_rule('/',index)
    app.run(host='0.0.0.0', port=8888, debug=True)
