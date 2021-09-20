import os
import time
from machine import Pin
import _thread

##################################################
# helper functions
def get_filename():
	dttm = time.localtime(time.time())
	year = dttm[0]
	month = '0' + str(dttm[1]) if dttm[1] < 10 else dttm[1]
	day = '0' + str(dttm[2]) if dttm[2] < 10 else dttm[2]
	filename = f'cpc_{year}{month}{day}.txt'
	return filename

def format_data(dttm, cps):
	year = dttm[0]
	month = '0' + str(dttm[1]) if dttm[1] < 10 else dttm[1]
	day = '0' + str(dttm[2]) if dttm[2] < 10 else dttm[2]
	hour = '0' + str(dttm[3]) if dttm[3] < 10 else dttm[3]
	minute = '0' + str(dttm[4]) if dttm[4] < 10 else dttm[4]
	second = '0' + str(dttm[5]) if dttm[5] < 10 else dttm[5]
	cps = int(cps)
	return f'{year}-{month}-{day} {hour}:{minute}:{second};{cps}'


##################################################
# init
test = True
if test:
	p_test_pulse = Pin(21, Pin.OUT, Pin.PULL_UP)

print('Start...')

n_file = 5
counts = 0
print_data = True
t0 = time.ticks_us()
day0 = time.time() // (60 * 1440)
p_count = Pin(22, Pin.IN)

files = [f for f in os.listdir() if f.endswith('.txt')]
while len(files) >= n_file:
	os.remove(files[0])
	files = os.listdir()

filename = get_filename()
file = open(filename, 'w')


##################################################
# counter
def count(p):
	global counts
	counts += 1

p_count.irq(trigger=Pin.IRQ_FALLING, handler=count)


##################################################
# main
while True:
	time.sleep(0.005)

	if test:
		p_test_pulse.toggle()

	if time.ticks_us() // 1000000 != t0 // 1000000:
		counts_read = counts
		t1 = time.ticks_us()
		if t1 > t0:
			cps = counts_read / ((t1 - t0) / 1000000)
		counts = 0
		t0 = time.ticks_us()
		dttm = time.localtime(time.time())
		data = format_data(dttm, cps)
		if print_data:
			print('--;' + data)
		file.write(data + "\n")
		file.flush()
		timeup = False

	day1 = time.time() // (60 * 1440)
	if day1 > day0:
		files = [f for f in os.listdir() if f.endswith('.txt')]
		while len(files) >= n_file:
			os.remove(files[0])
			files = [f for f in os.listdir() if f.endswith('.txt')]
		file.close()
		filename = get_filename()
		file = open(filename, 'w')
