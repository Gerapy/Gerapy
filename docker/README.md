### RUN Gerapy from Docker

```
# pull Gerapy images

docker pull thsheep/gerapy:master

# RUN

docker run -d --name=gerapy --restart=always -v {The absolute path to your project}:/app/gerapy -p 8000:8000 thsheep/gerapy:master

# docker run -d --name=gerapy --restart=always -v /root/test:/app/gerapy -p 8000:8000 thsheep/gerapy:master
```

This Docker contains the following pip packages:
* cryptography>=2.1.1
* docopt
* django>=1.11
* django-cors-headers
* jinja2
* scrapy>=1.4.0
* scrapy-redis==0.6.8
* scrapy-splash
* python-scrapyd-api
* redis
* requests>=2.14.0
* pymongo>=3.2.0
* pymysql
* selenium
* setproctitle
* apscheduler
* DbUtils
* pika
* celery[redis,auth,msgpack]
* gerapy

If you need pip package, not in it; you need to build Docker

1、Write the package name to requirements.txt

2、RUN

```
docker build -t {docker_name}:{version}  .
```

###### Example:

```
docker build -t thsheep/gerapy:master .
```


### Install Docker


```
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

sudo yum makecache fast

sudo yum -y install docker-ce

##Optional add accelerator（Get it from here：https://www.daocloud.io/mirror）

systemctl restart docker

```