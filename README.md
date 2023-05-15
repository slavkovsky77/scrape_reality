# yit-scrapy-task

Scrapes  appartments from yit.sk

## How to run

- Run command
```
docker compose up
```
## docker compose settings

- if you want to change settings for scrapping look athe docker-compose.yml

- PAGES_TO_SCRAP  ->  number of pages to scrape from yit.sk
- SCRAP_INTERVAL_SECONDS  ->  scraping interval
- DROP_DATABASE  ->  this will drop the database on docker compose up


## How to run  tests

- Run command

```
docker compose -f docker-compose-test.yml up
```


## Links

- [http://127.0.0.1:5000/](http://127.0.0.1:5000/)