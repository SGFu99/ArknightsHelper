import requests
import tools
import baiduOCR
import json
from itertools import combinations

def update_HR_data():
    """
    从 aktools.graueneko.xyz 更新干员信息表
    """
    print("向aktools.graueneko.xyz获取数据...")
    response = requests.get("https://aktools.graueneko.xyz/assets/data/akhr.json") 
    if response:
        with open("./bin/akhr.json",'w',encoding="utf-8") as f:
            f.write(response.text)
        response.text
        print("数据更新完成")
    else:
        raise Exception("公开招募数据更新失败")

def get_tag(img_path='sCr33n.png',refresh=True):
    """
    提取截图中的招募tag信息
        :param img_path='sCr33n.png': 截图路径
        :param refresh=True: 是否刷新截图
    """
    tags = [
        "新手", "资深干员", "高级资深干员",
        "远程位", "近战位",
        "先锋干员", "狙击干员", "医疗干员", "术师干员", 
        "近卫干员", "重装干员", "辅助干员", "特种干员",
        "治疗", "支援", "输出", "群攻", "减速", "生存", 
        "防护", "削弱", "位移", "控场", "爆发", "召唤", 
        "快速复活", "费用回复", "支援机械"
    ]
    avalible_tag=[]
    if refresh:
        tools.screen_shoot()
    cur_tags=baiduOCR.text_rec(img_path)

    for tag in cur_tags:
        if tag in tags:
            avalible_tag.append(tag)

    if len(avalible_tag) != 5:
        raise Exception('招募tag提取失败，请确认进入正确界面。')

    return avalible_tag

def get_operator(super_flag=False):              #筛选可公开招募的干员
    """
    从配置文件获取可招募的干员信息
        :param super_flag=False: 是否有高级资深干员标签
    """
    recruit_data = []
    with open("./bin/akhr.json",'r',encoding="utf-8") as f:
        temp_data =json.loads(f.read())
    
    for item in temp_data:
        add_flag=False
        if not item['hidden']:
            if item['level'] != 6:
                add_flag=True
            else:
                if super_flag:      #有高级资深干员标签则添加
                    add_flag=True
        if add_flag:
            temp={
                'name':item['name'],
                'type':item['type'],
                'level':item['level'],
                'tags':item['tags'],
            }
            recruit_data.append(temp)
    return recruit_data


def HR_searcher(own_tags):
    """
    根据招募标签筛选出符合要求的干员
        :param own_tags: 招募标签列表
    """
    super_tag=False
    if "高级资深干员" in own_tags:
        super_tag=True
    operators=get_operator(super_tag)

    tag_combs=[]
    for i in range(3):      #最多挑选3个tag
        for item in combinations(own_tags,i+1):
            tag_combs.append(item)
            
    result={}
    for op in operators:
        for comb in tag_combs:
            aval_flag=True
            for tag in comb:
                if tag not in op['tags'] and tag != (op['type']+'干员'):
                    aval_flag=False
                    break
            if aval_flag:       #该组合存在招募干员
                if comb not in result:
                    result.update({comb:{}})
                result[comb].update({str(op['level'])+'★'+op['name']:op['level']})
                # if '治疗' in op['tags']:
                #     print(op['name'])
    #print(result)
    return result

def result_processer(result):
    """
    结果排序，计算权值
        :param result: 结果
    """
    tmp_result={}
    for tags in result.keys():
        tag_str='/'.join(tags)                    #合并tag标签
        op_str=','.join(sorted(list(result[tags].keys()),reverse=True))#星级降序排序干员并合并
        total_weight=0.0

        for item in result[tags].keys():    #统计并计算权值
            total_weight+=result[tags][item]
        total_weight/=len(result[tags])

        tmp_result.update({str(total_weight)+'#'+tag_str:op_str})   #拼接权值加入字典(防止重复键值)
    
    fin_result=[]
    for num in sorted(tmp_result,reverse=True):     #排序结果，去掉键值信息写入结果列表
        fin_result.append([num.split("#")[1],tmp_result[num]])

    return fin_result

def test_func():
    own_tags=['先锋干员', '新手',]#get_tag("MuMu.png",False)
    a=HR_searcher(own_tags)
    result=result_processer(a)

if __name__ == "__main__":
    update_HR_data()