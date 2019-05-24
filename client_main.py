from threading import Thread
from tkinter import *
from socket import *
import time


# 对 terminal 的指令进行分析操作
def deal_cmd(cmd):
    if cmd == None:
        return
    if cmd == "/help":
        print("/CORNER-LIST      --List foregin corner\n"
              "/USER-LIST        --List all users\n"
              "/join []     --join corner []\n"
              "/@[userid]  []       --send private message [] to [userid] here\n"
              "/msg []      --concer public-message []\n"
              "/LEAVE          --leave corner\n"
              "/Register [name]  [key]    --Register new account\n")
    else:
        sendData(cmd)


# 监听 terminal 的命令指令
def Termi_cmd():
    Login2()
    global cmd
    while True:
        cmd = input(">>")
        deal_cmd(cmd)


def private_msg():
    send = "/@"+GUI.PRIVATE_MSG()+" "+ GUI.GET_MSG()
    sendData(send)
    return


def msg():
    send = "/msg "+GUI.GET_MSG()
    sendData(send)
    return


def JOIN_CORNER():
    send = "/join "+GUI.CORNER_SELECT()
    sendData(send)
    return


def CORNER():
    sendData("/CORNER-LIST")
    return


def LISTUSER():
    sendData("/USER-LIST")
    return


def LEAVE():
    sendData("/LEAVE")
    return


# 注册界面
def register():
    global udpSocket
    global UserName
    global Password
    global  destIp
    global LoginOK
    global GUI
    destIp = str(GUI.GET_SERVER_IP().strip())
    UserName = str(GUI.GET_ID().strip())
    Password = str(GUI.GET_PASSWORD().strip())
    # print(destIp)
    # print(UserName)
    # print(Password)
    if len(destIp) < 7 or len(UserName) < 4 or len(Password) < 2:
        return GUI.PUT_DATA("  INPUT ERROR!")
    sendInfo = "/Register "+UserName+" "+Password
    udpSocket.sendto(sendInfo.encode("gb2312"), (destIp, ServerPort))
    return



# GUI 界面登陆函数
def Login():
    global udpSocket
    global UserName
    global Password
    global  destIp
    global LoginOK
    global GUI
    destIp = str(GUI.GET_SERVER_IP().strip())
    UserName = str(GUI.GET_ID().strip())
    Password = str(GUI.GET_PASSWORD().strip())
    sendInfo = "Login "+UserName+" "+Password
    # print(destIp+sendInfo+str(ServerPort))
    udpSocket.sendto(sendInfo.encode("gb2312"), (destIp, ServerPort))
    time.sleep(1)
    if LoginOK:
        GUI.PUT_DATA("  Login success!!!\n")
        print("Login success\n")
    else:
        GUI.PUT_DATA("  Login failed!!!\n")
        print("Login failed\n")
    return


# terminal cmd 登陆函数
def Login2():
    global udpSocket
    global UserName
    global Password
    global  destIp
    global LoginOK
    destIp = input("服务器的ip:")
    UserName = input("Your id:")
    Password = input("Input your password:")
    sendInfo = "Login "+UserName+" "+Password
    # print(destIp+sendInfo+str(ServerPort))
    udpSocket.sendto(sendInfo.encode("gb2312"), (destIp, ServerPort))
    time.sleep(1)
    if LoginOK:
        print("Login success\n")
    else:
        print("Login failed\n")
    return


# 对接收的数据进行处理
def deal_rec_data(data):
    global LoginOK
    global GUI
    this_data = str(data).split()
    num = len(this_data)
    mes = ""
    if this_data[0] == 'LoginOK':   # 收到登陆成功的返回值，设置全局变量LoginOK为真
        LoginOK = True
        return
    if this_data[0][0] == '/':
        GUI.PUT_DATA(">>>" + this_data[0][1:] + "\n")
        print(">>>%s \n" % (this_data[0][1:]))
        for i in range(1, num - 1):
            mes = mes + this_data[i] + "   "
        GUI.PUT_DATA("     "+mes+"\n")
        print("%s\n" % (mes))
        return
    for i in range(0, num-1):            # 转换成标准的 String 类型
        mes = mes + this_data[i] + " "
    GUI.PUT_DATA(">>>" + mes+"\n")
    print(">>>%s \n" % ( mes ))
    return


# 接收数据的函数
def recvData():
    while True:
        recvInfo = udpSocket.recvfrom(1024)   # 次接受1k的数据
        # print(recvInfo[0].decode("gb2312"))
        if recvInfo[0] is not None:
            deal_rec_data(recvInfo[0].decode("gb2312"))


# 发送数据
def sendData(sendInfo):
    global udpSocket
    udpSocket.sendto(sendInfo.encode("gb2312"), (destIp, ServerPort))
    return


# GUI 界面的实现
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.row = 1.0

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("Foreign Language Client by:hailong")      # 窗口名
        self.init_window_name.geometry('1068x680+10+10')                 # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "pink"                            # 窗口背景色
        self.init_window_name.attributes("-alpha",5)                    # 虚化，值越小虚化程度越高
        self.init_window_name.resizable(0, 0)                           # 不可缩放，可以修改

        self.message_label = Label(self.init_window_name, text="MESSAGE", font=('Arial', 14), bg="pink", width=12, height=2)
        self.message_label.place(x=620, y=6)

        self.username_data_label = Label(self.init_window_name, text="USERNAME", font=('Arial',10), bg="pink")
        self.username_data_label.place(x=2, y=13)

        self.password_data_label = Label(self.init_window_name, text="PASSWORD", font=('Arial',10), bg="pink")
        self.password_data_label.place(x=2, y=49)

        self.server_ip_label = Label(self.init_window_name, text="SERVERIP", font=('Arial',10), bg="pink")
        self.server_ip_label.place(x=2, y=85)

        self.message_window_text = Text(self.init_window_name, font=('Arial', 14), width=67, height=20)
        self.message_window_text.place(x=310, y=55)  # 消息框

        self.username_text = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)
        self.username_text.place(x=83, y=12)

        self.password_text = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)
        self.password_text.place(x=83, y=47)

        self.server_ip_text = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)
        self.server_ip_text.place(x=83, y=82)

        self.login_button = Button(self.init_window_name, text="LOGIN", bg="lightblue", width=10,
                                   command=Login)  # 调用内部方法  加()为直接调用
        self.login_button.place(x=200, y=122)
        self.register_button = Button(self.init_window_name, text="REGISTER", bg="lightblue", width=10,
                                              command=register)  # 调用内部方法  加()为直接调用
        self.register_button.place(x=85, y=122)

        self.menu_bar_label = Label(self.init_window_name, text="MENU", font=('Arial', 15), bg='Pink', width=18, height=1)
        self.menu_bar_label.place(x=40, y=200)

        self.corner_list_button = Button(self.init_window_name, text="CORNERLIST", font=('Arial', 13), bg="lightblue", width=18, height=1,
                                   command=CORNER)  # 调用内部方法  加()为直接调用
        self.corner_list_button.place(x=60, y=250)
        self.user_list_button = Button(self.init_window_name, text="USERLIST", font=('Arial', 13), bg="lightblue", width=18, height=1,
                                   command=LISTUSER)  # 调用内部方法  加()为直接调用
        self.user_list_button.place(x=60, y=320)
        self.leave_button = Button(self.init_window_name, text="LOGOUT", font=('Arial', 13), bg="lightblue", width=18, height=1,
                                   command=LEAVE)  # 调用内部方法  加()为直接调用
        self.leave_button.place(x=60, y=390)
        self.select_button = Button(self.init_window_name, text="SELECT", font=('Arial', 13), bg="lightblue",
                                   width=18, height=1)  # 调用内部方法  加()为直接调用
        self.select_button.place(x=60, y=460)

        self.send_message_bar_text = Text(self.init_window_name, font=('Arial', 14), width=55, height=4)
        self.send_message_bar_text.place(x=440, y=525)

        self.join_corner_text = Text(self.init_window_name, font=('Arial', 17), width=18, height=1)
        self.join_corner_text.place(x=113, y=540)

        self.private_msg_id_text = Text(self.init_window_name, font=('Arial', 17), width=18, height=1)
        self.private_msg_id_text.place(x=113, y=590)
        # self.result_data_label = Label(self.init_window_name, text="JOINCORNER", font=('Arial', 12), bg="pink")
        # self.result_data_label.place(x=2, y=545)
        self.private_msg_id_bar_label = Label(self.init_window_name, text="PRIVATE-ID", font=('Arial', 12), bg="pink")
        self.private_msg_id_bar_label.place(x=5, y=595)

        self.send_button = Button(self.init_window_name, text="SNED", font=('Arial', 13),
                                   bg="lightblue", width=18, height=1,
                                   command=msg)  # 调用内部方法  加()为直接调用
        self.send_button.place(x=820, y=635)
        self.private_send_button = Button(self.init_window_name, text="PRIVATE_SEND", font=('Arial', 13), bg="lightblue",
                                   width=18, height=1,
                                   command=private_msg)  # 调用内部方法  加()为直接调用
        self.private_send_button.place(x=520, y=635)

        self.join_corner_button = Button(self.init_window_name, text="JOINCORNER", font=('Arial', 11), bg="pink",
                                         command=JOIN_CORNER)  # 调用内部方法  加()为直接调用
        self.join_corner_button.place(x=2, y=540)

    def GET_ID(self):
        return self.username_text.get(1.0, END)

    def GET_PASSWORD(self):
        return self.password_text.get(1.0, END)

    def GET_SERVER_IP(self):
        return self.server_ip_text.get(1.0, END)

    def PUT_DATA(self, data):
        self.message_window_text.insert(self.row, data)
        self.row = self.row % 20.0 + 1.0
        return

    def CORNER_SELECT(self):
        return self.join_corner_text.get(1.0, END)

    def PRIVATE_MSG(self):
        return self.private_msg_id_text.get(1.0, END)

    def GET_MSG(self):
        return self.send_message_bar_text.get(1.0, END)


def gui_start():
    global init_window
    global GUI
    GUI = MY_GUI(init_window) # 设置根窗口默认属性
    GUI.set_init_window()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


init_window = Tk()  # GUI 页面引用对象
GUI = None
UserName = ""
Password = ""
udpSocket = None
destIp = ""
myclient_Port = 6766
ServerPort = 8082
SendInfo = ""       # 发送的数据对象
cmd = ""            # cmd 的命令指令对象
LoginOK = False     # Login 成功的参数


def main():
    global ServerPort
    global udpSocket
    global myclient_Port
    global init_window
    global GUI
    # myclient_Port = int(input("Input my client port:"))
    udpSocket = socket(AF_INET, SOCK_DGRAM)    # UDP的传输的实例
    udpSocket.bind(("", myclient_Port))        # 端口的绑定
    GUI = MY_GUI(init_window)  # 设置根窗口默认属性
    GUI.set_init_window()      # 各个功能部件的实现
    tr = Thread(target=recvData)  # 线程1：只是监听端口，接收数据
    ts = Thread(target=Termi_cmd)  # 线程2：人机交互，处理本地指令
    tr.start()
    ts.start()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

    tr.join()
    ts.join()

    udpSocket.close()


if __name__ == '__main__':
    main()
