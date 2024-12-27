# import
import tkinter as tk
from tkinter import messagebox
from typing import List
from WordEdit_WordsClass import *
from tkinter import ttk
import tools
from random import *

# 开始的一些全局变量
WEversion = 'alpha-v2.1'
_font = '等线'
focus_in_entry_addword_en = '输入英文...'
focus_in_entry_addword_ch = '输入中文...（不同的中文以空格分隔）'
setting = tools.WE_file()
log = logfile(loglevel=1)
word = word_list()

# 清空
def clear_WE():
    log.write('用户清空了窗口的所有组件',2,'windows_delete')
    sum = 0
    for packs in mainwindow.winfo_children(): # 对于每个组件
        log.write(f'销毁组件 {type(packs)}',3,'window_delete')
        sum += 1
        packs.destroy() # 销毁
    
    log.write(f'清空了 {sum} 个组件',2,'window_delete')

# 按下退出：退出程序
def button_exit_WEmain():
    log.write('退出……',1,'window')
    mainwindow.destroy()
    log.write('销毁窗口',2,'window')
    # 设置文件
    setting.write('settings.WE')
    log.write('保存设置',2,'setting')
    # 输出单词
    op = word.output_words()
    if op:
        log.write('单词写入文件出现问题。',1,'error_word')
    else:
        log.write('单词写入文件成功！',2,'word')

    exit(0)

# 按下设置：到达设置
def _button_settings():
    log.write('用户按下设置按钮',2,'window')
    WE_show_settings()

# 按下返回主菜单：回到主菜单
def _button_return_main():
    log.write('用户按下返回主菜单按钮',2,'window')
    WE_show_main()

# 更新单词列表
def refresh_list(wordlist : ttk.Treeview,key = ''):
    log.write(f'更新显示单词列表(key={key})',2,'window')
    global word

    # 删除所有项
    wordlist.delete(*wordlist.get_children())

    def find(st:List[str]):
        #log.write(f'查询 {key} 是否在列表内',3)
        for x in st:
            if(x.find(key) >= 0):
                #log.write('是',3)
                return 1
        #log.write('否',3)
        return 0

    # 重新放入
    i=0
    sum=0
    for w in word:
        if w.wEn.find(key) >= 0 or key == '' or find(w.wCh):
            sum+=1
            wordlist.insert("",tk.END,iid=str(i),values=(w.wEn,",".join(w.wCh)))
        i+=1
    log.write(f'在 key={key} 下找到了 {sum} 个单词',3,'word_list')

# 按下“修改单词”中的“删除”按钮
def _button_del(wordlist : ttk.Treeview):
    log.write(f'用户删除单词',1)
    # 获取选的项（列表）
    focuson = wordlist.selection()

    # 未选中
    if not focuson:
        log.write(f'删除单词：未选中任何项',1)
        messagebox.showerror('错误','未选中表格的任何项！\n请选择后再删除！')
        return None

    # 确认框
    ret = messagebox.askyesno('确认选项',f'确认删除 {len(focuson)} 个单词？')

    # 确认删除
    if ret:
        log.write(f'删除单词：用户确认删除 {len(focuson)} 个单词',1)
        focuson=sorted(focuson,reverse=True)
        for wid in focuson:
            log.write(f'删除单词：删除了单词 {word[int(wid)].wEn},{word[int(wid)].wCh}',2)
            del word[int(wid)]
            wordlist.delete(wid)
        refresh_list(wordlist)

# 按下“修改单词”中的“修改”按钮
def _button_change(wordlist : ttk.Treeview):
    log.write('用户修改单词',1)
    # 获取选的项（列表）
    focuson = wordlist.selection()

    # 未选中
    if not focuson:
        log.write('修改单词：未选中任何项',1)
        messagebox.showerror('错误','未选中表格的任何项！\n请选择一项后再更改！')
        return None

    # 选太多
    if len(focuson) > 1:
        log.write(f'修改单词：选中太多项（{len(focuson)} 项）',1)
        messagebox.showerror('错误','选中的项太多！（最多一个）');
        return None

    # 在 word 中的 id
    wid=int(focuson[0])

    # 更改窗口
    window_chg = tk.Toplevel(master=mainwindow)
    log.write('更改单词：新建更改窗口',2)

    window_chg.resizable(0,0)
    window_chg.config(background='white')
    window_chg.geometry(f'500x300+{(window_chg.winfo_screenwidth()-500)//2}+{(window_chg.winfo_screenheight()-300)//2}')
    window_chg.iconbitmap('alpha_icon.ico')
    window_chg.title('更改单词')

    # 设置子窗口的行为
    window_chg.transient(mainwindow)  # 将子窗口设置为父窗口的子级
    window_chg.grab_set()       # 阻止与父窗口的交互（模态窗口）
    log.write('更改单词：窗口设置成功！',2)

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
    log.write('更改单词：内容设置成功！',2)

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
    log.write('更改单词：按钮设置成功！',2)

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
    log.write('更改单词：内容放置成功，进入消息循环！',2)

    # 消息循环
    window_chg.mainloop()

# 添加单词按钮
def _button_addword(entry_en : tk.Entry,entry_ch : tk.Entry,show_listbox : tk.Listbox):
    log.write('添加单词',1)
    global word
    if entry_en.get().strip() == '' or entry_en.get() == focus_in_entry_addword_en or entry_ch.get().strip() == '' or entry_ch.get() == focus_in_entry_addword_ch:
        log.write('添加单词：用户没有输入',1)
        show_listbox.insert(0,'单词添加失败，请检查后重试！')
    else:
        log.write('添加单词：正在添加',1)
        word.push_back(entry_en.get().strip(),entry_ch.get().strip().split())
        show_listbox.insert(0,'单词 ' + entry_en.get().strip() + ' 添加成功！')
        log.write('添加单词：添加成功',2)
        log.write(f'添加单词：英 {entry_en.get().strip()}，中 {entry_ch.get().strip()}',3)

        # 清空
        entry_en.delete(0,tk.END)
        entry_ch.delete(0,tk.END)
        log.write('添加单词：清空输入框！',2)

        # 检测焦点状况
        if mainwindow.focus_get() != entry_en:
            log.write('添加单词：焦点不在英文输入框！',2)
            entry_en.insert(0,focus_in_entry_addword_en)
            entry_en.config(fg='gray')
        if mainwindow.focus_get() != entry_ch:
            log.write('添加单词：焦点不在中文输入框！',2)
            entry_ch.insert(0,focus_in_entry_addword_ch)
            entry_ch.config(fg='gray')
        log.write('添加单词：根据焦点情况更新完成输入框情况！',2)
    
# 编辑单词界面
def WE_show_editword():
    log.write('进入编辑单词界面',1)
    global word

    clear_WE()

    # 创建标题行
    la = tk.Label(mainwindow,text='编辑单词',background='white',font=(_font,18),width=30,height=2)
    la.pack(pady=0)

    # 创建“单词列表”文本框
    txt1 = tk.Label(mainwindow,text='单词列表',background='white',font=(_font,14))
    txt1.pack(pady=5)

    # 创建“查询单词”输入框
    en_query=tools.EntryEx(mainwindow,placeholder='输入以查询单词……',font=(_font,14),width=50,command=lambda:refresh_list(wordlist,en_query.get()))
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
    log.write('编辑单词：显示完成',1)

# 显示设置界面
def WE_show_settings():
    global setting
    log.write('显示设置界面',1)
    clear_WE()

    # 创建标题行
    la = tk.Label(mainwindow,text='设置',background='white',font=(_font,18),width=30,height=2)
    la.pack(pady=0)

    # 显示一个窗口，并获得用户输入
    def get_user_input(setting_key : str):
        global setting

        # 创建子窗口
        get_inp = tk.Toplevel(master=mainwindow)
        log.write('更改设置：新建获取用户输入窗口',1)

        get_inp.resizable(0,0)
        get_inp.config(background='white')
        get_inp.geometry(f'500x300+{(get_inp.winfo_screenwidth()-500)//2}+{(get_inp.winfo_screenheight()-300)//2}')
        get_inp.iconbitmap('alpha_icon.ico')
        get_inp.title('更改设置')

        # 设置子窗口的行为
        get_inp.transient(mainwindow)  # 将子窗口设置为父窗口的子级
        get_inp.grab_set()       # 阻止与父窗口的交互（模态窗口）
        log.write('更改设置：窗口设置成功！',2)

        # 创建文本框
        entry = tk.Entry(get_inp,font=(_font,14),width=30)
        # 文本框显示初始文字
        entry.insert(0,str(setting[setting_key]))

        fr = tk.Frame(get_inp,background='white')

        def _command_sure(_setting_key : str):pass
        def _command_cancel():pass

        # 创建按钮
        _button_sure=tk.Button(fr,text='确定',font=(_font,14),relief='solid',bd=1,command=lambda _key = setting_key: _command_sure(_key))
        _button_cancel=tk.Button(fr,text='取消',font=(_font,14),relief='solid',bd=1,command=lambda:_command_cancel())
        log.write('更改设置：按钮设置成功！',2)

        # 放置
        entry.pack(pady=5)
        fr.pack(pady=5)
        _button_sure.pack(side=tk.RIGHT,padx=5)
        _button_cancel.pack(side=tk.RIGHT,padx=5)

        # 按下确定
        def _command_sure(_setting_key : str):
            log.write(f'更改设置：用户按下了“确定”',2)
            global setting
            lst_val = setting[_setting_key]
            changed = entry.get()

            # 检验 type 并把返回值变为 type 类型
            if type(lst_val) == int:
                try:
                    changed = int(changed)
                except ValueError:
                    log.write(f'更改设置：用户输入了不符合整数的类型',2)
                    messagebox.showerror('错误','必须输入整数！')
                    return
            elif type(lst_val) == float:
                try:
                    changed = float(changed)
                except ValueError:
                    log.write(f'更改设置：用户输入了不符合浮点数的类型',2)
                    messagebox.showerror('错误','必须输入浮点数！')
                    return

            # 成功更改
            setting[_setting_key] = changed
            log.write(f'更改设置：用户成功更改 {_setting_key} 为 {changed}',1)
            _command_cancel()
            WE_show_settings()

        # 按下取消~~销毁~~按钮
        def _command_cancel():
            log.write('更改设置：用户退出',2)
            get_inp.destroy()

        get_inp.mainloop()

    # 更改的框架
    # 带输入框
    def change_frame_input(setting_key : str,default_value,text = None) -> tk.Frame:
        global setting

        log.write(f'设置：框架创建中（{text},aka({setting_key})）',3)

        if not text: text = setting_key

        # 框架
        fr = tk.Frame(mainwindow,background='white')

        # 显示内容
        lab = tk.Label(fr,text=text,bg='white',font=(_font,14))
        value_lab = tk.Label(fr,text=str(setting[setting_key]),bg='lightgray',font=(_font,14))
        button_reset = tk.Button(fr,text='重置',font=(_font,14),relief='solid',bd=1,command=lambda: _reset_bt(setting_key,default_value))
        button_change = tk.Button(fr,text='更改',font=(_font,14),relief='solid',bd=1,command=lambda: get_user_input(setting_key))

        # pack
        lab.pack(side=tk.LEFT,padx = 5)
        value_lab.pack(side = tk.LEFT,padx = 5)
        button_reset.pack(side = tk.LEFT,padx = 5)
        button_change.pack(side = tk.LEFT,padx = 5)

        # 重设按钮执行函数
        def _reset_bt(setting_key : str,default_value):
            global setting

            setting[setting_key] = default_value

            WE_show_settings()

        log.write(f'设置：框架创建成功（{text},aka({setting_key})）',3)

        return fr

    # 更改类型
    c1 = change_frame_input('checker_num',1,'设置中文的正确个数下限')
    c2 = change_frame_input('show_num',1000,'设置显示中文时显示多少个')

    lb_advance = tk.Label(mainwindow,text='高级',background='white',font=(_font,14,'bold'))
    c3 = change_frame_input('log_level',1,'设置日志级别（0最少，3最多）') # 当然你输入其他数字也行，我不限范围

    # pack
    c1.pack(pady = 5)
    c2.pack(pady = 5)

    lb_advance.pack(pady = 5)
    c3.pack(pady = 5)

    # 返回主菜单按钮
    button_return_main = tk.Button(mainwindow,text='返回主菜单',font=(_font,14),command=_button_return_main,relief='solid',bd=1,width=15)
    button_return_main.pack(pady=10)

    log.write('设置：显示完成',1)

# 显示加单词界面
def WE_show_addword():
    log.write('显示加单词界面',2)

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

    log.write('添加单词：页面显示完成！',2)

# 背单词界面
def WE_show_start():
    global word

    init = 0

    # 没有单词
    if len(word) <= 0:
        log.write('用户尝试背单词，但是好像没有单词呢qwq',1)
        messagebox.showinfo('单词缺失','你还没添加单词！\n快去添加一些吧！')
        return
    
    log.write('用户开始背单词！',1)
    
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
    show1 = tk.Label(mainwindow,background='white',font=(_font,10))
    show1.pack(pady=0)

    # 创建“返回主菜单”按钮
    button_return_main = tk.Button(mainwindow,text='返回主菜单',font=(_font,14),command=_button_return_main,relief='solid',bd=1,width=15)
    button_return_main.pack(pady=10)

    log.write('背单词界面显示完成！',2)

    # 检验是否正确
    def check_word() -> bool:
        log.write('背诵单词：检验单词！',2)
        global ce_type
        global wid
        if ce_type:
            return word[wid].Check_Ch(entry.get().strip().split(),setting['checker_num']) # checker_nums:用户指定至少对的个数
        else:
            return word[wid].Check_En(entry.get().strip())

    # 更新单词
    def update_word():
        log.write('背诵单词：寻找下一个单词！',2)
        global ce_type
        global wid
        wid=word.rand_word()
        ce_type=randint(0,1)
        if ce_type:
            show_word['text']='请根据英文输入中文：'+word[wid].wEn
            log.write(f'背诵单词：给出英文：{word[wid].wEn}',2)
        else:
            tmp1=word[wid].get_Ch(setting['show_num']) # show_num:用户指定显示个数
            show_word['text']='请根据中文输入英文：'+tmp1
            log.write(f'背诵单词：给出英文：{tmp1}',2)

    # 检验并更新结果
    def check_and_update(event = None):
        global init
        init=1
        global ce_type
        global wid
        log.write('背诵单词：检验并更新！',2)
        # 未输入
        if entry.get().strip() == '':
            log.write('背诵单词：检验：用户好像没有输入呢……',2)
            result['text']='请输入内容！'
            show1['text']=''
            result.config(fg='black')
            return

        # 判断
        if check_word():
            log.write('检验单词：单词正确了！太强了！',1)
            result['text']='正确！'
            result.config(fg='green')
            word.Change_P(wid,1)
        else:
            log.write('检验单词：错误了，再接再厉！',1)
            result['text']='错误！'
            result.config(fg='red')
            word.Change_P(wid,0)

        show1['text']='答案：' + (word[wid].wEn if not ce_type else ','.join(word[wid].wCh))

        entry.delete(0,tk.END)
        update_word()
        init=0

    # 更新单词
    update_word()

    entry.bind('<Return>',check_and_update)

# 显示主界面
def WE_show_main():
    log.write('显示主页！',2)
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
    log.write('显示主页完毕！',2)

# 输入单词
log.write('读入单词……')
ret=word.input_words()
if ret:
    if ret == 1:
        log.write('读入单词：找不到文件',1,'warning')
    if ret == 2:
        log.write('读入单词：打不开文件',1,'error')
    if ret == -1:
        log.write('读入单词：格式错误',1,'error')
else:
    log.write('读入成功！')

# 输入设置
log.write('读入设置……')
tmp = setting.read('settings.WE')
if tmp:
    if tmp == 1:
        log.write('文件后缀名不对！不是这怎么弄出来的？',1,'error')
    if tmp == 2:
        log.write('文件格式不对！',1,'error')
    if tmp == 3:
        log.write('找不到设置文件。',1,'warning')
    if tmp == 4:
        log.write('无法打开设置文件',1,'error')
else:
    log.write('读入成功！')

init_settings(setting)
# print(setting)

log.write('进入主程序')

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

log.write('创建窗口成功！')

# 显示窗口
WE_show_main()

log.write('窗口控件显示成功，进入消息循环！')

# 消息循环
mainwindow.mainloop()