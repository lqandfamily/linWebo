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
  flask-cors
  ```
 - uwsgi配置
 uwsgi.ini位于项目根目录下，需要修改一下内容
    ```
    ＃ 项目目录
    chdir=/home/blue/PycharmProjects/weboAnalyze
    # 虚拟环境
    home=/home/blue/PycharmProjects/weboAnalyze/venv
    ```


###  开始安装

- 初始化数据库，建立所需要的表

  - 成功后输出“创建表成功！“
  - 若一直卡住，请停止连接到当前数据库的所有程序，包括爬取服务，web服务

  ```bash
  ./install.sh
  成功后输出“建表成功!”
  ```

- 推荐启动方式uwsgi配合nginx

  - python安装uWSGI模块

  - uwsig.ini配置，前面已经做了

  - nginx配置文件

    ```
        server {                                                                       
            listen 80;                   # 服务器监听端口                                                 
            server_name 127.0.0.1 # 这里写你的域名或者公网IP                                                    
            charset      utf-8;          # 编码                                                  
            client_max_body_size 75M;    # 之前写的关于GET和POST的区别，这里应该是原因之一吧                                                   
    
            location / {                                                                   
                include uwsgi_params;         # 导入uwsgi配置                                            
                uwsgi_pass unix:/home/blue/PycharmProjects/weboAnalyze/uwsgi/uwsgi.sock;               
            }                                                                              
        }
    }
    ```

    

- 启动web服务方式二(不建议使用，建议uwsgi配合nginx)

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
  
    