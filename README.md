# weather


## 1.环境版本

python3.13

json,openai最新版本

## 2.API设置

使用的是deepseek的API

在main.py文件内开头提示部分设置自己的API

## 3.运行

运行main.py文件后就能看到输出结果

## 4.参考和借助

参考了deepseek官网API接口文档

使用chatgpt对模拟函数进行了优化使其支持中英文输入问答，防止因为原模拟函数鲁棒性低，导致模型可能无法识别返回的信息是哪个城市，误判为Weather Unavailable引起的回答错误
