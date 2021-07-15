# de_assignment
for only de assignment

## Instruction for running this project

1. Clone this project by http or ssh

2. Create Virtual Environment and activate
  (Used in this project)
  ```
  virtualenv env
  source env/bin/activate
  ```
3. Install libary that used in this project
  ```
  pip install -r requirements.txt
  ```
4. Run docker build (make sure that docker desktop is running)
  ```
  docker-compose build
  ```
5. Run everything (Scrape all books and add to Postgres)
  ```
  docker-compose up
  ```
