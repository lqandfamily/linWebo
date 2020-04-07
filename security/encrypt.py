"""
加密模块
1.哈希(hash)是使用算法将任意大小的数据映射到固定长度的过程
2.加密是一种双向功能，能解密，而散列是一种单向功能，尽管技术上可以反向
  散列值，但所需要的计算能力使其不可行
3.加密是为了保护传输中的数据，而散列是为了验证数据没有被更改并且是真实的
4.盐是固定长度的加密强度的随机值，将其添加到哈希的输入中为每一个输入创建唯一哈希
  添加盐可以使密码哈希输出唯一，即使对于采用通用密码的用户也是如此
"""

import bcrypt


def encrypt(pwd):
    salt = bcrypt.gensalt()
    mHashed = bcrypt.hashpw(bytes(pwd, encoding='utf-8'), salt)
    strHashed = str(mHashed)[2:-1]
    return strHashed


def encryptCheck(pwd, _hashed):
    """
    验证密码
    需要明文和已经hash的密文
    """
    bytesPwd = bytes(pwd, encoding='utf-8')
    bytesHashed = bytes(_hashed, encoding='utf-8')
    if bcrypt.checkpw(bytesPwd, bytesHashed):
        return True
    return False


if __name__ == "__main__":
    password = "xjf121"
    hashed = encrypt(password)
    print("加密后:" + str(hashed))
    if encryptCheck("xjf121", hashed):
        print("匹配")
    else:
        print("失败")
