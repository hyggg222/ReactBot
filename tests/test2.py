import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException


def login_facebook(driver):
    driver.get("https://www.facebook.com/")
    time.sleep(0.1)
    print("✅ Đã đăng nhập vào Facebook.")

def open_fanpage(driver, page_url):
    print(f"🎬 Đang mở fanpage: {page_url}")
    try:
        driver.get(page_url)
    except Exception as e:
        print("Lỗi khi mở fanpage:", e)
    time.sleep(1)
    print(f"✅ Đã mở fanpage: {page_url}")

def like_post(driver, post_url):
    driver.get(post_url)
    time.sleep(1)
    try:
        # Like button - có thể thay đổi theo ngôn ngữ và phiên bản
        like_button = driver.find_element(By.XPATH, "//div[@aria-label='Like']") 
        like_button.click()
        print("Đã like post:", post_url)
    except:
        print("Không tìm thấy nút like ở:", post_url)

def scroll_element_by_xpath_js(driver, xpath, scroll_amount=250, element_name="vùng chứa cuộn"):
    """
    Sử dụng JavaScript để cuộn một phần tử được tìm thấy bằng XPATH.
    Args:
        driver: Đối tượng WebDriver.
        xpath: XPATH của phần tử cần cuộn (ví dụ: vùng chứa cuộn) hoặc phần tử con cần hiển thị.
        scroll_amount: "top", "center", "bottom", hoặc một số pixel để cuộn xuống (ví dụ: 500).
                       Nếu là "bottom", cuộn vùng chứa xuống cuối.
                       Nếu là "top" / "center", cuộn phần tử mục tiêu vào tầm nhìn.
        element_name: Tên hiển thị của phần tử cho log.
    Returns:
        True nếu cuộn thành công, False nếu không tìm thấy phần tử.
    """
    js_find_element = f"""
    var element = document.evaluate("{xpath}", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    return element;
    """

    try:
        print(f"Đang tìm {element_name} bằng XPATH: {xpath} để cuộn...")
        target_element = driver.execute_script(js_find_element)

        if not target_element:
            print(f"❌ Không tìm thấy {element_name} với XPATH: {xpath}. Không thể cuộn.")
            return False

        print(f"Đã tìm thấy {element_name}. Tiến hành cuộn...")

        if scroll_amount == "top":
            driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
            print(f"Đã cuộn {element_name} vào đầu tầm nhìn.")
        elif scroll_amount == "center":
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
            print(f"Đã cuộn {element_name} vào giữa tầm nhìn.")
        elif scroll_amount == "bottom":
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", target_element)
            print(f"Đã cuộn {element_name} (vùng chứa) xuống cuối cùng.")
        elif isinstance(scroll_amount, (int, float)):
            # Đây là phần chính bạn quan tâm: cuộn xuống một lượng pixel cố định
            driver.execute_script(f"arguments[0].scrollTop += {scroll_amount};", target_element)
            print(f"Đã cuộn {element_name} xuống {scroll_amount} pixel.")
        else:
            print(f"Cảnh báo: Giá trị scroll_amount không hợp lệ: {scroll_amount}. Không cuộn.")
            return False

        time.sleep(1) # Cho thời gian để render sau khi cuộn
        return True

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi cố gắng cuộn {element_name} bằng JavaScript: {e}")
        return False

# --- Hàm click_button_container (sử dụng scroll_element_by_xpath_js) ---
# ... (Nội dung của hàm click_button_container) ...
def click_button_container(driver, button_xpath, container_xpath, button_name="nút"):
    """
    Tìm và nhấn vào một nút nằm trong vùng cuộn riêng biệt.
    Sử dụng hàm scroll_element_by_xpath_js để cuộn.
    """
    try:
        print(f"Đang tìm kiếm vùng chứa cuộn: {container_xpath}...")
        scrollable_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, container_xpath))
        )
        print(f"Đã tìm thấy vùng chứa cuộn.")

        print(f"Đang cố gắng cuộn và tìm {button_name} trong vùng chứa...")
        
        max_scroll_attempts = 30 
        scroll_attempt = 0
        
        while scroll_attempt < max_scroll_attempts:
            try:
                # Cố gắng tìm nút ngay lập tức với thời gian chờ ngắn
                button_element = WebDriverWait(driver, 10).until( 
                    EC.presence_of_element_located((By.XPATH, button_xpath))
                )
                print(f"Đã tìm thấy {button_name} !!")
                
                # Cuộn chính nút vào tầm nhìn trong vùng chứa cuộn bằng JS
                scroll_element_by_xpath_js(driver, button_xpath, "center", button_name)
                time.sleep(3) # Cho thời gian ổn định

                # Chờ nút có thể click được và click
                clickable_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                clickable_button.click()
                print(f"✅ Đã nhấn vào {button_name} thành công.")
                time.sleep(1)
                return # Hoàn thành và thoát hàm

            except TimeoutException:
                print(f"Chưa tìm thấy {button_name}. Tiến hành cuộn vùng chứa...")
                
                # Cuộn vùng chứa xuống một lượng nhỏ để kích hoạt tải nội dung mới
                # Sử dụng hàm scroll_element_by_xpath_js để cuộn vùng chứa
                # Cuộn xuống 1000 pixel
                if not scroll_element_by_xpath_js(driver, container_xpath, 250, "vùng chứa cuộn"):
                    print("Không thể cuộn vùng chứa. Có thể XPATH sai hoặc không còn gì để cuộn.")
                    raise TimeoutException(f"Không tìm thấy '{button_name}' sau nhiều lần cuộn do vùng chứa không cuộn được.")
                
                scroll_attempt += 1
                if scroll_attempt == max_scroll_attempts:
                    print(f"❌ Lỗi: Đã đạt số lần cuộn tối đa ({max_scroll_attempts}), nhưng không tìm thấy '{button_name}'.")
                    raise TimeoutException(f"Không tìm thấy '{button_name}' sau nhiều lần cuộn.")
        
        # Nếu vòng lặp kết thúc mà không tìm thấy nút
        raise NoSuchElementException(f"Không tìm thấy '{button_name}' trong vùng chứa cuộn sau tất cả các lần thử.")
        
    except TimeoutException as te:
        print(f"❌ Lỗi Timeout: {te.msg}")
        print("Vui lòng kiểm tra lại XPATH của nút và vùng chứa.")
    except NoSuchElementException as nse:
        print(f"❌ Lỗi NoSuchElement: {nse.msg}")
        print("Không tìm thấy phần tử với XPATH đã cung cấp.")
    except ElementClickInterceptedException:
        print(f"❌ Lỗi: '{button_name}' bị một phần tử khác che khuất hoặc không thể nhấn được.")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi tổng quát khi nhấn vào {button_name}: {e}")

def click_button(driver, path, button_name="switch account"):
    """
    Tìm và nhấn vào một nút trên fanpage.
    Args:
        driver: Đối tượng WebDriver.
        button_xpath_or_css: XPATH hoặc CSS Selector của nút cần nhấn.
        button_name: Tên của nút để in ra log.
    """
    try:
    
        print(f"Đang tìm kiếm {button_name}...")
        # Sử dụng WebDriverWait để chờ nút xuất hiện và có thể click được
        # Thời gian chờ tối đa 20 giây
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, path))  # Nếu dùng XPATH: (By.XPATH, button_xpath_or_css)
            # Nếu dùng CSS Selector: (By.CSS_SELECTOR, button_xpath_or_css)
        )
        button.click()
        print(f"✅ Đã nhấn vào {button_name} thành công.")
        time.sleep(1) # Đợi một chút sau khi nhấn
    except TimeoutException:
        print(f"❌ Lỗi: Không tìm thấy hoặc không thể nhấn vào {button_name} sau 20 giây. XPATH/CSS Selector có thể sai hoặc nút chưa tải.")
    except NoSuchElementException:
        print(f"❌ Lỗi: Không tìm thấy {button_name} với XPATH/CSS Selector đã cung cấp.")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi nhấn vào {button_name}: {e}")

def switch_own_fanpage(driver, page_url):
    try:
        open_fanpage(driver, page_url) 
        click_button(driver, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div[1]/span/div/div/div[1]/div[2]/div[1]/div/div/div/span", "switch account")  # Nhấn nút "Switch account"
        click_button(driver, "/html/body/div[1]/div/div[1]/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div/div/div[1]/div/span/span", "accept switch account")  # Nhấn nút "Accept Switch account"
    except Exception as e:
        print("Lỗi khi mở fanpage:", e)
    time.sleep(1) 
    print(f"✅ Đã mở fanpage: {page_url}")

def like_post(driver, post_url):   
    open_fanpage(driver, post_url) 
    time.sleep(1)
    try:
        click_button_container(
            driver,
            button_xpath="/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div[13]/div/div/div[4]/div/div/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/div[1]", # Nút like post
            container_xpath="/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[2]/div/div/div/div/div/div/div/div[2]", # tab chứa nút like post
            button_name="nút like post"
        )  
        print("Đã like post!")
    except:
        print("Không tìm thấy nút like ở:", post_url)

def like_page(driver, page_url):
    open_fanpage(driver, page_url) 
    time.sleep(1)
    try:
        
        click_button(driver, 
            path="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[1]/div/div/div/div[1]", # Nút like fanpage
            button_name="nút like fanpage"
        )
        print("Đã like fanpage!")
    except:
        print("Không tìm thấy nút like ở:", page_url)


from PIL import Image

def take_cropped_screenshot(driver, output_path, x, y, width, height):
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    temp_full_screenshot_path = "temp_full_screenshot.png" # File tạm thời
    
    try:
        driver.save_screenshot(temp_full_screenshot_path)
        print(f"Đã chụp toàn bộ màn hình vào: {temp_full_screenshot_path}")

        img = Image.open(temp_full_screenshot_path)

        crop_area = (x, y, x + width, y + height)

        cropped_img = img.crop(crop_area)
        
        cropped_img.save(output_path)
        print(f"✅ Đã chụp và cắt màn hình thành công, lưu tại: {output_path}")

    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file tạm {temp_full_screenshot_path}. Đảm bảo Selenium có thể ghi file.")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi chụp và cắt màn hình: {e}")
    finally:
        if os.path.exists(temp_full_screenshot_path):
            os.remove(temp_full_screenshot_path)        

def cap_mh(driver, output_path, num_posts=2):
    # nút ảnh đại diện
    click_button(
        driver,
        path="/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[1]/span/div/div[1]/div/div[2]/div/div[1]" 
    )
    # nút "Cài đặt và quyền riêng tư"
    click_button(
        driver,
        path="/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div/div/div[1]/div/div[3]"
    )
    # nút "Nhật ký hoạt động"
    click_button(
        driver,
        path="/html/body/div[1]/div/div[1]/div/div[2]/div[5]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div[3]/div/div/a/div[1]/div/div[2]/div/div/div"
    )
    # nút "Trang, lượt thích trang và sở thích"
    click_button_container(
        driver,
        button_xpath="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[9]/div[1]/div/div[1]/div[2]",
        container_xpath="/html"
    )
    time.sleep(3)
    # Cap màn hình like fanpage
    print("\n--- Bắt đầu cap màn hình like fanpage ---")
    action_name = "page"
    file_name_context = f"{action_name}.png"
    output_path_context = os.path.join(output_path, file_name_context)
    take_cropped_screenshot(driver, output_path_context, x = 580, y = 370, width = 640, height = 100) 
    # Nút "Bình luận và cảm xúc"

    click_button(
        driver,
        path="/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div[1]"
    )
    time.sleep(3)
    # Cap màn hình like post
    print("\n--- Bắt đầu cap màn hình like post ---")
    action_name = "post"
    file_name_context = f"{action_name}.png"
    output_path_context = os.path.join(output_path, file_name_context)
    take_cropped_screenshot(driver, output_path_context, x = 530, y = 255, width = 1000, height = 140 * num_posts) 


if __name__ == "__main__":

    selenium_profile_dir = r"D:\\selenium_profiles\\my_bot_profile"
    os.makedirs(selenium_profile_dir, exist_ok=True) # Tạo thư mục nếu chưa có

    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={selenium_profile_dir}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()  

    """

    print("🚀 Bắt đầu thực hiện các thao tác trên fanpage...")
    with open(r"D:/project/bot_tt_facebook/input.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # INPUT TỪ FILE TXT 
    # Dòng đầu: số lượng post
    num_posts = int(lines[0])
    # Dòng 2: link fanpage
    fanpage_link = lines[1]
    # Dòng 3 đến dòng (3 + num_posts - 1): link post
    post_links = lines[2:2 + num_posts]
    """
    own_fanpage_links = [
        "https://www.facebook.com/profile.php?id=61578618757193"
        #,"https://www.facebook.com/profile.php?id=61578810026612"
    ]

    login_facebook(driver) 
    
    """
    like_page(driver, fanpage_link) 
    for post_link in post_links:
        like_post(driver, post_link)
    cap_mh(driver)
    """
    cnt = 1
    for own_fanpage_link in own_fanpage_links:
        switch_own_fanpage(driver, own_fanpage_link) 
        output_dir = f"D:\\project\\bot_tt_facebook\\output\\huy-15acc\\acc_{cnt}"
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        cap_mh(driver, output_dir, num_posts)
        cnt += 1

    switch_own_fanpage(driver, page_url = "https://www.facebook.com/profile.php?id=61578777720156") 

    driver.quit()
    print("✅ Đã hoàn thành các thao tác trên fanpage.")