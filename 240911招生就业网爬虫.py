import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 初始化Safari浏览器
driver = webdriver.Safari()

# 尝试打开目标网页
target_url = "http://scc.hnu.edu.cn/module/careers?menu_id=3231"
print(f"正在访问目标网页: {target_url}")
driver.get(target_url)

# 创建一个空的DataFrame来存储数据
data = pd.DataFrame(columns=["公司", "链接", "行业", "企业性质", "需求专业", "工作城市"])

def scrape_page():
    try:
        # 等待页面加载完成并确保pub-list元素可见，延长等待时间到20秒
        print("等待页面加载完成...")
        wait = WebDriverWait(driver, 20)
        pub_list = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "pub-list")))
        
        # 只从pub-list中查找item
        items = pub_list.find_elements(By.CLASS_NAME, "item")
        
        # 如果没有找到职位条目，返回False停止翻页
        if len(items) == 0:
            print("当前页面没有职位条目，停止抓取。")
            return False
        
        for item in items:
            try:
                # 公司名称在 'item-link' 的 title 属性中
                company = item.find_element(By.CLASS_NAME, "item-link").get_attribute("title")
                
                # 链接
                link = item.find_element(By.CLASS_NAME, "item-link").get_attribute("href")
                
                # 使用XPath定位企业性质和行业
                nature = item.find_element(By.XPATH, "./div/div[2]/div/ul[1]/li[1]/p").text  # 定位企业性质
                industry = item.find_element(By.XPATH, "./div/div[2]/div/ul[1]/li[2]/p").text.strip()  # 定位行业
                
                # 需求专业和工作城市 - 使用你提供的 XPath
                major_requirements = item.find_element(By.XPATH, "./div/div[2]/div/ul[2]/li/p[1]").text.strip()  # 定位需求专业
                city = item.find_element(By.XPATH, "./div/div[2]/div/ul[2]/li/p[2]").text.strip()  # 定位工作城市并去除空白
                
                # 将信息添加到DataFrame中
                data.loc[len(data)] = [company, link, industry, nature, major_requirements, city]
            
            except Exception as e:
                print(f"跳过一个条目: {e}")
        
        return True  # 页面有内容，继续翻页
    
    except Exception as e:
        print(f"页面加载失败或无内容: {e}")
        return False

# 自动翻页并抓取多页数据
for page in range(1, 55):
    print(f"正在抓取第{page}页...")
    
    # 如果某一页为空，停止继续抓取
    if not scrape_page():
        print(f"第{page}页没有内容，停止翻页。")
        break
    
    # 每10页暂停5秒钟
    if page % 10 == 0:
        print("已抓取10页，暂停5秒...")
        time.sleep(5)
    
    # 查找输入框并输入目标页码
    try:
        page_input = driver.find_element(By.CLASS_NAME, "J-paginationjs-go-pagenumber")
        page_input.clear()
        page_input.send_keys(str(page + 1))  # 输入下一页的页码
        
        # 点击跳转按钮
        go_button = driver.find_element(By.CLASS_NAME, "J-paginationjs-go-button")
        go_button.click()
        time.sleep(3)  # 等待新页面加载
    except Exception as e:
        print(f"翻页失败: {e}")
        break

# 保存到Excel文件
data.to_excel("job_data.xlsx", index=False)
print("数据抓取完成并保存到Excel文件。")

# 关闭浏览器
driver.quit()
