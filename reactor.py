import requests
import json
import os

BASE_URL = "https://mephi.opentoshi.net/api/v1"
TEAM_FILE = 'team_id.txt'

def print_result(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))

def send_request(method, url, params=None):
    try:
        response = requests.request(method, BASE_URL + url, params=params, timeout=10)
        return response.json()
    except:
        return {"error": "Ошибка запроса"}

def save_team_id(team_id):
    with open(TEAM_FILE, 'w') as f:
        f.write(team_id)

def load_team_id():
    if os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, "r") as f:
            return f.read().strip()
    return None

def get_team_id():
    team_id = load_team_id()

    if team_id:
        return team_id

    while True:
        team_id = input("Введите team_id:").strip()
        if team_id:
            save_team_id(team_id)
            return team_id
        print("team_id не должен быть пустым")

def get_number(text, default, min_value, max_value, num_type=float):
    while True:
        value = input(f"{text} [{default}]:").strip()
        if value == "":
            return num_type(default)

        try:
            value = num_type(value)
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Введите число от {min_value} до {max_value}")
        except:
            print("Неверный ввод")

def register_team():
    result = send_request("GET","/team/register")
    print_result(result)

    if "team_id" in result:
        save_team_id(result["team_id"])
        print("team_id сохранён")

def create_reactor():
    team_id = get_team_id()
    result = send_request("POST","/reactor/create_reactor",{"team_id":team_id})
    print_result(result)

def get_data():
    team_id = get_team_id()
    result = send_request("GET","/reactor/data", {"team_id": team_id})
    print_result(result)

def get_history():
    team_id = get_team_id()
    limit = get_number("Введите лимит", 100, 1, 200, int)
    result = send_request("GET","/reactor/history",{"team_id":team_id,"limit": limit})
    print_result(result)

def add_water():
    team_id = get_team_id()
    amount = get_number("Введите количество воды", 20,0.1, 30)
    result = send_request("POST","/reactor/refill-water", {"team_id": team_id, "amount": amount})
    print_result(result)

def cooling():
    team_id = get_team_id()
    duration = get_number("Введите длительность охлаждения", 5, 1, 30, int)
    result = send_request("POST","/reactor/activate-cooling", {"team_id": team_id, "duration": duration})
    print(result)

def change_speed():
    team_id = get_team_id()
    speed = get_number("Введите скорость", 1, 1, 20)
    result = send_request("POST", "/reactor/set-speed",{"team_id":team_id,"speed": speed})
    print_result(result)

def stop_reactor():
    team_id = get_team_id()
    result = send_request("POST","/reactor/emergency-shutdown",{"team_id": team_id})
    print_result(result)

def reset_reactor():
    team_id = get_team_id()
    result = send_request("POST","/reactor/reset_reactor", {"team_id": team_id})
    print_result(result)

def show_menu():
    print("\n1 - Зарегистрировать команду")
    print("2 - Создать реактор")
    print("3 - Получить данные реактора")
    print("4 - Посмотреть историю")
    print("5 - Долить воду")
    print("6 - Включить охлаждение")
    print("7 - Изменить скорость")
    print("8 - Аварийная остановка")
    print("9 - Сбросить реактор")
    print("0 - Выход")

def main():
    while True:
        show_menu()
        choice = input("Выберите действие:").strip()

        if choice == "1":
            register_team()
        elif choice == "2":
            create_reactor()
        elif choice == "3":
            get_data()
        elif choice == "4":
            get_history()
        elif choice == "5":
            add_water()
        elif choice == "6":
            cooling()
        elif choice == "7":
            change_speed()
        elif choice == "8":
            stop_reactor()
        elif choice == "9":
            reset_reactor()
        elif choice == "0":
            print("Выход из программы")
            break
        else:
            print("Такого пункта нет")

main()
