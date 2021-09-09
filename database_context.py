import psycopg2
import os
import sys

connection = psycopg2.connect(dbname='d40blfu5hq3mdk',
                               user='aquljnybflueun',
                               password=os.getenv("DB_PASSWORD"),
                               host='ec2-107-22-18-26.compute-1.amazonaws.com')