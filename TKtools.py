import tkinter as tk

# EntryEx
# 可以自定义不输入的时候框内自动保留内容
# 其余与 Entry 一样
# powered by chatgpt-4o
class EntryEx(tk.Entry):
    def __init__(self, master=None, command=None, placeholder="Enter text...", placeholder_color="gray", text_color="black", **kwargs):
        # 初始化父类 tk.Entry
        super().__init__(master, **kwargs)
        
        # 初始化属性
        self.command = command  # 输入或删除时调用的回调函数
        self.placeholder = placeholder
        self.placeholder_color = placeholder_color
        self.text_color = text_color

        # 初始化内部状态
        self._is_placeholder = True  # 是否处于占位符状态

        # 绑定事件
        self.bind("<FocusIn>", self._focus_in)
        self.bind("<FocusOut>", self._focus_out)
        self.bind("<KeyPress>", self._on_key_press)  # 处理按键事件

        # 设置初始占位符
        self._add_placeholder()

    def _focus_in(self, event=None):
        """处理 Entry 获取焦点的事件"""
        if self._is_placeholder:
            self.delete(0, tk.END)  # 删除占位符
            self["fg"] = self.text_color  # 改变字体颜色

    def _focus_out(self, event=None):
        """处理 Entry 失去焦点的事件"""
        if not self.get():  # 如果内容为空
            self._add_placeholder()

    def _add_placeholder(self):
        """添加占位符"""
        self.delete(0, tk.END)
        self.insert(0, self.placeholder)
        self["fg"] = self.placeholder_color
        self._is_placeholder = True

    def _on_key_press(self, event=None):
        """处理用户按键事件"""
        if self._is_placeholder:
            # 删除占位符，同时避免覆盖用户当前输入的按键字符
            self.delete(0, tk.END)
            self["fg"] = self.text_color
            self._is_placeholder = False

        # 如果有 command 回调函数，调用它
        if self.command:
            # 使用 `after` 延迟调用，确保输入字符被正确捕获
            self.after(1, self.command)

    def get(self):
        """重写 get 方法，返回用户真实输入内容"""
        if self._is_placeholder:
            return ""
        return super().get()

    def get_real_value(self):
        """获取真实用户输入内容"""
        return self.get()