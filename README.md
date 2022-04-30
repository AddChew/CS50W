# CS50W Project 4: Network

Twitter-like social network website

[Link to Demo]()

## How to run the project

1. Clone project branch
```
git clone -branch network https://github.com/AddChew/CS50W.git
```

2. Navigate into project folder
```
cd network
```

3. Install required dependencies
```
pip install -r requirements.txt
```

4. Migrate database
```
python manage.py makemigrations network
python manage.py migrate
```

5. Start web server
```
python manage.py runserver
```