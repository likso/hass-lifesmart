# 注意

本 repo 已经由更先进的 lifesmart-HACS-for-hass 替代，可以访问 https://github.com/MapleEve/lifesmart-HACS-for-hass 来直接用
HACS 安装

本 repo 的 LTS 支持时间将支持到所有新增变量导入过期。同时由于门锁类型的二元传感器无法注册为设备实体，所以只是“将将能用”，请使用
HACS 插件来完成更复杂的功能


使用说明
==== 
lifesmart 设备接入 HomeAssistant插件

Updates:
-------
[2024年4月9日累计更新]

* Home Assitant 新版本适配：
  * XXXDevice 改为 XXXEntity
  * Climate 类中，统一修改为使用内置属性
  * TODO:新增帐号密码认证

[2023-06-08]

1. 修改耶鲁盖特曼指纹锁开关门 wss 记录，用实际数据来判断是否真正的处于开门或者关门状态

[2020年12月26日更新]

支持流光开关灯光控制

更新manifest内容以适配新版本home assistant

[2020年8月21日更新]

新增设备支持：

**超能面板**：SL_NATURE

PS：其实就是个开关...

[2020年2月4日更新]

优化实体ID生成逻辑：解决未加入或存在多个智慧中心时，me号可能存在重复的问题。

[2019年12月6日更新]

新增支持设备：

**中央空调面板**：V_AIR_P

**智能门锁反馈信息**：SL_LK_LS、SL_LK_GTM、SL_LK_AG、SL_LK_SG、SL_LK_YL

目前支持的设备：
-------  
1、开关；

2、灯光：目前仅支持超级碗夜灯；

3、万能遥控；

4、窗帘电机（仅支持杜亚电机）

5、动态感应器、门磁、环境感应器、甲醛/燃气感应器

6、空调控制面板

7、智能门锁信息反馈

使用方法：
-------  
1、将lifesmart目录复制到config/custom_components/下

2、在configuration.yaml文件中增加配置：

```
lifesmart:
  appkey: "your_appkey" 
  apptoken: "your_apptoken"
  usertoken: "your_usertoken" 
  userid: "your_userid"
  exclude:
    - "0011" #需屏蔽设备的me值,这个暂时为必填项，可以填任意内容
```

如何获取 User Token 和 User ID
---
通过iLifeSmart后台的小工具拼接appkey,apptoken,回调地址、时间戳、did（可以为空）并在页面里面生成sign来访问用户页面进行授权
[访问小工具页面](http://www.ilifesmart.com/open/login#/open/document/tool)
点击“获取用户授权签名验证”然后参考下面 Python 脚本拼接，或者直接执行 Python 脚本

``` python
import time
import hashlib
tick = int(time.time())
appkey = " 你的应用 APPKEY"
callbackurl = "http://localhost"
apptoken = "你的应用 APPK TOKEN"
sdata = "appkey=" + appkey
sdata += "&auth_callback=" + callbackurl
sdata += "&time=" + str(tick)
sdata += "&apptoken=" + apptoken
sign = hashlib.md5(sdata.encode(encoding='UTF-8')).hexdigest()
url = "https://api.ilifesmart.com/app/auth.authorize?id=001&"
url += "&appkey=" + appkey
url += "&time=" + str(tick)
url += "&auth_callback=" + callbackurl
url += "&sign=" + sign
url += "&lang=zh"
print(url)
```

脚本运行之后会打印一个地址，浏览器访问这个地址，用你的 Lifesmart APP 帐号密码登录即可从浏览器跳转到空页面 URI 中获取到
User ID、User Token、Token 过期时间、和优选的 API 域名地址

## 请注意：每次通过这个方法授权得到的 User Token 有效期为一年，你需要在到期前重新构建方法获取新的 Token
