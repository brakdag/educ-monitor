#!/bin/bash
export $(grep -v '^#' /mnt/DataSD/sandbox/educacionales/.env | xargs)
cd /mnt/DataSD/sandbox/educacionales
./venv/bin/python3 -m educ_monitor.cli --run >> cron.log 2>&1
