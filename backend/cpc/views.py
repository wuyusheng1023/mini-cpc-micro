import sys
import glob
import json
import serial

from django.http import JsonResponse
from django.views import View

port = ''
baudrate = 115200
timeout = 10
ser = serial.Serial()


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/cu.*')
    else:
        raise EnvironmentError('Unsupported platform')

    # result = []
    # for port in ports:
    #     try:
    #         s = serial.Serial(port)
    #         s.close()
    #         result.append(port)
    #     except (OSError, serial.SerialException):
    #         pass
    return ports


class Port(View):
	def get(self, request):
		ports = serial_ports()
		# print(ports)
		return JsonResponse(ports, safe=False)

	def post(self, request):
		global port
		port = json.loads(request.body)['port']
		print(port)
		return JsonResponse({'port': port})


class Connect(View):
	def get(self, request):
		try:
			ser.port = port
			ser.baudrate = baudrate
			ser.timeout = timeout
			ser.open()
			return JsonResponse({'Message': 'Serial opened'})
		except:
			return JsonResponse({'Message': 'Serial open fail'})


class Disonnect(View):
	def get(self, request):
		try:
			ser.close()
			return JsonResponse({'Message': 'Serial closed'})
		except:
			return JsonResponse({'Message': 'Serial close fail'})


class RealTime(View):
	def get(self, request):
		try:
			if ser.is_open:
				data = {
					'SerOpen': True,
					'SerName': ser.name,
				}
				return JsonResponse(data)
			else:
				return JsonResponse({'SerOpen': False})
		except:
			return JsonResponse({'Message': 'Get real time data fail'})


class History(View):
	def get(self, request):
		pass
