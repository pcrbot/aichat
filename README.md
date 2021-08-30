# aichat
该项目源自https://github.com/pcrbot/Hoshino-plugin-transplant/tree/master/aichat
由于此项目使用的旧api已无法使用，所以用新api重写一下

## 使用说明

在 https://console.cloud.tencent.com/nlp/openconfirm 页面开通服务

在 https://console.cloud.tencent.com/cam/capi 页面创建密钥

在 `aichat.py`中填入你的`SecretId`和`SecretKey`

使用 `pip install --upgrade tencentcloud-sdk-python`指令安装依赖

把文件夹放入`modules`中并在`__bot__.py`中添加该插件

## 功能
|指令|说明|
|-----|-----|
|调整AI概率+数字|调整ai接话的概率|
|关闭人工智障|机器人不再接话|

at机器人对话必定回复,使用`关闭人工智障`指令后依旧回复,若要彻底关闭使用`禁用 人工智障`指令