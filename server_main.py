from threading import Thread
from socket import *
import threading
from tkinter import *


# 操作整个用户数据的类集合
class data(object):
    def __init__(self):
        self.user = {'hailong': '0000', 'liangliang': '1111', 'junjun': '2222'}   # 所有注册用户
        self.login_user = set(['hailong'])    # 所有登录用户
        self.login_user_detail = {'hailong': {'ip': '127.0.0.1', 'EnterCorner': 'English_show'}}   # 登陆用户的详细信息
        self.corner_list = set(['English_show'])  # 所有打开的外语角
        self.corner_list_detail = {'English_show': {'language': 'English', 'this_corner_user': set(['hailong'])}}  # 外语角的详细信息
        self.ip_to_name ={'127.0.0.1': 'hailong'}  # 记录用户ip以及用户名，为了更好地服务，只需一台设备同时登录一个账号
        filename = 'user_data.txt'   # 储存用户信息的文件，当每次开启服务器时，读取以前的用户信息
        with open(filename, 'r') as f:
            for line in f.readlines():  # 依次读取每行
                line = line.strip()  # 去掉每行头尾空白
                mss = line.split()
                self.user.setdefault(mss[0], mss[1])
        if f:
            f.close()

    def __del__(self):   # 当关闭服务器时，储存用户信息
        filename = 'user_data.txt'
        with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            for (id, key) in self.user.items():
                f.write(id+" "+key+"\n")
        if f:
            f.close()

    def dele_user_in_corner(self, temp_corner, kick_id):
        this_corner_detail = self.corner_list_detail.get(temp_corner)
        this_users = this_corner_detail.get('this_corner_user')
        this_users.pop(kick_id)
        self.corner_list_detail.setdefault(temp_corner,this_corner_detail.setdefault('this_corner_user',this_users))
        return

    def name_to_corner(self,name):
        return self.login_user_detail.get(name).get('EnterCorner')

    def ip_to_ip_list(self, ip):
        print(ip)
        print("ip=%s" % (ip))
        return self.ip_list(self.name_to_corner(self.ip_to_name2(ip)))

    def ip_to_name2(self, ip):
        print(self.ip_to_name)
        return self.ip_to_name.get(ip)

    def name_to_ip(self, name):
        if name not in self.login_user:
            return
        return self.login_user_detail.get(name).get('ip')

    def ip_list(self, corner_name):
        if corner_name not in self.corner_list:
            return
        this_user_list = self.corner_list_detail.get(corner_name).get('this_corner_user')
        ip_list = set([])
        for name in this_user_list:
            ip_list.add(self.login_user_detail.get(name).get('ip'))
        return ip_list

    def use_leave(self, ip):
        print(ip)
        UserName = self.ip_to_name.get(ip[0])
        leave_corner = self.login_user_detail.get(UserName).get('EnterCorner')
        self.login_user_detail.setdefault(UserName,{'ip':ip[0], 'EnterCorner':''})
        this_user_list = self.corner_list_detail.get(leave_corner).get('this_corner_user')
        this_user_list.remove(UserName)
        self.corner_list_detail.setdefault(leave_corner,{'language':self.corner_list_detail.get(leave_corner).get('language'),'this_corner_user':this_user_list})
        return  self.ip_list(leave_corner)

    def add_corner(self, data):
        add_corner = data.split()
        if add_corner is None or len(add_corner) < 3:
            return
        self.corner_list.add(add_corner[1])
        self.corner_list_detail[add_corner[1]] = {'language': add_corner[2], 'this_corner_user': set(['hailong'])}
        return

    def list_corner(self):
        print(self.corner_list)
        return

    def c_list_corner(self, ip):
        send_data = "/corner "
        for name in self.corner_list:
            send_data = send_data + name +" "
        return send_data+ip[0]

    def c_list_user(self, ip):
        send_data = "/listuser "
        for name in self.login_user:
            send_data = send_data + name + ' '
        return send_data+ip[0]

    def list_all_user(self):
        print(self.login_user)
        return

    def c_join_corner(self, cornername, ip):
        if cornername in self.corner_list:
            UserName = self.ip_to_name.get(ip[0])
            this_user = self.corner_list_detail[cornername]['this_corner_user']
            this_user.add(UserName)
            self.corner_list_detail.setdefault(cornername,self.corner_list_detail[cornername].setdefault('this_corner_user',this_user))
            self.login_user_detail.setdefault(UserName,{'ip':ip[0],'EnterCorner':cornername})
            return UserName
        return None

    def enter_corner(self, data):
        if data in self.corner_list:
            print(self.corner_list_detail[data])
            return
        else:
            print("No this conner!!!\n")
            return

    def delect_user(self,id):
        if id not in self.login_user:
            return
        self.login_user.remove(id)
        temp_corner = self.login_user_detail.get(id).get("EnterCorner")
        self.login_user_detail.pop(id)
        return temp_corner

    def close_corner(self,concer_name):
        self.corner_list.remove(concer_name)
        self.corner_list_detail.pop(concer_name)
        return

    def if_in_user(self,id,key,ip):
        if id not in self.user:
            return None
        # print(self.user.get('hailong'))
        print(id)
        print(key)
        print(self.user.get(id,None))
        if self.user.get(str(id),None) == key:
            self.login_user.add(id)
            self.login_user_detail.setdefault(id,{'ip':ip[0],'EnterCorner':''})
            self.ip_to_name.setdefault(ip[0],id)
            return "LoginOK "+ip[0]
        else:
            return None

    def add_in_user(self, id, key, ip):
        if id in self.user:
            return "REGISTER FAILED "+ip[0]
        else:
            self.user.setdefault(id, key)
            return "REGISTER SUCCESSED " + ip[0]


# 收到来自网络的信息，分析操作收到的信息
def analyse_data(recv_data):
    global Data
    recv = recv_data[0].decode("gb2312").split()
    # print("Rece{0}=%s" % (recv[0]))
    if recv[0] == 'Login' and recv[1] != None and recv[2] != None:
        print("Login")
        sendData(Data.if_in_user(recv[1],recv[2],recv_data[1]))
        return
    if recv[0] == '/Register' and recv[1] != None and recv[2] != None:
        print("Register")
        sendData(Data.add_in_user(recv[1],recv[2],recv_data[1]))
        return
    if recv[0] == '/CORNER-LIST':
        sendData(Data.c_list_corner(recv_data[1]))
        return
    if recv[0] == '/USER-LIST':
        sendData(Data.c_list_user(recv_data[1]))
        return
    if recv[0] == '/join' and recv[1] != None:
        UserName = Data.c_join_corner(recv[1], recv_data[1])
        if UserName != None:
            send_Data(UserName+" joined " + str(recv[1]), Data.ip_list(recv[1]))
        else:
            sendData("Joined failed "+recv_data[1][0])
        return
    if recv[0] == '/LEAVE':
        send_Data(Data.ip_to_name2(recv_data[1][0])+" leaved",Data.use_leave(recv_data[1]))
        return
    if recv[0] == '/msg':
        send_Data(recv_data[0].decode("gb2312"), Data.ip_to_ip_list(recv_data[1][0]))
        return
    if recv[0][0:2] == '/@':
        sendData(Data.ip_to_name2(recv_data[1][0])+": "+str(" ".join(recv[1:]))+" "+Data.name_to_ip(recv[0][2:]))
        return
    return


# 分析cmd输入的信息
def deal_with_cmd(cmd):
    global Data
    s_cmd = cmd.split()
    if s_cmd[0][0] != '/':
        print("cmd error")
        return
    if s_cmd[0] == '/opencorner':
        if s_cmd[1] != None and s_cmd[2] != None:
            Data.add_corner(cmd)
            return
    else:
        if s_cmd[0] == '/corners':
            Data.list_corner()
            return
    if s_cmd[0] == '/listuser':
        Data.list_all_user()
        return
    if s_cmd[0] == '/enter':
        if s_cmd[1] != None:
            Data.enter_corner(s_cmd[1])
        return
    if s_cmd[0] == '/kickout':
        Data.delect_user(s_cmd[1])
        return
    if s_cmd[0] == '/closecorner' and s_cmd[1] != None:
        Data.close_corner(s_cmd[1])
        return
    if s_cmd[0] == '/leave':
        return
    return


# 分析输入的cmd指令
def deal_cmd(cmd):
    global Data
    if cmd == None:
        return
    # temp = Data.ip_to_ip_list('127.0.0.1')
    # send_Data("my naem",temp)
    # print(temp)
    if cmd == "/help":
        print("/opencorner [name] [lauanage]        --open foregin corner\n"
              "/corners     --list all corner\n"
              "/enter [CornerName]      --enter cornerName\n"
              "/listuser        --List all users\n"
              "/kickout [id]        --kickout userid\n"
              "/closecorner [CornerName]        --closecorner cornername\n"
              "/leave       --leave corner\n")
    else:
        deal_with_cmd(cmd)
    return


# 等待输入cmd的指令
def Termi_cmd():
    global udpSocket
    global cmd
    # ip = '127.0.0.1'
    # udpSocket.sendto(mmm.encode(), (ip, 6789))
    while True:
        cmd = input(">>")
        deal_cmd(cmd)


# 接受数据
def recvData():
    while True:
        recvInfo = udpSocket.recvfrom(1024)   # 一次接受最大1k的数据
        analyse_data(recvInfo)


# 组装发送信息的格式
def send_Data(sendInfo,ip_list):
    # print(str(ip_list))
    sendmes = sendInfo.split()
    if len(ip_list) == 0:
        ip_list.add('127.0.0.1')
        # print(1)
        # print(ip_list)
    for ip in ip_list:
        # print(str(sendInfo))
        if sendmes[0] == '/msg':
            sendmes[0] = Data.ip_to_name2(ip)+':'
        sendData(' '.join(sendmes)+' '+ip)
    return

# 具体的发送信息
def sendData(sendInfo):
    ClientPort = 6766
    if sendInfo == None:
        return
    send_data = sendInfo.split()
    count = len(send_data)
    # print("send[0]=%s" % (send_data[0:count-1]))
    string = ""
    for i in range(0, count):
        string = string + send_data[i] + " "
    udpSocket.sendto(string.encode("gb2312"), (send_data[-1], ClientPort))


# 私信的处理函数
def private_msg():
    global GUI
    global Data
    thickname = GUI.PRIVATE_ID().strip()
    ip = Data.name_to_ip(thickname)
    if ip == None:
        return
    sendData("MANAGER:"+GUI.GET_MSG().strip()+" "+ip)
    return


# 发送管理员信息
def msg():
    global Data
    global GUI
    global ENTER_CORNER
    if ENTER_CORNER != None:
        send = "!!!MANANGER: "+GUI.GET_MSG().strip()
        if ENTER_CORNER not in Data.corner_list:
            return
        send_Data(send, Data.ip_list(ENTER_CORNER))
        return
    return

# 显示打开的外语角
def CORNER():
    global GUI
    global Data
    GUI.PUT_DATA(">>OPEN CORNER\n")
    return GUI.PUT_DATA("        "+("  ".join(Data.corner_list))+"\n")


# 显示在线的用户
def LISTUSER():
    global Data
    global GUI
    GUI.PUT_DATA(">>LOGIN USER\n")
    return GUI.PUT_DATA("         "+("   ".join(Data.login_user))+"\n")


def LEAVE():
    global ENTER_CORNER
    ENTER_CORNER = None
    return


# 关闭一个外语角并通知，里面的所有用户
def CLOSECOR():
    global GUI
    close_corner = GUI.PRIVATE_MSG().strip()
    if close_corner in Data.corner_list:
        send_Data(close_corner+ " is closed by manager ", Data.ip_list(close_corner))
        Data.close_corner(close_corner)
    return

# 踢出某个用户，并通知其他人
def KICKOUT():
    global Data
    global ENTER_CORNER
    global GUI
    kick_id = GUI.CORNER_SELECT().strip()
    if ENTER_CORNER != None:
        temp_corner = Data.delect_user(kick_id)
        Data.dele_user_in_corner(temp_corner,kick_id)
        send_Data(kick_id + " leaved ", Data.ip_list(temp_corner))
        return
    else:
        return

# 新开一个外语角
def open_corner():
    global GUI
    corner_name = GUI.GET_ID().strip()
    corner_language = GUI.GET_PASSWORD().strip()
    s_cmd = "/opencorner "+corner_name + " "+corner_language
    Data.add_corner(s_cmd)
    return

def ENTER():
    global GUI
    global ENTER_CORNER
    ENTER_CORNER = GUI.GET_SERVER_IP().strip()
    return


# 主界面GUI
class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.row = 1.0

    # 设置窗口
    def set_init_window(self):
        self.init_window_name.title("Foreign Language Server by:hailong")  # 窗口名
        self.init_window_name.geometry('1068x680+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "pink"  # 窗口背景色
        self.init_window_name.attributes("-alpha", 5)  # 虚化，值越小虚化程度越高
        self.init_window_name.resizable(0, 0)
        self.message_label = Label(self.init_window_name, text="MESSAGE", font=('Arial', 14), bg="pink", width=12,
                                     height=2)
        self.message_label.place(x=620, y=6)

        self.input_corner_label = Label(self.init_window_name, text="COR-NAME", font=('Arial', 10), bg="pink")
        self.input_corner_label.place(x=2, y=13)
        self.input_language_label = Label(self.init_window_name, text="CORRLAUG", font=('Arial', 10), bg="pink")
        self.input_language_label.place(x=2, y=49)
        # self.result_data_label = Label(self.init_window_name, text="SERVERIP", font=('Arial', 10), bg="pink")
        # self.result_data_label.place(x=2, y=85)

        self.message_text = Text(self.init_window_name, font=('Arial', 14), width=67, height=20)  # 处理结果展示
        self.message_text.place(x=310, y=55)  # 消息框
        self.add_corner_text = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)  # 处理结果展示
        self.add_corner_text.place(x=83, y=12)  #
        self.corner_language_text = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)  # 处理结果展示
        self.corner_language_text.place(x=83, y=47)
        self.result_data_Text4 = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)  # 处理结果展示
        self.result_data_Text4.place(x=96, y=482)

        self.enter_corner_button = Button(self.init_window_name, text="ENTER", bg="lightblue", width=12,
                                          command=ENTER)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=2, y=480)
        self.register_button = Button(self.init_window_name, text="ADD-COR", bg="lightblue", width=12,
                                      command=open_corner)  # 调用内部方法  加()为直接调用
        self.register_button.place(x=120, y=90)

        self.result_label = Label(self.init_window_name, text="MENU", font=('Arial', 15), bg='Pink', width=18,
                                       height=1)
        self.result_label.place(x=40, y=150)

        self.enter_corner_button = Button(self.init_window_name, text="CORNERLIST", font=('Arial', 13),
                                          bg="lightblue", width=18, height=1,
                                          command=CORNER)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=60, y=200)
        self.enter_corner_button = Button(self.init_window_name, text="USERLIST", font=('Arial', 13),
                                          bg="lightblue", width=18, height=1,
                                          command=LISTUSER)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=60, y=270)
        self.enter_corner_button = Button(self.init_window_name, text="LEAVE", font=('Arial', 13), bg="lightblue",
                                          width=18, height=1,
                                          command=LEAVE)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=60, y=340)
        self.enter_corner_button = Button(self.init_window_name, text="SELECT", font=('Arial', 13), bg="lightblue",
                                          width=18, height=1)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=60, y=410)

        self.result_data_Text5 = Text(self.init_window_name, font=('Arial', 14), width=55, height=4)  # 处理结果展示
        self.result_data_Text5.place(x=440, y=525)

        self.result_data_Text6 = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)  # 处理结果展示
        self.result_data_Text6.place(x=96, y=540)
        self.result_data_Text7 = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)  # 处理结果展示
        self.result_data_Text7.place(x=96, y=590)
        # self.result_data_label = Label(self.init_window_name, text="JOINCORNER", font=('Arial', 12), bg="pink")
        # self.result_data_label.place(x=2, y=545)
        self.close_corner_button= Button(self.init_window_name, text="CLOSECOR", bg="lightblue",width = 12,
                                       command=CLOSECOR)
        self.close_corner_button.place(x=2, y=590)

        self.enter_corner_button = Button(self.init_window_name, text="SNED", font=('Arial', 13),
                                          bg="lightblue", width=18, height=1,
                                          command=msg)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=820, y=635)
        self.enter_corner_button = Button(self.init_window_name, text="PRIVATE_SEND", font=('Arial', 13),
                                          bg="lightblue",
                                          width=18, height=1,
                                          command=private_msg)  # 调用内部方法  加()为直接调用
        self.enter_corner_button.place(x=520, y=635)

        self.str_trans_button = Button(self.init_window_name, text="KICKOUT", bg="lightblue",width = 12,
                                       command=KICKOUT)  # 调用内部方法  加()为直接调用
        self.str_trans_button.place(x=2, y=540)

        self.result_data_Text8 = Text(self.init_window_name, font=('Arial', 14), width=18, height=1)  # 处理结果展示
        self.result_data_Text8.place(x=96, y=638)
        self.private_id = Label(self.init_window_name, text="PRIV-ID",font=('Arial', 14),  bg="lightblue", width=8)  # 调用内部方法  加()为直接调用
        self.private_id.place(x=2, y=638)

    def GET_ID(self):
        return self.add_corner_text.get(1.0, END)

    def GET_PASSWORD(self):
        return self.corner_language_text.get(1.0, END)

    def GET_SERVER_IP(self):
        return self.result_data_Text4.get(1.0, END)

    def PUT_DATA(self, data):
        self.message_text.insert(self.row, data)
        self.row = self.row % 20.0 + 1.0
        return

    def CORNER_SELECT(self):
        return self.result_data_Text6.get(1.0, END)

    def PRIVATE_MSG(self):
        return self.result_data_Text7.get(1.0, END)

    def PRIVATE_ID(self):
        return self.result_data_Text8.get(1.0,END)

    def GET_MSG(self):
        return self.result_data_Text5.get(1.0, END)



udpSocket = socket(AF_INET, SOCK_DGRAM)
destIp = ""
myserver_Port = 8082
cmd = ""
Data = data()
sendInfo = ""
threadLock = threading.Lock()
init_window = Tk()
GUI = None
ENTER_CORNER = None


def main():

    global udpSocket
    global destIp
    global myserver_Port
    global init_window
    global GUI
    myserver_Port = 8082

    udpSocket = socket(AF_INET, SOCK_DGRAM)
    udpSocket.bind(("", myserver_Port))

    GUI = MY_GUI(init_window)  # 设置根窗口默认属性
    GUI.set_init_window()

    tr = Thread(target=recvData)
    ts = Thread(target=Termi_cmd)
    tr.start()
    ts.start()
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    tr.join()
    ts.join()

    udpSocket.close()


if __name__ == '__main__':
    main()