import sys
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configuration settings.
    Automatically reads from environment variables if set.
    """
    
    # Base Paths
    APP_ROOT: Path = Path(__file__).resolve().parent.parent.parent.parent
    
    @property
    def RESOURCES_DIR(self) -> Path:
        return self.APP_ROOT / "resources"
        
    @property
    def PROFILES_DIR(self) -> Path:
        return self.RESOURCES_DIR / "profiles"
        
    @property
    def DRIVERS_DIR(self) -> Path:
        return self.RESOURCES_DIR / "drivers"
        
    @property
    def OUTPUT_DIR(self) -> Path:
        return self.APP_ROOT / "output"

    def get_profile_path(self, profile_name: str) -> Path:
        """Returns the absolute path to a specific user profile."""
        return self.PROFILES_DIR / profile_name
        
    def get_driver_path(self) -> Optional[Path]:
        """
        Returns the path to the chromedriver executable.
        Can be extended to detect OS and return appropriate driver.
        """
        # Example for Windows, can be made dynamic
        driver_path = self.DRIVERS_DIR / "chromedriver.exe"
        if driver_path.exists():
            return driver_path
        return None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Singleton instance
settings = Settings()

if __name__ == "__main__":
    print(f"App Root: {settings.APP_ROOT}")
    print(f"Resources: {settings.RESOURCES_DIR}")
    print(f"Profiles: {settings.PROFILES_DIR}")
