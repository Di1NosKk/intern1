from fastapi import FastAPI, Request
import json
import uvicorn, json, datetime
import torch
import sys
import os
import time

import multi_tags

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


multiTag = multi_tags.Tag()
tags = [['财经', '财经是指财政与经济，如：他对财经方面的问题非常有研究。'],['股票', '股票（stock、shares）是股份公司所有权的一部分，也是发行的所有权凭证，是股份公司为筹集资金而发行给各个股东作为持股凭证并借以取得股息和红利的一种有价证券。股票是资本市场的长期信用工具'],['基金', '基金，英文是fund，广义是指为了某种目的而设立的具有一定数量的资金。主要包括公积金、信托投资基金、保险基金、退休基金，各种基金会的基金。'],['外汇', '外汇，英文名是Foreign currency，是货币行政当局（中央银行、货币管理机构、外汇平准基金及财政部）以银行存款、财政部库券、长短期政府证券等形式保有的在国际收支逆差时可以使用的债权。'],['科技', '社会上习惯于把科学和技术连在一起，统称为科学技术，简称科技。实际二者既有密切联系，又有重要区别。科学解决理论问题，技术解决实际问题。科学要解决的问题，是发现自然界中确凿的事实与现象之间的关系，并建立理论把事实与现象联系起来'],['手机', '手机，全称为移动电话或无线电话，通常称为手机，原本只是一种通讯工具，早期又有“大哥大”的俗称 [1] ，是可以在较广范围内使用的便携式电话终端，最早是由美国贝尔实验室在1940年制造的战地移动电话机发展而来。'],['智能', '智能，是智力和能力的总称，也有不少思想家把二者结合起来作为一个整体看待。'],['游戏', '按游戏的载体区分，游戏可分为电子游戏和非电子游戏，游戏种类还有团体性游戏，桌面游戏以及野外生存游戏等。'],['电竞', '电子竞技（Electronic Sports），是电子游戏比赛达到“竞技”层面的体育项目。电子竞技就是利用电子设备作为运动器械进行的、人与人之间的智力和体力结合的比拼。'],['旅游', '旅游是结合自己的喜好，主动挖掘尚未熟知的目的地，获得更独特的体验。旅游是一种情绪消费，远离居住地的旅游愈发成为人们舒缓心境、重获力量的重要目的。'],['文化', '文化，广义指人类在社会实践过程中所获得的物质、精神的生产能力和创造的物质、精神财富的总和，狭义指精神生产能力和精神产品，包括一切社会意识形式'],['娱乐', '现代娱乐可被看作是一种通过表现喜怒哀乐或自己和他人的技巧而给予受者喜悦、放松感觉的形式。很显然，这种定义是广泛的，它包含了悲喜剧、各种比赛和游戏、音乐舞蹈表演和欣赏等等。'],['影视', '影视是以拷贝、磁带、胶片、存储器等为载体，以银幕、屏幕放映为目的，从而实现视觉与听觉综合观赏的艺术形式，是现代艺术的综合形态，包含了电影、电视剧、节目、动画等内容。'],['音乐', '在最一般的形式中，将音乐描述为一种艺术形式或文化活动，包括音乐作品的创作（歌曲、曲调、交响曲等），表演，对音乐的评价，对音乐历史的研究以及音乐教学。'],['汽车', '由动力驱动，具有4个或4个以上车轮的非轨道承载的车辆，主要用于：载运人员和（或）货物；牵引载运人员和（或）货物的车辆；特殊用途。'],['教育', '教育（Education）狭义上指专门组织的学校教育；广义上指影响人的身心发展的社会实践活动。拉丁语educare是西方“教育”一词的来源，意思是“引出”。'],['留学', '留学，旧称留洋，一般是指一个人去母国以外的国家接受各类教育，时间可以为短期或长期（从几个星期到几年）。这些学生被称为留学生。'],['高考', '普通高等学校招生全国统一考试（Nationwide Unified Examination for Admissions to General Universities and Colleges），简称“高考”，是合格的高中毕业生或具有同等学力的考生参加的选拔性考试。'],['体育', '体育（physical education，缩写PE或P.E.），是一种复杂的社会文化现象，它是一种以身体与智力活动为基本手段，根据人体生长发育、技能形成和机能提高等规律，达到促进全面发育'],['时政', '当代的政治情况、政治措施,主要和政府政策相关'],['军事','军事（Military） [1] ，即军队事务，古称军务，是与一个国家及政权的国防之武装力量有关的学问及事务。有人认为，军事为政治的一部分，但在中国古代，军、政是分开的。比较正式的说法为，军事是一种政治延续。'],['国际', '国际（International）是一个非常常见的政治用语。它的直接意思是“各个国家之间的”。国际这个词是一个在近代产生的比较新的政治名词'],['太空','星座，是指占星学中必不可少的组成部分之一，亦指天上一群群的恒星组合。自从古代以来，人类便把三五成群的恒星与他们神话中的人物或器具联系起来，称之为“星座”。'],['时尚', '时尚，汉语词语，拼音是shí shàng，指符合潮流的、入时的；流行的风尚；当时的风气和习惯。'],['天气', '天气（weather）是指某一个地区距离地表较近的大气层在短时间内的具体状态。而天气现象则是指发生在大气中的各种自然现象，即某瞬时内大气中各种气象要素（如气温、气压、湿度、风、云、雾、雨、闪、雪、霜、雷、雹、霾等）空间分布的综合表现。'],['自然灾害', '自然灾害（Natural disasters）是指给人类生存带来危害或损害人类生活环境的自然现象。']]



def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


 
if __name__ == "__main__":
    content = "据中国地震台网正式测定，8 月 6 日 2 时 33 分在山东德州市平原县发生 5.5 级地震，震源深度10 公里；3 时 2 分发生 3.0 级地震，震源深度 9 千米。山东全省普遍有震感，北京、河北等多地震感明显。救地震时的自救与互救很重要首先，评估环境与自身状态评估自己的身体状况，对于逃离危险也很重要。我遭遇了什么？我受伤了吗？评估自己是否受伤，伤情的轻重等。如是否出血、是否骨折等。如果发生了出血，特别是喷射状的动脉出血，必须迅速进行止血自救。一般应迅速采取指压止血，或用弹*较好的带子捆压住出血口的上方进行止血。其次，被**时正确脱险 科学自救如果地震时被**在**中，自救最重要的是镇静、除险、求救。设法保护自己，及时排除险情保存生命，坚定生存信念，等待救援。当手臂或其他部位能动时，应逐步清除压物，尽量挣脱出来。不能脱险时，应在嘴和胸的部位 ，逃出一定空间，保证呼吸。其间要想方设法向外界传递求救信息，要尽可能利用手边的简易工具，间歇*地敲打附近坚硬器物，发出求救信号，耐心等待救援。如果被埋在**下的时间比较长，救援人员未到，或者没有听到呼唤信号，就要想办法维持自己的生命，水和食物一定要节约使用，尽量寻找食品和饮用水，必要时自己的*液也能起到解渴作用。防了解地震知识建立应急预案地震是地球运动的必然结果。在地震之前居民最好了解一些地震的基本知识，建立家庭地震应急预案。①在地震高发区，居民可储备饼干、矿泉水等基本的应急食品。②了解居家附近可能的危险源分布情况，一旦发生地震，便于回避。③积极参加单位或社区组织的地震应急演练训练，掌握自救互救基本技能。在已发布地震预报地区的居民须做好家庭防震准备，制定一个家庭防震计划，检查并及时消除家里不利防震的隐患。检查和加固住房，对不利于**的房屋要加固，不宜加固的危房人员要撤离。笨重的房屋装饰物等应拆掉。合理放置家具、物品固定好高大家具，防止倾倒砸人，牢固的家具下面要腾空，以备震时藏身；家具物品摆放做到“重在下，轻在上”，墙上的悬*物要取下来，防止掉下来伤人。清理好杂物，让门口、楼道畅通；阳台护墙要清理，拿掉花盆、杂物。"
    
    start = time.time() 
    multi_classifier = multiTag.get_tags(content, tags)
    end = time.time()
    print(end-start)
    print(multi_classifier)


