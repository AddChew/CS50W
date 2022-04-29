# CS50W Project 4: Network

Twitter-like social network website
[Link to Demo](https://youtu.be/rR-ContBkNA)

## How to run the project

1. Clone project branch
```
git clone -branch commerce https://github.com/AddChew/CS50W.git
```

2. Navigate into project folder
```
cd commerce
```

3. Install required dependencies
```
pip install -r requirements.txt
```

4. Migrate database
```
python manage.py makemigrations
python manage.py migrate
```

5. Create admin user
```
python manage.py createsuperuser
```

6. Start web server
```
python manage.py runserver --insecure
```