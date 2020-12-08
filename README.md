# CRUD模板网站

> 一个基于Django + Vue.js 的培训项目

## 下载项目代码

``` bash
# 记得先安装Git，然后下载代码
git clone git@github.com:Ray57468260/crud-example.git
```

## 安装Python环境
``` bash
# python3.6 安装bz2依赖库
wget https://www.sourceware.org/pub/bzip2/bzip2-latest.tar.gz
tar -zxf  bzip2-1.0.6.tar.gz 
cd bzip2-1.0.6  
make -f  Makefile-libbz2_so 
make && make install

# 重新编译python3.6

# 安装virtualenv 沙盒环境包
pip install virtualenv

# 创建虚拟环境（进入项目根目录）
virtualenv env -p python3.6 # python3.6指向上面重新编译的版本，换成你的实际路径

# 安装依赖
pip install -r requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.douban.com
``` 

## 安装前端环境
``` bash
# 安装node和npm

# 安装vuejs和其他依赖包（进入项目根目录）
cd appfront/
npm install
``` 

## 配置MySQL环境
``` mysql
# 安装MySQL5.7

# 设置root用户密码：37wan#&&#

# 放开本地访问权限
ALTER USER 'root'@'localhost' IDENTIFIED BY '37wan#&&#';

# 进入mysql，创建数据库
CREATE DATABASE crud;

# 创建表
CREATE TABLE `app_crudexample` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `field1` varchar(255) NOT NULL, `field2` varchar(255) NOT NULL, `field3` varchar(255) NOT NULL, `createTime` datetime(6) NOT NULL, `updateTime` datetime(6) NOT NULL);
``` 

## 启动服务器
``` bash
# 启动前端服务器，监听端口3000
cd appfront/
npm run start

# 启动后端服务器，监听端口8000
cd crud/
python manager.py runserver 0:8000

# 清空防火墙规则（危险操作，仅限测试）
iptables --flush
``` 

## 测试
打开浏览器，访问：
http://你的IP:3000
如果一切顺利，你能看到一个简单的页面。