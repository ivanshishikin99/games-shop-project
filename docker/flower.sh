#!/bin/bash

celery -A tasks.celery:celery flower