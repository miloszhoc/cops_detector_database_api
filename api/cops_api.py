import os

import psycopg2
import psycopg2.extras
from fastapi import FastAPI

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Basic"})
    return credentials.username


@app.get("/copsdetector/check")
def checker(licenseplate: str, _verification=Depends(verification)):
    if _verification:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM cars WHERE current_plate_number=%s LIMIT 1;",
                    (licenseplate,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={'found': 'nok', 'error': 'plate number not found'})
        else:
            return {
                "found": "ok",
                "plate_number": row["current_plate_number"],
                "details": {
                    "vehicle_color": row["vehicle_color"],
                    "s3_picture": row["img_s3_path"],
                    "voivodeship": row["voivodeship"],
                    "roads": row["roads"],
                    "description": row["description"],
                    "old_plate_number": row["old_plate_number"],
                    "city": row["city"],
                    "source": row["source"],
                    "car_info": row["car_info"],
                    "llm_extracted": row["llm_extracted"]
                }
            }
    else:
        return {'Error': 'User Not Authorized'}
