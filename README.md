# CS50W Project 2: Commerce

eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to their watchlist.

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

7. Add categories via the admin interface, accessed by adding /admin to the default url