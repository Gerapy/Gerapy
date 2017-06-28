
/**
 * 时间格式化函数
 * 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
 * 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
 *
 * @param {Date||number} date Date对象或者时间戳
 * @param {string} fmt 格式化字符串
 *        ("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
 *        ("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18
 * @returns {string} 格式化后的字符串
 */
export default (date, fmt) => {
  //如果是时间戳的话那么转换成Date类型
  if (typeof date === 'number') {
    date = new Date(date)
  } else if (typeof date === 'string') {
    date = new Date(parseInt(date))
  }

  let o = {
    //月份
    "M+": date.getMonth() + 1,
    //日
    "d+": date.getDate(),
    //小时
    "h+": date.getHours(),
    //分
    "m+": date.getMinutes(),
    //秒
    "s+": date.getSeconds(),
    //季度
    "q+": Math.floor((date.getMonth() + 3) / 3),
    //毫秒
    "S": date.getMilliseconds()
  }
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + "").substr(4 - RegExp.$1.length))
  for (let k in o)
    if (new RegExp("(" + k + ")").test(fmt))
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)))
  return fmt
}
