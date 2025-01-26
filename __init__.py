import maliang as ml
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
import maliang.core.configs as configs
import maliang.toolbox as toolbox
import maliang.animation as animation
import maliang.theme as theme

import time
import random
import math
import tools

from WEinfo import *

# 临时动画管理
animations = []

class App_main(ml.Tk):
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
		global animations
				
		#controller = animation.generate(math.sin, 0, math.pi, map_y=False)
		#animation.Animation(1000, self.alpha, controller = controller)

		for at in animations:
			at.stop()
		animations.clear()
		for cv in self.canvases:
			cv.destroy()

	def preload(self):
		# 载入语言
		global lang
		lang = tools.language()

		# 载入设置
		global _setting
		_setting = settings()

		# 载入 tips
		global tip
		tip = tools.tips(pack = _setting['tips_pack'] if 'tips_pack' in _setting else None)

class Home():
	def __init__(self, root : App_main):
		global tip
		global lang
		global _setting
		global animations

		root.clear_window()

		bg_cv = ml.Canvas(root, width = 540, height = 607,auto_zoom = True)
		bg_cv.place(x = 0, y = 0)

		main_cv = ml.Canvas(root, width = 540, expand = 'x', auto_zoom = True)
		main_cv.place(x = 0, y = 15)

		ml.Text(main_cv, (540/2, 0+54), fontsize = 32, text = f'WordEdit Alpha {WordEditVersion[0]}.{WordEditVersion[1]}', anchor = 'center')
		says = ml.Text(main_cv, (540/2, 80), fontsize = 16, text = tip.random_tips(), anchor = 'center')
		ml.Button(main_cv, (540/2-48*2-5, 54*2), fontsize = 24, text = lang.get('tip_refresh', Language),size = [48*4+10,24+10], 
			command = lambda: says.set(tip.random_tips()))
		ml.Button(main_cv, (540/2-48*2-5, 54*3), fontsize = 24, text = lang.get('start', Language),size = [48*4+10,24+10])
		ml.Button(main_cv, (540/2-48*2-5, 54*4), fontsize = 24, text = lang.get('settings', Language),
			 size = [48*4+10,24+10], command = lambda: _setting.show(root))
		ml.Button(main_cv, (540/2-48*2-5, 54*5), fontsize = 24, text = lang.get('exit', Language),
			 size = [48*4+10,24+10], command = lambda: root.quit())

		an1 = animation.GradientItem(
            main_cv, says.texts[0].items[0], "fill", (_setting['tips_color_begin'], _setting['tips_color_end']), _setting['tips_change_time'], controller=lambda p: math.sin(p*math.pi), repeat=-1)
		animations.append(an1)
		an1.start()
		
		main_cv.update_idletasks()
		main_cv.zoom()

class settings(tools.WEfile):
	def __init__(self):
		self.read('settings.WE')
		self.update_settings()

	#def __del__(self):
	#	self.write('settings.WE')

	def show(self, root : App_main, default = None):
		root.clear_window() # 删掉！删掉！一定要删掉！
		self.rt = root

		cv = ml.Canvas(root, width = 540, height = 607, expand = 'x', auto_zoom = True)
		cv.place(x = 0, y = 0)

		self.cvleft = cvleft = ml.Canvas(root, width = 150, height = 607, auto_zoom = True)
		cvleft.place(x = 0, y = 0)
		self.create_left_rect(default)

		self.cvright = cvright = ml.Canvas(root, width = 540-150, height = 607, auto_zoom = True)
		cvright.place(x = 150, y = 0)
		
	def create_left_rect(self, default = None):
		if theme.get_color_mode() == 'light':
			self.cvleft.create_rectangle(0, 0, 150, 607, fill = "gray97", outline = 'gray97')
		else:
			self.cvleft.create_rectangle(0, 0, 150, 607, fill = "gray3", outline = 'gray3')

		ml.Text(self.cvleft, (150 / 2, 32), text = lang.get('settings', Language), fontsize = 32, anchor = 'center')
		ml.SegmentedButton(self.cvleft, (150 / 2, 64), sizes = [[160, 40], [160, 40], [160, 40]], text = 
					  (lang.get('show', Language), lang.get('tips', Language), lang.get('language', Language)), 
					  fontsize = 24, anchor = 'n', layout="vertical", command = self.call_segbutton,default = default)
		ml.Button(self.cvleft, (150 / 2, 580), size = [160, 40], fontsize = 24,
			 text = lang.get('return', Language), anchor = 'center', command = lambda root = root: Home(root))

	# 各标签页的转换和渲染
	def call_segbutton(self, index : int):
		#print(index)
		for ans in animations:
			ans.stop()
		self.cvright.destroy()
		self.cvright = ml.Canvas(root, width = 540-150, height = 607, auto_zoom = True)
		self.cvright.place(x = 150, y = 0)
		#for things in self.cvright.children.values():
		#	print(type(things))
		#	things.destroy()

		match index:
			case 0: # 图像
				# ----dark mode----
				ml.Text(self.cvright, (10, 10), fontsize = 20, text = lang.get('dark_mode',Language))
				def switchh():pass
				sw = ml.Switch(self.cvright, (300, 10), default = theme.get_color_mode() == 'dark', command = lambda b:switchh(b))
				def switchh(b):
					sw.disable()
					theme.set_color_mode("dark" if b else "light")
					self.create_left_rect()
					sw.disable(False)
				
			case 1:
				# ----小贴士包----
				ml.Text(self.cvright, (10, 10), fontsize = 20, text = lang.get('tips_pack', Language))

				# ----小贴士包重新检测按钮----
				entry = None
				def reload_command():
					tip.load()
					self.call_segbutton(1)

				ml.Button(self.cvright, (170, 48), fontsize = 20, text = lang.get('refresh_tp', Language),
			   			   size = [200, 30], command = reload_command)
				
				# 颜色选择
				ml.Text(self.cvright, (10, 90), fontsize = 20, text = lang.get('tips_change_color', Language))
				txt = ml.Button(self.cvright, (150, 88), fontsize = 20, text = _setting['tips_color_begin'], 
					 size = [100, 30], command = lambda: ml.TkColorChooser(title = lang.get('select_tips_color', Language), 
											 color = _setting['tips_color_begin'], master = self.rt, command = select_color_1))
				an1 = animation.GradientItem(
            		self.cvright, txt.texts[0].items[0], "fill", (_setting['tips_color_begin'], _setting['tips_color_begin']), 1, repeat = -1)
				an1.start()
				txt2 = ml.Button(self.cvright, (270, 88), fontsize = 20, text = _setting['tips_color_end'], 
					  size = [100, 30], command = lambda: ml.TkColorChooser(title = lang.get('select_tips_color', Language), 
											 color = _setting['tips_color_end'], master = self.rt, command = select_color_2))
				an2 = animation.GradientItem(
            		self.cvright, txt2.texts[0].items[0], "fill", (_setting['tips_color_end'], _setting['tips_color_end']), 1, repeat = -1)
				an2.start()
				animations.append(an1)
				animations.append(an2)
				ml.Text(self.cvright, (255, 90), fontsize = 20, text = '~')

				def select_color_1(color):
					_setting['tips_color_begin'] = color
					self.call_segbutton(1)
				def select_color_2(color):
					_setting['tips_color_end'] = color
					self.call_segbutton(1)

				# 时间修改
				def change_command(new_val):
					if self.rt.focus_get() == entry_sb: return
					new_val = entry_sb.get()
					print('new_val')
					try:
						new_val = int(new_val)
					except ValueError:
						print('VE')
						messagebox.showerror(message = lang.get('time_should_be_int', Language))
						#if entry_sb != None: entry_sb.set(str(_setting['tips_change_time']))
						self.call_segbutton(1)
						return
					
					if new_val <= 0:
						print('VE2')
						messagebox.showerror(message = lang.get('time_should_bigger_than_0', Language))
						#if entry_sb != None: entry_sb.set(str(_setting['tips_change_time']))
						self.call_segbutton(1)
						return
					
					_setting['tips_change_time'] = new_val

				ml.Text(self.cvright, (10, 130), fontsize = 20, text = lang.get('tips_change_time', Language))
				#tmp_cv = ml.Canvas(self.cvright, width = 120, height = 50, auto_zoom = True).place(x = 190, y = 118)
				entry_sb = ml.SpinBox(self.cvright, (200, 128), fontsize = 20, default = str(_setting['tips_change_time']), size = [100, 30])
				entry_sb.bind('<Leave>', change_command)

				# ----小贴士包切换按钮----
				def sure_command(b : int):pass
				entry = ml.OptionButton(self.cvright, (170, 8), fontsize = 20, text = tip.packs, 
							 size = [200,30], align = 'down',command = lambda b: sure_command(b))
				entry.set(tip.packs.index(tip.pack))				

				def sure_command(b : int):
					global Language
					#print(entry.get())
					tip.pack = _setting['tips_pack'] = tip.packs[b]
				
				# ----小贴士提示----
				ml.Text(self.cvright, (10, 170), fontsize = 20, text = lang.get('tips_pack_tip', Language))

			case 2:
				# ----文本----
				# ----语言切换----
				ml.Text(self.cvright, (10, 10), fontsize = 20, text = lang.get('language',Language))

				#ml.Button(self.cvright, (355, 8), fontsize = 20, size = [30, 30], text = '√', family = 'Consolas', command = sure_command)

				# ----语言切换提示----
				ml.Text(self.cvright, (10, 90), fontsize = 20, text = lang.get('language_change_tip',Language))

				# ----按钮----
				# 刷新语言按钮
				ml.Button(self.cvright, (170, 48), fontsize = 20, text = lang.get('refresh_l', Language), 
							 size = [200,30], command = lambda: 0 or lang.__init__() or self.call_segbutton(2))
				# 语言切换按钮
				def sure_command(b : int):pass
				entry = ml.OptionButton(self.cvright, (170, 8), fontsize = 20, text = list(lang.keys()), 
							 size = [200,30], align = 'down',command = lambda b: sure_command(b))
				entry.set(list(lang.keys()).index(Language))

				def sure_command(b : int):
					global Language
					#print(entry.get())
					_setting['language'] = Language = list(lang.keys())[b]
					self.show(self.rt, 2)
					self.call_segbutton(2)


	def update_settings(self):
		global Language

		#print(self)

		if 'language' in self.keys():
			Language = self['language']
			if not (Language in lang.keys()):
				print('settings:language cannot find.')
				Language = self['language'] = 'English'
		else:
			Language = 'English'

		if 'tips_pack' in self.keys():
			pass
		else:
			self['tips_pack'] = 'English'
		if 'dark_mode' in self.keys():
			theme.set_color_mode('dark' if self['dark_mode'] else 'light')

		if not ('tips_color_begin' in self.keys() and 'tips_color_end' in self.keys()):
			self['tips_color_begin'] = '#FFA500'
			self['tips_color_end'] = '#FF0000'

		if not 'tips_change_time' in self.keys():
			self['tips_change_time'] = 500

	def save(self):
		self['dark_mode'] = theme.get_color_mode() == 'dark'
		self.write('settings.WE')

# 设置字体
if toolbox.load_font("./LXGWWenKai-Regular.ttf"):
    configs.Font.family = "LXGW WenKai"
root = App_main(title = f'WordEdit Alpha {WordEditVersion[0]}.{WordEditVersion[1]}',size=[540, 607])
root.mainloop()

# 保存设置
_setting.save()

# 删除动画
for a in animations:
	a.stop()