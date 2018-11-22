import selenium
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import time
import unittest

#
# #webdriver中的PhantomJS方法可以打开一个我们下载的静默浏览器。
# #输入executable_path为当前文件夹下的phantomjs.exe以启动浏览器
#
# driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
#
# #使用浏览器请求页面
# driver.get('http://www.shfe.com.cn')
#
# # 加载5秒，等待所有数据加载完毕
# time.sleep(5)
# # 通过id来定位元素，
# # .text获取元素的文本数据
# print(driver.find_element_by_id('subnav').text)
#
# # 关闭浏览器
# driver.close()

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        #创建驱动程序对象
        self.driver = webdriver.Chrome()

    def test_search_in_python_org(self):
        #创建驱动程序对象的本地引用
        driver = self.driver
        #打开对应网页
        driver.get("http://www.shfe.com.cn")
        # 加载5秒，等待所有数据加载完毕
        time.sleep(3)
        #使用assert断言的方法判断在页面标题中是否包含 “Python”，assert 语句将会在之后的语句返回false后抛出异常
        #self.assertIn("ul", driver.title)
        #获取到id为subnav的ul，也就是最外层的ul
        elemul = driver.find_element_by_id('subnav')#.text
        print(elemul.text)
        #此处用的是elements！返回的是list，此层获取到的是金属，能源等的列表
        elemlis_first = elemul.find_elements_by_xpath('.//li[2]/ul/li')
        for elemli_first in elemlis_first:
            #将每一个li打开，里面还有一层ul，此处为铜铝等详细列表
            elemlis_second = elemli_first.find_elements_by_xpath('.//ul/li')
            for elemli_second in elemlis_second:
                #selenium获取a的href需要get_attribute方法
                href = elemli_second.find_element_by_tag_name('a').get_attribute('href')
        #向页面文本框输入内容
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        #assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.close()


if __name__=="__main__":
    unittest.main()







