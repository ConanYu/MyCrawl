import requests
from selenium import webdriver
robot, session = None

def todo(url, operator, **kw):
    global robot
    robot.get(url)
    operator(kw)
