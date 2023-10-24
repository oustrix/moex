#!/bin/bash

# Создание уникального ID в формате dd.mm.yyyy
id=$(date +'%d.%m.%Y')

# Создание папки с названием id
mkdir $id

# Клонирование нужного репозитория в папку id
git clone https://github.com/heroku/node-js-getting-started.git $id

# Добавление Dockefile в папку к исходному коду
cp 1_Dockerfile ./$id/Dockerfile

# Переход в папку склонированного репозитория
cd $id

# Билд
docker build -t node-app:$id .

# Запуск созданного image в режиме сервиса, прокидывая порт 5001 (см. index.js)
docker run -d -p 5001:5001 node-app:$id