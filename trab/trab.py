#!/usr/bin/env python3
import socket
import struct
import math

pkt = ['header', 'daddr', 'lsaddr', 'mlen', 'gid', 'hid',
 		'nid', 'temp', 'hum', 'lum']

def humidity(temp,hv):
	return (-2.0468+0.0367*float(hv) - 0.0000015955*math.pow(float(hv),2.0)) + (temp-25)*(0.01+0.00008*float(hv))

def convert(data):
	temp = (float(data[7])*0.01) - 39.4
	hum = humidity(temp,data[8])
	for i in pkt:
		d[i] =
	#  (float(data[8])*0.0367)-2.0468-0.0000015955*math.pow(float(data[8]),2.0)+

def main(ip='192.168.100.112',pn=44000):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
		sck.connect((ip, pn))
		sck.recv(128)
		sck.send(b'U ')
		while(True):
			data = sck.recv(128)
			if(len(data) != 1):
				# print(data, len(data))
				# print(data.hex())
				recv_data = struct.unpack(">BHHBBBHHHH", data)
				print(convert(recv_data),'\n')

if __name__ == '__main__':
	main()
