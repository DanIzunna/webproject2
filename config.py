# config.py
import os
import secrets

# Generate a random secret key
secret_key = secrets.token_hex(16)  # Generates a 32-character hex string
secret_key = str(secret_key)

class Config:
    DATABASE_NAME = 'defaultdb'
    DATABASE_HOST = 'mysql-001-joeradnitz-483e.l.aivencloud.com'
    DATABASE_USER = 'avnadmin'
    DATABASE_PASSWORD = 'AVNS_h3B29i7yn0D3PvqkcZF'
    DATABASE_PORT = 16936
    

    SECRET_KEY = secret_key
    UNSPLASH_ACCESS_KEY =  '9zXMTqIIAc2fz6iC4XZzsIcSI9TgSlzom7TzpKgvGJM'
