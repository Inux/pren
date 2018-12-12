#!/usr/bin/env python
#---------------------------------------------------
#
#	This is a program for Passive Buzzer Module
#		It will play simple songs.
#	You could try to make songs by youselves!
# 
#		Passive buzzer 			   Pi 
#			VCC ----------------- 3.3V
#			GND ------------------ GND
#			SIG ---------------- Pin 11
#
#---------------------------------------------------

import RPi.GPIO as GPIO
import time

Buzzer = 11

#FREQUENCIES for song 1, 2
CL = [0, 131, 147, 165, 175, 196, 211, 248]		# Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]		# Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]		# Frequency of High C notes

#FREQUENCIES
cL = 129
cLS 139
dL 146
dLS 156
eL 163
fL 173
fLS 185
gL 194
gLS 207
aL 219
aLS 228
bL 232

c 261
cS 277
d 294
dS 311
e 329
f 349
fS 370
g 391
gS 415
a 440
aS 455
b 466

cH 523
cHS 554
dH 587
dHS 622
eH 659
fH 698
fHS 740
gH 784
gHS 830
aH 880
aHS 910
bH 933

song_1 = [	CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
			CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
			CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
			CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5]	]

beat_1 = [	1, 1, 3, 1, 1, 3, 1, 1, 			# Beats of song 1, 1 means 1/8 beats
			1, 1, 1, 1, 1, 1, 3, 1, 
			1, 3, 1, 1, 1, 1, 1, 1, 
			1, 2, 1, 1, 1, 1, 1, 1, 
			1, 1, 3	]

song_2 = [	CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
			CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
			CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
			CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]	]

beat_2 = [	1, 1, 2, 2, 1, 1, 2, 2, 			# Beats of song 2, 1 means 1/8 beats
			1, 1, 2, 2, 1, 1, 3, 1, 
			1, 2, 2, 1, 1, 2, 2, 1, 
			1, 2, 2, 1, 1, 3 ]
			
imperial_march_song = [	a, a, f, cH, 
						a, f, cH, a, eH, 
						eH, eH, fH, cH, gS, 
						f, cH, a, aH, a, 
						a, aH, gHS, gH, fHS, 
						fH, fHS]

imperial_march_beat = [	500, 500, 350, 150,
						500, 350, 150, 1000, 500, 
						500, 500, 350, 150, 500, 
						350, 150, 1000, 500, 350, 
						150, 500, 250, 250, 125, 
						125, 125]

'''
  beep( a, 500);
  beep( a, 500);
  beep( f, 350);
  beep( cH, 150);

  beep( a, 500);
  beep( f, 350);
  beep( cH, 150);
  beep( a, 1000);
  beep( eH, 500);

  beep( eH, 500);
  beep( eH, 500);
  beep( fH, 350);
  beep( cH, 150);
  beep( gS, 500);

  beep( f, 350);
  beep( cH, 150);
  beep( a, 1000);
  beep( aH, 500);
  beep( a, 350);

  beep( a, 150);
  beep( aH, 500);
  beep( gHS, 250);
  beep( gH, 250);
  beep( fHS, 125);

  beep( fH, 125);
  beep( fHS, 250);

  delay(250);

  beep( aS, 250);
  beep( dHS, 500);
  beep( dH, 250);
  beep( cHS, 250);
  beep( cH, 125);

  beep( b, 125);
  beep( cH, 250);

  delay(250);

  beep( f, 125);
  beep( gS, 500);
  beep( f, 375);
  beep( a, 125);
  beep( cH, 500);

  beep( a, 375);
  beep( cH, 125);
  beep( eH, 1000);
  beep( aH, 500);
  beep( a, 350);

  beep( a, 150);
  beep( aH, 500);
  beep( gHS, 250);
  beep( gH, 250);
  beep( fHS, 125);

  beep( fH, 125);
  beep( fHS, 250);

  delay(250);

  beep( aS, 250);
  beep( dHS, 500);
  beep( dH, 250);
  beep( cHS, 250);
  beep( cH, 125);

  beep( b, 125);
  beep( cH, 250);

  delay(250);

  beep( f, 250);
  beep( gS, 500);
  beep( f, 375);
  beep( cH, 125);
  beep( a, 500);

  beep( f, 375);
  beep( c, 125);
  beep( a, 1000);
'''

def setup():
	GPIO.setmode(GPIO.BOARD)		# Numbers GPIOs by physical location
	GPIO.setup(Buzzer, GPIO.OUT)	# Set pins' mode is output
	global Buzz						# Assign a global variable to replace GPIO.PWM 
	Buzz = GPIO.PWM(Buzzer, 440)	# 440 is initial frequency.
	Buzz.start(50)					# Start Buzzer pin with 50% duty ration

def loop():
	while True:
		print '\n    Playing song 1...'
		for i in range(1, len(song_1)):		# Play song 1
			Buzz.ChangeFrequency(song_1[i])	# Change the frequency along the song note
			time.sleep(beat_1[i] * 0.5)		# delay a note for beat * 0.5s
		time.sleep(1)						# Wait a second for next song.

		print '\n\n    Playing song 2...'
		for i in range(1, len(song_2)):     # Play song 1
			Buzz.ChangeFrequency(song_2[i]) # Change the frequency along the song note
			time.sleep(beat_2[i] * 0.5)     # delay a note for beat * 0.5s
			
def imperial_march():
	while True:
		print 'playing imperial march from starwars'
		for i in range(1, len(imperial_march_song)):
			Buzz.ChangeFrequency(imperial_march_song[i])
			time.sleep(imperial_march_beat[i] / 1000)		#python time.sleep() takes seconds

def destory():
	Buzz.stop()					# Stop the buzzer
	GPIO.output(Buzzer, 1)		# Set Buzzer pin to High
	GPIO.cleanup()				# Release resource

if __name__ == '__main__':		# Program start from here
	setup()
	try:
		imperial_march()
		#loop()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destory()
