#!/bin/sh
source env/bin/activate
gunicorn app
