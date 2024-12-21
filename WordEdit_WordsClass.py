from typing import List

class words:
    # 自己，英语，中文，熟练度
    def __init__(self,wEn : str,wCh : List[str],wP = 5):
        self.wEn=wEn
        self.wCh=wCh
        self.wP=wP
        
    # 检验英文是否正确
    def Check_En(self,En : str) -> bool:
        print(f'检验英文：{En}')
        if En == self.wEn:
            return 1
        else:
            return 0

    # 检验中文是否正确
    def Check_Ch(self,Ch : List[str]) -> bool:
        print(f'检验中文：{Ch}')
        for useropt in Ch:
            for selfword in self.wCh:
                if useropt == selfword:
                    return 1
        return 0

    # 根据回答正确与否更改熟练度
    def Change_P(self,check_result : bool) -> None:
        if check_result:
            self.wP = max(self.wP-1,1)
        else:
            self.wP = min(self.wP+2,5)

word = []

# 读入
def input_words() -> int:
    print('正在读取单词……')
    global word
    # 文件格式
    # English (\t) Chinese1 Chinese2 ... (\t) 熟练度
    try:
        # 读入 words.dat 文件
        with open('words.dat','r',encoding = 'UTF-8') as file:
            for line in file:
                # 分开
                En,Ch,P = line.split('\t')

                # 再分
                Ch=Ch.split()
                P=int(P)

                # 判定
                if En == '' or Ch == '' or P < 1 or P > 5:
                    print('文件格式错误！')
                    word=[]
                    return -1

                # 放入后面
                word.append(words(En,Ch,P))
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
        word = []
        return -1

# 输出
def output_words():
    with open('words.dat','w',encoding = 'UTF-8') as opt:
        print('正在保存单词……')
        for _word in word:
            opt.write(_word.wEn + '\t' + ' '.join(_word.wCh) + '\t' + str(_word.wP) + '\n')
            # print("111")
        print('保存成功')