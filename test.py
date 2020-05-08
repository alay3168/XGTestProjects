import telnetlib
import pyexpat

Host = '10.58.122.205' # Telnet服务器IP
username = b'root\n'  # 登录用户名
password = b'HZ*SF#ai1xS!\n'  # 登录密码
# finish = 'LEVEL COMMAND <___>'      # 命令提示符
finish = b'~ #'  # 命令提示符

memFreeCommand = b'cat /proc/meminfo;exit\n'
BoxmainPidCommand = b'ps|grep -v grep|grep /usr/local/app/bin/BoxMain;exit\n'

tn = telnetlib.Telnet(Host, port=23, timeout=60)
# 输入登录用户名
tn.read_until(b'login:')
tn.write(username)

# 输入登录密码
tn.read_until(b'Password:')
tn.write(password)

# 登录完毕后执行命令
tn.read_until(finish)
tn.write(memFreeCommand)
# for command in cmds:
#     result = tn.write('%s \\r\\n' % command);
# 执行结果保存至文件
Outres = tn.expect()

print(Outres)
Outres = tn.read_all()