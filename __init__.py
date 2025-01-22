import tkintertools as tkt
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import tkintertools.core.configs as configs
import tkintertools.toolbox as toolbox
import tkintertools.animation as animation

import random
import math
import tools

from WEinfo import *

if toolbox.load_font("./LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"

class App_main(tkt.Tk):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		super().center()
		super().resizable(False, False)
		super().icon('./alpha_icon.ico')
		global tip
		tip = tools.tips()
		Home(self)

	# 销毁组件
	def clear_window(self):
		for widget in self.winfo_children():
			widget.destroy()
	
	pass

class Home():
	def __init__(self, root):
		global tip
		#tip = tools.tips()

		main_cv = tkt.Canvas(root, width = 540 / 3 * 2, expand = 'x', auto_zoom = True)
		main_cv.place(x = (540-540/3*2)/2, y = 15)

		tkt.Text(main_cv, (540/3, 0+54), fontsize = 32, text = f'WordEdit Alpha {WordEditVersion[0]}.{WordEditVersion[1]}', anchor = 'center', auto_update = True)
		says = tkt.Text(main_cv, (540/3, 80), fontsize = 16, text = tip.random_tips(Language), anchor = 'center', auto_update = True)
		tkt.Button(main_cv, (540/3-48*2-5, 54+54), fontsize = 24, text = 'Refresh',size = [48*4+10,24+10], 
			command = lambda: says.set(tip.random_tips(Language)))

		animation.GradientItem(
            main_cv, says.texts[0].items[0], "fill", ("red", "orange"), 500, controller=lambda p: math.sin(p*math.pi), repeat=-1).start()
		
		main_cv.update_idletasks()
		main_cv.zoom()

root = App_main(title = f'WordEdit Alpha {WordEditVersion[0]}.{WordEditVersion[1]}',size=[540, 607])
root.mainloop()