# scraper_selenium
Python web scraping model using selenium. Main targets are news pages on a blue colour social media platform.

# Run
_Developed on Python 3.8_
Clone this repo and run the following
```
pip install -r /path/to/requirements.txt
python scraper.py
```
Finer adjustments can be made by modifying `fb_scraper_config.ini`

# Logging In
Logging into Facebook should not be required. Nonetheless, to login, provide the credentials in `facebook_credentials.txt` and change `user_login` field in `fb_scraper_config.ini` to "True".