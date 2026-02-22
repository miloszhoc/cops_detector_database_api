#!/bin/bash
set -e

# CONFIG
CONTAINER="cops_detector_api"
DB_USER="<user>"
DB_NAME="<db name>"
BACKUP_DIR="/var/backups/postgres"
S3_BUCKET="<bucket name>"
S3_PREFIX="db_backups"

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
FILE="backup_${DATE}.sql"

mkdir -p "${BACKUP_DIR}"

# BACKUP
docker exec -t ${CONTAINER} pg_dump -U ${DB_USER} ${DB_NAME} \
  > "${BACKUP_DIR}/${FILE}"

# UPLOAD TO S3
aws s3 cp "${BACKUP_DIR}/${FILE}" "s3://${S3_BUCKET}/${S3_PREFIX}/${FILE}"

# cleanup local backups older than 7 days
find "${BACKUP_DIR}" -type f -mtime +7 -delete