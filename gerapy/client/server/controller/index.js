/**
 * Created by zzmhot on 2017/3/21.
 *
 * @author: zzmhot
 * @github: https://github.com/zzmhot
 * @email: zzmhot@163.com
 * @Date: 2017/3/21 10:49
 * @Copyright(©) 2017 by zzmhot.
 *
 */

var express = require('express')
var apiRouter = express.Router()
var axios = require('axios')
var base = require('./uri')
apiRouter.all(/api/, function(req, res) {
  axios({
    method: req.method,
    url: base.base_url + req.url,
    data: req.body
  })
    .then(function(response) {
      res.json(response.data)
    })
    .catch(function(error) {
      console.log(error)
    });
})
module.exports = apiRouter