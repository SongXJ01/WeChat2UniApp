# WeChat2UniApp
将微信小程序代码转换成 uni-app 代码

前段时间做了一个微信小程序，使用了云开发，但是云开发对业务逻辑的限制实在是太多了，因此想将其重构成 uni-app。最近将 wxml 改成 Vue 实在让人头大，因此“偷懒”使用 Python 写了一些正则表达式进行自动替换。

-----
## 代码
详见  [`transform.py`](transform.py)


-----
## “食用”步骤
1. 将需要转换的 wxml 命名为 “WeChat.wxml”，并放在与 Python代码的同级目录下；
2. 运行 Python 代码；
3. 转换后的结果会生成在同级目录的 “uniApp.vue”。


-----
## 持续更新
* 本程序暂未支持 js 的转换
* 欢迎各位大佬丰富本项目
