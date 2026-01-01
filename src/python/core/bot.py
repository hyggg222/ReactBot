import os
import time
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from PIL import Image

# Import settings from the new config module
from src.python.utils.config import settings

class FacebookBot:
    """
    Refactored Facebook Automation Bot.
    Uses Dependency Injection for paths and configuration.
    """
    def __init__(self, profile_id: str = "default_profile", headless: bool = False):
        self.profile_id = profile_id
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.profile_path = settings.get_profile_path(profile_id)
        
    def _initialize_driver(self):
        """Initializes the Selenium WebDriver with correct profile and options."""
        print(f"🚀 Initializing Bot with profile: {self.profile_id}")
        
        # Ensure profile directory exists
        if not self.profile_path.exists():
            self.profile_path.mkdir(parents=True, exist_ok=True)

        options = Options()
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")
        # Use centralized path for user data
        options.add_argument(f"--user-data-dir={self.profile_path.resolve()}")
        
        if self.headless:
            options.add_argument("--headless")

        # Use webdriver_manager or custom driver path if configured
        driver_path = settings.get_driver_path()
        if driver_path:
            service = Service(executable_path=str(driver_path))
        else:
            service = Service(ChromeDriverManager().install())
            
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def start(self):
        """Starts the browser session."""
        if not self.driver:
            self._initialize_driver()
        
    def stop(self):
        """Closes the browser session."""
        if self.driver:
            print("🛑 Stopping Bot...")
            self.driver.quit()
            self.driver = None

    def login_facebook(self):
        """Simple check to ensure we are on Facebook."""
        if not self.driver: raise RuntimeError("Driver not initialized")
        self.driver.get("https://www.facebook.com/")
        time.sleep(2) # Wait for page load
        print("✅ Opened Facebook home.")

    def open_fanpage(self, page_url: str):
        if not self.driver: raise RuntimeError("Driver not initialized")
        print(f"🎬 Opening fanpage: {page_url}")
        try:
            self.driver.get(page_url)
            time.sleep(2)
            print(f"✅ Fanpage opened.")
        except Exception as e:
            print(f"❌ Error opening fanpage: {e}")

    def like_post(self, post_url: str):
        if not self.driver: raise RuntimeError("Driver not initialized")
        self.driver.get(post_url)
        time.sleep(2)
        try:
            # More robust like button finder could be implemented here
            like_button = self.driver.find_element(By.XPATH, "//div[@aria-label='Like']")
            like_button.click()
            print(f"✅ Liked post: {post_url}")
        except Exception as e:
            print(f"⚠️ Could not like post {post_url}: {e}")

    def like_page(self, page_url: str):
         # Logic from original like_page
        self.open_fanpage(page_url)
        time.sleep(2)
        try:
            # Example XPath from original code
            # Note: This is brittle and might need updating if FB changes
            xpath = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[4]/div/div/div[1]/div/div/div/div[1]"
            self._click_button(xpath, "Like Page Button")
            print("✅ Liked Fanpage!")
        except Exception as e:
            print(f"⚠️ Could not like page {page_url}: {e}")

    def switch_profile(self, target_url: str):
        """Logic for switching profiles (if applicable)."""
        # Refactored from 'switch_own_fanpage'
        # This seems to be specific logic for the user's workflow
        try:
            self.open_fanpage(target_url)
            # Switch account buttons (Old XPaths preserved but wrapped)
            self._click_button("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[4]/div/div[1]/span/div/div/div[1]/div[2]/div[1]/div/div/div/span", "Switch Account 1")
            time.sleep(1)
            self._click_button("/html/body/div[1]/div/div[1]/div/div[4]/div/div[1]/div[1]/div/div[2]/div/div/div/div/div/div/div[3]/div/div/div/div/div[1]/div/div/div[1]/div/span/span", "Switch Account Confirm")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error switching profile: {e}")

    def capture_screenshot(self, output_path: str, x=0, y=0, width=1920, height=1080):
        """Captures and crops screenshot."""
        if not self.driver: raise RuntimeError("Driver not initialized")
        
        # Ensure output dir uses Settings if relative
        out_file = Path(output_path)
        if not out_file.is_absolute():
            out_file = settings.OUTPUT_DIR / output_path
            
        if not out_file.parent.exists():
            out_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            temp = "temp_full.png"
            self.driver.save_screenshot(temp)
            img = Image.open(temp)
            cropped = img.crop((x, y, x + width, y + height))
            cropped.save(out_file)
            print(f"📸 Screenshot saved to {out_file}")
            os.remove(temp)
            return str(out_file)
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

    # --- Internal Helpers ---
    def _click_button(self, xpath: str, name: str = "Button"):
        """Helper to find and click an element."""
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            print(f"✅ Clicked: {name}")
        except Exception as e:
            print(f"❌ Failed to click {name}: {e}")
            raise

    # --- Main Execution Task ---
    def run_task(self, task_type: str, params: dict):
        """
        Unified entry point for API to trigger tasks.
        """
        self.start()
        try:
            if task_type == "like_post":
                self.like_post(params.get("url"))
            elif task_type == "like_page":
                self.like_page(params.get("url"))
            elif task_type == "full_flow":
                # Replicates the original 'run_facebook_bot' loop logic
                # using the new class methods
                fanpage_link = params.get("fanpage_link")
                post_links = params.get("post_links", [])
                
                self.login_facebook()
                if fanpage_link:
                    self.like_page(fanpage_link)
                
                for post in post_links:
                    self.like_post(post)
                    
            print(f"Task {task_type} completed.")
        except Exception as e:
            print(f"Task failed: {e}")
        finally:
             if params.get("close_after", True):
                 self.stop()

if __name__ == "__main__":
    # Test run
    bot = FacebookBot(profile_id="test_profile")
    bot.start()
    bot.login_facebook()
    bot.stop()
