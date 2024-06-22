import logging
import os
import sqlite3
from datetime import datetime
from sys import stdout

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            f"hazel/logs/init-database-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.log"
        ),
        logging.StreamHandler(stdout),
    ],
)

# warn if database already exists
if "data.db" in os.listdir("hazel"):
    logging.warning(
        "init_database: Database already exists in hazel/data.db, overwriting"
    )

# create the database
logging.info("init_database: Creating database in hazel/data.db")
conn = sqlite3.connect("hazel/data.db")
c = conn.cursor()

# drop HACKER table if it exists
c.execute("DROP TABLE IF EXISTS HACKER")

# create HACKER table
c.execute(
    """
    CREATE TABLE HACKER (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT NOT NULL UNIQUE,
        SKILLS TEXT,
        JOINED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        JOINED_MATCHMAKING BOOLEAN DEFAULT FALSE,
        MATCHMADE BOOLEAN DEFAULT FALSE
    )
    """
)
logging.info("init_database: Created HACKER table")

# commit changes and close connection
conn.commit()
conn.close()
logging.info("init_database: Database creation complete")
