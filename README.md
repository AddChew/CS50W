# CS50W Project 3: Mail

Front-end for an email client that makes Django API calls to send and receive emails.

[Link to Demo](https://youtu.be/uhamGxxxjnc)

## How to run the project

1. Clone project branch
```
git clone -branch mail https://github.com/AddChew/CS50W.git
```

2. Navigate into project folder
```
cd mail
```

3. Install required dependencies
```
pip install -r requirements.txt
```

4. Migrate database
```
python manage.py makemigrations mail
python manage.py migrate
```

5. Start web server
```
python manage.py runserver
```
