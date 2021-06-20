# Fantasy Football Site

A fun site for displaying fantasy football information. Mostly used for my ability to talk trash.

Check out the progress of the site [here](http://172.104.7.13/)

## Starting/stopping the server

```bash
sudo supervisorctl stop ffs
git pull origin main
rm instance/ffs.sqlite
flask init-db
python3 scraper/espn-ffl.py --load True
gunicorn -b localhost:8000 -w 4 wsgi:app
sudo supervisorctl start ffs
```