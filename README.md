## 安装前的准备

- 数据库

  数据库配置在webserver/db/dao/baseDao.py中，对应修改

  ```
  db = pymysql.connect("localhost", "root", "xxx", "demo", autocommit=1)
  ```

- Python模块

  ```
  xlwt
  bcrypt
  requests
  lxml
  schedule
  json
  flask
  pymysql
  ```

###  开始安装

- 初始化数据库，建立所需要的表

  - 成功后输出“创建表成功！“
  - 若一直卡住，请停止连接到当前数据库的所有程序，包括爬取服务，web服务

  ```bash
  ./install.sh
  成功后输出“建表成功!”
  ```

- 启动web服务

  ```
  ./start.sh
  ```

  - 默认端口在5000，外网可访问

  - 可以在webserver/server/app.py中配置(最后一行)

    ```
    if __name__ == '__main__':
        app.run(host="0.0.0.0", port=5000)
    ```

- 启动爬取服务

  ```
  ./startCrawl.sh
  ```

  - 可以在webserver\spider\scheduleTask.py中配置爬取间隔(网页后台上的爬取间隔设置暂不可用)
  
    ```
    schedule.every(10).minutes.do(job)
    # 其中10表示10个单位
    # minutes表示单位，还可选seconds,hours,days
    ```
  
    