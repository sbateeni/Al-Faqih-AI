#!/bin/bash

# تثبيت المتطلبات الأساسية
apt-get update
apt-get install -y \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel

# تثبيت متطلبات Python
pip install -r requirements.txt 