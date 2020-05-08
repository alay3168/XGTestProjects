import socket
import sys
import cv2


def videoPlayer(videoDir):
    cap = cv2.VideoCapture(videoDir)
    print("开始播放视频")
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
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
    videoDir = '3m258.mp4'
    serverIp = '10.58.122.65'  # 服务端IP
    serverPort = 6666  # 服务端端口

    try:
        # 创建于服务端的socket连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((serverIp, serverPort))
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    num = 1
    while True:
        print('开始播放%d次视频'%num)
        videoPlayer(videoDir)
        print('视频播放完，通知服务端进行抓拍结果分析')
        data = "over"  # 输入要传输的数据
        s.send(data.encode())  # 将要传输的数据编码发送，如果是字符数据就必须要编码发送

        buf = s.recv(1024)
        if buf.decode() =='over':
            print('接收到服务端抓拍结果分析完成，继续播放视频进行下一轮人脸抓拍测试')
            num += 1
            continue
        if buf.decode() =='gameOver':
            print("运行结束，无需再继续播放视频")
            break

