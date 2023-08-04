import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import time
import json
import random
import socket
import os
import re
import numpy as np
from datetime import datetime
import psycopg2
import threading


# Function to perform the database operations
def insert_to_db(data_to_insert):
    # Set up the database connection
    cnx = psycopg2.connect(
        host='buildwise.digital',
        user='postgresCedric',
        password='postgresCedric',
        database='postgres',
        port='5438'
    )

    # Create a cursor object
    cursor = cnx.cursor()

    # Define the query outside of the loop
    query = """
    INSERT INTO measurements_sensors (Sensor_ID, Time_of_Measurement, Sensor_Value_S, Sensor_Value_T)
    VALUES (%s, %s, %s, %s);
    """

    # Use executemany() to execute the query for all data
    cursor.executemany(query, data_to_insert)

    # Commit the transaction
    cnx.commit()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

now = datetime.now()

date_time = {'date': 0, 'time': 0}
sensor_ch1 = {'ch1_fbg1': 0, 'ch1_fbg2': 0.1, 'ch1_fbg3': 0, 'ch1_fbg4': 0, 'ch1_fbg5': 0, 'ch1_fbg6': 0, 'ch1_fbg7': 0, 'ch1_fbg8': 0, 'ch1_fbg9': 0, 'ch1_fbg10': 0, 'ch1_fbg11': 0, 'ch1_fbg12': 0, 'ch1_fbg13': 0, 'ch1_fbg14': 0, 'ch1_fbg15': 0, 'ch1_fbg16': 0, 'ch1_fbg17': 0, 'ch1_fbg18': 0, 'ch1_fbg19': 0, 'ch1_fbg20': 0, 'ch1_fbg21': 0, 'ch1_fbg22': 0, 'ch1_fbg23': 0, 'ch1_fbg24': 0, 'ch1_fbg25': 0, 'ch1_fbg26': 0, 'ch1_fbg27': 0, 'ch1_fbg28': 0, 'ch1_fbg29': 0, 'ch1_fbg30': 0}
sensor_ch2 = {'ch2_fbg1': 0, 'ch2_fbg2': 0, 'ch2_fbg3': 0, 'ch2_fbg4': 0, 'ch2_fbg5': 0, 'ch2_fbg6': 0, 'ch2_fbg7': 0, 'ch2_fbg8': 0, 'ch2_fbg9': 0, 'ch2_fbg10': 0, 'ch2_fbg11': 0, 'ch2_fbg12': 0, 'ch2_fbg13': 0, 'ch2_fbg14': 0, 'ch2_fbg15': 0, 'ch2_fbg16': 0, 'ch2_fbg17': 0, 'ch2_fbg18': 0, 'ch2_fbg19': 0, 'ch2_fbg20': 0, 'ch2_fbg21': 0, 'ch2_fbg22': 0}
sensor_ch3 = {'ch3_fbg1': 0, 'ch3_fbg2': 0, 'ch3_fbg3': 0, 'ch3_fbg4': 0, 'ch3_fbg5': 0, 'ch3_fbg6': 0, 'ch3_fbg7': 0, 'ch3_fbg8': 0, 'ch3_fbg9': 0, 'ch3_fbg10': 0, 'ch3_fbg11': 0, 'ch3_fbg12': 0, 'ch3_fbg13': 0, 'ch3_fbg14': 0, 'ch3_fbg15': 0, 'ch3_fbg16': 0, 'ch3_fbg17': 0, 'ch3_fbg18': 0, 'ch3_fbg19': 0, 'ch3_fbg20': 0, 'ch3_fbg21': 0, 'ch3_fbg22': 0}
sensor_ch4 = {'ch4_fbg1': 0, 'ch4_fbg2': 0, 'ch4_fbg3': 0, 'ch4_fbg4': 0, 'ch4_fbg5': 0, 'ch4_fbg6': 0, 'ch4_fbg7': 0, 'ch4_fbg8': 0, 'ch4_fbg9': 0, 'ch4_fbg10': 0, 'ch4_fbg11': 0, 'ch4_fbg12': 0, 'ch4_fbg13': 0, 'ch4_fbg14': 0, 'ch4_fbg15': 0, 'ch4_fbg16': 0, 'ch4_fbg17': 0, 'ch4_fbg18': 0, 'ch4_fbg19': 0, 'ch4_fbg20': 0, 'ch4_fbg21': 0, 'ch4_fbg22': 0}
sensor_ch5 = {'ch5_fbg1': 0, 'ch5_fbg2': 0, 'ch5_fbg3': 0, 'ch5_fbg4': 0, 'ch5_fbg5': 0, 'ch5_fbg6': 0, 'ch5_fbg7': 0, 'ch5_fbg8': 0, 'ch5_fbg9': 0, 'ch5_fbg10': 0, 'ch5_fbg11': 0, 'ch5_fbg12': 0, 'ch5_fbg13': 0, 'ch5_fbg14': 0, 'ch5_fbg15': 0, 'ch5_fbg16': 0, 'ch5_fbg17': 0, 'ch5_fbg18': 0, 'ch5_fbg19': 0,'ch5_fbg20': 0, 'ch5_fbg21': 0, 'ch5_fbg22': 0}
sensor_ch6 = {'ch6_fbg1': 0, 'ch6_fbg2': 0, 'ch6_fbg3': 0, 'ch6_fbg4': 0, 'ch6_fbg5': 0, 'ch6_fbg6': 0, 'ch6_fbg7': 0, 'ch6_fbg8': 0, 'ch6_fbg9': 0, 'ch6_fbg10': 0, 'ch6_fbg11': 0, 'ch6_fbg12': 0, 'ch6_fbg13': 0, 'ch6_fbg14': 0, 'ch6_fbg15': 0, 'ch6_fbg16': 0, 'ch6_fbg17': 0, 'ch6_fbg18': 0, 'ch6_fbg19': 0, 'ch6_fbg20': 0, 'ch6_fbg21': 0, 'ch6_fbg22': 0}
sensor_ch7 = {'ch7_fbg1': 0, 'ch7_fbg2': 0, 'ch7_fbg3': 0, 'ch7_fbg4': 0, 'ch7_fbg5': 0, 'ch7_fbg6': 0, 'ch7_fbg7': 0, 'ch7_fbg8': 0, 'ch7_fbg9': 0, 'ch7_fbg10': 0, 'ch7_fbg11': 0, 'ch7_fbg12': 0, 'ch7_fbg13': 0, 'ch7_fbg14': 0, 'ch7_fbg15': 0, 'ch7_fbg16': 0, 'ch7_fbg17': 0, 'ch7_fbg18': 0, 'ch7_fbg19': 0, 'ch7_fbg20': 0, 'ch7_fbg21': 0, 'ch7_fbg22': 0}
sensor_ch8 = {'ch8_fbg1': 0, 'ch8_fbg2': 0, 'ch8_fbg3': 0, 'ch8_fbg4': 0, 'ch8_fbg5': 0, 'ch8_fbg6': 0, 'ch8_fbg7': 0, 'ch8_fbg8': 0, 'ch8_fbg9': 0, 'ch8_fbg10': 0, 'ch8_fbg11': 0, 'ch8_fbg12': 0, 'ch8_fbg13': 0, 'ch8_fbg14': 0, 'ch8_fbg15': 0, 'ch8_fbg16': 0, 'ch8_fbg17': 0, 'ch8_fbg18': 0, 'ch8_fbg19': 0, 'ch8_fbg20': 0, 'ch8_fbg21': 0, 'ch8_fbg22': 0}
sensor_ch9 = {'ch9_fbg1': 0, 'ch9_fbg2': 0, 'ch9_fbg3': 0, 'ch9_fbg4': 0, 'ch9_fbg5': 0, 'ch9_fbg6': 0, 'ch9_fbg7': 0, 'ch9_fbg8': 0, 'ch9_fbg9': 0, 'ch9_fbg10': 0, 'ch9_fbg11': 0, 'ch9_fbg12': 0, 'ch9_fbg13': 0, 'ch9_fbg14': 0, 'ch9_fbg15': 0, 'ch9_fbg16': 0, 'ch9_fbg17': 0, 'ch9_fbg18': 0, 'ch9_fbg19': 0, 'ch9_fbg20': 0, 'ch9_fbg21': 0, 'ch9_fbg22': 0, 'ch9_fbg23': 0, 'ch9_fbg24': 0, 'ch9_fbg25': 0, 'ch9_fbg26': 0}
sensor_ch10 = {'ch10_fbg1': 0, 'ch10_fbg2': 0, 'ch10_fbg3': 0, 'ch10_fbg4': 0, 'ch10_fbg5': 0, 'ch10_fbg6': 0, 'ch10_fbg7': 0, 'ch10_fbg8': 0, 'ch10_fbg9': 0, 'ch10_fbg10': 0, 'ch10_fbg11': 0, 'ch10_fbg12': 0, 'ch10_fbg13': 0, 'ch10_fbg14': 0, 'ch10_fbg15': 0, 'ch10_fbg16': 0, 'ch10_fbg17': 0, 'ch10_fbg18': 0, 'ch10_fbg19': 0, 'ch10_fbg20': 0}
sensor_ch11 = {'ch11_fbg1': 0, 'ch11_fbg2': 0, 'ch11_fbg3': 0, 'ch11_fbg4': 0, 'ch11_fbg5': 0, 'ch11_fbg6': 0, 'ch11_fbg7': 0, 'ch11_fbg8': 0, 'ch11_fbg9': 0, 'ch11_fbg10': 0, 'ch11_fbg11': 0, 'ch11_fbg12': 0, 'ch11_fbg13': 0, 'ch11_fbg14': 0, 'ch11_fbg15': 0, 'ch11_fbg16': 0, 'ch11_fbg17': 0, 'ch11_fbg18': 0, 'ch11_fbg19': 0, 'ch11_fbg20': 0}
sensor_ch12 = {'ch12_fbg1': 0, 'ch12_fbg2': 0, 'ch12_fbg3': 0, 'ch12_fbg4': 0, 'ch12_fbg5': 0, 'ch12_fbg6': 0, 'ch12_fbg7': 0, 'ch12_fbg8': 0, 'ch12_fbg9': 0, 'ch12_fbg10': 0, 'ch12_fbg11': 0, 'ch12_fbg12': 0}
sensor_ch13 = {'ch13_fbg1': 0, 'ch13_fbg2': 0, 'ch13_fbg3': 0, 'ch13_fbg4': 0, 'ch13_fbg5': 0, 'ch13_fbg6': 0, 'ch13_fbg7': 0, 'ch13_fbg8': 0, 'ch13_fbg9': 0, 'ch13_fbg10': 0, 'ch13_fbg11': 0, 'ch13_fbg12': 0}
sensor_ch14 = {'ch14_fbg1': 0, 'ch14_fbg2': 0, 'ch14_fbg3': 0, 'ch14_fbg4': 0, 'ch14_fbg5': 0, 'ch14_fbg6': 0, 'ch14_fbg7': 0, 'ch14_fbg8': 0, 'ch14_fbg9': 0, 'ch14_fbg10': 0, 'ch14_fbg11': 0, 'ch14_fbg12': 0}
sensor_ch15 = {'ch15_fbg1': 0, 'ch15_fbg2': 0, 'ch15_fbg3': 0, 'ch15_fbg4': 0, 'ch15_fbg5': 0, 'ch15_fbg6': 0, 'ch15_fbg7': 0, 'ch15_fbg8': 0}

all_ch_data = sensor_ch1 | sensor_ch2 | sensor_ch3 | sensor_ch4 | sensor_ch5 | sensor_ch6 | sensor_ch7 | sensor_ch8 | sensor_ch9 | sensor_ch10 | sensor_ch11 | sensor_ch12 | sensor_ch13 | sensor_ch14 | sensor_ch15

sensor_ch1_T = {'ch1_fbg1_T': 0, 'ch1_fbg2_T': 0, 'ch1_fbg3_T': 0, 'ch1_fbg4_T': 0, 'ch1_fbg5_T': 0, 'ch1_fbg6_T': 0, 'ch1_fbg7_T': 0, 'ch1_fbg8_T': 0, 'ch1_fbg9_T': 0, 'ch1_fbg10_T': 0, 'ch1_fbg11_T': 0, 'ch1_fbg12_T': 0, 'ch1_fbg13_T': 0, 'ch1_fbg14_T': 0, 'ch1_fbg15_T': 0, 'ch1_fbg16_T': 0, 'ch1_fbg17_T': 0, 'ch1_fbg18_T': 0, 'ch1_fbg19_T': 0, 'ch1_fbg20_T': 0, 'ch1_fbg21_T': 0, 'ch1_fbg22_T': 0, 'ch1_fbg23_T': 0, 'ch1_fbg24_T': 0, 'ch1_fbg25_T': 0, 'ch1_fbg26_T': 0, 'ch1_fbg27_T': 0, 'ch1_fbg28_T': 0, 'ch1_fbg29_T': 0, 'ch1_fbg30_T': 0}
sensor_ch2_T = {'ch2_fbg1_T': 0, 'ch2_fbg2_T': 0, 'ch2_fbg3_T': 0, 'ch2_fbg4_T': 0, 'ch2_fbg5_T': 0, 'ch2_fbg6_T': 0, 'ch2_fbg7_T': 0, 'ch2_fbg8_T': 0, 'ch2_fbg9_T': 0, 'ch2_fbg10_T': 0, 'ch2_fbg11_T': 0, 'ch2_fbg12_T': 0, 'ch2_fbg13_T': 0, 'ch2_fbg14_T': 0, 'ch2_fbg15_T': 0, 'ch2_fbg16_T': 0, 'ch2_fbg17_T': 0, 'ch2_fbg18_T': 0, 'ch2_fbg19_T': 0, 'ch2_fbg20_T': 0, 'ch2_fbg21_T': 0, 'ch2_fbg22_T': 0}
sensor_ch3_T = {'ch3_fbg1_T': 0, 'ch3_fbg2_T': 0, 'ch3_fbg3_T': 0, 'ch3_fbg4_T': 0, 'ch3_fbg5_T': 0, 'ch3_fbg6_T': 0, 'ch3_fbg7_T': 0, 'ch3_fbg8_T': 0, 'ch3_fbg9_T': 0, 'ch3_fbg10_T': 0, 'ch3_fbg11_T': 0, 'ch3_fbg12_T': 0, 'ch3_fbg13_T': 0, 'ch3_fbg14_T': 0, 'ch3_fbg15_T': 0, 'ch3_fbg16_T': 0, 'ch3_fbg17_T': 0, 'ch3_fbg18_T': 0, 'ch3_fbg19_T': 0, 'ch3_fbg20_T': 0, 'ch3_fbg21_T': 0, 'ch3_fbg22_T': 0}
sensor_ch4_T = {'ch4_fbg1_T': 0, 'ch4_fbg2_T': 0, 'ch4_fbg3_T': 0, 'ch4_fbg4_T': 0, 'ch4_fbg5_T': 0, 'ch4_fbg6_T': 0, 'ch4_fbg7_T': 0, 'ch4_fbg8_T': 0, 'ch4_fbg9_T': 0, 'ch4_fbg10_T': 0, 'ch4_fbg11_T': 0, 'ch4_fbg12_T': 0, 'ch4_fbg13_T': 0, 'ch4_fbg14_T': 0, 'ch4_fbg15_T': 0, 'ch4_fbg16_T': 0, 'ch4_fbg17_T': 0, 'ch4_fbg18_T': 0, 'ch4_fbg19_T': 0, 'ch4_fbg20_T': 0, 'ch4_fbg21_T': 0, 'ch4_fbg22_T': 0}
sensor_ch5_T = {'ch5_fbg1_T': 0, 'ch5_fbg2_T': 0, 'ch5_fbg3_T': 0, 'ch5_fbg4_T': 0, 'ch5_fbg5_T': 0, 'ch5_fbg6_T': 0, 'ch5_fbg7_T': 0, 'ch5_fbg8_T': 0, 'ch5_fbg9_T': 0, 'ch5_fbg10_T': 0, 'ch5_fbg11_T': 0, 'ch5_fbg12_T': 0, 'ch5_fbg13_T': 0, 'ch5_fbg14_T': 0, 'ch5_fbg15_T': 0, 'ch5_fbg16_T': 0, 'ch5_fbg17_T': 0,'ch5_fbg18_T': 0, 'ch5_fbg19_T': 0, 'ch5_fbg20_T': 0, 'ch5_fbg21_T': 0, 'ch5_fbg22_T': 0}
sensor_ch6_T = {'ch6_fbg1_T': 0, 'ch6_fbg2_T': 0, 'ch6_fbg3_T': 0, 'ch6_fbg4_T': 0, 'ch6_fbg5_T': 0, 'ch6_fbg6_T': 0, 'ch6_fbg7_T': 0, 'ch6_fbg8_T': 0, 'ch6_fbg9_T': 0, 'ch6_fbg10_T': 0, 'ch6_fbg11_T': 0, 'ch6_fbg12_T': 0, 'ch6_fbg13_T': 0, 'ch6_fbg14_T': 0, 'ch6_fbg15_T': 0, 'ch6_fbg16_T': 0, 'ch6_fbg17_T': 0, 'ch6_fbg18_T': 0, 'ch6_fbg19_T': 0, 'ch6_fbg20_T': 0, 'ch6_fbg21_T': 0, 'ch6_fbg22_T': 0}
sensor_ch7_T = {'ch7_fbg1_T': 0, 'ch7_fbg2_T': 0, 'ch7_fbg3_T': 0, 'ch7_fbg4_T': 0, 'ch7_fbg5_T': 0, 'ch7_fbg6_T': 0, 'ch7_fbg7_T': 0, 'ch7_fbg8_T': 0, 'ch7_fbg9_T': 0, 'ch7_fbg10_T': 0, 'ch7_fbg11_T': 0, 'ch7_fbg12_T': 0, 'ch7_fbg13_T': 0, 'ch7_fbg14_T': 0, 'ch7_fbg15_T': 0, 'ch7_fbg16_T': 0, 'ch7_fbg17_T': 0, 'ch7_fbg18_T': 0, 'ch7_fbg19_T': 0, 'ch7_fbg20_T': 0, 'ch7_fbg21_T': 0, 'ch7_fbg22_T': 0}
sensor_ch8_T = {'ch8_fbg1_T': 0, 'ch8_fbg2_T': 0, 'ch8_fbg3_T': 0, 'ch8_fbg4_T': 0, 'ch8_fbg5_T': 0, 'ch8_fbg6_T': 0, 'ch8_fbg7_T': 0, 'ch8_fbg8_T': 0, 'ch8_fbg9_T': 0, 'ch8_fbg10_T': 0, 'ch8_fbg11_T': 0, 'ch8_fbg12_T': 0, 'ch8_fbg13_T': 0, 'ch8_fbg14_T': 0, 'ch8_fbg15_T': 0, 'ch8_fbg16_T': 0, 'ch8_fbg17_T': 0, 'ch8_fbg18_T': 0, 'ch8_fbg19_T': 0, 'ch8_fbg20_T': 0, 'ch8_fbg21_T': 0, 'ch8_fbg22_T': 0}
sensor_ch9_T = {'ch9_fbg1_T': 0, 'ch9_fbg2_T': 0, 'ch9_fbg3_T': 0, 'ch9_fbg4_T': 0, 'ch9_fbg5_T': 0, 'ch9_fbg6_T': 0, 'ch9_fbg7_T': 0, 'ch9_fbg8_T': 0, 'ch9_fbg9_T': 0, 'ch9_fbg10_T': 0, 'ch9_fbg11_T': 0, 'ch9_fbg12_T': 0, 'ch9_fbg13_T': 0, 'ch9_fbg14_T': 0, 'ch9_fbg15_T': 0, 'ch9_fbg16_T': 0, 'ch9_fbg17_T': 0,'ch9_fbg18_T': 0, 'ch9_fbg19_T': 0, 'ch9_fbg20_T': 0, 'ch9_fbg21_T': 0, 'ch9_fbg22_T': 0, 'ch9_fbg23_T': 0, 'ch9_fbg24_T': 0, 'ch9_fbg25_T': 0, 'ch9_fbg26_T': 0}
sensor_ch10_T = {'ch10_fbg1_T': 0, 'ch10_fbg2_T': 0, 'ch10_fbg3_T': 0, 'ch10_fbg4_T': 0, 'ch10_fbg5_T': 0, 'ch10_fbg6_T': 0, 'ch10_fbg7_T': 0, 'ch10_fbg8_T': 0, 'ch10_fbg9_T': 0, 'ch10_fbg10_T': 0, 'ch10_fbg11_T': 0, 'ch10_fbg12_T': 0, 'ch10_fbg13_T': 0, 'ch10_fbg14_T': 0, 'ch10_fbg15_T': 0, 'ch10_fbg16_T': 0, 'ch10_fbg17_T': 0, 'ch10_fbg18_T': 0, 'ch10_fbg19_T': 0, 'ch10_fbg20_T': 0}
sensor_ch11_T = {'ch11_fbg1_T': 0, 'ch11_fbg2_T': 0, 'ch11_fbg3_T': 0, 'ch11_fbg4_T': 0, 'ch11_fbg5_T': 0, 'ch11_fbg6_T': 0, 'ch11_fbg7_T': 0, 'ch11_fbg8_T': 0, 'ch11_fbg9_T': 0, 'ch11_fbg10_T': 0, 'ch11_fbg11_T': 0, 'ch11_fbg12_T': 0, 'ch11_fbg13_T': 0, 'ch11_fbg14_T': 0, 'ch11_fbg15_T': 0, 'ch11_fbg16_T': 0, 'ch11_fbg17_T': 0, 'ch11_fbg18_T': 0, 'ch11_fbg19_T': 0, 'ch11_fbg20_T': 0}
sensor_ch12_T = {'ch12_fbg1_T': 0, 'ch12_fbg2_T': 0, 'ch12_fbg3_T': 0, 'ch12_fbg4_T': 0, 'ch12_fbg5_T': 0, 'ch12_fbg6_T': 0, 'ch12_fbg7_T': 0, 'ch12_fbg8_T': 0, 'ch12_fbg9_T': 0, 'ch12_fbg10_T': 0, 'ch12_fbg11_T': 0, 'ch12_fbg12_T': 0}
sensor_ch13_T = {'ch13_fbg1_T': 0, 'ch13_fbg2_T': 0, 'ch13_fbg3_T': 0, 'ch13_fbg4_T': 0, 'ch13_fbg5_T': 0, 'ch13_fbg6_T': 0, 'ch13_fbg7_T': 0, 'ch13_fbg8_T': 0, 'ch13_fbg9_T': 0, 'ch13_fbg10_T': 0, 'ch13_fbg11_T': 0, 'ch13_fbg12_T': 0}
sensor_ch14_T = {'ch14_fbg1_T': 0, 'ch14_fbg2_T': 0, 'ch14_fbg3_T': 0, 'ch14_fbg4_T': 0, 'ch14_fbg5_T': 0, 'ch14_fbg6_T': 0, 'ch14_fbg7_T': 0, 'ch14_fbg8_T': 0, 'ch14_fbg9_T': 0, 'ch14_fbg10_T': 0, 'ch14_fbg11_T': 0, 'ch14_fbg12_T': 0}
sensor_ch15_T = {'ch15_fbg1_T': 0, 'ch15_fbg2_T': 0, 'ch15_fbg3_T': 0, 'ch15_fbg4_T': 0, 'ch15_fbg5_T': 0, 'ch15_fbg6_T': 0, 'ch15_fbg7_T': 0, 'ch15_fbg8_T': 0}

all_ch_data_Tcorr = sensor_ch1_T | sensor_ch2_T | sensor_ch3_T | sensor_ch4_T | sensor_ch5_T | sensor_ch6_T | sensor_ch7_T | sensor_ch8_T | sensor_ch9_T | sensor_ch10_T | sensor_ch11_T | sensor_ch12_T | sensor_ch13_T | sensor_ch14_T | sensor_ch15_T

# Main section of your program
data_to_insert = []

for key in all_ch_data:
    keyt = key + '_T'

    # Create a tuple of data and append it to the list
    data_tuple = (key, now, all_ch_data[key], all_ch_data_Tcorr[keyt])
    data_to_insert.append(data_tuple)

# Create a Thread object
t = threading.Thread(target=insert_to_db, args=(data_to_insert,))

# Start the thread, this will initiate the DB insert in a separate thread.
t.start()