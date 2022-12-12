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

# Website Elements
Under the you will see something like
```
post_class_type = div
post_class_name = x9f619 x1n2onr6 x1ja2u2z x2bj2ny x1qpq9i9 xdney7k xu5ydu1 xt3gfkd xh8yej3 x6ikm8r x10wlt62 xquyuld
```
These are component names obtained from inspecting FB post. The names may change and a quick fix would be inspecting the elements again and change the config file component name.
[Inspecting for component name and type](images/component_inspect.png)
