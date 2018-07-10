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
	# for i in len(pkt):
		# d[pkt[i]] =
	return list(zip(pkt,data[:7]+(temp,) + (hum,) + data[9:]))

def main(ip='192.168.100.112',pn=44000):
	samples = {}
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
				c = convert(recv_data)
				# [('header', 0), ('daddr', 65535), ('lsaddr', 1), ('mlen', 8), ('gid', 34), ('hid', 1), ('nid', 1), ('temp', 27.729), ('hum', 48.286), ('lum', 14)]
				if(c[6][1] in samples):
					samples[c[6][1]]["tem"].append(c[7][1])
					samples[c[6][1]]["hum"].append(c[8][1])
					samples[c[6][1]]["lum"].append(c[9][1])
				else:
					samples[c[6][1]] = {}
					samples[c[6][1]]["tem"] = [c[7][1]]
					samples[c[6][1]]["hum"] = [c[8][1]]
					samples[c[6][1]]["lum"] = [c[9][1]]
				print(samples)

if __name__ == '__main__':
	main()
