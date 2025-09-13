1. In main directory create .env file with these variables:
```
- POSTGRES_USER=<postgres user>
- POSTGRES_PASSWORD=<postgres pass>
- POSTGRES_DB=cops_detector_db
- WEBSITE_USERNAME=<HTTP username>
- WEBSITE_PASSWORD=<HTTP Basic auth password>
- TABLE_NAME=cars
```

2. Run command:
- `sudo docker compose up -d`