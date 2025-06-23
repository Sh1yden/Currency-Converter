from pathlib import Path
import requests
import json

# Константы
# Путь к файлу с API ключами. Изменить на свой.
API_DIR = Path("c:/Users/Shayden/Documents/GitHub/_secret_api_keys/api_keys.json")
# Константы директорий.
SAVE_DIR = Path("save/rates")
SAVE_FILE = SAVE_DIR / "save_rates.json"
# URL api запроса курсов валют.
URL = "https://api.freecurrencyapi.com/v1/latest?apikey="


class CurrencyConverter:
    """
    Класс для конвертации валюты.
    """

    # Конструктор класса.
    def __init__(self):
        # Инициализация API ключа.
        self.api_key = self._get_api_key()
        # URL запроса с ключом.
        self.URL = URL + str(self.api_key)
        self.rates = {"data": {}}
        self._initialize_files()

    def _get_api_key(self):
        """
        Получение API ключа из файла.
        Возвращение API ключа.
        """
        try:
            with open(API_DIR, "r") as f:
                data = json.load(f)
                return data["free_currency_api"]
        except Exception as e:
            print(f"Ошибка при чтении API-ключа: {e}")

    def _get_rates(self):
        """
        Получение курсов валют.
        Возвращение курсов валют.
        """
        try:
            response = requests.get(self.URL)
            return response.json()
        except Exception as e:
            print(f"Ошибка при получении курсов валют: {e}")

    def _initialize_files(self):
        """
        Инициализация директорий и файлов.
        """
        try:
            # Создаём директорию
            SAVE_DIR.mkdir(parents=True, exist_ok=True)
            # Если файла нет, создаём новый.
            if not SAVE_FILE.exists():
                self._save_to_file()
        except Exception as e:
            print(f"Ошибка при инициализации: {e}")

    def _load_from_file(self):
        """
        Загрузка курсов валют из файла.
        Возвращение курсов валют.
        """
        try:
            with open(SAVE_FILE, "r") as f:
                self.rates = json.load(f)
        except Exception as e:
            print(f"Ошибка при загрузке из файла: {e}")

    def _save_to_file(self):
        """
        Сохранение курсов валют в файл.
        Для экономии квоты запросов к API.
        """
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump(self._get_rates(), f, indent=2)
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")

    def convert(self):
        try:
            print("\nConvert Menu:")
            print("1. Show All Currencies")
            print("2. Convert Currency")
            print("3. Exit")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                self._load_from_file()

                print("Available Currencies:")
                for key, value in self.rates["data"].items():
                    print(f"{key}: {value}")
                print("All currencies displayed successfully.")
            elif choice == "2":
                target = float(input("Enter the amount of the target currency: "))
                usd_amount = target / self.rates["data"][str(input("from: ").upper())]

                result = usd_amount * self.rates["data"][str(input("to: ").upper())]
                print(result)
                pass
            elif choice == "3":
                exit()
            else:
                print("Invalid choice. Please try again.")
                return
        except Exception as e:
            print(f"Ошибка при конвертации: {e}")


def main():
    converter = CurrencyConverter()

    print(type(converter._load_from_file()))
    while True:
        print("\n" + "=" * 30)
        print("CURRENCY CONVERTER IN TERMINAL")
        print("=" * 30)
        print("Currency Converter Menu:")
        print("1. Convert Currency")
        print("2. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            converter.convert()
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
