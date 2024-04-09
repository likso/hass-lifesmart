使用说明
==== 
lifesmart 设备接入 HomeAssistant插件

Updates:
-------
[2024年4月9日累计更新]

* Home Assitant 新版本适配：
  * XXXDevice 改为 XXXEntity
  * FanSpeed 枚举修改
  * device_state_attributes 改为 extra_state_attributes
  * Climate 类中，统一修改为使用内置属性
  *

[2023-06-08]
1. 修改耶鲁盖特曼指纹锁开关门 wss 记录，用实际数据来判断是否真正的处于开门或者关门状态

[2022-10-09]
1. Added scene_set service
2. Added ai and scene as a switch
3. Added included AI agt and me setting as a switch setting in configuration.yaml

Added the following into configuration.yaml：

```
lifesmart:
  appkey: "your_appkey" 
  apptoken: "your_apptoken"
  usertoken: "your_usertoken" 
  userid: "your_userid"
  exclude:
    - "0011" #需屏蔽设备的me值,必填项，写9999可以防止屏蔽任何设备
  exclude_agt:
    - "XXXX" #exlucde all devices in these smart stations,必填项，写9999可以防止屏蔽任何设备
  ai_include_agt:
    - "XXXXXXXXX" # agt to be included for AI or Scene as a switch, fill any value to omit,必填项，写9999可以防止屏蔽任何设备
  ai_include_me:
    - "xxxx" # me to be included for AI or Scene as a switch, fill any value to omit,必填项，写9999可以防止屏蔽任何设备
  
```

-------  
[20220-07-12]
1. Added async support
2. Fix entity_id format 
3. Added unique_id property
4. Added switch SL_NATURE, SL_SW_NS[1|2|3] support
5. Added light SL_SPOT colour and brightness support
6. Added light strip SL_CT_RGBW colour and brightness support
7. Added light SL_LI_WW colour temperature and brightness support
8. Fixed Door sensor SL_SC_BG open/closed status
9. Changed server url to https://api.us.ilifesmart.com/
10. Added excluded agt setting in configuration.yaml

Added the following into configuration.yaml：

```
lifesmart:
  appkey: "your_appkey" 
  apptoken: "your_apptoken"
  usertoken: "your_usertoken" 
  userid: "your_userid"
  exclude:
    - "0011" #需屏蔽设备的me值,这个暂时为必填项，可以填任意内容
  exclude_agt:
    - "XXXX" #exlucde all devices in these smart stations
```

更新说明
-------  
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
```
获取usertoken和username:
通过iLifeSmart后台小工具拼接appkey,apptoken,回调地址、时间戳、did（可以为空）并在页面里面生成sign来访问用户页面进行授权
通过回调地址里面得到用户id和usertoken即可按照配置使用
```
    
