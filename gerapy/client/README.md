## CallScheduler FrontEnd

### Used Packages

- vue
- axios
- vue-router
- vuex
- font-awesome
- element-ui
- scss
- webpack
- mock

### Installation

#### Clone Repository

```shell
git clone ssh://xiaoice@xiaoice.visualstudio.com:22/DefaultCollection/Nautilus/_git/CallSchedulerFrontEnd
```

#### Install Node.js

Install [Node.js](https://nodejs.org/en/) Version 7 or Newer.

#### Install Packages

```
npm install
```

#### Run Server

```
npm run dev
```

### Structure

<pre>
├── build                     // 项目的 Webpack 配置文件
├── config                    // 项目配置目录
├── server                    // 项目开发的请求数据
├── src                       // 生产目录
│   ├── assets                // 一些资源文件
│   ├── common                // 通用文件、如工具类、状态码
│   ├── components            // 各种组件
│   ├── pages                 // 各种页面
│   ├── plugins               // 各种插件
│   ├── router                // 路由配置及map
│   ├── store                 // Vuex 状态管理器
│   ├── App.vue               // 根组件
│   ├── favicon.ico           // ico小图标
│   ├── index.html            // 项目入口文件
│   ├── main.js               // Webpack 编译入口文件，入口js
├── static                    // 静态资源，一般把不需要处理的文件可以放这里
├── .babelrc                  // babelrc配置文件
├── .editorconfig             // 代码风格文件，前提是要你的编辑器支持
├── .gitignore                // 用于Git配置不需要加入版本管理的文件
├── .postcssrc.js             // autoprefixer的配置文件
├── package.json              // 项目配置文件
</pre>

### Preview

![](https://ws3.sinaimg.cn/large/006tNc79gy1fgn690en5oj31d90sc7ck.jpg)

![](https://ws4.sinaimg.cn/large/006tNc79gy1fgn69vom3wj31d90sc76u.jpg)

![](https://ws4.sinaimg.cn/large/006tNc79gy1fgn6ae924wj31d90sctbn.jpg)