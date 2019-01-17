# Python-Space-Instagram 
### This repo shows you how to load photo's from hubble API, Spacex API and push them to instagram
## Requirements
Python >= 3.5 required.  
Install dependencies with 
```bash
pip install -r requirements.txt
```
For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

If you want to not only fetch images, but also push to instagram, when it's required to have an
[Instagram](https://www.instagram.com/) account. 

## Usage
Main logic is separated to 3 scripts
* fetch_hubble.py
* fetch_spacex.py
* publish_photos.py

You can run separately __fetch_hubble.py__ and __fetch_spacex.py__ to just load last photos. 
It may take some time to load photos depending on your internet connection.
```bash
python fetch_hubble.py
```
```bash
python fetch_spacex.py
```

If you want to publish these photo's to instagram, you need to:
1. Signup to [Instagram](https://www.instagram.com/)
2. Create .env file and store your account name and password in ***instagram_login*** and 
***instagram_password*** variables. 
Run 
```bash
python publish_photos.py
```
and watch your account fill up with new photos