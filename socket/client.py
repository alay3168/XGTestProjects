import socket
import sys
import cv2

def sock_client_data():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect(('192.168.20.1', 6666))  #服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
            s.connect(('127.0.0.1', 6666))  #服务器和客户端都在一个系统下时使用的ip和端口
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))
        data = input("input data:")   #输入要传输的数据
        s.send(data.encode())  #将要传输的数据编码发送，如果是字符数据就必须要编码发送
        s.close()

def videoPlayer():
    cap = cv2.VideoCapture('tongdao720p_proc.264')
    print("开始播放视频")
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret ==True:
            out_win = "output_style_full_screen"
            cv2.namedWindow(out_win, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(out_win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(out_win, frame)
            k = cv2.waitKey(20)
            # q键退出
            if (k & 0xff == ord('q')):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    print("视频播放结束")

if __name__ == "__main__":

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect(('192.168.20.1', 6666))  #服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
        s.connect(('127.0.0.1', 6666))  # 服务器和客户端都在一个系统下时使用的ip和端口
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    num = 0
    while num < 2:
        videoPlayer()
        data = "over"  # 输入要传输的数据
        s.send(data.encode())  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送
        buf = s.recv(1024)
        buf = buf.decode()
        print(buf)
        num +=1
