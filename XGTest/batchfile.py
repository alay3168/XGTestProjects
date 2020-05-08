import os

import xlsxwriter


def all_path(dirname):
    filelistlog = dirname + "\\filelistlog.txt"  # 保存文件路径
    postfix = set(['pdf', 'doc', 'docx', 'epub', 'txt', 'xlsx', 'djvu', 'chm', 'ppt', 'pptx'])  # 设置要保存的文件格式
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if True:  # 保存全部文件名。若要保留指定文件格式的文件名则注释该句
                # if apath.split('.')[-1] in postfix:   # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句
                try:
                    with open(filelistlog, 'a+') as fo:
                        fo.writelines(apath)
                        fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


def all_pathxlsx(dirname):
    filelistlog = dirname + "\\filelistlog.xlsx"  # 保存文件路径
    postfix = set(['pdf', 'doc', 'docx', 'epub', 'txt', 'xlsx', 'djvu', 'chm', 'ppt', 'pptx'])  # 设置要保存的文件格式
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if True:  # 保存全部文件名。若要保留指定文件格式的文件名则注释该句
                # if apath.split('.')[-1] in postfix:   # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句
                try:
                    with open(filelistlog, 'a+') as fo:
                        fo.writelines(apath)
                        fo.write('\n')
                except:
                    pass  # 所以异常全部忽略即可


dirname = "C:\\Users\\admin\Desktop\\verify\g_out"

book = xlsxwriter.Workbook('pict.xlsx')
sheet = book.add_worksheet('demo')
apath_all = []
for maindir, subdir, file_name_list in os.walk(dirname):
    for filename in file_name_list:
        apath = os.path.join(maindir, filename)
        apath_all.append(apath)
# print(apath_all)
number = 1
for i in apath_all:
    # print('D'+str(number))
    sheet.insert_image('D' + str(number), i, {'x_scale': 1, 'y_scale': 1})
    number += 1
book.close()

# if __name__ == '__main__':
#     dirpath = "C:\\Users\\admin\Desktop\\verify\g"  # 指定根目录
#     all_path(dirpath)
