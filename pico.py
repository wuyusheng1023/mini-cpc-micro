import time
from machine import Pin
import _thread


test = True

print('Start...')

global counts
counts = 0
t0 = time.ticks_us()
p_count = Pin(22, Pin.IN)

if test:
	p_test_pulse = Pin(21, Pin.OUT, Pin.PULL_UP)


def count(p):
	global counts
	counts += 1

p_count.irq(trigger=Pin.IRQ_FALLING, handler=count)


def format_data(dttm, cps):
	year = dttm[0]
	month = '0' + str(dttm[1]) if dttm[1] < 10 else dttm[1]
	day = '0' + str(dttm[2]) if dttm[2] < 10 else dttm[2]
	hour = '0' + str(dttm[3]) if dttm[3] < 10 else dttm[3]
	minute = '0' + str(dttm[4]) if dttm[4] < 10 else dttm[4]
	second = '0' + str(dttm[5]) if dttm[5] < 10 else dttm[5]
	cps = int(cps)
	return f'{year}-{month}-{day} {hour}:{minute}:{second};{cps}'


while True:
	time.sleep(0.005)

	if test:
		p_test_pulse.toggle()

	if time.ticks_us() // 1000000 != t0 // 1000000:
		global counts
		counts_read = counts
		t1 = time.ticks_us()
		if t1 > t0:
			cps = counts_read / ((t1 - t0) / 1000000)
		counts = 0
		t0 = time.ticks_us()
		dttm = time.localtime(time.time())
		data = format_data(dttm, cps)
		print(data)
		timeup = False

	if 