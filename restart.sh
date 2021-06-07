#!/bin/bash

git pull origin main
sudo supervisorctl stop ffs
# flask db upgrade
sudo supervisorctl start ffs
