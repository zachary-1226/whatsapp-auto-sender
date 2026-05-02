# Program to send bulk messages through WhatsApp web from an excel sheet without saving contact numbers

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas

excel_data = pandas.read_excel('Recipients data.xlsx', sheet_name='Recipients')

count = 0

# 设置 Chrome 选项
chrome_options = Options()
# 在 Docker 容器内运行必须启用 Headless 无头模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 显式使用 Service 初始化 Selenium 驱动，完美适配 Selenium 4
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get('https://web.whatsapp.com')
input("Zachary 的本地服务已启动，请在登录 WhatsApp 网页版并加载完聊天记录后按回车继续...")
for column in excel_data['Contact'].tolist():
    try:
        url = 'https://web.whatsapp.com/send?phone={}&text={}'.format(excel_data['Contact'][count], excel_data['Message'][0])
        sent = False
        # It tries 3 times to send a message in case if there any error occurred
        driver.get(url)
        try:
            click_btn = WebDriverWait(driver, 35).until(
                EC.element_to_be_clickable((By.CLASS_NAME, '_3XKXx')))
        except Exception as e:
            print("抱歉，消息未能发送给 " + str(excel_data['Contact'][count]))
        else:
            sleep(2)
            click_btn.click()
            sent = True
            sleep(5)
            print('消息成功发送至: ' + str(excel_data['Contact'][count]))
        count = count + 1
    except Exception as e:
        print('发送消息失败至 ' + str(excel_data['Contact'][count]) + ': ' + str(e))
driver.quit()
print("Zachary 的本地服务：脚本已成功执行完毕！")
