#!/usr/bin/env python

from classes.rs485 import *
import time

ser = RS485()

# Connect only ONE Device!
# print(ser.SetAddr(2))
# print(ser.GetAddr())

# exit()

print('Set Status: Addr 1, 10101010')
print(ser.SetStatus(1, '10101010'))
print("-----")
time.sleep(1)

print('Set Status: Addr 2, 01010101')
print(ser.SetStatus(2, '01010101'))
print("-----")
time.sleep(1)

print('Get Status: Addr 1')
print(ser.GetStatus(1, 255))
print("-----")

print('Get Status: Addr 2')
print(ser.GetStatus(2, 255))
print("-----")
time.sleep(1)

print('Off: Addr 1, All')
print(ser.RelaisOff(1, 255))
print("-----")
time.sleep(1)

print('Off: Addr 2, All')
print(ser.RelaisOff(2, 255))
print("-----")
time.sleep(1)

print('Get Status: Addr 1')
print(ser.GetStatus(1, 255))
print("-----")

print('Get Status: Addr 2')
print(ser.GetStatus(2, 255))
print("-----")

print('Get Version: Addr 1')
print(ser.GetVersion(1))
print("-----")

print('Get Version: Addr 2')
print(ser.GetVersion(2))
print("-----")
