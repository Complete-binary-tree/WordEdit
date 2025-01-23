import tkintertools as tkt
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import tkintertools.core.configs as configs
import tkintertools.toolbox as toolbox
import tkintertools.animation as animation
import tkintertools.theme as theme

import random
import math
import tools

from WEinfo import *

class App_main(tkt.Tk):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		super().center()
		super().resizable(False, False)
		super().icon('./alpha_icon.ico')

		# 加载必备项
		self.preload()

		Home(self)

	# 销毁组件
	def clear_window(self):
		for widget in self.winfo_children():
			widget.destroy()

	def preload(self):
		# 载入设置

		# 载入语言
		global lang
		lang = tools.language()

		# 载入 tips
		global tip
		tip = tools.tips()

class Home():
	def __init__(self, root):
		global tip
		global lang

		main_cv = tkt.Canvas(root, width = 540 / 3 * 2, expand = 'x', auto_zoom = True)
		main_cv.place(x = (540-540/3*2)/2, y = 15)

		tkt.Text(main_cv, (540/3, 0+54), fontsize = 32, text = f'WordEdit Alpha {WordEditVersion[0]}.{WordEditVersion[1]}', anchor = 'center', auto_update = True)
		says = tkt.Text(main_cv, (540/3, 80), fontsize = 16, text = tip.random_tips(Language), anchor = 'center', auto_update = True)
		tkt.Button(main_cv, (540/3-48*2-5, 54+54), fontsize = 24, text = lang.get('refresh', Language),size = [48*4+10,24+10], 
			command = lambda: says.set(tip.random_tips(Language)))
		tkt.Button(main_cv, (540/3-48*2-5, 54+54+54), fontsize = 24, text = lang.get('settings', Language),size = [48*4+10,24+10])

		animation.GradientItem(
            main_cv, says.texts[0].items[0], "fill", ("red", "orange"), 500, controller=lambda p: math.sin(p*math.pi), repeat=-1).start()
		
		main_cv.update_idletasks()
		main_cv.zoom()

# 设置字体
if toolbox.load_font("./LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"
root = App_main(title = f'WordEdit Alpha {WordEditVersion[0]}.{WordEditVersion[1]}',size=[540, 607])
root.mainloop()