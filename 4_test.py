import argparse
import time
import requests
import psycopg2

appURL = "http://localhost:3000"
esURL = "http://localhost:9200"

pgHost = "localhost"
pgPort = 5432
pgUser = "postgres"


def check_app():
    try:
        res = requests.get(appURL) # отправляем запрос приложению
        res.raise_for_status() # выкидываем исключение, если статус ответа >=400
        print(f'Node App is OK. Status: {res.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error while checking Node App: {e}')


def check_postgres():
    # попытка установления соединения с бд
    try:
        conn = psycopg2.connect(
            host=pgHost,
            user=pgUser,
            port=pgPort,
        )
        # закрытие соединения, т.к. само по себе оно нам не нужно. Если бы база была недоступна,
        # то уже было бы выкинуто исключение
        conn.close()
        print('PostgreSQL is OK')

    except psycopg2.OperationalError as e:
        print(f'Error while checking PostgreSQL: {e}')


def check_elasticsearch():
    try:
        res = requests.get(esURL) # отправляем запрос эластику
        res.raise_for_status()  # выкидываем исключение, если статус ответа >=400
        print(f"Elasticsearch is OK. Status: {res.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error while checking Elasticsearch: {e}")


def test(args):
    # бесконечный прогон тестов с заданным интервалом
    while True:
        check_app()
        check_postgres()
        check_elasticsearch()

        time.sleep(args.interval)



if __name__ == '__main__':
    # Создание парсера аргументов командной строки
    parser = argparse.ArgumentParser()
    # Добавление аргумента interval, который будет использоваться для задержки между наборами проверок
    parser.add_argument("-i", "--interval",type=int, default=60, help="Интервал проверки (по умолчанию - 60) в секундах")

    test(parser.parse_args())
