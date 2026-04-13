import os
import sys
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def encrypt_file(input_file, output_file):
    # 1. Генерируем ключ 32 байта для AES-256 и IV (вектор инициализации) 16 байт
    key = os.urandom(32)
    iv = os.urandom(16)

    # 2. Читаем данные из нашего CSV
    with open(input_file, 'rb') as f:
        data = f.read()

    # 3. AES требует, чтобы длина данных делилась на размер блока (128 бит / 16 байт)
    # Поэтому добавляем паддинг (дополнение) по стандарту PKCS7
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()

    # 4. Настраиваем шифратор (AES-256, режим CBC)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 5. Шифруем данные
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # 6. Сохраняем IV вместе с зашифрованными данными 
    # (IV нужен для расшифровки, прятать его не обязательно)
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

    print(f"Файл '{input_file}' успешно зашифрован и сохранен как '{output_file}'")
    print(f"Секретный ключ {key.hex()}")

if __name__ == "__main__":
    # Убедись, что файл grades.csv лежит в той же папке
    try:
        encrypt_file('grades.csv', 'grades.enc')
    except FileNotFoundError:
        print("Ошибка: файл grades.csv не найден! Создай его перед запуском.")