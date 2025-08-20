import json
import time
import tkinter



class Base:
    def __init__(self):

        self.filename = "date111"
        self.learning_multiplier_coefficient = 0.75

        self.learning_time = False

        self.last_timeA = 0
        self.last_timeB = 0

        #自适应字号
        self.window_w = 300
        self.window_h = 500
        self.font_size = min(self.window_w,self.window_h) // 20
        #创建根窗口
        self.window1 = tkinter.Tk()
        #设定窗口大小，不可变化
        self.window1.geometry(f"{self.window_w}x{self.window_h}")
        self.window1.resizable(False,False)
        #上面的是显示时间的窗口，
        self.up_frame1 = tkinter.LabelFrame(
            master=self.window1,
            bd=2,
            relief="sunken",
            text="时间账户"
        )
        self.up_frame1.pack(side="top",expand=True,fill="both")
        # 时间显示窗口上面是当前学习时长，
        self.up_frame1_1 = tkinter.Frame(
            master=self.up_frame1,
            bd=2,
            relief="sunken"
        )
        self.up_frame1_1.pack(side="top",expand=True,fill="both")
        #   这个是标签
        self.up_f1_1_label1 = tkinter.Label(
            master=self.up_frame1_1,
            text="工作时长余额",
            font=("Arial",self.font_size)
        )
        self.up_f1_1_label1.pack(side="left",expand=True,fill="both")
        #   这个是变量
        self.learning_account_balance = tkinter.DoubleVar()
        self.learning_account_balance.set(0.0)
        #   这个是显示变量的标签
        self.up_f1_1_label2 = tkinter.Label(
            master=self.up_frame1_1,
            textvariable=self.learning_account_balance,
            font=("Arial", self.font_size)
        )
        self.up_f1_1_label2.pack(side="right",expand=True,fill="both")
        #上面的下面是当前的休息时长
        self.up_frame1_2 = tkinter.Frame(
            master=self.up_frame1,
            bd=2,
            relief="sunken"
        )
        self.up_frame1_2.pack(side="top",expand=True,fill="both")
        #   标签
        self.up_f1_2_label1 = tkinter.Label(
            master=self.up_frame1_2,
            text="休息时长余额",
            font=("Arial", self.font_size)
        )
        self.up_f1_2_label1.pack(side="left",expand=True,fill="both")
        #   变量
        self.rest_account_balance = tkinter.DoubleVar()
        self.rest_account_balance.set(0.0)
        self.up_f1_2_label2 = tkinter.Label(
            master=self.up_frame1_2,
            textvariable=self.rest_account_balance,
            font=("Arial", self.font_size)
        )
        self.up_f1_2_label2.pack(side="right",expand=True,fill="both")
        #下面是控制台和状态管理器
        self.down_frame1 = tkinter.Frame(
            master=self.window1,
            bd=2,
            relief="sunken"
        )
        self.down_frame1.pack(side="bottom",expand=True,fill="both")
        #下面的上面是命令行
        self.down_f1_frame1 = tkinter.LabelFrame(
            master=self.down_frame1,
            bd=2,
            relief="sunken"
        )
        self.down_f1_frame1.pack(side="top",expand=True,fill="both")
        #   命令行的文本框
        self.down_command_line = tkinter.Text(
            master=self.down_f1_frame1,
            height= 10
        )
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.down_command_line.insert(tkinter.END,f"{current_time}:hello")
        self.down_command_line.config(state="disabled")
        self.down_command_line.pack(side="top",expand=True,fill="both")
        #下面的下面是功能按钮
        self.down_f1_frame2 = tkinter.Frame(
            master=self.down_frame1,
            bd=2,
            relief="sunken",
        )
        self.down_f1_frame2.pack(side="bottom",expand=True,fill="both")
        #按钮有这些个：开始（继续）积累学习时长，（转换为休息时长）开始积累休息时长，安全退出程序，从存档点加载数据
        self.button_switch_button = tkinter.Button(
            master=self.down_f1_frame2,
            text="switch",
            font=("Arial", self.font_size),
            command=self.start_accumulating_learning_time
            #command=lambda :print("self.button_switch_button = tkinter.Button(")
        )
        self.button_switch_button.pack(side="left",expand=True,fill="both")
        self.button_load_from_file = tkinter.Button(
            master=self.down_f1_frame2,
            text="load_from_file",
            font=("Arial", self.font_size ),
            command=self.load_from_json
            #command=lambda :print("self.button_load_from_file = tkinter.Button(")
        )
        self.button_load_from_file.pack(side="left",expand=True,fill="both")
        self.button_exit_safe = tkinter.Button(
            master=self.down_f1_frame2,
            text="exit_safe",
            font=("Arial", self.font_size),
            command=self.exit_safe
            #command=lambda :print("self.button_exit_safe = tkinter.Button(")
        )
        self.button_exit_safe.pack(side="left",expand=True,fill="both")

        #业务逻辑是：点击开始积累学习时长，学习时长按照时间增加，
        # 点击转换时长，过去积累的学习时长清零，然后按照系数折算为休息时长，这时状态进入休息状态，休息状态是倒计时
        #当倒计时为正时，开始学习会暂停休息时长的损耗，并从0开始累加学习时长
        #当倒计时为0时，这不会停止计时而是会计时出负值，此时再点击积累学习时长，就会把负值也折算成学习时长
        #当学习时长为负时，不清零，转换出休息时长为0
    def start_accumulating_learning_time(self,event=None):
        #如果没在学习
        if not self.learning_time:

            #开始进行学习计时
            self.learning_time = True
            #把背景颜色改一下
            self.up_f1_1_label1.config(background="red")
            self.up_f1_1_label2.config(background="red")
            self.up_f1_2_label1.config(background="gray")
            self.up_f1_2_label2.config(background="gray")
            #运行折算模块
            #   得到休息剩余时长
            delta_time = self.rest_account_balance.get()
            #   如果欠债了
            if delta_time < 0.0 :
                #把债给到学习时间
                count_time = delta_time / self.learning_multiplier_coefficient
                self.learning_account_balance.set(self.learning_account_balance.get() + count_time)
                #重置
                self.rest_account_balance.set(0.0)
            else:
                pass

            #开始学习计时器的运行
            self.set_text("开始工作")
            self.last_timeA = time.time()
            self.SALT_timer()

        else:
            #这时正在学习
            self.learning_time = False
            #背景颜色
            self.up_f1_2_label1.config(background="red")
            self.up_f1_2_label2.config(background="red")
            self.up_f1_1_label1.config(background="gray")
            self.up_f1_1_label2.config(background="gray")
            #运行折算模块
            delta_time2 = self.learning_account_balance.get()
            #   如果积累的学习时间是正的
            if delta_time2 > 0:
                self.learning_account_balance.set(0)
                #给到休息时间
                count_time2 = delta_time2 * self.learning_multiplier_coefficient
                self.rest_account_balance.set(self.rest_account_balance.get() + count_time2)

            #开始休息计时器的运行
            self.set_text("开始休息")
            self.last_timeB = time.time()
            self.antiSALT_timer()


    def SALT_timer(self):
        if self.learning_time:
            current_time = time.time()  # 获取当前时间戳（秒）
            getted_delta_time = current_time - self.last_timeA
            ps_time = round((self.learning_account_balance.get() + getted_delta_time), 2)
            self.learning_account_balance.set(ps_time)
            self.last_timeA = current_time
        self.window1.after(100,self.SALT_timer)

    def antiSALT_timer(self):
        if not self.learning_time:
            current_time = time.time()  # 获取当前时间戳（秒）
            getted_delta_time = current_time - self.last_timeB
            ps_time = round((self.rest_account_balance.get() - getted_delta_time), 2)
            self.rest_account_balance.set(ps_time)
            self.last_timeB = current_time
        self.window1.after(100, self.antiSALT_timer)

    def set_text(self,text):
        self.down_command_line.config(state="normal")
        current_time = time.strftime("%H:%M:%S", time.localtime())
        self.down_command_line.insert(tkinter.END,"\n")
        self.down_command_line.insert(tkinter.END, f"{current_time}:{text}")
        self.down_command_line.config(state="disabled")
        self.down_command_line.see(tkinter.END)


    def exit_safe(self,event=None):
        self.set_text("正在保存并退出")
        self.save_to_json()
        self.window1.destroy()

    def save_to_json(self,event = None):
        """将类数据保存到JSON文件"""
        data = {
            #'self.learning_time':self.learning_time,
            'self.learning_account_balance' : self.learning_account_balance.get(),
            'self.rest_account_balance':self.rest_account_balance.get()
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)
        self.set_text("账户数据已保存")

    def load_from_json(self,event=None):
        """从JSON文件加载数据到类实例"""
        self.set_text("从文件加载数据")
        with open(self.filename, 'r') as f:
            data = json.load(f)
        #self.learning_time = data['self.learning_time']
        learning_account_balance = data['self.learning_account_balance']
        rest_account_balance = data['self.rest_account_balance']
        self.learning_account_balance.set(learning_account_balance)
        self.rest_account_balance.set(rest_account_balance)

    def run(self):
        self.window1.mainloop()


if __name__ == "__main__":
    base = Base()
    base.run()
