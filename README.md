# mySite

## Описание

Этот проект представляет собой веб-приложение для редактирования изображений и распознавания объектов. Пользователи могут загружать изображения, редактировать их с помощью доступных инструментов, а затем распознавать объекты на загруженных фотографиях. Каждый пользователь имеет свою историю редактирования
## Функциональность

- Регистрация и вход в систему для пользователей.
- Загрузка изображений.
- Редактирование изображений с использованием инструмента для редактирования.
- Распознавание объектов на загруженных изображениях.
- Хранение истории редактирования для каждого пользователя
## Структура проекта 

- **Django**: веб-фреймворк для создания серверной части приложения.
- **PostgreSQL**: реляционная база данных для хранения данных пользователей и их истории.
- **yolov5**: обученная модель для распознавания объектов.
- **Bootstrap**: CSS-фреймворк для создания адаптивного дизайна.
- **Pintura**: инструмент для редактирования изображений.

## Установка

### Установка зависимостей

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/DumpishSad/mysite.git
   cd mysite
   ```

2. Установите необходимые библиотеки:
   ```bash
   pip install -r requirements.txt
   ```

### Настройка базы данных
1. Создайте базу данных в PostgreSQL:
   ```sql
   CREATE DATABASE users;
   ```

2. Измените настройки базы данных в файле settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'users',
           'USER': 'postgres',
           'PASSWORD': 'ваш_пароль',
           'HOST': '127.0.0.1',
           'PORT': '5432',
      }
   }
   ```

### Миграции
  ```bash
  python manage.py migrate
  ```
### Запуск сервера
``` bash
python manage.py runserver
```
### Использование
1. Зарегестрируйтесь
   ![](/images/рег.png)
2. Редактируйте изображения с помощью встроенного редактора.
   ![](/images/редак.png)
3. Используйте инструмент для распознавания объектов на загруженных изображениях.
   ![](/images/распоз.png)
4. Просматривайте свою историю редактирования, чтобы видеть загруженные и отредактированные изображения.
   ![](/images/истор.png)
