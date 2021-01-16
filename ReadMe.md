# read me

## 直接运行方法
下载 项目代码
git pull https://github.com/xuzhuolalala/qiniuinterface.git
测试使用 runserver 运行
python3 manage.py runserver 0.0.0.0:8000



## django + uwsgi  + nginx 部署

### 1.安装 python3 环境
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
tar -zxvf Python-3.6.3.tar.gz
tar -zxvf Python-3.6.3.tar.gz
cd Python-3.6.3
./configure
make  && make install

### 2.下载 项目代码
git pull https://github.com/xuzhuolalala/qiniuinterface.git
测试使用 runserver 运行
python3 manage.py runserver 0.0.0.0:8000
报错 django.core.exceptions.ImproperlyConfigured: SQLite 3.8.3 or later is required (found 3.7.17).  系统环境默认安装的 sqlite 版本过低
升级 sqlite
wget https://www.sqlite.org/2019/sqlite-autoconf-3270200.tar.gz
tar -zxvf sqlite-autoconf-3270200.tar.gz
cd sqlite-autoconf-3270200
./configure --prefix=/usr/local
make && make install
find /usr/ -name sqlite3
/usr/local/bin/sqlite3 --version   —新安装的
/usr/bin/sqlite3 --version	—系统自带
更新操作
mv /usr/bin/sqlite3  /usr/bin/sqlite3_old
ln -s /usr/local/bin/sqlite3   /usr/bin/sqlite3
~/.bashrc  文件新增： export LD_LIBRARY_PATH="/usr/local/lib"		—增加环境变量
source 〜/.bashrc
sqlite3 --version    —检查是否更新成功
重新运行  python3 manage.py runserver 0.0.0.0:8000  后成功

### 3.安装 uwsgi
pip3 install uwsgi
测试 uswgi
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"]
uwsgi –http :8001 –wsgi-file test.py  测试http://ip/  可以正常访问，说明uwsgi 安装成功
进入项目目录
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "qiniuinterface.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

uwsgi --http :8000 --chdir /root/qiniuinterface --module django_wsgi		运行 ok 

### 4.nginx 安装
yum install nginx
systemctl  start nginx  http://ip  访问 ok ，说明安装成功
nginx 与 uwsgi 互连
在 项目目录下新建文件 djangochina_socket.xml ，以配置文件的方式允许 uwsgi
<uwsgi>
    <http>:8000</http>											//正式环境建议修改为 <http>127.0.0.1:8000</http>  ，不对外暴露
    <chdir>/root/qiniuinterface</chdir>
    <module>django_wsgi</module>
    <processes>4</processes>
    <daemonize>/var/log/uwsgi/uwsgi.log</daemonize>
</uwsgi>
启动 uwsgi  uwsgi -x djangochina_socket.xml

修改 nginx 配置文件
在http{…}中的最后一行添加：
	server {

        listen   8001;
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

	location /index/ {
       		proxy_pass http://127.0.0.1:8000/index/;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        location /static/ {									//静态文件地址
            alias  /home/ubuntu/mysite/static/;
            index  index.html index.htm;
       }
systemctl start nginx 
http://ip:8001/index/  访问

### 5、关闭服务的方法
将uWSGi进程杀死即可。
sudo killall -9 uwsgi
systemctl stop nginx 
