import os
import tarfile
import sys

def create_pger_package(folder_path, output_name):
    """Создает пакет в формате .pger из указанной папки и сохраняет его в /repository/packages/.
    
    Args:
        folder_path (str): Путь к папке, которую нужно заархивировать.
        output_name (str): Имя выходного файла (без расширения).
        
    Returns:
        bool: True, если пакет успешно создан, иначе False.
    """
    # Путь к директории, где будут храниться пакеты
    output_directory = "/repository/packages/"
    
    # Создаем директорию, если она не существует
    os.makedirs(output_directory, exist_ok=True)

    # Полный путь к выходному файлу
    pger_name = os.path.join(output_directory, f"{output_name}.pger")
    
    if not os.path.exists(folder_path):
        print(f"Ошибка: Папка '{folder_path}' не найдена.")
        return False

    # Создаем tar.gz архив
    with tarfile.open(pger_name, 'w:gz') as pger_tar:
        pger_tar.add(folder_path, arcname=os.path.basename(folder_path))
    
    print(f"Пакет успешно создан: {pger_name}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:  # Проверяем, что передано 2 аргумента + имя скрипта
        print("Использование: python create_pger.py <путь_к_папке> <имя_пакета>")
    else:
        folder_path = sys.argv[1]
        output_name = sys.argv[2]
        create_pger_package(folder_path, output_name)
