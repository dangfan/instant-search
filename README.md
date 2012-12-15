Requirements

* Python (above v2.7)
* Related Python libraries
    * Beautiful Soup
    * Flask
    * stemming
* Redis

Configuration

* Install Redis (refer to [Redis docs](http://redis.io/);
* Install related python libs;

    `$ pip install beautifulsoup4 redis flask stemming`
* Configure crawler, please refer to crawler/README
* Build index

	`$ python searching/make_index.py`
* Run the server

	`$ python run.py`
