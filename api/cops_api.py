import os

import psycopg2
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
    return psycopg2.connect(DATABASE_URL)


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
        cur.execute(f"SELECT * FROM {TABLE_NAME} WHERE id = 1 LIMIT 1;")
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail={'found': 'nok', 'error': 'plate number not found'})
        else:
            return {'found': 'ok', 'plate_number': licenseplate, 'data': row}

        # plates = ['DW123', 'DWL432']
        # if licenseplate in plates:
        #     return {'found': 'ok', 'plate_number': licenseplate,
        #             'details': {'vehicle_color': 'black', 'voivodeship': 'Dolnoslaskie', 'roads': ['S3', 'A1']}}
        # else:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                         detail={'found': 'nok', 'error': 'number not found'})
        cur.close()
        conn.close()
    else:
        return {'Error': 'User Not Authorized'}
