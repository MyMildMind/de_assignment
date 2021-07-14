# import web grabbing client and
# HTML parser
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
import base64
import requests


def get_as_base64(url):

    return base64.b64encode(requests.get(url).content)


conn = psycopg2.connect(
    host="db", port=5432, database="dev", user="admin", password="admin"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
conn.autocommit = True
cur = conn.cursor()
cur.execute(
    """CREATE TABLE book_image(
    book_id SERIAL PRIMARY KEY,
    img_url VARCHAR(256) NOT NULL,
    img_base64 bytea NOT NULL)
    """
)
cur.execute(
    """CREATE TABLE book_info(
    book_id SERIAL PRIMARY KEY,
    book_title VARCHAR(256) NOT NULL,
    price VARCHAR(32) NOT NULL,
    star VARCHAR(8) NOT NULL) 
    """
)


for i in range(1, 51):
    # variable to store website link as string
    myurl = f"http://books.toscrape.com/catalogue/page-{i}.html"

    # grab website and store in variable uclient
    uClient = uReq(myurl)

    # read and close HTML
    page_html = uClient.read()
    uClient.close()

    # call BeautifulSoup for parsing
    page_soup = soup(page_html, "html.parser")

    # grabs all the products under list tag
    bookshelf = page_soup.findAll(
        "li", {"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}
    )

    for books in bookshelf:
        img_url = books.a.img["src"].lstrip("..")
        img_url = f"http://books.toscrape.com{img_url}"
        img_base64 = get_as_base64(img_url)
        # collect title of all books
        book_title = books.h3.a["title"]

        # collect book price of all books
        book_price = books.find_all("p", {"class": "price_color"})
        book_star = books.find("p").get("class")[1]
        price = book_price[0].text.strip()

        print("Title of the book :" + book_title)
        print("Price of the book :" + price)

        cur.execute(
            """INSERT INTO book_image(img_url, img_base64) VALUES(%s, %s)""",
            (img_url, img_base64),
        )
        cur.execute(
            """INSERT INTO book_info(book_title, price, star) VALUES(%s, %s, %s)""",
            (book_title, price, book_star),
        )
        conn.commit()

cur.close()
conn.close()
