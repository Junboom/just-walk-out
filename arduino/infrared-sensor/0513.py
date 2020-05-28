import serial
import time
import MySQLdb
from datetime import datetime
import cv2
import boto3

port ="COM15"
brate = 9600

arduino =serial.Serial(port, baudrate = brate, timeout=None)
