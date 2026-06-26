# ---------
#      Демо Портал с Увольнениями
#      [Нажми на меня для просмотра сайта](https://shoqan.pythonanywhere.com/hr/leave/)
# ---------


## Описание проекта 
DemoPortal - это корпоративный HR-портал на основе Django связанный с БД, разработанный для управления рабочими процессами, связанными с сотрудниками, в одном месте. Проект включает в себя регистрацию сотрудников, аутентификацию, отслеживание увольнений, расчет потребности в найме и простой ИИ-помощник для ответа на внутренние вопросы.

Главная цель проекта - продемонстрировать, как небольшая организация может автоматизировать основные HR-процессы и предоставить сотрудникам быстрый доступ к полезной информации через веб-интерфейс. 

#      Как начать

1. Скопируйте git clone, создайте виртуальную среду, внедрите нужные требования 

```bash
git clone https://github.com/Shoqann/DemoPortal.git
python -m venv myvenv or virtualenv myenv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Выполните миграций и создайте пользователя:

```bash
python manage.py migrate
python manage.py createsuperuser
```

3. Запуск сервера:

```bash
python manage.py runserver
```
4. Открыть ссылку:

```bash
http://127.0.0.1:8000/hr/index
```

5. Пример API вызова:

```bash
curl 'http://127.0.0.1:8000/hr/api/hiring-need/?start=2026-01-01&end=2026-12-31'
```

6. Тесты:
```bash
python manage.py test
```

#                   Полезные ссылки

* /admin/                     Django admin
* /hr/index/                  Main portal
* /hr/register/               Employee registration
* /hr/leave/                  Departure management
* /hr/api/hiring-need/        Hiring need API





# ---------
#      Demo Portal with Staff planning
#      [Click on me to view web page](https://shoqan.pythonanywhere.com/hr/leave/)
# ---------

## Project Description

DemoPortal is a Django-based corporate HR portal designed to help manage employee-related workflows in one place. The project includes employee registration, authentication, departure tracking, hiring need calculation, and a simple AI assistant for answering internal questions.

The main goal of the project is to demonstrate how a small organization can automate basic HR processes and provide employees with quick access to useful information through a web interface.

#      How to start

1. Copy and activate a virtual environment and install dependencies:

```bash
git clone https://github.com/Shoqann/DemoPortal.git
python -m venv myvenv or virtualenv myenv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

3. Run the server:

```bash
python manage.py runserver
```
4. Open:

```bash
http://127.0.0.1:8000/hr/index
```

5. Example API call:

```bash
curl 'http://127.0.0.1:8000/hr/api/hiring-need/?start=2026-01-01&end=2026-12-31'
```

6. Test:
```bash
python manage.py test
```

#                   Useful URLs

* /admin/                     Django admin
* /hr/index/                  Main portal
* /hr/register/               Employee registration
* /hr/leave/                  Departure management
* /hr/api/hiring-need/        Hiring need API