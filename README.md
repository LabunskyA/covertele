# CoverTele - A private covert channel over the Telegram
A tool and a library to provide a simple way of exchanging private text messages through the covert channel based on blacklising users written in Python. 

## Installation
- Clone this repo: `git clone https://github.com/LabunskyA/covertele`;
- Acquire Telegram api_id and api_hash by following [this manual](https://core.telegram.org/api/obtaining_api_id);
- Edit covertele.py: set your new values to `api_id` and `api_hash` in the [file header](https://github.com/LabunskyA/covertele/blob/master/covertele.py#L9);
- You're done.

### Dependencies
Python 3 is required.
You will also need [Telethon](https://github.com/LonamiWebs/Telethon) as it's used to call Telegram API methods.
You may install it with pip: `pip install telethon`

## Usage
If nothing is happening on the connection (no output), try setting a proxy in [covertele.py file](https://github.com/LabunskyA/covertele/blob/master/covertele.py#L12).
### Command-line tool
~~~bash
python3 covertele.py [-s/-r] [your username] [other username] [message]
~~~
To get message as user @mark from @tommy you call:
~~~bash
python3 covertele.py -r mark tommy
~~~
And to send "OH, HI MARK!..." from @tommy to @mark do this after mark has started listening with the command above:
~~~bash
python3 covertele.py -s tommy mark oh, hi mark!..
~~~

### API
Here is a basic usage example:
~~~python
from covertele import TelegramBlockingAPI
from cochannel import CovertChannel


# For channel to use telegram you need to create a suitable interface
# By default, standard IO used to authorize you, 
# but you can do it programmatically if you want to (see the source code)
id = input("Enter your id")
api = TelegramBlockingAPI(id)

# Now you can create channel object
friend = input("Enter your friend's id:")
channel = CovertChannel(api, friend)

# Use channel.receive() and channel.send() to transmit data between the users
channel.send("Bork, bork!")
print(channel.receive) 

# If you want to send and receive raw codes, you can call functions with '_raw' suffix
codes = channel.receive_raw()
for code in codes:
    check_correct(code)
channel.send_raw([19, 24, 24, 13])
~~~

## License
Simplified BSD, see [LICENSE](LICENSE) file.
