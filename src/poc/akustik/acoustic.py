import time
from pygame import mixer

'''
Document by: Joel Grepper
Purpose: Testing acoustic functionality of python libraries with raspberry and 3rd party speakers
Date: 24.10.18
State: TBD
Comment: 
Converting via Sound() only possible with .wav files
Conversions available via: https://www.text2speech.org/de.html
'''

print('start')

def main():

    mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
    mixer.init() #turn all of pygame on.
    mixer.music.set_volume(0.5)
    print(mixer.get_init())

    mixer.music.load('Soundfiles/E9.mp3')
    print('playing mp3 in main')
    mixer.music.play()
    #play() is asynchronous and will stop as soon as the programm ends
    time.sleep(2)
    mixer.music.stop()

    #loading .mp3 via Sound() currently not working
    #testSoundMp3 = mixer.Sound('Soundfiles/E9.mp3')
    testSoundWav = mixer.Sound('Soundfiles/E9.wav')

    #testSoundMp3.play()
    print('playing wav in main')
    testSoundWav.play()
    mixer.music.play()
    time.sleep(2)
    mixer.music.stop()


def play_sound_by_number(number):
    my_soundfile = 'Soundfiles/E' + str(number) + '.mp3'
    print(my_soundfile)
    mixer.music.load(my_soundfile)
    print('playing dynamic mp3 in play_sound_by_number')
    mixer.music.play()
    time.sleep(2)
    mixer.music.stop()


def buzz_by_number(number):
    print('buzzing ' + str(number) + ' times')
    for i in range(number):
        print('bzzzz')




main()
play_sound_by_number(1)
buzz_by_number(5)
print('finish')
