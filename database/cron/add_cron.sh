#!/bin/bash

CRON_CMD="/usr/local/bin/db_backup.sh"
CRON_SCHEDULE="0 2 * * *"  # everyday at 02:00
CRON_ENTRY="${CRON_SCHEDULE} ${CRON_CMD} >> /var/log/db_backup.log 2>&1"

(crontab -l 2>/dev/null | grep -F "${CRON_CMD}") || \
( crontab -l 2>/dev/null; echo "${CRON_ENTRY}" ) | crontab -