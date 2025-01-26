import random
import os
import maliang as ml

# tips~
class tips(dict):
	def __init__(self, pack):
		self.pack = pack
		
		self.load()
		
		if not (self.pack in self.packs):
			print(f'[Warning]TipsLoader:tippack "{self.pack}" is not exist.')
			self.pack = 'English(Inside)'

	def load(self):
		self.packs = ['English(Inside)']
		self['English(Inside)'] = ['Oh there is no tips!', 'Try to click "Refresh"!']

		files = [f for f in os.listdir('./tips') if os.path.isfile(os.path.join('./tips', f))] # 获取文件夹下所有语言文件
		for file in files:
			if file[-4:] == '.txt':
				self.packs.append(file[:-4])
				self[file[:-4]] = [line if line[-1] != '\n' else line[:-1] for line in open('./tips/'+file, 'r', encoding = 'UTF-8')]
		print(f'TipsLoader:Find {len(self.keys())} tipspacks.')

	def random_tips(self):
		if self.pack in self.packs:
			return self[self.pack][random.randint(0,len(self[self.pack])-1)]
		else:
			return ' '
	
# WE file（类 JS）
class WEfile(dict):
	def __init__(self, filename = None, cpydict = None):
		super().__init__()
		if cpydict:
			super().__init__(cpydict)
		if filename:
			self.read(filename)

	def read(self, filename : str):
		if filename[-3:] != '.WE':
			print(f'[ERROR]WEreder:The file extension of a WE file must be .WE,but found {filename}.')
			return 1
		
		try:
			with open(filename, 'r', encoding = 'UTF-8') as reader:
				for line in reader:
					try:
						key, val = line.split(':')
						key = key.strip(); val = val.strip()

						if val[0] == val[-1] and (val[0] == '"' or val[-1] == "'"):
							val = val[1:-1]
							i = 0
							while i < len(val):
								if val[i] == '\\':
									if val[i+1] == 'n':
										val = val[:i] + '\n' + val[i+2:]
									elif val[i+1] == '\\':
										val = val[:i] + '\\' + val[i+2:]
									else:
										print('[Warning]WEreader:Invalid character after \'\\\'.')
								i += 1

						elif val[-1] == 'f':
							val = float(val[:-1])
						else:
							val = int(val)

						self[key] = val
						#print(key,val)

					except ValueError:
						print(f'[ERROR]WEreader:The format of {filename} is incorrect.(ValueError)')
						return 2
					
					except IndexError:
						print(f'[ERROR]WEreader:The format of {filename} is incorrect.(IndexError)')
						return 2
					
		except FileNotFoundError:
			print(f'[ERROR]WEreader:Cannot found {filename}.')
			return -1
		
		except IOError:
			print(f'[ERROR]WEreader:File IO Error.(filename:{filename})')
			return -2
		
		print(f'WEreader:Successfully read from {filename}!')
		return 0
	
	def write(self, filename : str):
		if filename[-3:] != '.WE':
			print('[Warning]WEwriter:The file extension is not .WE(found {filename}).')

		try:
			with open(filename, 'w', encoding = 'UTF-8') as writer:
				for key, value in self.items():
					if type(value) == bool:
						value = int(value)

					if type(value) == int:
						value = str(value)
					elif type(value) == float:
						value = str(value) + 'f'
					elif type(value) == str:
						value = "'" + value + "'"
					else:
						print(f'[Error]WEwriter:Unexpected typename({str(type(value))}) while writing.(file:{filename})')
						return 1
					
					writer.write(key + ':' + value + '\n')
		
		except IOError:
			print(f'[ERROR]WEwriter:File IO Error.(filename:{filename})')
			return -2
		
		print(f'WEwriter:Successfully write to {filename}')
		return 0
	
	def getdict(self) -> dict:
		return dict(self)

# 基于 WE 的 language
class language(dict):
	def __init__(self):
		
		if len([file for file in os.listdir('./Language') if os.path.isfile(os.path.join('./Language', file))]) == 0:
			print('[Warning]Language:No Any Language File.')
		
		self.load_english()
		
		for file in os.listdir('./Language'):
			if os.path.isfile(os.path.join('./Language', file)):
				if file[-3:] == '.WE':
					self[file[:-3]] = WEfile('./Language/' + file).getdict()
		
		print(f'Language:Load {len(self.keys())} languages.')

	def load_english(self):
		self['English'] = {
			'tip_refresh' : 'Refresh tips',
			'settings' : 'Settings',
			'start' : 'Start',
			'none' : 'No Text',
			'test' : 'This is an English text.',
			'show' : 'Display',
			'dark_mode' : 'Dark mode',
			'exit' : 'Exit',
			'return' : 'Return',
			'language' : 'Language',
			'tips' : 'Tips',
			'language_change_tip' : 'More language?\nPut the language file in "./Language" \nfolder,then click "Refresh language list".',
			'refresh_l' : 'Refresh language list',
			'tips_pack' : 'Tip pack',
			'refresh_tp' : 'Refresh packs',
			'tips_change_color' : 'Flick color',
			'tips_change_time' : 'Flick time(ms)',
			'tips_pack_tip' : 'More tip packs?\nPut the tip pack file in "./tips" \nfolder,then click "Refresh packs".'
		}

	def get(self, _key = 'none', language = 'English'):
		if _key in self[language].keys():
			return self[language][_key]
		print(f'language:cannot find word "{_key}" in language "{language}".')
		if _key in self['English'].keys():
			return self['English'][_key]
		else:
			return _key

# deepseek贡献的BetterSpinbox，具有焦点离开时回调功能
class CustomSpinBox(ml.SpinBox):
	def __init__(self, root, pos, **kwrgs):
		if 'command_fc_out' in kwrgs.keys():
			print(kwrgs['command_fc_out'])
			self.command_fc_out = kwrgs['command_fc_out']
			del kwrgs['command_fc_out']
		super().__init__(root, pos, **kwrgs)
		self.clicked = False  # 记录是否点击了 SpinBox
		self.bind('<Button>', self.on_mouse_clicked)

	def on_mouse_clicked(self, x, y, button):
		"""处理鼠标点击事件"""
		if self.collide_point(x, y):  # 判断是否点击了 SpinBox
			self.clicked = True
		elif self.clicked and not self.collide_point(x, y):  # 判断是否离开了 SpinBox
			if self.command_fc_out:  # 如果提供了回调函数
				self.command_fc_out(self.get_value())  # 调用回调函数
			self.clicked = False

	#def on_mouse_released(self, x, y, button):
	#	"""处理鼠标释放事件"""
		

"""
# 玩 florr 玩的
class florrio(dict):
	def __init__(self,**kwargs):
		common().__init__(**kwargs)
		unusual().__init__(**kwargs)
		rare().__init__(**kwargs)
		epic().__init__(**kwargs)
		legendary().__init__(**kwargs)
		mythic().__init__(**kwargs)
		ultra().__init__(**kwargs)
		super().__init__(**kwargs)
		unique().__init__(**kwargs)
"""

# small test
if __name__ == '__main__':
	# ----tips-----
	t = tips()
	print(t.random_tips())			# get a random chinese tip
	print(t.random_tips('English'))	# get a random english tip

	# ----WEfile----
	testWE = WEfile(filename = 'test.WE')
	print(testWE)
	testWE = WEfile(cpydict = {'a':114514,'b':12.0,'c':'str'})
	testWE.write('test.WE')

	# ----language----
	testlang = language()
	print(testlang['English'])
	print(testlang['中文（简体）'])
	print(testlang.get(language = '中文（简体）'))
	print(testlang.get('test'))
	print(testlang.get('test', '中文（简体）'))