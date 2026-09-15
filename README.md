DataWar — Customer Analytics Dashboard

Интерактивный дашборд для анализа клиентских данных.

Проект загружает данные о клиентах в MongoDB и отображает их в виде KPI, фильтров, графиков и таблицы с помощью Streamlit.

Возможности

* 📊 количество клиентов и основные показатели;
* 👤 средний возраст клиентов;
* 💰 средний и суммарный CAC;
* 🌍 анализ клиентов по странам и регионам;
* 👥 распределение по сегментам и полу;
* 📈 графики по возрасту и CAC;
* 🔎 фильтрация данных;
* 📋 просмотр таблицы клиентов.

Стек

* Python
* Streamlit — интерфейс дашборда
* MongoDB — хранение данных
* Docker — запуск MongoDB
* Pandas — обработка данных

Структура проекта

DataWar/
├── app.py                 # Streamlit-приложение
├── load_to_mongo.py       # загрузка CSV в MongoDB
├── customer_master.csv    # исходный датасет
├── requirements.txt       # зависимости Python
├── README.md
└── .gitignore

Как запустить

1. Клонировать репозиторий

git clone https://github.com/DimaKuzin05/DataWar.git
cd DataWar

2. Установить зависимости

Рекомендуется использовать виртуальное окружение:

python3 -m venv .venv
source .venv/bin/activate

Установить зависимости:

pip install -r requirements.txt

3. Запустить MongoDB

MongoDB используется в Docker-контейнере.

Если контейнер уже создан:

docker start customer-mongo

Если контейнера ещё нет:

docker run -d \
  --name customer-mongo \
  -p 27017:27017 \
  mongo

4. Загрузить данные

python3 load_to_mongo.py

Скрипт загружает данные из customer_master.csv в MongoDB.

По умолчанию используются:

MongoDB:    mongodb://localhost:27017
Database:   dataset_zalupa
Collection: customers

5. Запустить дашборд

python3 -m streamlit run app.py

После запуска приложение будет доступно по адресу:

http://localhost:8501

Настройка MongoDB

Параметры подключения можно изменить через переменные окружения:

export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB="dataset_zalupa"
export MONGO_COLLECTION="customers"

После этого запустить приложение:

python3 -m streamlit run app.py

Дашборд

Основная информация отображается в виде:

* KPI-карточек;
* фильтров;
* графиков;
* таблицы клиентов.

Фильтры позволяют изменять отображаемые данные по стране, сегменту, региону, полу и возрасту.

Архитектура

customer_master.csv
        │
        ▼
load_to_mongo.py
        │
        ▼
     MongoDB
        │
        ▼
      app.py
        │
        ▼
    Streamlit
        │
        ▼
  Web Dashboard

Используемые технологии

Технология	Назначение
Python	основная логика проекта
Streamlit	веб-интерфейс
MongoDB	хранение данных
Docker	запуск MongoDB
Pandas	работа с данными

Статус проекта

Проект выполнен в учебных целях и может использоваться как пример простого аналитического дашборда с хранением данных в MongoDB.

Автор

Dima Kuzin

GitHub: DimaKuzin05
