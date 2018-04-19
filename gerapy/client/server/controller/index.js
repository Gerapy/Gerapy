var express = require('express')
var apiRouter = express.Router()
var axios = require('axios')
var base = require('./uri')
apiRouter.all(/api/, function(req, res) {
  axios({
    method: req.method,
    url: base.baseUrl + req.url,
    data: req.body,
  })
    .then(function(response) {
      res.json(response.data)
    })
    .catch(function(error) {
      console.log(error)
    });
})
module.exports = apiRouter
