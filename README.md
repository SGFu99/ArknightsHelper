#ArknightsHelper
安卓模拟器使用的明日方舟挂机脚本

原理主要opencv图像模板匹配出点击区域，然后再通过adb模拟点击，优势就是可以在挂机的时候最小化窗口干其他事

目前支持的功能：
   * 代肝常驻的主线，直线关卡，可通过快捷菜单直接挑战常用的材料本
   * 公开招募计算器

环境需求
--------------------------------------------------------------------

--------------------------注意！！！------------------------------
**！！！本脚本只支持1280*720分辨率的Android模拟器！！！**
**！！！本脚本只支持1280*720分辨率的Android模拟器！！！**
**！！！本脚本只支持1280*720分辨率的Android模拟器！！！**

可以直接下载打包好了的exe文件跳过这些配置

* 下载一个Android模拟器，我用的时mumu模拟器**模拟器设置分辨率1280*720并确保开启adb**（我用的mumu模拟器，其它模拟器没测试过，理论上编辑`tools.py`修改`connect_command`就行了吧）

* 安装相关依赖（本脚本运行需要python3环境和opencv库，opencv库国内下载比较慢，如果不想折腾的话可以直接下载打包好了的exe文件）：
`pip install -r requirements.txt`

* 运行`run.py`

使用说明
--------------------------------------------------------------------
* 输入 【关卡序号,次数】 进行指定关卡挑战，例如：`1-7,3`
*  创建任务队列请使用半角分号【;】隔开，例如 挑战1-7，3次；剿灭2，2次：`1-7,3;JM-2,3`
* 输入 【`*,次数`】 开始当前关卡挑战(需要手动开启代理指挥)

* ★ 输入【r】使用公开招募计算器功能(需要进入公招tag界面)，干员信息表来源于[明日方舟工具箱](https://aktools.graueneko.xyz/)

* 输入指定序号,次数直接开始挑战，以下为最佳掉落表：(相关掉落统计来源于[企鹅物流统计](https://penguin-stats.io/))

            1. 龙门币    CE-5      5. 扭转醇    6-11
            2. 合成玉    JM-2      6. 研磨石    3-3
            3. 采购凭证  AP-5      7. 轻锰矿    3-2
            4. 技巧概要  CA-5      8. RMA70-12  2-10

            a. 固源岩    1-7       z. 聚酸酯    S3-2
            s. 酮凝集    3-7       x. 异铁      S3-3
            d. 装置      S3-4      c. 糖        S3-1


ps:  这脚本感觉除了刷1-7和公招计算器其它用处不大，毕竟每天就那么点体力 -_-
pss:  pyinstaller打包体积好大啊，有没有大佬指点一下~
