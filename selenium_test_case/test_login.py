#coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart   
from email.mime.image import MIMEImage
import smtplib
import unittest ,HTMLTestRunner,os,time,sys

reload(sys)
sys.setdefaultencoding('utf8')


#读取测试用例文件
listaa='E:\\selenium_test_case\\login'
def creatsuit():
    testunit=unittest.TestSuite()
    discover=unittest.defaultTestLoader.discover(listaa,
                      pattern ='*_sta.py', #读取符合规则的用例
                      top_level_dir=None)

    for test_suite in discover:
        for  test_case in test_suite:
            testunit.addTests(test_case)
            #print testunit
    return testunit



#生成测试报告
now = time.strftime('%Y-%m-%d-%H_%M_%S',time.localtime(time.time()))
filename = 'E:\\selenium_test_case\\report\\'+now+'login_result.html'
fp = file(filename,'wb') 



runner =HTMLTestRunner.HTMLTestRunner(
     stream=fp,
     title=u'快播社区登录测试报告',
     description=u'运行浏览器：Firefox' )


if __name__ == '__main__':
    runner.run(creatsuit())
    fp.close()

