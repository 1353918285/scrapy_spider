import time
import re
import csv
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions


# option=Options()
# option.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=option)
option = ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])
driver = Chrome(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
   'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
driver.get('https://www.51job.com/')
input = driver.find_element_by_xpath('//input[@id="kwdselectid"]')
keyword = 'python开发'
input.send_keys(keyword)
time.sleep(1)
driver.find_element_by_xpath('//div[contains(@class,"ush")]/button').click()
handle = driver.current_window_handle
has_next = True
file = open('data/%s_positionDesc.csv' % keyword, 'a', encoding='utf-8')
writer = csv.DictWriter(file,fieldnames=['keyword', 'position_desc'])
while has_next:
    time.sleep(5)
    list = driver.find_elements_by_xpath('//div[@class="j_joblist"]/div')
    for li in list:
        row = {}
        curr = li.find_element_by_xpath('//ul/li[@class="on"]/div').text
        print("-------current page is %s---------" % curr)
        print(driver.title)
        driver.implicitly_wait(2)
        time.sleep(1)
        links = li.find_element_by_xpath('./a').click()
        driver.switch_to.window(driver.window_handles[-1])
        print(driver.title)
        word = keyword
        if '滑动验证页面' in driver.title:
            wait = WebDriverWait(driver,10)
            source = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.nc-container .nc_scale span')))
            # driver.find_elements_by_css_selector('#nc_1_n1z')
            box = driver.find_element_by_class_name('nc_scale')
            width = box.value_of_css_property('width')
            move_width =  re.findall(r'(.*?)px',width)[0]
            try:
                ActionChains(driver).drag_and_drop_by_offset(source, move_width, 0).perform()
                driver.refresh()
            except Exception:
                driver.refresh()
                continue
        else:
            try:
                time.sleep(2)
                position = driver.find_element_by_xpath('//div[@class="tBorderTop_box"]/div[contains(@class,"job_msg")]').text
            except Exception:
                position = ''
            time.sleep(3)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            writer.writerow({'keyword':keyword,'position_desc':position})
            print(position)
    time.sleep(2)
    # driver.execute_script('window.scrollTo(0,6775)')
    next = driver.find_element_by_xpath('//ul/li[@class="next"]/a')
    if 'bk next' in next.get_attribute('class'):
        has_next = False
    else:
        next.click()
        time.sleep(5)
driver.quit()