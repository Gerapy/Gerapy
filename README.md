# Gerapy

Distributed Crawler Management Framework Based on Scrapy, Scrapyd, Scrapyd-Client, Scrapyd-API, Django and Vue.js.

## Support

Gerapy is developed over Python 3.x. Python 2.x will be supported later.

## Usage

Install Gerapy by pip:

```bash
pip3 install gerapy
```

After the installation, you need to do these things below to run Gerapy server:

If you have installed Gerapy successfully, you can use command `gerapy`. If not, check the installation.

First use this command to initialize the workspace:

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

Or you can configure host and port like this:

```
gerapy runserver 0.0.0.0:8888
```

Then it will run with public host and port 8888.

You can create a configurable project and then configure and generate code automatically.Also you can drag your Scrapy Project to `gerapy/projects` folder. Then refresh web, it will appear in the Project Index Page and comes to un-configurable, but you can edit this
project in the web interface.

As for the deploy, you can move to Deploy Page. Firstly you need to build your project and add client in the Client Index Page, then you can deploy the project by clicking button.

After the deployment, you can manage the job in Monitor Page.

## Docker

Just run this command:

```
docker run -d -v ~/gerapy:/app/gerapy -p 8000:8000 thsheep/gerapy:master
```

Then it will run at port 8000.

Command:

```
docker run -d -v <your_workspace>:/app/gerapy -p <public_port>:<container_port> thsheep/gerapy:master
```

Please specify your workspace to mount Gerapy workspace by `-v <your_workspace>:/app/gerapy` and specify server port by `-p <public_port>:<container_port>`.

If you run Gerapy by Docker, you can visit Gerapy website such as [http://localhost:8000](http://localhost:8000) and enjoy it, no need to do other initialzation things.

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
![](https://ws1.sinaimg.cn/large/0069RVTdgy1fv87ktrbocj30zx0nswfh.jpg)
![](https://ws1.sinaimg.cn/large/0069RVTdgy1fv87l6w3rrj310g0o1mxx.jpg)
![](https://ws4.sinaimg.cn/large/0069RVTdgy1fv87leaxgqj310f0pcwhg.jpg)

## TodoList

- [x] Add Visual Configuration of Spider with Previewing Website
- [x] Add Scrapyd Auth Management
- [ ] Add Automatic Python & Scrapyd Environment Deployment
- [ ] Add MongoDB & Redis & MySQL Monitor
- [x] Add Timed Task Scheduler

## Communication

If you have any questions or ideas, you can join this QQ Group:

![](https://ws2.sinaimg.cn/large/006tNc79gy1fno6qey8a3j307609k3zs.jpg)
