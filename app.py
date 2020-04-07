import os, sys

sys.path.append(os.getcwd())

import json
from datetime import timedelta
from flask_cors import cross_origin, CORS
from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, jsonify, Response
from db.dao.user import UserDao
from db.dao.hostSpot import HostSpotDao, SpiderDataDao, SpiderDateEntity
from db.entity.hostSpot import HostSpotEntityJSONEncoder
from db.entity.user import User
from excel.SaveExcel import saveOne, saveSelWholeMany
from spider.crawlData import crawl

app = Flask(__name__)

# 秘钥
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 创建DAO
spiderDataDao = SpiderDataDao()
hostSpotDao = HostSpotDao()


@app.route("/")
def hi():
    return render_template("index.html")


# 登录
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        if not (username is None and password is None):
            user = User(0, username, password)
            userDao = UserDao()
            if userDao.dbCheck(user):
                session['username'] = username
                app.permanent_session_lifetime = timedelta(hours=12)
                return redirect(url_for('admin'))
        return render_template("login.html", loginError=True)


# 注销
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


# 注册
@app.route("/register", methods=["POST"])
def register():
    username = request.form['username']
    password = request.form['password']
    if not (username is None and password is None):
        user = User(0, username, password)
        userDao = UserDao()
        if userDao.ins(user):
            session['username'] = username
            app.permanent_session_lifetime = timedelta(hours=12)
            return redirect(url_for('admin'))
    return render_template("admin-user-manage.html", repateName=True)


# 修改信息
@app.route("/user/modifyInfo", methods=["POST"])
def modifyInfo():
    username = request.form['username']
    originPwd = request.form['origin-pwd']
    newPwd = request.form['new-pwd']
    if username is None or originPwd is None or newPwd is None:
        return "ERROR: 不能为空"
    user = User(0, session['username'], originPwd)
    userDao = UserDao()
    if userDao.dbCheck(user):
        user.username = username
        user.password = newPwd
        print(str(user.ID) + user.username + user.password)
        if userDao.updSelf(user):
            return redirect(url_for("login"))
        else:
            return "内部错误"
    else:
        return "密码错误!"


# 后台列表
@app.route("/admin/infoList")
def admin():
    if 'username' in session:
        ll = spiderDataDao.selAll()
        return render_template("admin-info-list.html", username=session['username'], spiderList=ll)
    else:
        return redirect(url_for('login'))


# 查看数据
@app.route("/admin/infoDetails/<ID>")
def infoDetails(ID):
    if 'username' in session:
        ll = hostSpotDao.selByOneDate(ID)
        return render_template("admin-info-details.html", infoDetails=ll, username=session['username'])
    return redirect(url_for('login'))


# 后台系统设置
@app.route("/admin/sysSetting")
def sysSetting():
    if 'username' in session:
        return render_template("admin-sys-setting.html", username=session['username'])
    return redirect(url_for('login'))


# 后台用户设置
@app.route("/admin/userSetting")
def userSetting():
    if 'username' in session:
        return render_template("admin-user-setting.html", username=session['username'])
    return redirect(url_for('login'))


# 用户管理
@app.route("/admin/manageUser")
def manageUser():
    if session['username'] != "admin":
        return redirect(url_for('admin'))
    userDao = UserDao()
    ll = userDao.selAll()
    return render_template("admin-user-manage.html", userList=ll, username=session['username'])


@app.route("/admin/deleteUser/<ID>")
def deleteMangeUser(ID):
    if session['username'] != "admin":
        return "无权限"
    userDao = UserDao()
    userDao.delete(ID)
    return redirect(url_for("manageUser"))


# 首页实时数据
@app.route("/curData")
# @cross_origin()
def indexCurData():
    ll = crawl()
    return Response(json.dumps(ll[0:10], cls=HostSpotEntityJSONEncoder), mimetype='application/json')


# 免责声明
@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html")


# 单个文件下载
@app.route("/admin/download/<timeId>")
def downloadOneExcel(timeId):
    if 'username' in session:
        # 保存文件
        saveOne(timeId)
        # 下载文件
        crawlDate = spiderDataDao.selCrawlTime(timeId)
        crawlDate = crawlDate.replace(" ", "_").replace(":", '-')
        return send_from_directory(os.getcwd(), str(crawlDate) + ".xls", as_attachment=True)
    else:
        return redirect(url_for("login"))


# 多个文件下载
@app.route("/admin/downloads/", methods=["POST"])
def downloadManyExcel():
    if 'username' in session:
        # 获取下载列表
        downloadList = request.form.getlist("infoCheckbox")
        if not downloadList:
            return redirect(url_for("admin"))
        # 转为int
        for i in range(len(downloadList)):
            downloadList[i] = int(downloadList[i])
        # 保存文件
        saveSelWholeMany(downloadList)
        # 下载文件
        return send_from_directory(os.getcwd(), "selected_all.xls", as_attachment=True)
    else:
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
    CORS(app)
