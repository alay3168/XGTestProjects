import socket
import sys
import time

def socket_service_data():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))  # 在同一台主机的ip下使用测试ip进行通信
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("Wait for Connection..................")
    while True:
        sock, addr = s.accept()
        buf = sock.recv(1024)  #接收数据
        buf = buf.decode()  #解码
        print("The data from " + str(addr[0]) + " is " + str(buf))
        print("Successfully")

if __name__ == "__main__":
    num = 0
    while num <2:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', 6666))  # 在同一台主机的ip下使用测试ip进行通信
            s.listen(10)
        except socket.error as msg:
            print(msg)
            sys.exit(1)
        print("Wait for Connection..................")
        while True:
            sock, addr = s.accept()
            print("已经连接，等待视频播放完成")
            buf = sock.recv(1024)  # 接收数据
            buf = buf.decode()  # 解码
            if buf =="over":
                print("The data from " + str(addr[0]) + " is " + str(buf))
                print("Successfully")
            data = "over"  # 输入要传输的数据
            time.sleep(5)
            sock.send(data.encode())  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送
            print('发送数据成功')