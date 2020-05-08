import time
import os

localtime = time.asctime( time.localtime(time.time()) )
print(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))

print(os.getcwd())