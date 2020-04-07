"""
User模型
"""


class User:

    def __init__(self, ID, username, password):
        self.ID = ID
        self.username = username
        self.password = password

    def modifyPwd(self, password):
        self.password = password
