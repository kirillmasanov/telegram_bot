# Example of use package "python-telegram-bot"

### Installation

Create a virtual environment and activate it.

Install the dependencies:

```python
pip install -r requirements.txt
```

### Settings

Create file **settings.py** with the next parameters:

```python
PROXY = {'proxy_url': 'socks5://URL',
         'urllib3_proxy_kwargs': {'username': 'LOGIN', 'password': 'PASSWORD'}
         }

TOKEN = 'TOKEN from BotFather'

USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:']
```

### Getting started