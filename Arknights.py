import tools
import sys
import ArkHR
from os import system
from time import strftime,localtime,sleep
from random import uniform

class Arknights():
    __last_click_pos=[0,0]  #上一次的点击位置

    def __cur_time(self):   #获取当前时间
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

    def message(self,msg):  #输出信息
        print(self.__cur_time()+msg)

    def __init__(self, *args, **kwargs):
        self.message('  开始初始化...')
        self.__imgs=tools.load_imgs('imgs')
        self.message('  加载资源文件成功')
        if tools.connect():
            self.message('  连接设备成功')
        else:
            self.message('  设备连接失败,exiting...')
            sys.exit(0)
        self.__back=tools.screen_shoot()
        self.message('  屏幕分辨率：{0}*{1}\n'.format(self.__back.shape[0],self.__back.shape[1]))

    def __refresh(self):
        self.__back=tools.screen_shoot()

    def __contains(self,destimg,refresh=True):
        if refresh:
            self.__refresh()
        if len(tools.search(self.__back,self.__imgs[destimg]))==0:
            return False
        return True

    def __random_click(self,pos=[(0,0),(1280,720)]):
            tools.touch(tools.cheat(pos))
            #print('random click')

    #等待
    def __wait(self,t):
        sleep(uniform(t,t+0.1))
    
    #防封点击
    def __click(self,destimg,refresh=True):
        if refresh:
            self.__refresh()
        pos=tools.search(self.__back,self.__imgs[destimg])
        if len(pos)!=0:
            tools.touch(tools.cheat(pos))
            #print("click "+destimg)
            return True
        return False

    #防封滑动
    def __swipe_to(self,dest="right",time=500):
        right_pos=tools.cheat([(1069,305),(1125,364)])
        left_pos=tools.cheat([(546,324),(596,375)])
        lleft_pos=tools.cheat([(146,324),(196,375)])
        stop_pos=tools.cheat([(1181,42),(1229,85)])
        if dest=="right":   #  ->
            tools.swipe(right_pos,left_pos,time)
            self.__wait(time/1000.0)
            tools.touch(stop_pos)
        elif dest=="left":  #  <-
            tools.swipe(left_pos,right_pos,time)
            self.__wait(time/1000.0)
            tools.touch(stop_pos)
        elif dest=="lleft": # <<<----
            tools.swipe(lleft_pos,right_pos,time)
        else:
            print("swipe error")

    def chapter_task(self,chapter="chapter1",task="1-7"):
        """
        到达指定章节任务
            :param chapter="chapter1": 章节名称
            :param task="1-7": 任务名称
        """
        #点击主界面作战
        while not self.__click("main_zuozhan"):
            if self.__click("main_menu",refresh=False):
                self.__wait(0.3)
                self.__random_click([(61,159),(109,285)])
            else:
                self.__click("back")
            self.__wait(0.3)

        #初始化章节位置
        self.__wait(0.3)
        self.__swipe_to('lleft',200)
        self.__wait(0.6)
        #点击相关章节
        while not self.__click(chapter):
            self.__swipe_to("right")
            self.__wait(0.9)
        #初始化关卡位置
        self.__wait(1)
        self.__swipe_to('lleft',200)
        self.__wait(0.6)
        #点击相关关卡
        while not self.__click(task):
            self.__swipe_to("right")
            self.__wait(0.9)
        while not self.__contains("kaishixingdong"):
            self.__click(task,refresh=False)
        self.message(" 已进入[{0} {1}]".format(chapter,task))
        #开启代理指挥
        while not self.__contains("daili_on"):
            self.__click("daili_off",refresh=False)
            self.message(" 开启代理指挥")

        

    def loop(self,num=1,hcy=False,others=False):
        """
        循环挑战当前任务
            :param num: 循环次数
            :param hcy=False: 合成玉模式(剿灭关卡)
            :param others=False: 挑战完成后需要手动再次点开关卡的其它模式
        """  
        wait_time=60        #默认关卡的等待时间
        #game_over_click=[(816,180),(956,352)]   #挑战结束后随机点击坐标
        game_over_click=[(966,184),(1230,276)]
        #start_pos=[(1053,398),(1154,600)]        #第二个开始行动的坐标
        if hcy:             #合成玉模式的固定等待时间
            wait_time=600

        self.message(" 开始挑战")
        #循环挑战关卡
        for i in range(num):
            #点击开始行动
            if i==0:       #第一次不需要刷新
                self.__click("kaishixingdong",refresh=False)
                self.__wait(0.6)
            else:
                while not self.__click("kaishixingdong"):
                    if others:      #点击上一次打开关卡的位置
                        tools.touch(self.__last_click_pos)
                    self.__wait(0.3)

            #点击第二个开始行动
            while not self.__click("kaishixingdong1"):
                #理智不足退出
                if self.__contains("empty",refresh=False):
                    #self.__random_click([(1249,24),(1268,32)])
                    self.message(" 理智不足，已退出")
                    return False
                self.__wait(0.3)

            #等待行动结束
            self.__wait(wait_time)
            if hcy:
                while not self.__contains("jiaomie_fin"):       #剿灭报告跳过，存在账号升级无法跳过风险，待修复
                    if self.__contains("update",refresh=False): #升级
                        self.__random_click([(1249,24),(1268,32)])
                        self.message(" 账号等级已提升")
                    self.__wait(2)
                self.__random_click([(1249,24),(1268,32)])
                self.__wait(2)

            while not self.__contains("task_over"):         #行动结束点击
                if self.__contains("update",refresh=False): #升级
                    self.__random_click(game_over_click)
                    self.message(" 账号等级已提升")
                self.__wait(2)
            self.__random_click(game_over_click)
            self.__wait(0.3)
            self.__random_click(game_over_click)
            self.__wait(0.3)
            self.__random_click(game_over_click)
            self.message(" 已完成 {0}/{1}".format(i+1,num))
            self.__wait(2)
        
        return True

    
    def other_task(self,mode="wuzichoubei",submode="huowuyunsong",level=5):
        """
        到达其它模式任务
            :param mode: 模式
                物资筹备："wuzichoubei"
                芯片搜索："xinpiansousuo"
                剿灭作战："jiaomiezuozhan"
            :param submode="": 子模式
                物资筹备：战术演习 "zhanshuyanxi"
                         空中威胁 "kongzhongweixie"
                         货物运送 "huowuyunsong"
                         资源保障 "ziyuanbaozhang"
                         粉碎防御 "fensuifangyu"
                芯片搜索：身先士卒 "shenxianshizu"
                         摧枯拉朽 "cuikulaxiu"
                         势不可挡 "shibukedang"
                         固若金汤 "guruojintang"
                剿灭作战：无需设置
            :param level=5: 难度等级
                物资筹备：1~5
                芯片搜索：1~2
                剿灭作战：1~3
        """
        #物资难度选择坐标范围
        wuzi_level_pos=[
            [(141,554),(266,584)],
            [(415,502),(552,530)],
            [(621,386),(747,416)],
            [(784,272),(921,306)],
            [(883,159),(1026,187)]
        ]
        #芯片难度选择坐标范围
        xinpian_level_pos=[
            [(340,425),(462,449)],
            [(774,240),(884,278)]
        ]
        #剿灭难度选择坐标范围
        jiaomie_level_pos=[
            [(113,167),(286,392)],
            [(660,409),(829,622)],
            [(986,198),(1163,423)]
        ]

        info={      #用于日志输出
            'wuzichoubei':'物资筹备',
            'xinpiansousuo':'芯片搜索',
            'jiaomiezuozhan':'剿灭作战',

            'zhanshuyanxi':'战术演习',
            'kongzhongweixie':'空中威胁',
            'huowuyunsong':'货物运送',
            'fensuifangyu':'粉碎防御',
            'ziyuanbaozhang':'资源保障',
        
            'shenxianshizu':'身先士卒',
            'cuikulaxiu':'摧枯拉朽',
            'guruojintang':'固若金汤',
            'shibukedang':'势不可挡'
        }

        #点击主界面作战
        while not self.__click("main_zuozhan"):
            if self.__click("main_menu",refresh=False):
                self.__wait(0.3)
                self.__random_click([(61,159),(109,285)])
            else:
                self.__click("back")
            self.__wait(0.3)
        #点击相关模式
        while not self.__click(mode):
            self.__wait(0.3)

        if mode!="jiaomiezuozhan":
            #选择相关子模式
            self.__wait(0.3)
            while not self.__click(submode):
                self.__wait(0.3)

        #随机难度坐标
        self.__wait(0.6)
        pos=[0,0]
        if mode=="wuzichoubei":     #物资筹备难度选择
            pos=tools.cheat(wuzi_level_pos[level-1])
        elif mode=="xinpiansousuo": #芯片搜索难度选择
            pos=tools.cheat(xinpian_level_pos[level-1])
        elif mode=="jiaomiezuozhan":#剿灭作战难度选择
            pos=tools.cheat(jiaomie_level_pos[level-1])
        else:
            print("err: no such mode.")
            return
        #点击难度坐标
        tools.touch(pos)
        self.__last_click_pos=pos
        self.__wait(0.4)
        while not self.__contains("kaishixingdong"):
            tools.touch(pos)
        
        #日志打印
        if mode=="jiaomiezuozhan":
            self.message(" 进入[{0}]，等级：{1}".format(info[mode],level))
        else:
            self.message(" 进入[{0}-{1}]，等级：{2}".format(info[mode],info[submode],level))

        #开启代理指挥
        while not self.__contains("daili_on"):
            self.__click("daili_off",refresh=False)
            self.message(" 开启代理指挥")
        
    def exit_game(self):
        system(r".\bin\adb.exe shell am force-stop com.hypergryph.arknights")

    def task_map(self,taskname='1-2',conut=1):
        """
        根据关卡名称循环挑战
            :param self: 
            :param taskname='1-2': 关卡代号
            :param conut=3: 挑战次数

            关卡名称    掉落物品    关卡代号    开放时间
        ----------------------主线----------------------------
                                  0-1 S2-1   ALL
        --------------------物资筹备---------------------------
            战术演习    作战记录    LS-1~5     ALL
            空中威胁    技巧概要    CA-1~5     2，3，5，7
            货物运送    龙门币      CE-1~5     2，4，6，7
            资源保障    基建材料    SK-1~5     1，3，5，6
            粉碎防御    采购凭证    AP-1~5     1，4，6，7
        --------------------芯片搜索----------------------------
            固若金汤    重装，医疗  PR-A-1~2   1，5，6，7
            摧枯拉朽    狙击，术士  PR-B-1~2   1，2，5，6
            势不可挡    先锋，辅助  PR-C-1~2   3，4，6，7
            身先士卒    近卫，特种  PR-D-1~2   2，3，6，7
        --------------------剿灭作战----------------------------
            切尔诺伯格  合成玉      JM-1      ALL
            龙门外环    合成玉      JM-2      ALL
            龙门市区    合成玉      JM-3      ALL
        """
        mode='zhuxian'
        a,b,c=['0','0','0']
        is_jiaomie=False       #剿灭关卡需要循环函数特殊处理
        week=strftime('%w')    #获取周次信息'0'-'6'
                               #未超过凌晨四点算前一天
        if int(strftime('%H'))<=4:
            week=str((int(week)-1)%7)

        #四大模式特征表，映射表
        zhuxian=['0','1','2','3','4','5','6','7','S2','S3','S4','S5','S6','S7']
        wuzi={'LS':'zhanshuyanxi','CA':'kongzhongweixie','CE':'huowuyunsong','SK':'ziyuanbaozhang','AP':'fensuifangyu'}
        xinpian=['PR']
        jiaomie=['JM']

        #周限时关卡开放表
        week_map={
            '1':['A','B','LS','SK','AP'],
            '2':['B','D','LS','CA','CE'],
            '3':['C','D','LS','CA','SK'],
            '4':['C','A','LS','CE','AP','JM'],
            '5':['A','B','LS','CA','SK','JM'],
            '6':['B','C','D','LS','CE','SK','AP'],
            '0':['A','C','D','LS','CA','CE','AP']
        }

        #拆分关卡信息
        taskname=taskname.strip().upper()
        items=taskname.split('-')
        if len(items)==2:
            a,b=items
        elif len(items)==3:
            a,b,c=items
        else:
            raise Exception("错误：无法处理的关卡名称！")

        #判断关卡种类，生成关卡访问路径并访问
        others=False
        if a in zhuxian:        #主线关卡访问
            chapter='chapter'+a.replace('S','')
            task=taskname
            self.chapter_task(chapter,task)
        elif a in wuzi:         #物资关卡访问
            others=True
            if a in week_map[week]:
                mode='wuzichoubei'
                submode=wuzi[a]
                level=int(b)
                self.other_task(mode,submode,level)
            else:
                raise Exception("错误：关卡未开放！")
        elif a in xinpian:      #芯片关卡访问
            others=True
            if b in week_map[week]:
                mode='xinpiansousuo'
                submode_map={'A':'guruojintang','B':'cuikulaxiu','C':'shibukedang','D':'shenxianshizu'}
                submode=submode_map[b]
                level=int(c)
                self.other_task(mode,submode,level)
            else:
                raise Exception("错误：关卡未开放！")
        elif a in jiaomie:      #剿灭作战关卡访问
            mode='jiaomiezuozhan'
            submode='nul'
            is_jiaomie=True
            level=int(b)
            self.other_task(mode,submode,level)
        else:
            raise Exception("错误：未定义的关卡名称！")
        #循环挑战关卡
        self.loop(conut,is_jiaomie,others)

    def show_help(self):
        message='''
------------------参考掉落表---------------------
关卡名称    掉落物品    关卡代号    开放时间
----------------主线推荐材料本-------------------
1. 龙门币    CE-5      5. 扭转醇    6-11
2. 合成玉    JM-2      6. 研磨石    3-3
3. 采购凭证  AP-5      7. 轻锰矿    3-2
4. 技巧概要  CA-5      8. RMA70-12  2-10
a. 固源岩    1-7       z. 聚酸酯    S3-2
s. 酮凝集    3-7       x. 异铁      S3-3
d. 装置      S3-4      c. 糖        S3-1
--------------------物资筹备---------------------
战术演习    作战记录    LS-1~5     ALL
空中威胁    技巧概要    CA-1~5     2，3，5，7
货物运送    龙门币      CE-1~5     2，4，6，7
资源保障    基建材料    SK-1~5     1，3，5，6
粉碎防御    采购凭证    AP-1~5     1，4，6，7
--------------------芯片搜索---------------------
固若金汤    重装，医疗  PR-A-1~2   1，4，5，7
摧枯拉朽    狙击，术士  PR-B-1~2   1，2，5，6
势不可挡    先锋，辅助  PR-C-1~2   3，4，6，7
身先士卒    近卫，特种  PR-D-1~2   2，3，6，7
--------------------剿灭作战---------------------
切尔诺伯格  合成玉      JM-1       ALL
龙门外环    合成玉      JM-2       ALL
龙门市区    合成玉      JM-3       ALL
-------------------------------------------------
'''
        print(message)

    def start_game(self,username,passwd):
        """
        打开游戏并自动登录至主界面（不稳定）
            :param username: 用户名
            :param passwd: 密码
        """   
        username_pos=[(493,413),(775,441)]
        passwd_pos=[(495,462),(776,493)]
        account_login_pos=[(319,482),(503,529)]
        system(r".\bin\adb.exe shell am start com.hypergryph.arknights/com.u8.sdk.U8UnityContext >nul")
        self.message(" 打开游戏")
        while not self.__contains("game_start"):
            self.__wait(0.5)
        self.__click("game_start",refresh=False)

        skip_flag=False
        while not self.__contains("game_manage"):
            if self.__contains("login_background",refresh=False):
                skip_flag=True
                break
            self.__wait(0.5)

        if not skip_flag:
            self.__click("game_manage",refresh=False)
            #self.message(" 进入账号管理")
        
        self.__random_click(account_login_pos)
        self.message(" 进入登录界面")
        self.__wait(1)
        #self.message(" 输入用户名")
        self.__random_click(username_pos)
        self.__wait(0.2)
        system(r'''.\bin\adb.exe shell input text "{0}"'''.format(username))
        self.__wait(0.2)
        #self.message(" 输入密码")
        self.__random_click(passwd_pos)
        self.__wait(0.2)
        self.__random_click(passwd_pos)
        self.__wait(0.2)
        system(r'''.\bin\adb.exe shell input text "{0}"'''.format(passwd))
        self.__wait(0.2)
        #self.message(" 点击登录")

        while self.__contains("login_btn"):
            self.__click("login_btn",refresh=False)
        
        loop_count=0
        while not self.__contains("main_zuozhan"):
            self.__wait(0.5)
            loop_count+=1
            if loop_count>20:
                self.message(" 登录出错，请手动登录")
                return False

        self.__wait(5)
        if self.__contains("login_qiandao"):
            self.__random_click(account_login_pos)
        while self.__contains("login_X"):
            self.__click("login_X",refresh=False)
            self.__wait(3)
        self.message(" 已进入游戏主界面")

    def HR_helper(self):
        self.message("获取招募标签...")
        own_tags = ArkHR.get_tag()
        print("===========================================================")
        print("可选标签："+"/".join(own_tags))
        #self.message("计算招募结果...")
        tmp_result=ArkHR.HR_searcher(own_tags)
        #self.message("排序结果...")
        result=ArkHR.result_processer(tmp_result)
        print("-----------------------------------------------------------")
        for item in result:                 # 对齐输出。。。
            op_list=item[1].split(',')
            op_str=''
            counter=0
            tmp_list=[]
            for op in op_list:
                counter+=1
                tmp_list.append(op)
                if counter==4:
                    op_str+=', '.join(tmp_list)
                    tmp_list=[]
                    op_str+='\n          '
                    counter=0
            op_str+=', '.join(tmp_list)
            if '3★' not in op_str and '2★' not in op_str:
                item[0]='★'+item[0]
            print(item[0]+' : '+op_str.strip())
        
#     def test_func(self):
#         # self.__swipe_to('lleft')
#         # self.__contains('2-5')
#         self.HR_helper(self)

# if __name__ == "__main__":
#     ark=Arknights()
#     ark.test_func()
