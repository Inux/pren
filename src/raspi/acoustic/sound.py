import pyttsx3

class Sound:
    @staticmethod
    def play_sound_by_number(number):
        engine = pyttsx3.init()
        engine.say('Number ' + str(number))
        print('start playing')
        engine.runAndWait()
        print('stopped playing')

    @staticmethod
    def buzz_by_number(number):
        print('buzzing ' + str(number) + ' times')
        for i in range(number):
            print('bzzzz')

