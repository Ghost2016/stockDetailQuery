// import { doLoop, setToken } from './getStockCode.js'
const getStockCode = require('./getStockCode.js')
console.log(getStockCode)
const { doLoop, startloop } = getStockCode
// return
var exec = require('child_process').exec;
// var cmds = ['100', '200', '300'];
var cmds = ['100'];
var no = 0;

//先发第一个环节码100，等待返回正确数据再进行发送下一个码
execCmd();

//该方法用于命令行执行python命令 类似于:  python py_test.py arg1
//这样在python中就可以接受传递过去的参数
function execCmd() {
    exec('python3 ./selenium_test.py '+ cmds[no++], function (error, stdout, stderr) {
        if(error){
            console.error('error: ' + error);
            return;
        }
        
        let token = stdout.split("#")[0]
        console.log('token', token)
        startloop(token)
        setTimeout(() => {
          execCmd()
        }, 4000);
        //将返回的json数据解析,判断是都执行下一步
        // var json = JSON.parse(stdout.split("#")[1]);
        // console.log(json.msg);
        // if(json.sign == "1" && no < 3){
        //     execCmd();
        // }
    });
}