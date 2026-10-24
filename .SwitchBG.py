import os
import shutil
import tkinter as tk
from tkinter import filedialog

def replace_background():
    
    root = tk.Tk()
    root.withdraw()  

    target_file = ".[System_UI]/.{Background}.jpg"

    print("Открывается окно выбора файла...")
    new_file = filedialog.askopenfilename(
        title="[▒] Switch background SHINKOR OS table:",
        
        filetypes=[
            ("JPEG изображения", "*.jpg"),
            ("JPEG изображения", "*.jpeg"),
            ("PNG изображения", "*.png"),
            ("WebP изображения", "*.webp"),
            ("ICO иконки", "*.ico"),
            ("Все поддерживаемые форматы", "*.jpg *.jpeg *.png *.webp *.ico и др.")
        ],
        initialdir=".[System_UI]/Walpaper"  
    )

    if not new_file:
        print("Процес замены обоев прекрашён.")
        root.destroy()
        return

   
    if not os.path.isfile(new_file):
        print("ERROR: Обои не найдены!")
        root.destroy()
        return

    
    ext = os.path.splitext(new_file)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.ico', '.bmp', '.tif', '.tiff', '.dib', '.jfif', '.gif']:
        print("ERROR: Такой формат пока что не поддерживается!")
        root.destroy()
        return

    try:
    
        if os.path.exists(target_file):
            os.remove(target_file)
            print(f"Старые обои убраны: {target_file}")

   
        shutil.copy2(new_file, target_file)
        print(f"Новые обои установлены: {target_file}")

    except Exception as e:
        print(f"Ошибка при замене обоев: {e}")

  
    root.destroy()

if __name__ == "__main__":
    replace_background()
