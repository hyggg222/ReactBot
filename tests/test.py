import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime # Import để lấy thời gian hiện tại cho tên file

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

from PIL import Image

# --- Các hàm setup_driver, login_facebook, open_fanpage (giữ nguyên) ---
def setup_driver():
    """Thiết lập và trả về đối tượng WebDriver."""
    selenium_profile_dir = r"C:\\selenium_profiles\\my_bot_profile"
    os.makedirs(selenium_profile_dir, exist_ok=True) 

    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument(f"--user-data-dir={selenium_profile_dir}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window() 
    return driver

def login_facebook(driver):
    """Đăng nhập vào Facebook."""
    driver.get("https://www.facebook.com/")
    print("Đang tải trang Facebook...")
    time.sleep(5) 

    try:
        email_field = driver.find_element(By.ID, "email")
        password_field = driver.find_element(By.ID, "pass")
        
        email_field.send_keys("your_facebook_email@example.com") 
        password_field.send_keys("your_facebook_password") 
        password_field.send_keys(Keys.RETURN) 
        print("Đang cố gắng đăng nhập...")
        time.sleep(10) 
        print("✅ Đã đăng nhập vào Facebook.")

    except Exception:
        print("Có vẻ như bạn đã đăng nhập trước đó (hoặc các trường đăng nhập không tìm thấy).")
        time.sleep(5) 
    
    if "facebook.com/home" in driver.current_url or "facebook.com/" == driver.current_url:
        print("Đã xác nhận đăng nhập thành công.")
    else:
        print("Không thể xác nhận đăng nhập thành công. Vui lòng kiểm tra lại thủ công.")

def open_fanpage(driver, page_url):
    """Mở fanpage cụ thể."""
    driver.get(page_url)
    print(f"Đang mở fanpage: {page_url}...")
    time.sleep(7) 
    print(f"✅ Đã mở fanpage: {page_url}")

def scroll_element_by_xpath_js(driver, xpath, scroll_amount="bottom", element_name="phần tử"):
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
            driver.execute_script(f"arguments[0].scrollTop += {scroll_amount};", target_element)
            print(f"Đã cuộn {element_name} xuống {scroll_amount} pixel.")
        else:
            print(f"Cảnh báo: Giá trị scroll_amount không hợp lệ: {scroll_amount}. Không cuộn.")
            return False

        time.sleep(2) 
        return True

    except Exception as e:
        print(f"❌ Đã xảy ra lỗi khi cố gắng cuộn {element_name} bằng JavaScript: {e}")
        return False

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
        
        max_scroll_attempts = 10 
        scroll_attempt = 0
        
        while scroll_attempt < max_scroll_attempts:
            try:
                button_element = WebDriverWait(driver, 5).until( 
                    EC.presence_of_element_located((By.XPATH, button_xpath))
                )
                print(f"Đã tìm thấy {button_name} sau cuộn/kiểm tra.")
                
                scroll_element_by_xpath_js(driver, button_xpath, "center", button_name)
                time.sleep(2) 

                clickable_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                
                clickable_button.click()
                print(f"✅ Đã nhấn vào {button_name} thành công.")
                time.sleep(3)
                return 

            except TimeoutException:
                print(f"Chưa tìm thấy {button_name}. Tiến hành cuộn vùng chứa...")
                
                if not scroll_element_by_xpath_js(driver, container_xpath, 1000, "vùng chứa cuộn"):
                    print("Không thể cuộn vùng chứa. Có thể XPATH sai hoặc không còn gì để cuộn.")
                    raise TimeoutException(f"Không tìm thấy '{button_name}' sau nhiều lần cuộn do vùng chứa không cuộn được.")
                
                scroll_attempt += 1
                if scroll_attempt == max_scroll_attempts:
                    print(f"❌ Lỗi: Đã đạt số lần cuộn tối đa ({max_scroll_attempts}), nhưng không tìm thấy '{button_name}'.")
                    raise TimeoutException(f"Không tìm thấy '{button_name}' sau nhiều lần cuộn.")
        
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

def like_post(driver, post_url=None):
    """
    Đi tới một bài post và nhấn nút Thích.
    Args:
        driver: Đối tượng WebDriver.
        post_url: URL trực tiếp của bài post (nếu bạn muốn đi thẳng đến nó).
                  Nếu None, sẽ giả định bạn đã ở trên trang có bài post.
    """
    if post_url:
        print(f"Đang truy cập bài post: {post_url}")
        driver.get(post_url)
        time.sleep(7) 

    print("Đang tìm nút 'Thích'...")
    
    like_button_xpaths = [
        "//div[@aria-label='Thích' and @role='button']",         
        "//div[@aria-label='Like' and @role='button']",           
        "//span[text()='Thích']/ancestor::div[@role='button']", 
        "//span[text()='Like']/ancestor::div[@role='button']",   
        "//div[@data-testid='UFI2ReactionLink/tooltip_placeholder']", 
        "//div[@data-testid='UFI2ReactionLink']"
    ]

    found_and_clicked = False
    for xpath in like_button_xpaths:
        try:
            print(f"Thử XPATH: {xpath}")
            like_button = WebDriverWait(driver, 15).until( 
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            
            like_button.click()
            print(f"✅ Đã nhấn nút 'Thích' thành công với XPATH: {xpath}")
            found_and_clicked = True
            break 
        except TimeoutException:
            print(f"❌ Nút 'Thích' không được tìm thấy với XPATH: {xpath}")
        except ElementClickInterceptedException:
            print(f"❌ Nút 'Thích' bị che khuất với XPATH: {xpath}. Thử click bằng JS.")
            driver.execute_script("arguments[0].click();", like_button) 
            print(f"✅ Đã thử nhấn nút 'Thích' bằng JavaScript.")
            found_and_clicked = True
            break
        except Exception as e:
            print(f"❌ Đã xảy ra lỗi khi cố gắng nhấn nút 'Thích' với XPATH {xpath}: {e}")
    
    if not found_and_clicked:
        print("❌ Không thể tìm thấy hoặc nhấn nút 'Thích' với bất kỳ XPATH nào đã thử.")
    
    time.sleep(3) 


# --- HÀM CHỤP MÀN HÌNH MỘT PHẦN (VẪN NHƯ CŨ, CHỈ THAY ĐỔI CÁCH GỌI) ---
def take_cropped_screenshot(driver, output_path, x, y, width, height):
    """
    Chụp ảnh màn hình toàn bộ trình duyệt và cắt ra một vùng cụ thể.
    Args:
        driver: Đối tượng WebDriver.
        output_path: Đường dẫn đầy đủ đến file ảnh sẽ lưu (ví dụ: "screenshots/cropped_area.png").
        x: Tọa độ X (ngang) của góc trên bên trái vùng muốn cắt.
        y: Tọa độ Y (dọc) của góc trên bên trái vùng muốn cắt.
        width: Chiều rộng của vùng muốn cắt.
        height: Chiều cao của vùng muốn cắt.
    """
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

# --- Logic chính của script ---
if __name__ == "__main__":
    driver = None
    try:
        driver = setup_driver()
        login_facebook(driver)

        # Mở một trang web để chụp ảnh
        driver.get("https://www.google.com") 
        print("Đã mở Google.com để chụp ảnh.")
        time.sleep(3) 

        print("\n--- Đang thực hiện chụp màn hình một phần với tên tùy chỉnh ---")
        
        # 1. Xác định tọa độ và kích thước
        crop_x = 310   
        crop_y = 260    
        crop_width = 740 
        crop_height = 80
        
        # 2. Định nghĩa thư mục lưu ảnh (nếu muốn)
        screenshot_dir = "D:\project\bot_tt_facebook\output"
        # Tạo thư mục nếu chưa có
        os.makedirs(screenshot_dir, exist_ok=True)
        
        # Ví dụ 3: Truyền một tên file theo ngữ cảnh
        action_name = "after_login"
        file_name_context = f"screenshot_{action_name}.png"
        output_path_context = os.path.join(screenshot_dir, file_name_context)
        take_cropped_screenshot(driver, output_path_context, 0, 0, 500, 400) # Chụp một vùng khác

        input("\nNhấn Enter để đóng trình duyệt...") 

    except Exception as e:
        print(f"Đã xảy ra lỗi tổng quát: {e}")
    finally:
        if driver:
            driver.quit()
            print("Đã đóng trình duyệt.")