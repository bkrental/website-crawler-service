# scrapy-rental

### Install Python

I assume that you had installed Python on your computer. For installation process, please checkout https://www.python.org/downloads/

### Install Dependencies

First, let's install virtualenv using pip

```
pip3 install virtualenv
```

Next, to create a virtual environment folder, you can replace venv by your custom folder name

```
virtualenv venv
```

Then, we can activate the virtual environment.
if you can open gitbash, or you are using MacOS, Linux

```
source venv/bin/activate
```

if you are using Windows, you can open command prompt

```
venv\Scripts\activate.bat
```

Finally, you can install the dependencies for the project without installing them into your global PC

```
pip3 install -r requirements.txt
```

### How to use it

#### Without storing the crawled posts into database

Step 1: Go to file `settings.py`, comment the following line:

```py
ITEM_PIPELINES = {
    # "website_scraper.pipelines.MogiPipeline": 300,
}
```

Step 2: Run the commands:

```sh
scrapy crawl mogi_spider -o mogi_rentals_data.csv -a pages_limit=PAGES_LIMIT (>2)
```

"-o mogi_rentals_data.csv": This is optional to export the result into csv file.

#### Storing the result to database

Step 1: Make sure the `rental-service` is running in "http://localhost:3000"

Step 2: Go to file `settings.py`, uncomment the following line:

```py
ITEM_PIPELINES = {
    "website_scraper.pipelines.MogiPipeline": 300,
}
```

Step 3: Run the commands:

```sh
scrapy crawl mogi_spider -o mogi_rentals_data.csv
```

If you have any problem or you want to contribute anything. Feel free to let me know.
