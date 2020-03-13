import signal,sys,getopt
from time import sleep
from os import system
import Arknights
import tools

def quit(signum, frame):
    print('退出程序')
    tools.disconnect()
    sys.exit(0)
    
signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)


def auto_run(auto=False,username='',password='',command=''):
    automode=auto
    system("mode con cols=59 lines=30")  #调整窗口大小
    menu='''------------------------快捷菜单--------------------------

* 输入 【关卡序号,次数】 进行指定关卡挑战，例如：1-7,3
  创建任务队列请使用半角分号【;】隔开，例如：1-7,3;JM-2,3
* 输入 【*,次数】 开始当前关卡挑战(请手动开启代理指挥)

★ 输入【r】使用公开招募计算器功能(应进入公招界面)

*输入指定序号,次数直接开始挑战：

    1. 龙门币    CE-5      5. 扭转醇    6-11
    2. 合成玉    JM-2      6. 研磨石    3-3
    3. 采购凭证  AP-5      7. 轻锰矿    3-2
    4. 技巧概要  CA-5      8. RMA70-12  2-10

    a. 固源岩    1-7       z. 聚酸酯    S3-2
    s. 酮凝集    3-7       x. 异铁      S3-3
    d. 装置      S3-4      c. 糖        S3-1
-----------------------------------------------------------
  [h] 显示详细关卡序号
  [q] 关闭游戏
  Ctrl-C 安全退出脚本
                                                  By SGFu
-----------------------------------------------------------
'''

    menu_list={ #快捷菜单列表  触发词：指令
        '1':'CE-5','5':'6-11',
        '2':'JM-2','6':'3-3',
        '3':'AP-5','7':'3-2',
        '4':'CA-5','8':'2-10',

        'a':'1-7','z':'S3-2',
        's':'3-7','x':'S3-3',
        'd':'S3-4','c':'S3-1'
    }

    ark=Arknights.Arknights()
    print(menu)
    choice='nul'
    tasks=[]
    count=1     #默认挑战次数

    while True:
        try:
            #输入处理
            if automode:
                ark.message(" 自动模式，登录后执行指令【{0}】".format(command))
                ark.start_game(username,password)
                ark.message(' 开始执行指令')
                opt=command
                automode=False
            else:
                opt=input('输入指令：')
            tasks=opt.replace(' ','').split(';')

            for task in tasks:
                if ',' in task:
                    try:
                        choice,count=task.split(',')
                        count=int(count)
                    except Exception as e:
                        print(e)
                        sleep(2)
                        choice='err'
                else:
                    choice=task
            
                #分支处理
                if choice in menu_list: #快捷菜单直接挑战
                    ark.task_map(menu_list[choice],count)
                    #print(menu_list[choice])

                elif choice=='*':       #直接挑战当前关卡
                    ark._Arknights__refresh()     #需要先手动刷新一次
                    ark.message(' 开始挑战当前关卡')
                    ark.loop(count)

                elif choice=='h':
                    ark.show_help()
                elif choice=='q':
                    ark.exit_game()
                elif choice=='r':
                    ark.HR_helper()
                elif choice=='debug':
                    tools.adb_console()
                elif choice=='':
                    pass
                elif choice=='err':
                    raise Exception("错误：格式错误！")
                else:                   #自定义关卡访问
                    ark.task_map(choice,count)
            
        except Exception as e:
            print(e)

    
if __name__=='__main__':
    try:
        opts,args=getopt.getopt(sys.argv[1:],'u:p:c:',['username=','password=','command='])
    except getopt.GetoptError:
        print( "run.py [-u <usernsme> -p <password>]")
    if len(opts)==0:
        auto_run()
    else:
        username=''
        password=''
        command=''
        for opt,arg in opts:
            if opt in ('-u','--username'):
                username=arg
            elif opt in ('-p','--password'):
                password=arg
            elif opt in ('-c','--command'):
                command=arg
        if username=='' or password=='':
            print(' Login info error!')
            sys.exit(0)
        auto_run(auto=True,username=username,password=password,command=command)    

