#!/bin/bash

celery -A tasks.celery:celery worker --loglevel=INFO --pool=solo