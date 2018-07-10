#!/usr/bin/env python3
import socket
import struct
import math
import matplotlib.pyplot as plt
# import numpy as np
# import pyformulas as pf

pkt = ['header', 'daddr', 'lsaddr', 'mlen', 'gid', 'hid',
 		'nid', 'temp', 'hum', 'lum']

def update(hl, data):
	hl.set_ydata(data)
	plt.draw()

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

	fig = plt.figure()
	# canvas = np.zeros((480,640))
	# screen = pf.screen(canvas, 'Figura')

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
		sck.connect((ip, pn))
		sck.recv(128)
		sck.send(b'U ')
		plt.ion()
		fig = plt.figure()
		a1 = fig.add_subplot(1,3,1)
		line1, = a1.plot(list(range(100)), [0]*100)

		a2 = fig.add_subplot(2,3,1)
		line2, = a2.plot(list(range(100)), [0]*100)

		a3 = fig.add_subplot(3,3,1)
		line3, = a3.plot(list(range(100)), [0]*100)
		while(True):
			data = sck.recv(1)
			data = sck.recv(16)
			if(len(data) != 1):
				# print(len(data))
				recv_data = struct.unpack(">BHHBBBHHHH", data)
				c = convert(recv_data)
				# [('header', 0), ('daddr', 65535), ('lsaddr', 1), ('mlen', 8), ('gid', 34), ('hid', 1), ('nid', 1), ('temp', 27.729), ('hum', 48.286), ('lum', 14)]
				if(c[6][1] in samples):
					samples[c[6][1]]["tem"].append(c[7][1])
					samples[c[6][1]]["hum"].append(c[8][1])
					samples[c[6][1]]["lum"].append(c[9][1])
				else:
					samples[c[6][1]] = {}
					samples[c[6][1]]["tem"] = ([1] * 100) + [c[7][1]]
					samples[c[6][1]]["hum"] = ([1] * 100) + [c[8][1]]
					samples[c[6][1]]["lum"] = ([1] * 100) + [c[9][1]]

				length = len(samples.keys())
				counter = length*3
				for id in samples.keys():
					for i in range(1, counter + 1, 3):
						# plt.subplot(3, length, i)
						line1.set_ydata(samples[id]["tem"][-100:])

						# plt.subplot(3, length, i + 1)
						line2.set_ydata(samples[id]["hum"][-100:])

						# plt.subplot(3, length, i + 2)
						line3.set_ydata(samples[id]["lum"][-100:])
				fig.canvas.draw()

				# plt.show()

				# fig.canvas.draw()
				# image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
				# image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
                #
				# screen.update(image)

if __name__ == '__main__':
	main()
