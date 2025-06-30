import os
import re
import shutil

def should_skip_path(path):
    """Проверяет, нужно ли пропустить папку из-за наличия 'microsoft' в пути"""
    path_parts = path.lower().split(os.sep)
    return any('microsoft' in part for part in path_parts)

def delete_unnecessary_folders(root_dir):
    folders_to_delete = ['.vs', 'build']
    for root, dirs, _ in os.walk(root_dir):
        # Удаляем папки из списка dirs, чтобы os.walk их не обрабатывал
        dirs[:] = [d for d in dirs if not should_skip_path(os.path.join(root, d))]
        
        for dirname in dirs:
            if dirname.lower() in folders_to_delete:
                dirpath = os.path.join(root, dirname)
                try:
                    if not should_skip_path(dirpath):
                        shutil.rmtree(dirpath)
                        print(f"🗑️ Удалена папка: {dirpath}")
                except Exception as e:
                    print(f"⚠️ Ошибка при удалении {dirpath}: {e}")

def replace_in_filename_and_content(root_dir, old_word, new_word):
    if should_skip_path(root_dir):
        print(f"⏩ Пропускаем папку (содержит Microsoft): {root_dir}")
        return

    root_dir_name = os.path.basename(root_dir)
    if old_word.lower() in root_dir_name.lower():
        new_root_dir = root_dir.replace(old_word, new_word)
        os.rename(root_dir, new_root_dir)
        root_dir = new_root_dir

    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Фильтруем папки, которые нужно пропустить
        dirs[:] = [d for d in dirs if not should_skip_path(os.path.join(root, d))]
        
        for filename in files:
            filepath = os.path.join(root, filename)
            
            if should_skip_path(filepath):
                print(f"⏩ Пропускаем файл (содержит Microsoft): {filepath}")
                continue
                
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
            
            if should_skip_path(dirpath):
                continue
                
            new_dirname = re.sub(
                re.compile(re.escape(old_word), re.IGNORECASE), 
                new_word, 
                dirname
            )
            if new_dirname != dirname:
                new_dirpath = os.path.join(root, new_dirname)
                os.rename(dirpath, new_dirpath)

def main():
    print("=== Gret v_1.2 dev. by svairwizard ===")
    folder_path = input("Путь к папке проекта: ").strip('"').strip()
    old_word = input("Какое слово заменяем?: ").strip()
    new_word = input("На какое слово меняем?: ").strip()

    if not os.path.exists(folder_path):
        print("Ошибка: папка не существует!")
        return
    
    print("\nУдаление ненужных папок (.vs, build)...")
    delete_unnecessary_folders(folder_path)
    
    print("\nНачинаем замену...")
    replace_in_filename_and_content(folder_path, old_word, new_word)
    print("\nГотово! Все файлы и папки обновлены, ненужные папки удалены.")

if __name__ == "__main__":
    main()
