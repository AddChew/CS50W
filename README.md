# CS50W Project 1: Wiki

Wikipedia-like online encyclopedia

[Link to Demo](https://youtu.be/Jp9lS4yTamU)

## How to run the project

1. Clone project branch
```
git clone -branch wiki https://github.com/AddChew/CS50W.git
```

2. Navigate into project folder
```
cd wiki
```

3. Install required dependencies
```
pip install -r requirements.txt
```

4. Migrate database
```
python manage.py migrate
```

5. Start web server
```
python manage.py runserver --insecure
```