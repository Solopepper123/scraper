import time
from selenium import webdriver
from selenium import __version__
print(__version__)
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 登入页面
def login_shumao():
    print("login_shumao")
    driver.find_element(by=By.CSS_SELECTOR, value='#app > div:nth-child(1) > div.flex.justify-between.header-content.items-center > div:nth-child(3) > div').click()
    wait = WebDriverWait(driver, TIME_OUT)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tab-PASSWORD')))
    driver.find_element(by=By.CSS_SELECTOR, value='#tab-PASSWORD').click()
    wait = WebDriverWait(driver, TIME_OUT)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div/div/div/div/div/div/div[3]/div[1]/div/input')))
    username = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div/div[3]/div[1]/div/input').send_keys(account)
    passwerd = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div/div[3]/div[2]/div/input').send_keys(passwd)
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div/div[3]/div[4]/label/span/span').click()
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div/div/div/div/div/div/div[3]/button').click()
    time.sleep(3)

# 查询页面
def search_infos():
    wait = WebDriverWait(driver, TIME_OUT)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[4]/div/div/div[1]/div[3]/div/div[1]/div/table')))
    table = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div[4]/div/div/div[1]/div[3]/div/div[1]/div/table')
    rows = table.find_elements(by=By.TAG_NAME, value='tr')
    dfi = pd.DataFrame([])
    time.sleep(TIME_OUT)
    for row in rows:
        cells = row.find_elements(by=By.TAG_NAME, value='td')
        idx = 0
        for cell in cells:
            # 找到采购商
            if idx == 3:
                print(cell.text)
                link = cell.find_element(by=By.CLASS_NAME, value='ep-link__inner')
                text = str(link.text)
                if duplicate_check(text, df):
                    print("drop duplucate df")
                    break
                if len(dfi) > 0 and duplicate_check(text, dfi):
                    print("drop duplucate df1")
                    break
                time.sleep(TIME_OUT)
                link.click()
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div/table/tbody/tr[2]/td[4]/a/span')))
                driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[3]/div/div[1]/div/div/div[2]/div/div/table/tbody/tr[2]/td[4]/a/span').click()
                time.sleep(TIME_OUT)
                df_res = search_info(text)
                dfi = pd.concat([dfi, df_res], ignore_index=True)
                break
            idx += 1
    return dfi

# 查询信息dfi
def search_info(company):
    # 定位表格元素
    wait = WebDriverWait(driver, TIME_OUT)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div/div/div/div[1]/div[3]/div/div[1]/div/table')))
    table = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/div/div/div[1]/div[3]/div/div[1]/div/table')

    # 获取表格中的所有行
    rows = table.find_elements(by=By.TAG_NAME, value='tr')
    # 创建一个空列表，用于存储数据
    data = []
    # 遍历每一行
    # 创建一个空字典，用于存储一行数据
    if len(rows) == 0:
        record = {}
        record['Company'] = company
        data.append(record)
        return pd.DataFrame(data)
    for r in rows:
        record = {}
        record['Company'] = company
        # 获取行中的所有单元格
        cells = r.find_elements(by=By.TAG_NAME, value='td')
        # 如果单元格数量大于0，则说明是数据行，而不是标题行或空行
        if len(cells) > 0:
            # 将每个单元格的文本和对应的列名作为键值对存入字典
            record['Email'] = cells[0].text
            record['Contact'] = cells[1].text
            record['Job'] = cells[2].text
            record['Phone'] = cells[3].text
            record['Web'] = cells[4].text
            # 将字典追加到列表中
            data.append(record)
            # 将列表转换为DataFrame对象
    df1 = pd.DataFrame(data)
    driver.back()
    return df1
    
def duplicate_check(company_name, df_check):
    if company_name in df_check['Company'].values:
        return True
    return False

if __name__ == "__main__":
    print("start")
    # options = webdriver.ChromeOptions()
    options = webdriver.EdgeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument('--headless')
    # service = Service('C:/Users/juefe/AppData/Local/Programs/Python/Python311/chromedriver.exe')
    # driver = webdriver.Chrome(options=options)
    print("start driver")
    driver= webdriver.Edge(options=options)
    print("get home page")
    driver.get("https://www.zhizhan360.com/home")
    account = "19542787020"
    passwd = "Swaremsc123!"
    TIME_OUT = 10
    df = pd.read_csv('./data_clothes.csv')
    login_shumao()
    driver.get("https://www.zhizhan360.com/product?searchValue=hoodie&csRelationFlag=0&preciseMatching=1&date=,&timeType=1&inOutType=0&hasContact=1")
    for i in range(40):
        df_ret = search_infos()
        df = pd.concat([df, df_ret], ignore_index=True)
        time.sleep(TIME_OUT)
        df.to_csv('./data_clothes.csv', sep=',', header=True, index=False)
        driver.find_element(by=By.CLASS_NAME, value='btn-next').click()
    # 打印DataFrame对象
    df.to_csv('./data_clothes.csv', sep=',', header=True, index=False)
    # 关闭浏览器对象
    driver.close()