import pyttsx3

'''
Document by: Joel Grepper
Purpose: Testing acoustic functionality of python libraries with raspberry and 3rd party speakers
Date: 24.10.18
State: TBD
Comment: 
'''

def main():
    print('main')


def play_sound_by_number(number):
    engine = pyttsx3.init()
    engine.say('Number ' + str(number))
    engine.runAndWait()


def buzz_by_number(number):
    print('buzzing ' + str(number) + ' times')
    for i in range(number):
        print('bzzzz')


main()
play_sound_by_number(1)
buzz_by_number(5)
print('finish')
