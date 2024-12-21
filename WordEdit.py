# import
import tkinter as tk
from tkinter import messagebox
from typing import List
from WordEdit_WordsClass import *
from tkinter import ttk
import TKtools as extk
from random import *

# 开始的一些全局变量
WEversion = 'alpha-v2.1'
_font = '等线'
focus_in_entry_addword_en = '输入英文...'
focus_in_entry_addword_ch = '输入中文...（不同的中文以空格分隔）'

# 清空
def clear_WE():
    for packs in mainwindow.winfo_children(): # 对于每个组件
        packs.destroy() # 销毁

# 按下退出：退出程序
def button_exit_WEmain():
    mainwindow.destroy()

    # 输出单词
    output_words()

    exit(0)

# 按下设置：到达设置
def _button_settings():
    WE_show_settings()

# 按下返回主菜单：回到主菜单
def _button_return_main():
    WE_show_main()

# 更新单词列表
def refresh_list(wordlist : ttk.Treeview,key = ''):
    global word

    # 删除所有项
    wordlist.delete(*wordlist.get_children())

    #wordlist.insert("",tk.END,values=(str('key'.find(key)),key))

    def find(st:List[str]):
        for x in st:
            if(x.find(key) >= 0):
                return 1
        return 0

    # 重新放入
    i=0
    for w in word:
        if w.wEn.find(key) >= 0 or key == '' or find(w.wCh):
            wordlist.insert("",tk.END,iid=str(i),values=(w.wEn,",".join(w.wCh)))
        i+=1

# 按下“修改单词”中的“删除”按钮
def _button_del(wordlist : ttk.Treeview):
    # 获取选的项（列表）
    focuson = wordlist.selection()

    # 未选中
    if not focuson:
        messagebox.showerror('错误','未选中表格的任何项！\n请选择后再删除！')
        return None

    # 确认框
    ret = messagebox.askyesno('确认选项',f'确认删除 {len(focuson)} 个单词？')

    # 确认删除
    if ret:
        for wid in focuson:
            del word[int(wid)]
            wordlist.delete(wid)
        refresh_list(wordlist)

# 按下“修改单词”中的“修改”按钮
def _button_change(wordlist : ttk.Treeview):
    # 获取选的项（列表）
    focuson = wordlist.selection()

    # 未选中
    if not focuson:
        messagebox.showerror('错误','未选中表格的任何项！\n请选择一项后再更改！')
        return None

    # 选太多
    if len(focuson) > 1:
        messagebox.showerror('错误','选中的项太多！（最多一个）');
        return None

    # 在 word 中的 id
    wid=int(focuson[0])

    # 更改窗口
    window_chg = tk.Toplevel(master=mainwindow)

    window_chg.resizable(0,0)
    window_chg.config(background='white')
    window_chg.geometry(f'500x300+{(window_chg.winfo_screenwidth()-500)//2}+{(window_chg.winfo_screenheight()-300)//2}')
    window_chg.iconbitmap('alpha_icon.ico')
    window_chg.title('更改单词')

    # 设置子窗口的行为
    window_chg.transient(mainwindow)  # 将子窗口设置为父窗口的子级
    window_chg.grab_set()       # 阻止与父窗口的交互（模态窗口）

    # 创建内容
    fren=tk.Frame(window_chg)
    frch=tk.Frame(window_chg)
    frbu=tk.Frame(window_chg,bg='white')
    la=tk.Label(window_chg,text='更改单词',background='white',font=(_font,18),width=30,height=2)
    en_en=tk.Entry(fren,font=(_font,14),width=30)
    en_en.insert(0,word[wid].wEn)
    en_ch=tk.Entry(frch,text=' '.join(word[wid].wCh),font=(_font,14),width=30)
    en_ch.insert(0,' '.join(word[wid].wCh))
    tit_en=tk.Label(fren,text='英文：',background='white',font=(_font,14))
    tit_ch=tk.Label(frch,text='中文：',background='white',font=(_font,14))

    # 按钮事件
    def _command_sure():
        if en_en.get() == '' or en_ch.get() == '':
            messagebox.showerror('错误','单词不能为空！')
        else:
            word[wid].wEn=en_en.get()
            word[wid].wCh=en_ch.get().split()
            refresh_list(wordlist)
            window_chg.destroy()

    def _command_cancel():
        window_chg.destroy()

    _button_sure=tk.Button(frbu,text='确定',font=(_font,14),relief='solid',bd=1,command=_command_sure)
    _button_cancel=tk.Button(frbu,text='取消',font=(_font,14),relief='solid',bd=1,command=_command_cancel)

    # 放置内容
    la.pack(pady=5)
    tit_en.pack(side=tk.LEFT)
    en_en.pack(side=tk.RIGHT)
    tit_ch.pack(side=tk.LEFT)
    en_ch.pack(side=tk.RIGHT)
    _button_sure.pack(side=tk.LEFT)
    _button_cancel.pack(side=tk.RIGHT,padx=5)

    fren.pack(pady=5)
    frch.pack(pady=5)
    frbu.pack(pady=10)

    # 消息循环
    window_chg.mainloop()

# 添加单词按钮
def _button_addword(entry_en : tk.Entry,entry_ch : tk.Entry,show_listbox : tk.Listbox):
    global word
    if entry_en.get().strip() == '' or entry_en.get() == focus_in_entry_addword_en or entry_ch.get().strip() == '' or entry_ch.get() == focus_in_entry_addword_ch:
        show_listbox.insert(0,'单词添加失败，请检查后重试！')
    else:
        word.append(words(entry_en.get().strip(),entry_ch.get().strip().split()))
        show_listbox.insert(0,'单词 ' + entry_en.get().strip() + ' 添加成功！')

        # 清空
        entry_en.delete(0,tk.END)
        entry_ch.delete(0,tk.END)

        # 检测焦点状况
        if mainwindow.focus_get() != entry_en:
            entry_en.insert(0,focus_in_entry_addword_en)
            entry_en.config(fg='gray')
        if mainwindow.focus_get() != entry_ch:
            entry_ch.insert(0,focus_in_entry_addword_ch)
            entry_ch.config(fg='gray')
    
# 编辑单词界面
def WE_show_editword():
    global word

    clear_WE()

    # 创建标题行
    la = tk.Label(mainwindow,text='编辑单词',background='white',font=(_font,18),width=30,height=2)
    la.pack(pady=0)

    # 创建“单词列表”文本框
    txt1 = tk.Label(mainwindow,text='单词列表',background='white',font=(_font,14))
    txt1.pack(pady=5)

    # 创建“查询单词”输入框
    en_query=extk.EntryEx(mainwindow,placeholder='输入以查询单词……',font=(_font,14),width=50,command=lambda:refresh_list(wordlist,en_query.get()))
    en_query.pack(pady=5)

    # 创建框架来存放单词列表
    wordlist_frame = tk.Frame(mainwindow,bg='white')
    wordlist_frame.pack(pady=5)

    # 创建单词列表
    wordlist = ttk.Treeview(wordlist_frame,columns=('单词','中文意思'),show='headings',height=9)
    wordlist.heading('单词',text='单词')
    wordlist.heading('中文意思',text='中文意思')
    wordlist.column('单词',width=100)
    wordlist.column('中文意思',width=300)

    # 创建单词表滚动条
    scroll_y = tk.Scrollbar(wordlist_frame, orient=tk.VERTICAL, command=wordlist.yview)

    # 输入单词
    refresh_list(wordlist)

    # 添加表格到框架
    wordlist.pack(side=tk.LEFT)
    scroll_y.pack(side=tk.LEFT, fill=tk.Y)

    # 按钮框架
    button_frame=tk.Frame(wordlist_frame,bg='white')
    button_frame.pack(side=tk.RIGHT, padx=20)

    # 创建按钮
    button_del=tk.Button(button_frame,text='删除',font=(_font,14),relief='solid',bd=1,command=lambda: _button_del(wordlist))
    button_del.pack(pady=5)

    button_chg=tk.Button(button_frame,text='修改',font=(_font,14),relief='solid',bd=1,command=lambda: _button_change(wordlist))
    button_chg.pack(pady=5)

    #button_chg=tk.Button(button_frame,text='查询',font=(_font,14),relief='solid',bd=1)
    #button_chg.pack(pady=5)

    # 返回主菜单按钮
    button_return_main = tk.Button(mainwindow,text='返回主菜单',font=(_font,14),command=_button_return_main,relief='solid',bd=1,width=15)
    button_return_main.pack(pady=10)

# 显示设置界面
def WE_show_settings():
    clear_WE()

    # 创建标题行
    la = tk.Label(mainwindow,text='设置',background='white',font=(_font,18),width=30,height=2)
    la.pack(pady=0)

    # 返回主菜单按钮
    button_return_main = tk.Button(mainwindow,text='返回主菜单',font=(_font,14),command=_button_return_main,relief='solid',bd=1,width=15)
    button_return_main.pack(pady=10)

# 显示加单词界面
def WE_show_addword():
    clear_WE()

    # 创建标题行
    la = tk.Label(mainwindow,text='添加单词',background='white',font=(_font,18),width=30,height=2)
    la.pack(pady=0)

    # 创建文本框
    entry_adden=tk.Entry(mainwindow,fg='gray',font=(_font,14),width=50)
    entry_adden.insert(0,focus_in_entry_addword_en)
    entry_addch=tk.Entry(mainwindow,fg='gray',font=(_font,14),width=50)
    entry_addch.insert(0,focus_in_entry_addword_ch)

    # 创建是否在焦点时的事件
    entry_adden.bind('<FocusIn>',lambda even: exec("entry_adden.delete(0,tk.END)\nentry_adden.config(fg='black')") if entry_adden.get() == focus_in_entry_addword_en else None)
    entry_adden.bind('<FocusOut>',lambda even: exec("entry_adden.insert(0,focus_in_entry_addword_en)\nentry_adden.config(fg='gray')")if entry_adden.get() == '' else None)
    entry_addch.bind('<FocusIn>',lambda even: exec("entry_addch.delete(0,tk.END)\nentry_addch.config(fg='black')") if entry_addch.get() == focus_in_entry_addword_ch else None)
    entry_addch.bind('<FocusOut>',lambda even: exec("entry_addch.insert(0,focus_in_entry_addword_ch)\nentry_addch.config(fg='gray')")if entry_addch.get() == '' else None)
    
    # 显示文本框
    entry_adden.pack(pady=3)
    entry_addch.pack(pady=3)

    # 创建状态列表
    listbox = tk.Listbox(width=30,height=5,font=(_font,14))

    # 创建“添加单词”按钮
    button_return_main = tk.Button(mainwindow,text='添加单词',font=(_font,14),command=lambda: _button_addword(entry_adden,entry_addch,listbox),relief='solid',bd=1,width=15)
    button_return_main.pack(pady=3)

    # 显示状态列表
    listbox.pack(pady=5)

    # 创建“返回主菜单”按钮
    button_return_main = tk.Button(mainwindow,text='返回主菜单',font=(_font,14),command=_button_return_main,relief='solid',bd=1,width=15)
    button_return_main.pack(pady=10)
# 背单词界面
def WE_show_start():
    global word

    # 没有单词
    if len(word) <= 0:
        messagebox.showinfo('单词缺失','你还没添加单词！\n快去添加一些吧！')
        return

    clear_WE()

    wid=0 # 单词编号
    ce_type=0 # 0英文1中文

    # 创建标题行
    la = tk.Label(mainwindow,text='背单词',background='white',font=(_font,18),width=30,height=2)
    la.pack(pady=0)

    # 创建单词行
    show_word = tk.Label(mainwindow,background='white',font=(_font,14))
    show_word.pack(pady=0)
    #word['text']='w'

    # 创建输入框
    entry = tk.Entry(mainwindow,font=(_font,14))
    entry.pack(pady=5)

    # 创建检验按钮
    check = tk.Button(mainwindow,font=(_font,14),text='确定(Enter)',width=15,relief='solid',bd=1,command=lambda: check_and_update())
    check.pack(pady=5)

    # 创建检验结果行
    result = tk.Label(mainwindow,background='white',font=(_font,14),text='还没有测试过哦！')
    result.pack(pady=0)

    # 创建“返回主菜单”按钮
    button_return_main = tk.Button(mainwindow,text='返回主菜单',font=(_font,14),command=_button_return_main,relief='solid',bd=1,width=15)
    button_return_main.pack(pady=10)

    # 检验是否正确
    def check_word() -> bool:
        global ce_type
        if ce_type:
            return word[wid].Check_Ch(entry.get().strip().split())
        else:
            return word[wid].Check_En(entry.get().strip())

    # 更新单词
    def update_word():
        global ce_type
        wid=randint(1,len(word))-1
        ce_type=randint(0,1)
        if ce_type:
            show_word['text']='请根据英文输入中文：'+word[wid].wEn
        else:
            show_word['text']='请根据中文输入英文：'+','.join(word[wid].wCh)

    # 检验并更新结果
    def check_and_update():
        # 未输入
        if entry.get().strip() == '':
            result['text']='请输入内容！'
            result.config(fg='black')
            return

        # 判断
        if check_word():
            result['text']='正确！'
            result.config(fg='green')
            word[wid].Change_P(1)
        else:
            result['text']='错误！'
            result.config(fg='red')
            word[wid].Change_P(0)
        entry.delete(0,tk.END)
        update_word()

    # 更新单词
    update_word()

# 显示主界面
def WE_show_main():
    clear_WE()

    # 创建标题行
    la = tk.Label(mainwindow,text='WordEdit(Alpha)',background='white',font=(_font,24),width=30,height=2)
    la.pack(pady=0)

    # 创建“开始背诵”按钮
    button_start=tk.Button(mainwindow,text='开始背诵',font=(_font,14),relief='solid',bd=1,width=15,command = lambda: WE_show_start())
    button_start.pack(pady=5)

    # 创建“添加单词”按钮
    button_addword=tk.Button(mainwindow,text='添加单词',font=(_font,14),command = lambda:WE_show_addword(),relief='solid',bd=1,width=15)
    button_addword.pack(pady=5)

    # 创建“编辑单词”按钮
    button_editword=tk.Button(mainwindow,text='编辑单词',font=(_font,14),command = lambda:WE_show_editword(),relief='solid',bd=1,width=15)
    button_editword.pack(pady=5)

    # 创建“设置”按钮
    button_settings=tk.Button(mainwindow,text='设置',font=(_font,14),command=_button_settings,relief='solid',bd=1,width=15)
    button_settings.pack(pady=5)

    # 创建“退出”按钮
    button_exit = tk.Button(mainwindow,text='退出',font=(_font,14),command=button_exit_WEmain,relief='solid',bd=1,width=15)
    button_exit.pack(pady=5)

# 输入单词
ret=input_words()

# 创建窗口
mainwindow = tk.Tk();

# 窗口标题
mainwindow.title('Wordedit Alpha')

# 窗口背景
mainwindow.config(background='white')

# 窗口大小、居中
mainwindow.geometry(f'700x400+{(mainwindow.winfo_screenwidth()-700)//2}+{(mainwindow.winfo_screenheight()-400)//2}');

# 锁定高度、宽度
mainwindow.resizable(0,0)

# 窗口图标
mainwindow.iconbitmap('alpha_icon.ico')

# 绑定窗口关闭事件
mainwindow.protocol("WM_DELETE_WINDOW", button_exit_WEmain)

# 显示窗口
WE_show_main()

# 消息循环
mainwindow.mainloop()