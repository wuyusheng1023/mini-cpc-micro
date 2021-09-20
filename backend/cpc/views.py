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

# ser.port(port)
# ser.baudrate(baudrate)
# ser.timeout(timeout)

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
		port = request.POST['port']
		return JsonResponse({'port': port})


class Connect(View):
	def get(self, request):
		pass


class Disonnect(View):
	def get(self, request):
		pass


class RealTime(View):
	def get(self, request):
		pass


class History(View):
	def get(self, request):
		pass
