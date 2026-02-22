import os
import logging
import time
import psycopg2
import psycopg2.extras
from fastapi import FastAPI
import secrets
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(f"vehicle_ingestion_{str(int(time.time()))}.log"), logging.StreamHandler()])
LOGGER = logging.getLogger(__name__)

USERNAME = os.environ['WEBSITE_USERNAME'].encode('utf-8')
PASSWORD = os.environ['WEBSITE_PASSWORD'].encode('utf-8')

TABLE_NAME = os.environ["TABLE_NAME"]
DATABASE_URL = os.environ["DATABASE_URL"]

security = HTTPBasic()
app = FastAPI(dependencies=[Depends(security)])


def get_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


def verification(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = USERNAME
    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username_bytes)

    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = PASSWORD
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password_bytes)

    if not (is_correct_username and is_correct_password):
        LOGGER.info("Incorrect username or password")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Basic"})
    LOGGER.info("Username and password correct!")
    return credentials.username


@app.get("/copsdetector/check")
def checker(licenseplate: str, _verification=Depends(verification)):
    if _verification:
        conn = get_connection()
        cur = conn.cursor()
        LOGGER.info(
            "Executing SQL query: SELECT * FROM cars WHERE current_plate_number LIKE %s LIMIT 100;" % licenseplate)
        cur.execute("SELECT * FROM cars WHERE current_plate_number LIKE %s LIMIT 100;",
                    (f"%{licenseplate}%",))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            LOGGER.info(f'404 ERROR, Plate number {licenseplate} not found')
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={'found': 'nok', 'error': 'plate number not found'})
        else:
            car_data = {"found": "ok",
                        "results": [{"plate_number": r["current_plate_number"],
                                     "details": {
                                         "vehicle_color": r["vehicle_color"],
                                         "s3_picture": r["img_s3_path"],
                                         "voivodeship": r["voivodeship"],
                                         "roads": r["roads"],
                                         "description": r["description"],
                                         "old_plate_number": r["old_plate_number"],
                                         "city": r["city"],
                                         "source": r["source"],
                                         "car_info": r["car_info"],
                                         "llm_extracted": r["llm_extracted"]}} for r in rows]}
            LOGGER.info(f'CAR DATA: {car_data}')
            return car_data
    else:
        return {'Error': 'User Not Authorized'}
