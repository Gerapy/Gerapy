# 安装

Gerapy 支持 Python 3.x，不支持 Python 2。

安装命令：

```
pip3 install -U gerapy
```

安装完成之后可以直接调用 gerapy 命令：

```
gerapy
```

如果出现类似输出结果，证明安装成功：

```
Usage: gerapy [-v] [-h]  ...

Gerapy 0.9.1 - Distributed Crawler Management Framework

Optional arguments:
  -v, --version       Get version of Gerapy
  -h, --help          Show this help message and exit

Available commands:  
    init              Init workspace, default to gerapy
    initadmin         Create default super user admin
    runserver         Start Gerapy server
    migrate           Migrate database
    createsuperuser   Create a custom superuser
    makemigrations    Generate migrations for database
    generate          Generate Scrapy code for configurable project
    parse             Parse project for debugging
    loaddata          Load data from configs
    dumpdata          Dump data to configs
```

如果出现报错，欢迎到 [Gerapy Issues](https://github.com/Gerapy/Gerapy/issues) 搜索解决方案或者提 Issue，感谢您的支持。

