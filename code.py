import os
import re

def replace_in_filename_and_content(root_dir, old_word, new_word):
    root_dir_name = os.path.basename(root_dir)
    if old_word.lower() in root_dir_name.lower():
        new_root_dir = root_dir.replace(old_word, new_word)
        os.rename(root_dir, new_root_dir)
        root_dir = new_root_dir

    for root, dirs, files in os.walk(root_dir, topdown=False):
        for filename in files:
            filepath = os.path.join(root, filename)
            
            new_filename = re.sub(
                re.compile(re.escape(old_word), re.IGNORECASE), 
                new_word, 
                filename
            )
            if new_filename != filename:
                new_filepath = os.path.join(root, new_filename)
                os.rename(filepath, new_filepath)
                filepath = new_filepath
            
            try:
                with open(filepath, 'rb') as file:
                    content = file.read().decode('utf-8', errors='ignore')
                
                new_content = re.sub(
                    re.compile(re.escape(old_word), re.IGNORECASE), 
                    new_word, 
                    content
                )
                
                if new_content != content:
                    with open(filepath, 'wb') as file:
                        file.write(new_content.encode('utf-8'))
            except Exception as e:
                print(f"⚠️ Ошибка при обработке {filepath}: {e}")
        
        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            new_dirname = re.sub(
                re.compile(re.escape(old_word), re.IGNORECASE), 
                new_word, 
                dirname
            )
            if new_dirname != dirname:
                new_dirpath = os.path.join(root, new_dirname)
                os.rename(dirpath, new_dirpath)

def main():
    print("=== Gret v_1.0 dev. by svairwizard ===")
    folder_path = input("Путь к папке проекта: ").strip('"').strip()
    old_word = input("Какое слово заменяем?: ").strip()
    new_word = input("На какое слово меняем?: ").strip()

    if not os.path.exists(folder_path):
        print("Ошибка: папка не существует!")
        return
    
    print("\nНачинаем замену...")
    replace_in_filename_and_content(folder_path, old_word, new_word)
    print("Готово! Все файлы и папки обновлены.")

if __name__ == "__main__":
    main()
