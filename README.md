# Gerapy

Distributed Management Framework Based on Scrapy and Scrapyd.

## Support

Gerapy is developed over Python 3.x. Python 2.x will be supported later.

## Installation

```bash
pip3 install gerapy
```

## Usage

After installing Gerapy, you can use command 'gerapy'. If not, check the installation.

Next use this command to initialize the workspace:

```bash
gerapy init
```

Now you will get a folder named `gerapy`.

Then cd to this folder, and run this command to initialize the Database:

```bash
cd gerapy
gerapy migrate
```

Next you can runserver by this command:

```bash
gerapy runserver
```

Then you can visit [http://localhost:8000](http://localhost:8000) to enjoy it.


You can create a configurable project and then configure and generate code automatically.

Also you can drag your Scrapy Project to `gerapy/projects` folder. Then refresh web, it
will appear in the Project Index Page and comes to un-configurable, but you can edit this
project in the web interface.

As for the deploy, you can move to Deploy Page. Firstly you need to build you project and 
add client, then you can deploy the project by clicking button.

After the deployment, you can manage the job in Scheduler Page.


## Preview

Client Management:

![](https://ws4.sinaimg.cn/large/006tKfTcly1fkbdxmxtg8j31kw0smak0.jpg)

Spider Monitor:

![](https://ws4.sinaimg.cn/large/006tKfTcly1fkbe2idj4tj31kw0skqfp.jpg)

Project Management:

![](https://ws2.sinaimg.cn/large/006tKfTcly1fkbebgjxguj31kw0l4jyp.jpg)

Project Edit:

![](https://ws1.sinaimg.cn/large/006tKfTcly1fkbe00vpakj31kw0qx7ez.jpg)

Project Deploy:

![](https://ws4.sinaimg.cn/large/006tKfTcly1fkbe3w2jrij31kw0shtgr.jpg)

Project Configuration:

![](https://ws2.sinaimg.cn/large/006tKfTcly1fkbe5aqerdj31kw0xggu0.jpg)