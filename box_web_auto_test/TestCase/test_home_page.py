import unittest
from selenium import webdriver
import time
import os
from WebPage.login_page import LoginPage
from WebPage.home_page import HomePage
from WebPage.video_manager_page import VideoManagerPage
from Common import common as cc
from ddt import ddt,file_data


case_yml = os.path.abspath(os.path.join(os.path.dirname(__file__), "../TestData"))
@ddt
class TestHomePage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.set_window_size(1920, 1080)
        cls.base_url = cc.baseUrl()
        cls.driver.get(cls.base_url)
        loginPage = LoginPage(cls.driver)
        cls.driver.implicitly_wait(30)
        loginPage.set_username('admin')
        loginPage.set_password('123456')
        time.sleep(1)
        loginPage.click_SignIn()
        time.sleep(2)

    @file_data(case_yml + "\\home_mainMenuButton.yaml")
    def test_0_mainMenuButton(self,**test_data):
        '''对登录首页各个按钮进行逐一点击，确认是否可用'''
        self.__dict__['_testMethodDoc'] = test_data.get('caseDescription')
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        time.sleep(1)
        videoManPage = VideoManagerPage(self.driver)
        text = videoManPage.get_videoAccessEml()
        self.assertEqual(test_data.get('expected_re1'),text,  msg=test_data.get('msg'))

        text = videoManPage.get_manualAddButton()
        self.assertEqual(test_data.get('expected_re2'),text,  msg=test_data.get('msg'))

        text = videoManPage.get_deviceTypeEml()
        self.assertEqual(test_data.get('expected_re3'),text,  msg=test_data.get('msg'))

    @file_data(case_yml + "\\home_previewButton.yaml")
    def test_1_previewButton(self, **test_data):
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        time.sleep(1)
        videoManPage = VideoManagerPage(self.driver)
        list = videoManPage.get_video_list()
        if len(list)>0:
            homepage.click_previewButton()
            text = homepage.get_monitorScreenEml()
            self.assertEqual(test_data.get('expected_re1'),text,  msg=test_data.get('msg'))

            text = homepage.get_cameraListEml()
            self.assertEqual(test_data.get('expected_re2'),text,  msg=test_data.get('msg'))

            # text = homepage.get_seemarCameratList()
            # self.assertEqual(test_data.get('expected_re3'),text,  msg=test_data.get('msg'))

            # text = homepage.get_ordinaryCameraList()
            # self.assertEqual(test_data.get('expected_re4'),text,  msg=test_data.get('msg'))

            text = homepage.get_realTimeCaptureEml()
            self.assertEqual(test_data.get('expected_re5'),text,  msg=test_data.get('msg'))

            text = homepage.get_detailsButton()
            self.assertEqual(test_data.get('expected_re6'),text,  msg=test_data.get('msg'))

            homepage.click_seemarCameratList()
            homepage.click_ordinaryCameraList()
        else:
            homepage.click_previewButton()
            homepage.wait_eml_presence(homepage.immediatelyAddButton)
            text = homepage.get_immediatelyAddButton()
            self.assertEqual(test_data.get('expected_re7'), text, msg=test_data.get('msg'))

    def test_2_immediatelyAdd_ordinary_Camera(self):
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        videoManagerPage = VideoManagerPage(self.driver)
        videoManagerPage.wait_eml_presence(videoManagerPage.manualAddButton)
        cameraIpList = videoManagerPage.get_video_list()
        if len(cameraIpList) > 0:
            videoManagerPage.click_batchDeleteRadio()
            time.sleep(1)
            videoManagerPage.click_batchDeleteButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.batchDeleteConfirmButton)

            videoManagerPage.click_batchDeleteConfirmButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.delSuccessToast)
            text = videoManagerPage.get_delSuccessToast()
            self.assertEqual('删除成功', text, msg='删除视频记录断言失败')
        time.sleep(3)
        homepage.click_previewButton()
        homepage.click_immediatelyAddButton()
        ipStreamAddPage = homepage.IpStreamAdd(self.driver)
        ipStreamAddPage.wait_eml_presence(homepage.IpStreamAdd.cameraType)
        ipStreamAddPage.click_cameraType()
        ipStreamAddPage.wait_eml_presence(homepage.IpStreamAdd.ordinaryCameraType)
        ipStreamAddPage.select_ordinaryCameraType()
        ipStreamAddPage.set_cameraIpBox('rtsp://10.58.122.171:554/MainStream')
        ipStreamAddPage.set_userName('admin')
        ipStreamAddPage.set_userpwd('123456')
        ipStreamAddPage.click_confirmButton()
        homepage.wait_eml_presence(homepage.addCameraSuccessTost)
        text = homepage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='批量添加普通摄像机断言失败')
        time.sleep(3)

    def test_3_immediatelyAdd_seemart_Camera(self):
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        videoManagerPage = VideoManagerPage(self.driver)
        videoManagerPage.wait_eml_presence(videoManagerPage.manualAddButton)
        cameraIpList = videoManagerPage.get_video_list()
        if len(cameraIpList) > 0:
            videoManagerPage.click_batchDeleteRadio()
            time.sleep(1)
            videoManagerPage.click_batchDeleteButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.batchDeleteConfirmButton)
            # WebDriverWait(self.driver, 5, 0.5).until(
            #     lambda x: x.find_element_by_css_selector('body > div.el-dialog__wrapper.xg-message.delVideoContainer > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span'))
            videoManagerPage.click_batchDeleteConfirmButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.delSuccessToast)
            # WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
            text = videoManagerPage.get_delSuccessToast()
            self.assertEqual('删除成功', text, msg='删除视频记录断言失败')

        time.sleep(3)
        homepage.click_previewButton()
        homepage.wait_eml_presence(homepage.immediatelyAddButton)
        homepage.click_immediatelyAddButton()
        ipStreamAddPage = homepage.IpStreamAdd(self.driver)
        ipStreamAddPage.wait_eml_presence(homepage.IpStreamAdd.cameraType)
        ipStreamAddPage.set_cameraIpBox('10.58.122.172')
        ipStreamAddPage.set_userName('admin')
        ipStreamAddPage.set_userpwd('123456')
        ipStreamAddPage.click_confirmButton()
        homepage.wait_eml_presence(homepage.addCameraSuccessTost)
        text = homepage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='批量添加普通摄像机断言失败')
        time.sleep(3)


    def test_4_batch_immediatelyAdd_ordinary_Camera(self):
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        videoManagerPage = VideoManagerPage(self.driver)
        videoManagerPage.wait_eml_presence(videoManagerPage.manualAddButton)
        cameraIpList = videoManagerPage.get_video_list()
        if len(cameraIpList) > 0:
            videoManagerPage.click_batchDeleteRadio()
            time.sleep(1)
            videoManagerPage.click_batchDeleteButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.batchDeleteConfirmButton)
            videoManagerPage.click_batchDeleteConfirmButton()
            time.sleep(1)
            videoManagerPage.wait_eml_presence(videoManagerPage.delSuccessToast)
            text = videoManagerPage.get_delSuccessToast()
            self.assertEqual('删除成功', text, msg='删除视频记录断言失败')
        time.sleep(3)
        homepage.click_previewButton()
        homepage.wait_eml_presence(homepage.immediatelyAddButton)
        homepage.click_immediatelyAddButton()
        ipStreamPage = homepage.IpStreamAdd(self.driver)
        ipStreamPage.wait_eml_presence(ipStreamPage.ipAddrMultAdd)
        ipStreamPage.click_ipAddrMultAdd()
        ipStreamPage.wait_eml_presence(ipStreamPage.mulCameraType)
        ipStreamPage.click_mulCameraType()
        ipStreamPage.wait_eml_presence(ipStreamPage.ordinaryCameraMultType)
        ipStreamPage.select_ordinaryCameraMultType()
        ipStreamPage.set_rtstStreamStartBox('rtsp://10.58.122.171:554/MainStream')
        ipStreamPage.set_rtstStreamEndBox('rtsp://10.58.122.172:554/MainStream')
        ipStreamPage.set_userNameoMultBox('admin')
        ipStreamPage.set_pwdoMultBox('123456')
        ipStreamPage.click_confirmButton()
        homepage.wait_eml_presence(homepage.addCameraSuccessTost)
        text = homepage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='批量添加普通摄像机断言失败')
        time.sleep(3)

    def test_5_batch_immediatelyAdd_seemart_Camera(self):
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        videoManagerPage = VideoManagerPage(self.driver)
        videoManagerPage.wait_eml_presence(videoManagerPage.manualAddButton)
        cameraIpList = videoManagerPage.get_video_list()
        if len(cameraIpList) > 0:
            videoManagerPage.click_batchDeleteRadio()
            time.sleep(1)
            videoManagerPage.click_batchDeleteButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.batchDeleteConfirmButton)
            # WebDriverWait(self.driver, 5, 0.5).until(
            #     lambda x: x.find_element_by_css_selector('body > div.el-dialog__wrapper.xg-message.delVideoContainer > div > div.el-dialog__footer > div > button.el-button.btn.ok.el-button--primary > span'))
            videoManagerPage.click_batchDeleteConfirmButton()
            time.sleep(1)
            videoManagerPage.wait_eml_presence(videoManagerPage.delSuccessToast)
            # WebDriverWait(self.driver, 5, 0.5).until(lambda x: x.find_element_by_css_selector('body > div.el-message.el-message--success > p'))
            text = videoManagerPage.get_delSuccessToast()
            self.assertEqual('删除成功', text, msg='删除视频记录断言失败')
        time.sleep(3)
        homepage.click_previewButton()
        homepage.wait_eml_presence(homepage.immediatelyAddButton)
        homepage.click_immediatelyAddButton()
        ipStreamAddPage = homepage.IpStreamAdd(self.driver)
        ipStreamAddPage.wait_eml_presence(ipStreamAddPage.ipAddrMultAdd)
        ipStreamAddPage.click_ipAddrMultAdd()
        ipStreamAddPage.set_cameraStartIpMultBox('10.58.122.175')
        ipStreamAddPage.set_cameraEndIpMultBox('10.58.122.176')
        ipStreamAddPage.set_userNameMultBox('admin')
        ipStreamAddPage.set_pwdMultBox('123456')
        ipStreamAddPage.click_confirmButton()
        homepage.wait_eml_presence(homepage.addCameraSuccessTost)
        text = homepage.get_addCameraSuccessTost()
        self.assertEqual('添加成功', text, msg='批量添加seemart摄像机ip断言失败')
        time.sleep(3)

    def test_6_add_new_Camera(self):
        homepage = HomePage(self.driver)
        homepage.click_mainMenuButton()
        videoManagerPage = VideoManagerPage(self.driver)
        videoManagerPage.wait_eml_presence(videoManagerPage.manualAddButton)
        cameraIpList = videoManagerPage.get_video_list()
        if len(cameraIpList) == 0:
            videoManagerPage.click_manualAddButton()
            ipStreamAddPage = videoManagerPage.IpStreamAdd(self.driver)
            ipStreamAddPage.wait_eml_presence(videoManagerPage.IpStreamAdd.cameraIpBox)
            ipStreamAddPage.set_cameraIpBox('10.58.122.172')
            ipStreamAddPage.set_userName('admin')
            ipStreamAddPage.set_userpwd('123456')
            ipStreamAddPage.click_confirmButton()
            ipStreamAddPage.wait_eml_presence(videoManagerPage.addCameraSuccessTost)
            text = videoManagerPage.get_addCameraSuccessTost()
            self.assertEqual('添加成功', text, msg='添加seemart摄像机ip断言失败')
        if len(cameraIpList) < 6:
            homepage.click_previewButton()
            homepage.wait_eml_presence(homepage.addCameraButton)
            homepage.click_addCameraButton()
            ipStreamAddPage = videoManagerPage.IpStreamAdd(self.driver)
            ipStreamAddPage.click_ipAddrMultAdd()
            ipStreamAddPage.set_cameraStartIpMultBox('10.58.122.175')
            ipStreamAddPage.set_cameraEndIpMultBox('10.58.122.176')
            ipStreamAddPage.set_userNameMultBox('admin')
            ipStreamAddPage.set_pwdMultBox('123456')
            ipStreamAddPage.click_confirmButton()
            videoManagerPage.wait_eml_presence(videoManagerPage.addCameraSuccessTost)
            text = videoManagerPage.get_addCameraSuccessTost()
            self.assertEqual('添加成功', text, msg='批量添加seemart摄像机ip断言失败')
            time.sleep(3)

    def test_7_logout(self):
        homepage = HomePage(self.driver)
        homepage.click_userNameButton()
        homepage.click_logoutButton()
        loginpage = LoginPage(self.driver)
        loginpage.wait_eml_presence(loginpage.login)
        text = loginpage.get_login()
        self.assertEqual('登录', text, msg='退出登录断言失败')

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        print("------------执行用例结束-----------")

if __name__ == '__main__':
    unittest.main()
    # suit = unittest.TestSuite()
    # suit.addTest(TestHomePage('test_mainMenuButton'))
    # suit.addTest(TestHomePage('test_previewButton'))
    # suit.addTest(TestHomePage('test_seemarCameratList'))
    # suit.addTest(TestHomePage('test_ordinaryCameraList'))
    # suit.addTest(TestHomePage('test_userNameButton'))
    # suit.addTest(TestHomePage('test_logoutButton'))
    # runner = unittest.TextTestRunner()
    # runner.run(suit)
