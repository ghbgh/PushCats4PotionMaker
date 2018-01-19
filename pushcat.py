"""

A simple 'push cat' ('tap cat'?) for game 'potion maker'
Stupid but powerful
Authored by curs0r, 2018.1.19

"""
import subprocess
from subprocess import Popen, PIPE
import time
import random
from time import sleep

class PushCat():
	def __init__(self):
		cmd = "adb shell"
		self.process = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE)
		print("creating process")

	def _writeline(self, str):
		print(str)
		self.process.stdin.write((str + '\r\n').encode("utf-8"))
		self.process.stdin.flush()

	def _readline(self):
	# not used
		b = self.process.stdout.readline()
		return b.decode("utf-8").strip('\r\n')

	def tap(self, x=215, y=500, dx=15, dy=50, z=30, dz=10):
	# x: top, y: left
	# use a random offset to cheat the game, otherwise 
		x1 = x + random.randint(-dx,dx)
		y1 = y + random.randint(-dy,dy)
		x2 = x1 + random.randint(-10,10)
		y2 = y1 + random.randint(-10,10)
		z += random.randint(-dz,dz)
		#self._writeline("input swipe %d %d %d %d %d&&echo newline"%(y1, x2, y2, x2, z))
		self._writeline("input tap %d %d&&echo newline"%(y1, x2))
		# must stop for a while, otherwise too much input will overfill the process
		#sleep(z/1000.0+0.001 )
	
	def	wait_one(self):
		self._readline()

	def loopTap(self, x=215, y=500, dx=15, dy=50):
		self._writeline("while true\r\n"
					  + "do\r\n"
					  + ("x=`expr %d + $RANDOM %% %d`\r\n"%(x,dx))
					  + ("y=`expr %d + $RANDOM %% %d`\r\n"%(y,dy))
					  + "input tap $y.$RANDOM $x.$RANDOM\r\n"
					  + "done")
	
	def terminateAll(self):
		#
		self._writeline("ps|grep shell|grep /system/bin/sh|while read LINE\r\n"
					  + "do\r\n"
					  + "PID=`echo $LINE|sed 's/shell \\([0-9]*\\) .*/\\1/'`\r\n"
					  + "if [[ $$ != $PID ]] then\r\n"
					  + "echo $PID\r\n"
					  + "kill $PID\r\n"
					  + "fi\r\n"
					  + "done")

	def __del__(self):
		self._writeline("\x03") # ctrl+c
		#self._writeline("exit")
		self.process.terminate()

# you can make this value bigger if not fast enough
# but too much will slow down performance
N_CATS = 9

def main(terminate=False):
	endcat = PushCat()
	if terminate:
		endcat.terminateAll()
		while True:
			line = endcat._readline()
			if line != "":
				print(endcat._readline())

	cats = [PushCat() for _ in range(N_CATS)]
	print("use Ctrl+C to stop")

	for i in range(len(cats)):
		cats[i].loopTap(220,350+i*450/N_CATS,20,50)
		sleep(0.02)
	input("press any key to stop")

	#
	endcat.terminateAll()
	sleep(1)
	exit()

	# start = False
	# try:
	# 	while True:
	# 		for i in range(len(cats)):
	# 			for j in range(5):
	# 				cats[i].tap(220,280+i*360/N_CATS,20,50)
	# 		if start:
	# 			for i in range(len(cats)):
	# 				for j in range(5):
	# 					cats[i].wait_one()
	# 		start = True
			
	# 		#__=input('press any key to continue: ')
	# except KeyboardInterrupt as e:
	# 	pass
	# finally:
	# 	# force all shell quit
	# 	endcat.terminateAll()
	# 	sleep(5)
	# 	exit()

if __name__ == "__main__":
	main()