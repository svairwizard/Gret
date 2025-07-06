import os
import re
import shutil
import sys

# Папки, которые нужно удалять (если они не внутри "неприкосновенных" папок)
FOLDERS_TO_DELETE = {'.vs', 'build', 'bin', 'x64'}

# "Неприкосновенные" папки, которые нельзя изменять
PROTECTED_FOLDERS = {'packages'}

# Расширения файлов, в которых нужно производить замену
REPLACE_IN_EXTENSIONS = {'.sln', '.hpp', '.cpp', '.h', '.c', '.vcxproj', '.txt', '.md'}

def should_process_path(path):
    """Проверяет, можно ли обрабатывать путь (не находится ли он в защищенной папке)"""
    parts = os.path.normpath(path).split(os.sep)
    return not any(protected in parts for protected in PROTECTED_FOLDERS)

def should_delete_folder(folder_name):
    """Проверяет, нужно ли удалять папку по её имени"""
    return folder_name.lower() in {f.lower() for f in FOLDERS_TO_DELETE}

def process_file(file_path, word1, word2):
    """Обрабатывает файл: заменяет word1 на word2 в его содержимом"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Используем регулярное выражение для замены без учета регистра
        pattern = re.compile(re.escape(word1), re.IGNORECASE)
        new_content = pattern.sub(word2, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(new_content)
            print(f"Изменено содержимое файла: {file_path}")
            return True
    except Exception as e:
        print(f"Ошибка при обработке файла {file_path}: {e}")
    return False

def rename_path(old_path, word1, word2):
    """Переименовывает путь (файл или папку), заменяя word1 на word2 в названии"""
    dirname, basename = os.path.split(old_path)
    
    # Заменяем word1 на word2 в имени файла/папки без учета регистра
    pattern = re.compile(re.escape(word1), re.IGNORECASE)
    new_basename = pattern.sub(word2, basename)
    
    if new_basename != basename:
        new_path = os.path.join(dirname, new_basename)
        try:
            os.rename(old_path, new_path)
            print(f"Переименовано: {old_path} -> {new_path}")
            return new_path
        except Exception as e:
            print(f"Ошибка при переименовании {old_path}: {e}")
    return old_path

def process_directory(root_dir, word1, word2):
    """Рекурсивно обрабатывает директорию, выполняя все необходимые замены"""
    # Сначала обрабатываем файлы и подпапки
    for root, dirs, files in os.walk(root_dir, topdown=False):
        # Проверяем, нужно ли обрабатывать эту папку
        if not should_process_path(root):
            continue
        
        # Обрабатываем файлы
        for file in files:
            file_path = os.path.join(root, file)
            if should_process_path(file_path):
                # Проверяем расширение файла
                ext = os.path.splitext(file)[1].lower()
                if ext in REPLACE_IN_EXTENSIONS:
                    process_file(file_path, word1, word2)
                # Переименовываем файл, если нужно
                rename_path(file_path, word1, word2)
        
        # Обрабатываем подпапки
        for dir_name in list(dirs):  # Используем list() для копирования, так как мы модифицируем dirs
            dir_path = os.path.join(root, dir_name)
            
            # Проверяем, нужно ли удалять эту папку
            if should_delete_folder(dir_name) and should_process_path(dir_path):
                try:
                    shutil.rmtree(dir_path)
                    print(f"Удалена папка: {dir_path}")
                    dirs.remove(dir_name)  # Удаляем из списка для обработки, чтобы os.walk не пытался войти
                except Exception as e:
                    print(f"Ошибка при удалении папки {dir_path}: {e}")
            else:
                # Переименовываем папку, если нужно
                new_path = rename_path(dir_path, word1, word2)
                if new_path != dir_path:
                    # Обновляем список dirs, если папка была переименована
                    idx = dirs.index(dir_name)
                    dirs[idx] = os.path.basename(new_path)
    
    # Переименовываем корневую папку, если нужно
    if should_process_path(root_dir):
        rename_path(root_dir, word1, word2)

def main():
    if len(sys.argv) != 4:
        print("Использование: python code.py <путь_до_папки> <слово1> <слово2>")
        sys.exit(1)
    
    root_dir = sys.argv[1]
    word1 = sys.argv[2]
    word2 = sys.argv[3]
    
    if not os.path.isdir(root_dir):
        print(f"Ошибка: {root_dir} не является папкой или не существует")
        sys.exit(1)
    
    print(f"Начало обработки папки: {root_dir}")
    print(f"Замена '{word1}' на '{word2}'")
    
    process_directory(root_dir, word1, word2)
    
    print("Обработка завершена")

if __name__ == "__main__":
    main()
