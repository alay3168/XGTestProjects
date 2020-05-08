#coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart   
from email.mime.image import MIMEImage
import smtplib,time,os,HTMLTestRunner


#=======定义发送邮件========
def sentmail(file_new):
    #发信邮箱
    mail_from='fnngj@126.com'
    #收信邮箱
    mail_to='huzhiheng@qvod.com'
    #定义正文
    f = open(file_new, 'rb')
    mail_body = f.read()
    f.close()
    msg=MIMEText(mail_body,_subtype='html',_charset='utf-8')
    #定义标题
    msg['Subject']=u"私有云测试报告"
    #定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')
    smtp=smtplib.SMTP()
    #连接SMTP服务器，此处用的126的SMTP服务器
    smtp.connect('smtp.126.com')
    #用户名密码
    smtp.login('fnngj@126.com','a123456')
    smtp.sendmail(mail_from,mail_to,msg.as_string())
    smtp.quit()
    print 'email has send out !'

#file_new2="E:\\selenium_test_case\\report\\2014-03-25-06_00_00result.html"
#sentmail(file_new2)


#========查找最新测试报告，调用发邮件功能=====
def sendreport():
    result_dir = 'E:\\selenium_test_case\\report'
    lists=os.listdir(result_dir)
    lists.sort(key=lambda fn: os.path.getmtime(result_dir+"\\"+fn) if not os.path.isdir(result_dir+"\\"+fn) else 0) 
    #找到最新生成的文件
    file_new = os.path.join(result_dir,lists[-1])
    print file_new
    
    #调用发邮件模块
    sentmail(file_new)

#sendreport()


#读取测试用例文件
listaa='E:\\selenium_test_case\\webcloud'
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
filename = 'E:\\selenium_test_case\\report\\'+now+'result.html'
fp = file(filename,'wb') 

#读取浏览器类型
br =open("E:\\selenium_test_case\\data\\browser.txt", "r")
browser = br.read()
print br

runner =HTMLTestRunner.HTMLTestRunner(
     stream=fp,
     title=u'快播私有云测试报告',
     description=u'运行浏览器：'+ browser)

if __name__ == '__main__':
    runner.run(creatsuit())
    fp.close()
    sendreport()
