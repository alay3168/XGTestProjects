import os

num = 0
rootdir = "G:\\data_800\\res"
newdir = "G:\\data_800\\newres"
isExists = os.path.exists(newdir)
if not isExists:
    # 如果不存在则创建目录
    # 创建目录操作函数
    newdir = os.mkdir(newdir)

for parent, dirnames, filenames in os.walk(rootdir):
    # Case1: traversal the directories
    for filename in filenames:
        if os.path.getsize(os.path.join(parent, filename)) == 0:
            # print(os.path.join(parent,filename))
            num += 1
            continue
        else:
            file_object = open(os.path.join(parent, filename), 'rU')
            lineList = file_object.readline().split(" ")
            # lineList[5] = lineList[5].strip("\n")
            lineListBak = [0, " ", 1, " ", 2, " ", 3, " ", 4, " ", " "]
            # print(len(lineListBak))
            # print(lineList)
            lineListBak[0] = lineList[1]
            lineListBak[2] = lineList[2]
            lineListBak[4] = str(int(lineList[1]) + int(lineList[3]))
            lineListBak[6] = str(int(lineList[2]) + int(lineList[4]))
            lineListBak[8] = lineList[0]
            lineListBak[10] = lineList[5]
            newline = "".join(lineListBak)

            # print(lineListBak)
            newFile = open(os.path.join(newdir, filename), 'w')
            # print("newfile",newFile)
            # print(newFile)
            # print(newline)
            newFile.write(newline)
            newFile.close()
            file_object.close()
print(num)
