ArknightsHelper
====================================================================
安卓模拟器使用的明日方舟挂机脚本

目前支持的功能：
   * 代肝常驻的主线，直线关卡，可通过快捷菜单直接挑战常用的材料本
   * 随机点击坐标，随机点击延迟，防止封号
   * **公开招募计算**
   

环境需求
--------------------------------------------------------------------

不想装环境的可以直接下载打包好了的exe文件（拒绝百毒云，从我做起）: [https://share.weiyun.com/sLM5JdgH](https://share.weiyun.com/sLM5JdgH) 密码：p7wx3b

* 脚本默认设置的是mumu模拟器连接指令，**模拟器设置分辨率1280*720并确保开启adb**。~~其它模拟器需要编辑`tools.py`修改`connect_command`为该模拟器的ADB连接指令~~（现在可以尝试搜索和连接不同模拟器了）

*  安装 python 3.7.2 环境

* 安装相关依赖（本脚本运行需要OpenCV库，OpenCV国内下载比较慢，如果不想折腾的话可以直接下载打包好了的exe文件）：
`pip install -r requirements.txt`

* 打开Android模拟器后，运行`run.py`

使用说明
--------------------------------------------------------------------
* 输入 【关卡序号,次数】 进行指定关卡挑战，例如：`1-7,3`
*  创建任务队列请使用半角分号【;】隔开，例如 挑战1-7，3次；剿灭2，2次：`1-7,3;JM-2,3`
* 输入 【`*,次数`】 开始当前关卡挑战(需要手动开启代理指挥)

* ★ 输入【r】使用公开招募计算器功能(需要进入公招tag界面)，干员信息来源于[明日方舟工具箱](https://aktools.graueneko.xyz/)

* 快捷菜单，输入指定序号,次数直接开始挑战：(相关掉落统计来源于[企鹅物流统计](https://penguin-stats.io/))

            1. 龙门币    CE-5      5. 扭转醇    6-11
            2. 合成玉    JM-2      6. 研磨石    3-3
            3. 采购凭证  AP-5      7. 轻锰矿    3-2
            4. 技巧概要  CA-5      8. RMA70-12  2-10

            a. 固源岩    1-7       z. 聚酸酯    S3-2
            s. 酮凝集    3-7       x. 异铁      S3-3
            d. 装置      S3-4      c. 糖        S3-1
