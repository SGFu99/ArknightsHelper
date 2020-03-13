import sys
from time import sleep
from random import uniform,randint
from numpy import where
from tempfile import gettempdir
from pickle import loads
from cv2 import matchTemplate,imread
from os import system,chdir,getcwd,listdir

temp_dir= '.'#sys._MEIPASS   #获取缓存目录（打包时取消注释）

#连接模拟器
def connect():
    #chdir(temp_dir)      #更改工作目录至缓存目录（打包时取消注释）
    connect_command=r'.\bin\adb.exe connect 127.0.0.1:7555'  #mumu模拟器
    #connect_command='adb connect 127.0.0.1:62001'  #夜神模拟器
    #connect_command='adb connect 127.0.0.1:5555'   #genymotion，谷歌原生，雷电
    b=system(connect_command)
    if b:   #连接失败，重置，重连
        system(r'.\bin\adb.exe kill-server')
        if system(connect_command):
            print('err:连接失败')
            return 0
    return 1

def disconnect():
    system(r'.\bin\adb.exe kill-server')
    return

def execute(command):
    if system(command):      #执行失败
        print('err:命令执行失败,请退出重连')
        sleep(5)
        disconnect()
        sys.exit(0)

#加载匹配资源图片
def load_imgs(folder):
    destimgs = {}
    path = temp_dir + '/'+folder
    file_list = listdir(path)

    for file in file_list:
        name = file.split('.')[0]
        file_path = path + '/' + file
        destimgs[name]=imread(file_path)

    return destimgs

#截屏
def screen_shoot():
    execute(r".\bin\adb.exe shell screencap -p /data/data/sCr33n.png >nul")
    execute(r".\bin\adb.exe pull /data/data/sCr33n.png >nul")
    screen=imread('sCr33n.png')
    #print(screen.shape)
    return screen

#adb模拟点击
def touch(pos):
    x,y=pos
    command= r".\bin\adb.exe shell input touchscreen tap {0} {1} >nul" .format(x, y)
    execute(command)

#adb模拟滑动
def swipe(pos1,pos2,time=500):
    x1,y1=pos1
    x2,y2=pos2
    command=r".\bin\adb.exe shell input swipe {0} {1} {2} {3} {4} >nul".format(x1,y1,x2,y2,time)
    execute(command)

#查找子区域（模板匹配）
def search(backimg,desimg):
    res_pos=[]
    h, w ,d= desimg.shape
    res = matchTemplate(backimg,desimg,5) #TM_CCOEFF_NORMED
    threshold = 0.90    #相似度设置
    loc = where( res >= threshold)

    rw,rh=0,0           #合并相似结果
    for pt in zip(*loc[::-1]):
        if (pt[0]-rw+pt[1]-rh)<10:
            continue
        rw,rh=pt[0],pt[1]
        res_pos.append((rw,rh))
        res_pos.append((rw+w,rh+h))
    
    return res_pos

#随机点击位置
def cheat(res_pos):
    x1,y1=res_pos[0]
    x2,y2=res_pos[1]
    res=[randint(x1,x2),randint(y1,y2)]
    return res

#延时
def delay(n=0.4):
    sleep(uniform(0.2,n))
    return

def touch_back():
    execute(r'.\bin\adb.exe shell input keyevent KEYCODE_BACK')

def adb_console():
    helpmenu='''
************* ADB debug console ***************
  * input 'quit' to quit debug console
  * input 'shell' get ADB shell
  * input 'exit' back to this shell
***********************************************'''
    print(helpmenu)
    while True:
        print('\n>',end='')
        command=input().strip()
        if command=='quit':
            return
        elif command=='shell':
            execute(r'.\bin\adb shell')
        elif command=='':
            pass
        else:
            execute(r'.\bin\adb shell '+command)

