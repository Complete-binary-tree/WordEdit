import random
import os

# tips~
class tips(dict):
	def __init__(self):
		self.languages = []
		files = [f for f in os.listdir('./tips') if os.path.isfile(os.path.join('./tips', f))] # 获取文件夹下所有语言文件
		for file in files:
			if file[-4:] == '.txt':
				self.languages.append(file[:-4])
				print(f'tips:find new language {file[:-4]}')
				self[file[:-4]] = [line if line[-1] != '\n' else line[:-1] for line in open('./tips/'+file, 'r', encoding = 'UTF-8')]

	def random_tips(self,language = 'Chinese'):
		return self[language][random.randint(0,len(self[language])-1)]
	
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
						elif val[-1] == 'f':
							val = float(val[:-1])
						else:
							val = int(val)

						self[key] = val
						#print(key,val)

					except ValueError:
						print(f'[ERROR]WEreader:The format of {filename} is incorrect.')
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
			'refresh' : 'Refresh',
			'settings' : 'Settings',
			'start' : 'Start',
			'none' : 'No Text',
			'test' : 'This is an English text.'
		}

	def get(self, _key = 'none', language = 'English'):
		if _key in self[language].keys():
			return self[language][_key]
		return self['English'][_key]

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
	print(testlang['Chinese'])
	print(testlang.get(language = 'Chinese'))
	print(testlang.get('test'))
	print(testlang.get('test', 'Chinese'))