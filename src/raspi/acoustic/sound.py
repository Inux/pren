import pyttsx3

class Sound:

    def play_sound_by_number(number):
        engine = pyttsx3.init()
        engine.say('Number ' + str(number))
        print('start playing')
        engine.runAndWait()
        print('stopped playing')

    def buzz_by_number(number):
        print('buzzing ' + str(number) + ' times')
        for i in range(number):
            print('bzzzz')

