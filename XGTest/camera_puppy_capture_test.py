import os
import  time

rootdir = "G:\\20200427"
# print(os.path.getmtime("G:\\20200427\\10.58.122.126_20200427171952447_1.jpg"))
capture_image_list = []
big__image_list = []
image_gtime_List = []
sum_lost_number = 0
sum_lost_time = 0
sum_capture_time = 0
interval_time_list = []
max_interval_time = 0
max_interval_file = [0,1]


#获取文件夹下的所有文件的创建时间并保存到data列表中
for parent,dirnames,filenames in os.walk(rootdir):
    # Case1: traversal the directories
    for filename in filenames:
        if 'YT' in filename:
            big__image_list.append(filename)
        else:
            capture_image_list.append(filename)
            image_gtime_List.append(os.path.getmtime((os.path.join(parent,filename))))
sum_capture_time = image_gtime_List[len(image_gtime_List)-1]-image_gtime_List[0]

#将data列表中的相邻时间进行相减，当大于2时进行计数
for i in range(len(image_gtime_List)):
    if i == len(image_gtime_List) -1 :
        break
    time = image_gtime_List[i + 1] - image_gtime_List[i]
    if time > 1:
        if time > max_interval_time:
            max_interval_time = time
            max_interval_file[0] = capture_image_list[i]
            max_interval_file[1] = capture_image_list[i+1]
        sum_lost_number+=1
        sum_lost_time = sum_lost_time + time - 1
        interval_time_list.append(time)

print('总计抓拍文件数量：',len(capture_image_list))
if len(capture_image_list) != len(big__image_list):
    print('抓拍图数量与大图数量存在不一致情况，其中抓拍图的数量为：%s------大图的数量为：%s'%(len(capture_image_list),len(big__image_list)))
else:
    print('抓拍图与大图数量一致')
print("总丢失的次数：",sum_lost_number)
print("总时丢失时长：",sum_lost_time)
print("总计抓拍时长：",sum_capture_time)
print("丢失时长百分百{:.5%}：".format(sum_lost_time/sum_capture_time))
interval_time_list=sorted(interval_time_list,reverse=True)
print("最大间隔时间Top10：",interval_time_list[0:10:1])
print("最大间隔时间的相邻文件名1：{0},其创建时间是：{1},".format(max_interval_file[0],os.path.getmtime((os.path.join(parent,max_interval_file[0])))))
print("最大间隔时间的相邻文件名2：{0},其创建时间是：{1},".format(max_interval_file[1],os.path.getmtime((os.path.join(parent,max_interval_file[1])))))
