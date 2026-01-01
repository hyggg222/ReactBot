import os
import shutil
from pathlib import Path

# Mapping of file/folder name -> destination path (relative to root)
MIGRATION_MAP = {
    "server.py": "src/python/api/server.py",
    "bot_code_main.py": "src/python/core/bot.py",
    "main.js": "src/main/main.js",
    "pages": "src/renderer/pages",
    "input.txt": "resources/input.txt",
    "bot_facebook.bat": "scripts/bot_facebook.bat",
    "test.py": "tests/test.py",
    "test2.py": "tests/test2.py",
    "main.py": "src/python/legacy/main.py", # Moving other python files to clarify root
     # Keeping package.json, node_modules in root
}

# Directories to create (ensure they exist even if empty)
DIRS_TO_CREATE = [
    "src/python/api",
    "src/python/core",
    "src/python/utils",
    "src/main",
    "src/renderer",
    "resources/profiles", # Ensure profile dir exists
    "resources/drivers",  # Ensure drivers dir exists
    "scripts",
    "tests",
    "output"
]

# INIT files to create for Python modules
INIT_FILES = [
    "src/python/__init__.py",
    "src/python/api/__init__.py",
    "src/python/core/__init__.py",
    "src/python/utils/__init__.py",
]

def migrate():
    root_dir = Path.cwd()
    print(f"🚀 Starting migration in: {root_dir}")

    # 1. Create Directory Tree
    print("\n[1/4] Creating directory structure...")
    for dir_path in DIRS_TO_CREATE:
        full_path = root_dir / dir_path
        if not full_path.exists():
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"  + Created: {dir_path}")
        else:
            print(f"  . Exists: {dir_path}")

    # 2. Move Files
    print("\n[2/4] Moving files...")
    for src_name, dest_rel_path in MIGRATION_MAP.items():
        src_path = root_dir / src_name
        dest_path = root_dir / dest_rel_path

        if src_path.exists():
            # Create parent dir for destination if it doesn't exist (double check)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.move(str(src_path), str(dest_path))
                print(f"  ✅ Moved: {src_name} -> {dest_rel_path}")
            except Exception as e:
                print(f"  ❌ Failed to move {src_name}: {e}")
        else:
            print(f"  ⚠️ Source not found: {src_name} (Skipping)")

    # 3. Create __init__.py files
    print("\n[3/4] Creating __init__.py files...")
    for init_rel_path in INIT_FILES:
        init_path = root_dir / init_rel_path
        if not init_path.exists():
            init_path.touch()
            print(f"  + Created: {init_rel_path}")
        else:
            print(f"  . Exists: {init_rel_path}")

    # 4. Cleanup (Optional - manual check recommended)
    print("\n[4/4] Migration Complete!")
    print("\nNOTE: Please check the 'src' folder and verify file locations.")
    print("      'node_modules', '.next', and 'package.json' remain in the root.")

if __name__ == "__main__":
    migrate()
