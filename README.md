# **DataWar — Customer Analytics Dashboard**

Интерактивный дашборд для анализа клиентских данных.

Проект загружает данные о клиентах из CSV в MongoDB и отображает их в удобном веб-интерфейсе на Streamlit.

## **Возможности**

- 📊 количество клиентов
- 👤 средний возраст клиентов
- 💰 средний CAC
- 💵 суммарный CAC
- 🌍 анализ клиентов по странам и регионам
- 👥 распределение по сегментам и полу
- 📈 графики по возрасту и CAC
- 🔎 фильтры по стране, сегменту, региону, полу и возрасту
- 📋 таблица с данными клиентов

## **Стек**

- **Python**
- **Streamlit** — веб-интерфейс и визуализация
- **MongoDB** — хранение данных
- **Docker** — запуск MongoDB
- **Pandas** — обработка данных

## **Как это работает**

```text
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
```

Сначала данные из `customer_master.csv` загружаются в MongoDB с помощью `load_to_mongo.py`.

После этого Streamlit-приложение получает данные непосредственно из MongoDB и отображает их на дашборде.

## **Структура проекта**

```text
DataWar/
│
├── app.py                 # Streamlit-приложение
├── load_to_mongo.py       # загрузка данных в MongoDB
├── customer_master.csv    # исходный датасет
├── requirements.txt       # зависимости Python
├── README.md
└── .gitignore
```

## **Запуск проекта**

### **1. Клонирование репозитория**

```bash
git clone https://github.com/DimaKuzin05/DataWar.git
cd DataWar
```

### **2. Создание виртуального окружения**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Для Windows:

```bash
.venv\Scripts\activate
```

### **3. Установка зависимостей**

```bash
pip install -r requirements.txt
```

### **4. Запуск MongoDB**

MongoDB запускается в Docker.

Если контейнер `customer-mongo` уже создан:

```bash
docker start customer-mongo
```

Если контейнер создаётся впервые:

```bash
docker run -d \
  --name customer-mongo \
  -p 27017:27017 \
  mongo
```

### **5. Загрузка данных**

```bash
python3 load_to_mongo.py
```

После выполнения скрипта данные из `customer_master.csv` будут загружены в MongoDB.

### **6. Запуск Streamlit**

```bash
python3 -m streamlit run app.py
```

После запуска дашборд будет доступен по адресу:

```text
http://localhost:8501
```

## **MongoDB**

По умолчанию используется:

```text
URI:        mongodb://localhost:27017
Database:   dataset_zalupa
Collection: customers
```

Параметры подключения можно изменить через переменные окружения:

```bash
export MONGO_URI="mongodb://localhost:27017"
export MONGO_DB="dataset_zalupa"
export MONGO_COLLECTION="customers"
```

## **Дашборд**

На главной странице отображаются основные показатели клиентов:

- общее количество клиентов;
- средний возраст;
- средний CAC;
- суммарный CAC.

Также доступны фильтры:

- страна;
- сегмент;
- регион;
- пол;
- возраст.

После применения фильтров графики и таблица обновляются автоматически.

## **Графики**

Дашборд содержит визуализации:

- распределение клиентов по сегментам;
- распределение по странам;
- распределение по полу;
- распределение по возрасту;
- анализ CAC.

## **Данные**

В проекте используется датасет с информацией о **25 000 клиентах**.

Исходные данные находятся в:

```text
customer_master.csv
```

После загрузки приложение работает с данными из MongoDB, а не читает CSV напрямую.

## **Требования**

Для запуска необходимы:

- Python 3
- Docker
- MongoDB
- зависимости из `requirements.txt`
