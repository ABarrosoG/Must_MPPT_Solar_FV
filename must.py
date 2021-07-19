#! /usr/bin/python
#pip install pymodbus
#pip install --upgrade setuptools
#pip install paho-mqtt
import time
import json
import httplib, urllib
import os.path as path
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from json import dumps
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

servidor_Must = '192.168.2.xx'
usuario_Must = 'xxxxx'
clave_Must = 'xxxxx'

def ejecutarProceso():
	DatosCargador = '';
	Minutos = time.strftime("%M");
	modbus = ModbusClient(method='rtu', port='/dev/ttyUSB1', baudrate=9600, timeout=1)
	modbus.connect()
	#Datos Cargador
	##################################################################################################################
	r3 = modbus.read_holding_registers(15201, 24, unit=1)
	#print "R3 cargador: "
	#print r3.registers
	#print "\r\n\r\n"
	try:
		rc3 = r3.registers
	except:
		rc3 = range(24)
		for i in range(24):
 			rc3[i] = 0
	time.sleep(0.1)

	#DatosCargador = rc1 + rc2 + rc3
        #print("voltaje bat :" + srt(r3.registers[6]))
        #print r3.registers[5]
	#print DatosCargador
	##################################################################################################################

	#Enviamos datos a MQTT
	##################################################################################################################
        #0 PV input voltage
        #1 Battery voltage
        #2 Charging current
        #5 Charging power
        #6 Unit temperature
        #8 Remote battery temperature
        MustPvVoltage = (float(r3.registers[4])/10)
        MustBatVolt = (float(r3.registers[5])/10)
        MustChargeAmp = r3.registers[6]
        MustChargeWatt = r3.registers[7]
        MustTempUnit = r3.registers[8]
        MustBatTempRemote = r3.registers[9]
        client_Must = paho.Client()
        client_Must.username_pw_set(usuario_Must, clave_Must)
        client_Must.connect(servidor_Must, 1883)
        client_Must.loop_start()
        ############# Must
        client_Must.publish("PVControl/Must/Musttime", time.strftime("%H%M"), qos=1)
        client_Must.publish("PVControl/Must/MustPvVoltage", MustPvVoltage, qos=1)
        client_Must.publish("PVControl/Must/MustBatVolt", MustBatVolt, qos=1)
        client_Must.publish("PVControl/Must/MustChargeAmp", MustChargeAmp, qos=1)
        client_Must.publish("PVControl/Must/MustChargeWatt", MustChargeWatt, qos=1)
        client_Must.publish("PVControl/Must/MustTempUnit", MustTempUnit, qos=1)
        client_Must.publish("PVControl/Must/MustBatTempRemote", MustBatTempRemote, qos=1)
        client_Must.loop_stop() #stop the loop
        time.sleep(1)
        ##################################################################################################################
	modbus.close()

while True:
	try:
		ejecutarProceso()
		time.sleep(3)
	except:
		print "Ha ocurrido un error... continuamos con el proceso..."
		ejecutarProceso()
		time.sleep(3)

#exit()
