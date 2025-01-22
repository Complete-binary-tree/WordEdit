import tkinter.ttk as ttk

import tkintertools as tkt
import tkintertools.core.configs as configs
import tkintertools.theme as theme

theme.set_color_mode("light")

root = tkt.Tk(title="登录")
root.center()

cv = tkt.Canvas(auto_zoom=True)
cv.place(width=1280, height=720)

ttk.Label(cv, text="账 号 登 录", font=(configs.Font.family, -48), anchor="center").place(width=400, height=100, x=440, y=150)

ttk.Label(cv, text="账号").place(x=450, y=300)
ttk.Entry(cv, font=(configs.Font.family, -20)).place(width=380, height=50, x=450, y=340)
ttk.Label(cv, text="密码").place(x=450, y=400)
ttk.Entry(cv, font=(configs.Font.family, -20), show="●").place(width=380, height=50, x=450, y=440)

ttk.Button(cv, text="注 册").place(width=180, height=50, x=450, y=540)
ttk.Button(cv, text="登 录").place(width=180, height=50, x=650, y=540)

root.mainloop()