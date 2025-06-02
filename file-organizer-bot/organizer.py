from pathlib import Path
import shutil
from file_types import FILE_TYPES

def organize_folder(folder_path):
    folder = Path(folder_path)
    if not folder.exists():
        return f"❌ โฟลเดอร์ {folder} ไม่พบ"

    logs = []
    for file in folder.iterdir():
        if file.is_file():
            ext = file.suffix.lower()
            moved = False
            for category, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_folder = folder / category
                    target_folder.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_folder / file.name))
                    logs.append(f"✔️ ย้าย {file.name} ไป {category}")
                    moved = True
                    break
            if not moved:
                target_folder = folder / "Others"
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(target_folder / file.name))
                logs.append(f"📦 ย้าย {file.name} ไป Others")
    return logs
