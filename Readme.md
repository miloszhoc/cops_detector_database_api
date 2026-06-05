# Cops Detector Database API

A FastAPI-based service for searching a database of vehicles. This project provides an interface to query vehicle information based on license plate numbers, stored in a PostgreSQL database.

## Features

- **Vehicle Search**: Query vehicle details by license plate (supports partial matching).
- **Dockerized**: deployment using Docker and Docker Compose.
- **Database Backups**: Automated backup scripts with S3 integration.

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org/) (managed via Docker)
- Python 3.9+ (for local development)

## Installation & Setup

1. **Clone the repository** (if not already done).

2. **Environment Variables**:

| Variable | Description |
| :--- | :--- |
| `POSTGRES_USER` | PostgreSQL database user |
| `POSTGRES_PASSWORD` | PostgreSQL database password |
| `POSTGRES_DB` | PostgreSQL database name |
| `WEBSITE_USERNAME` | Username for HTTP Basic Authentication |
| `WEBSITE_PASSWORD` | Password for HTTP Basic Authentication |
| `TABLE_NAME` | Name of the database table |

3. **Start the containers**:
   ```bash
   docker compose up -d
   ```
   This will start the PostgreSQL database and the FastAPI application.

## API Usage

### Authentication
The API uses **HTTP Basic Authentication**. You must provide the credentials defined in `WEBSITE_USERNAME` and `WEBSITE_PASSWORD`.

### Endpoint: Check License Plate
- **URL**: `/copsdetector/check`
- **Method**: `GET`
- **Parameters**: `licenseplate` (string)
- **Example Request**:
  ```bash
  curl -u username:password "http://localhost:8003/copsdetector/check?licenseplate=ABC12345"
  ```

### Example Response
```json
{
  "found": "ok",
  "results": [
    {
      "plate_number": "ABC12345",
      "details": {
        "vehicle_color": "Red",
        "s3_picture": "s3://bucket/car.jpg",
        "voivodeship": "Mazowieckie",
        "roads": ["A2", "S8"],
        "description": "test-image",
        "old_plate_number": "XYZ98765",
        "city": "Warszawa",
        "source": "camera1",
        "car_info": "Toyota Corolla 2020",
        "llm_extracted": {"status": "processed", "tags": ["car", "test"]}
      }
    }
  ]
}
```

## Database Management

### Backups
The project includes scripts to automate database backups.
- `database/cron/backup_db.sh`: Performs a `pg_dump`, uploads it to an S3 bucket, and cleans up local backups older than 7 days.
- `database/cron/add_cron.sh`: Adds the backup script to the system's crontab.

*Note: You may need to edit `database/cron/backup_db.sh` to set your specific S3 bucket and container details.*

### Restoring a Backup
To restore a database dump:
1. Clear the existing schema:
   ```bash
   docker exec -it cops_detector_database psql -U <DB_USER> -d <DB_NAME> -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
   ```
2. Import the backup:
   ```bash
   docker exec -i cops_detector_database psql -U <DB_USER> -d <DB_NAME> < "path/to/backup.sql"
   ```
