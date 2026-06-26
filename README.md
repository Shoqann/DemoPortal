# ---------
#      Demo Portal with Staff planning
# ---------


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