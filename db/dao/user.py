"""
User的数据库访问
添加
修改用户名，密码
删除
认证
"""
from db.dao.baseDao import db
from db.entity.user import User
from security.encrypt import encrypt, encryptCheck


class UserDao:
    __cursor = db.cursor()

    def ins(self, user):
        # 检查重名
        if self.selRepName(user):
            return False

        sqlIns = "insert into t_user values (default,%s,%s)"
        result = self.__cursor.execute(sqlIns, [user.username, encrypt(user.password)])
        db.commit()
        if result is None:
            return False
        else:
            # 设置新ID
            self.selId(user)
            return True

    def selAll(self):
        selSql = "select * from t_user;"
        self.__cursor.execute(selSql)
        result = self.__cursor.fetchall()
        if result is None:
            return None
        ll = []
        for it in result:
            user = User(it[0], it[1], None)
            ll.append(user)
        return ll

    def selRepName(self, user):
        """
        检查是否重名
        :return 重名返回True
        """
        sqlSel = "select id from t_user where username = %s"
        self.__cursor.execute(sqlSel, user.username)
        result = self.__cursor.fetchall()
        if len(result) != 0:
            return True
        return False

    def dbCheck(self, user):
        # 从数据库中读取已加密的密码字符串
        sqlCheck = "select password from t_user where username = %s;"
        self.__cursor.execute(sqlCheck, user.username)
        result = self.__cursor.fetchone()
        if result is None:
            return False
        # 检查密码是否正确
        if encryptCheck(user.password, result[0]):
            # 设置新ID
            self.selId(user)
            return True
        return False

    def upd(self, user):
        # 检查重名
        if self.selRepName(user):
            return False

        updSql = "update t_user set username = %s, password = %s where id = %s;"
        self.__cursor.execute(updSql, [user.username, encrypt(user.password), user.ID])
        db.commit()
        return True

    # 更新自己的用户信息
    def updSelf(self, user):
        updSql = "update t_user set username = %s, password = %s where id = %s;"
        self.__cursor.execute(updSql, [user.username, encrypt(user.password), user.ID])
        db.commit()
        return True

    def delete(self, ID):
        delSql = "delete from t_user where id = %s"
        self.__cursor.execute(delSql, ID)
        db.commit()
        return True

    def selId(self, user):
        selSql = "select id from t_user where username = %s;"
        self.__cursor.execute(selSql, user.username)
        result = self.__cursor.fetchone()
        if result is None:
            return False
        user.ID = result[0]
        return True


def testPwdCheck():
    u = User(0, "sksy", "1143")
    ud = UserDao()
    if ud.dbCheck(u):
        print("校验密码成功")
    else:
        print("校验密码失败")


def testModifyInfo():
    u = User(1, "sksy", "1143")
    ud = UserDao()
    ud.upd(u)


def testDel():
    u = User(2, "sksy", "1143")
    ud = UserDao()
    ud.delete(u)


def testAdd():
    u = User(0, "Blue", "12345")
    ud = UserDao()
    ud.ins(u)
    print("新的ID:" + str(u.ID))


def testGetId():
    u = User(0, "sksy", "1143")
    ud = UserDao()
    ud.selId(u)
    print("新的ID:" + str(u.ID))


def testSelAll():
    ud = UserDao()
    for u in ud.selAll():
        print(str(u.ID) + u.username)


if __name__ == "__main__":
    # testPwdCheck()
    # testDel()
    # testAdd()
    # testGetId()
    testSelAll()
