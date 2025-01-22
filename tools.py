import random
import os

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
	
# small test
if __name__ == '__main__':
	t = tips()
	print(t.random_tips())
	print(t.random_tips('English'))