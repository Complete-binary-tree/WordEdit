from typing import List
import tools
import time
import random

class logfile:
    def __init__(self,loglevel = 1): 
        if ('setting' in globals()) and ('log_level' in setting):
            self.loglevel = setting['log_level']
        self.logfile = open('WordEdit_LogFile_' + time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime()) + '.txt','w',encoding='utf-8')
        self.loglevel = loglevel # 日志等级，1~3，3为详细
        self.logfile.write('-' * 10 + f' [Logfile {time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())}] ' + '-' * 10)

    def write(self,logstr : str,log_level = 1,log_type = None):
        if ('setting' in globals()) and ('log_level' in setting):
            self.loglevel = setting['log_level']
        if log_level <= self.loglevel:
            self.logfile.write(time.strftime('[%H:%M:%S] ', time.localtime()) + (f'[{log_type}] ' if log_type else '') + logstr + '\n')

class words:
    # 自己，英语，中文，熟练度
    def __init__(self,wEn : str,wCh : List[str],wP = 5):
        self.wEn=wEn
        self.wCh=wCh
        self.wP=wP
        
    # 检验英文是否正确
    def Check_En(self,En : str) -> bool:
        # print(f'检验英文：{En}')
        if En == self.wEn:
            return 1
        else:
            return 0

    # 检验中文是否正确
    def Check_Ch(self,Ch : List[str], least_correct_num = 1) -> bool:
        # print(f'检验中文：{Ch}')
        Ch = list(set(Ch)) # 去重
        truecnt = 0
        for useropt in Ch:
            for selfword in self.wCh:
                # 特殊符号
                if selfword[0] == '(' and selfword[-1] == ')': continue
                if selfword[0] == '[' and selfword[-1] == ']': selfword=selfword[1:-1]

                if useropt == selfword:
                    truecnt += 1
                    break
        
        allcnt= 0
        for selfword in self.wCh:
            # 特殊符号
            if selfword[0] == '(' and selfword[-1] == ')': continue
            if selfword[0] == '[' and selfword[-1] == ']': continue
            allcnt += 1

        if truecnt >= least_correct_num or truecnt >= allcnt:
            return 1
        return 0
    
    # 获取中文
    def get_Ch(self,Ch_num = 1000000) -> str:
        if Ch_num <= 0: Ch_num = 1000000
        if Ch_num >= len(self.wCh):
            return ','.join(self.wCh)
        ret = self.wCh
        for i in range(len(self.wCh) - Ch_num):
            del ret[random(0,len(ret)-1)]
        return ','.join(ret)

class word_list(List):
    def __init__(self):
        self.clear()
    
    # 清空
    def clear(self):
        super().clear()
        self.p=[0,0,0,0,0,0]
    
    # 读入
    # 返回 0 正常
    # 1 找不到文件
    # 2 读取错误
    # -1 格式错误
    def input_words(self, filename = 'words.dat') -> int:
        self.clear()
        print('正在读取单词……')
        # 文件格式
        # English (\t) Chinese1 Chinese2 ... (\t) 熟练度
        try:
            # 读入 words.dat 文件
            with open(filename,'r',encoding = 'UTF-8') as file:
                for line in file:
                    # 分开
                    En,Ch,P = line.split('\t')

                    # 再分
                    Ch=Ch.split()
                    P=int(P)
                    #self.p[P] += 1

                    # 判定
                    if En == '' or Ch == '' or P < 1 or P > 5:
                        print('文件格式错误！')
                        self=[]
                        return -1

                    # 放入后面
                    self.push_back(En,Ch,P)
            print('读取成功！')
            return 0

        # 找不到文件
        except FileNotFoundError:
            print('读取失败：缺失文件 words.dat。')
            return 1
        # 文件读取错误
        except IOError:
            print('读取失败：文件读取错误。')
            return 2
        # 转换出错
        except ValueError:
            print('文件格式错误。')
            self = [],self.p=[]
            return -1
    
    # 输出
    # 返回 0 正常
    # 1 文件输出错误
    def output_words(self,filename='words.dat') -> int:
        try:
            with open(filename,'w',encoding = 'UTF-8') as opt:
                print('正在保存单词……')
                for _word in self:
                    opt.write(_word.wEn + '\t' + ' '.join(_word.wCh) + '\t' + str(_word.wP) + '\n')
                print('保存成功')
        except IOError:
            return 1
        return 0

    # 插入最后
    def push_back(self,wEn : str,wCh : List[str],wP = 5):
        wCh = list(set(wCh))
        for i in self:
            if i.wEn == wEn:
                i.wCh += wCh
                i.wCh = list(set(i.wCh))
                self.p[i.wP]=0
                i.wP = max(i.wP,wP)
                self.p[i.wP]=1
                return
        self.append(words(wEn,wCh,wP))
        self.p[wP] += 1

    # 随机单词
    def rand_word(self) -> words:
        tmp = 0
        while 1:
            tmp=random.randint(1,100)
            if tmp <= 10:
                if self.p[1]:
                    tmp = 1
                    break
            elif tmp <= 40:
                if self.p[2]:
                    tmp = 2
                    break
            elif self.p[3] or self.p[4] or self.p[5]:
                tmp = 3
                break
        
        while 1:
            tmp2 = random.randint(0,len(self)-1)
            if self[tmp2].wP == tmp and tmp <= 2:
                return tmp2
            if self[tmp2].wP >= 3 and tmp == 3:
                return tmp2
    
    # 更新一个单词
    # 正常返回 0
    def update_word(self, pos : int, word : words) -> int:
        self.p[self[pos].wP] -= 1
        self.p[word.wP] += 1
        self[pos] = word
    
    # 根据回答正确与否更改熟练度
    def Change_P(self,wid : int,check_result : bool) -> None:
        self.p[self[wid].wP]-=1
        if check_result:
            self[wid].wP = max(self[wid].wP-1,1)
        else:
            self[wid].wP = min(self[wid].wP+2,5)
        self.p[self[wid].wP]+=1

# 设置初始化
def init_settings(setting : tools.WE_file) -> tools.WE_file:
    ret = tools.WE_file()
    ret.update({
        'checker_num':1, # 检验答案需要几个（中文）正确
        'show_num':1000, # 显示几个中文
        'log_level':1 # 日志等级
    })
    for key,value in ret.items():
        if not (key in setting):
            setting[key]=value