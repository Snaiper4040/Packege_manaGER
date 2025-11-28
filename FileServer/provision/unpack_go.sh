#!/bin/bash

# Определяем имя файла и целевую директорию
TAR_FILE="go1.25.0.linux-amd64.tar.gz"
TARGET_DIR="go"

cd /vagrant

# Проверяем, существует ли файл
if [ ! -f "$TAR_FILE" ]; then
    echo "Ошибка: Файл '$TAR_FILE' не найден."
    exit 1
fi

# Распаковываем архив в целевую директорию
tar -xzf "$TAR_FILE" -C "$TARGET_DIR"

# Проверяем успешность операции
if [ $? -eq 0 ]; then
    echo "Файл '$TAR_FILE' успешно распакован в директорию '$TARGET_DIR'."
else
    echo "Ошибка при распаковке файла '$TAR_FILE'."
    exit 1
fi