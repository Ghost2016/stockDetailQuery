var request = require('request');


// 重复请求次数
let repeat_times = 120
// 请求间隔
let step_wait = [2000]
let token = ""
let isLooping = false
const setToken = (_token) => {
  
}
const startloop = (_token) => {
  token = _token.replace('\n', '')
  if(isLooping)return
  isLooping = true
  doLoop()
}
function doLoop() {
  if(!token) {
    console.log('token 为空')
    let _timer = setTimeout(() => {
      doLoop()
      _timer = null
    }, step_wait[0])
    return
  }
  let url = "http://www.iwencai.com/stockpick/load-data?typed=0&preParams=&ts=1&f=1&qs=result_original&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E6%98%A8%E5%A4%A9%E6%B6%A8%E5%81%9C%E5%B0%81%E5%8D%95%E5%A4%A7%E4%BA%8E1%E4%B8%87%E8%82%A1+%E6%98%A8%E5%A4%A9%E5%BC%80%E6%9D%BF%E6%AC%A1%E6%95%B0%E5%A4%A7%E4%BA%8E0+%E4%BB%8A%E5%A4%A9%E5%BC%80%E7%9B%98%E6%B6%A83%25%E5%88%B08%25+%E9%9D%9Est&queryarea="
  console.log(repeat_times)
  console.log({
    url: url,
    method: 'GET',                   // 请求方法
    headers: {                       // 指定请求头
      'hexin-v': token.replace('\n', '')
    }
  })
  // return
  request({
    url: url,
    method: 'GET',                   // 请求方法
    headers: {                       // 指定请求头
      'hexin-v': token
    }
  }, function (error, response, body) {
    console.log(error, response, body)
    if (!error && response.statusCode == 200) {
      console.log(body);
      // 输出网页内容
      try {
        let data = JSON.parse(body).data.tableTempl
        let reg = /\d{6}/g;
        let result = data.match(reg)
        console.log(_filter(result));
      } catch (e) {
        token = ''
        repeat_times = 0
        console.error(e)
      }
    }
    repeat_times--
    if(repeat_times > 0) {
      setTimeout(doLoop, step_wait[0])
    }
  });
}
//去除数组中重复值 
function _filter(s) { 
  return s.sort().join(",,").replace(/(,|^)([^,]+)(,,\2)+(,|$)/g,"$1$2$4").replace(/,,+/g,",").replace(/,$/,"").split(","); 
}

doLoop()
module.exports = {
  doLoop,
  startloop
}



