from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import unittest


class Douyu(unittest.TestCase):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    # 初始化方法，必须是setUp()
    def setUp(self):
        self.driver = webdriver.Chrome(chrome_options=Douyu.chrome_options)
        self.num = 0
        self.count = 0

    # 测试方法必须有test字样开头
    def testDouyu(self):
        self.driver.get('https://www.douyu.com/directory/all')
        while True:
            try:
                soup = bs(self.driver.page_source, features='lxml')
                names = soup.find_all('h3', attrs={'class': 'ellipsis'})
                categories = soup.find_all(
                    'span', attrs={
                        'class': 'tag ellipsis'
                    })
                authors = soup.find_all(
                    'span', attrs={
                        'class': 'dy-name ellipsis fl'
                    })
                viewer_numbers = soup.find_all(
                    'span', attrs={
                        'class': 'dy-num fr'
                    })

                for name, author, number, category in zip(
                        names, authors, viewer_numbers, categories):
                    print(name.get_text().strip())
                    # print(
                    #     f'观众人数: {number.get_text().strip()} \t房间名:{name.get_text().strip()},\t主播:{author.get_text.strip()}\t分类:{category.get_text().strip()}'
                    # )
                    self.num += 1
                    if self.driver.page_source.find(
                            'shark-pager-disable-next') != -1:
                        break
                    wait = WebDriverWait(self.driver, 100)
                    next_page_btn = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME,
                                                        'shark-pager-next')))
                    next_page_btn.click()
            except TimeoutError as e:
                print('time out')
                return self.testDouyu()
            except StaleElementReferenceException as e:
                print('not found')
                return self.testDouyu()

    # 测试结束执行的方法
    def tearDown(self):
        # 退出PhantomJS()浏览器
        print(f'当前网站直播人数{self.num}')
        print(f'当前网站观众人数{self.count}')
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()