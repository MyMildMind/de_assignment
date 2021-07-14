import random
import base64
import os
import shutil
from csv import writer
import psycopg2


def get_random_images(sample_number=10):
    FILED_NAME = ["book_id", "book_title", "price", "star"]

    if os.path.exists("sample_image"):
        shutil.rmtree("sample_image")
        os.mkdir("sample_image")
    with open("sample_image/info.csv", "a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(FILED_NAME)
    for i in range(0, sample_number):
        id = random.randint(1, 30)
        conn = psycopg2.connect(
            host="localhost", port=5432, database="dev", user="admin", password="admin"
        )
        cur = conn.cursor()
        cur.execute(
            """SELECT encode(img_base64::bytea,'escape') FROM book_image where book_id =%(id)s""",
            {"id": id},
        )
        query_results = cur.fetchall()[0][0]
        imgdata = base64.b64decode(query_results)
        filename = f"sample_image/book_id_{id}.jpg"
        with open(filename, "wb") as f:
            f.write(imgdata)
        cur.execute("""SELECT * FROM book_info where book_id =%(id)s""", {"id": id})
        query_results = cur.fetchall()[0]
        print(query_results)
        with open("sample_image/info.csv", "a") as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(query_results)
            f_object.close()
        cur.close()
        conn.close()


if __name__ == "__main__":
    get_random_images()
