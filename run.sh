#!/bin/bash
export $(grep -v '^#' /mnt/DataSD/sandbox/educacionales/.env | xargs)
cd /mnt/DataSD/sandbox/educacionales
./venv/bin/python3 educ_monitor.py --run >> cron.log 2>&1
