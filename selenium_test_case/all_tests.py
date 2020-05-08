#coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart   
from email.mime.image import MIMEImage
import smtplib
import unittest ,HTMLTestRunner,os,time,sys
import  xml.dom.minidom
reload(sys)
sys.setdefaultencoding('utf8')

#引入xml文件
dom = xml.dom.minidom.parse('E:\\selenium_test_case\\data\\info.xml')

#浏览器
bb=dom.getElementsByTagName('browser')
b=bb[0]
browser=b.firstChild.data


#读取测试用例文件
listaa='E:\\selenium_test_case\\webcloud'
def creatsuitel():
    testunit=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(listaa,
                      pattern ='*_sta.py',
                      top_level_dir=None)
    abc_.py
    #discover方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for  test_case in test_suite:
            testunit.addTests(test_case)
            print testunit
    return testunit
'''
def creatsuit():
    testunit=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(listaa,
                      pattern ='*_sta.py', #读取符合规则的用例
                      top_level_dir=None)

    for test_suite in discover:
        print test_suite
        for  test_case in test_suite:
            testunit.addTests(test_case)
            #print testunit
    return testunit
'''
alltestcase=creatsuitel()

#生成测试报告
now = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
filename = 'E:\\selenium_test_case\\report\\'+now+'result.html'
fp = file(filename,'wb') 

#读取浏览器类型
#br =open("E:\\selenium_test_case\\data\\browser.txt", "r")
#browser = br.read()
#print br

runner =HTMLTestRunner.HTMLTestRunner(
     stream=fp,
     title=u'快播私有云测试报告',
     description=u'运行浏览器：'+ browser)


if __name__ == '__main__':
    runner.run(alltestcase)
    fp.close()

