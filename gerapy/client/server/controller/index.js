var express = require('express')
var apiRouter = express.Router()
var axios = require('axios')
var base = require('./uri')

apiRouter.all(/api\/render/, function (req, res) {
  axios({
    method: req.method,
    url: base.baseUrl + req.url,
    data: req.body,
  }).then(function (response) {
    res.send(response.data)
  }).catch(function (error) {
    console.log(error)
  })
})
apiRouter.all(/api/, function (req, res) {
  axios({
    method: req.method,
    url: base.baseUrl + req.url,
    data: req.body,
  }).then(function (response) {
    res.json(response.data)
  }).catch(function (error) {
    console.log(error)
  })
})
apiRouter.all(/static\/dist\/.*\.js/, function (req, res) {
  axios({
    method: req.method,
    url: base.baseUrl + req.url,
    data: req.body,
  }).then(function (response) {
    res.type = function () {
      return this.set('Content-Type', 'text/javascript');
    }
    res.send(response.data)
  }).catch(function (error) {
    console.log(error)
  })
})

apiRouter.all(/static\/dist\/.*\.css/, function (req, res) {
  axios({
    method: req.method,
    url: base.baseUrl + req.url,
    data: req.body,
  }).then(function (response) {
    res.type = function () {
      return this.set('Content-Type', 'text/css');
    }
    res.send(response.data)
  }).catch(function (error) {
    console.log(error)
  })
})

module.exports = apiRouter
