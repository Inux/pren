from src.raspi.lib import log

logger = log.getLogger("SoulTrain.controlflow.phases.phase")

phases = {}

class Phase(object):
    def __init__(self, name, method, next_phase_key):
        self.name = name
        self.method = method
        self.next_phase_key = next_phase_key
        self.msg = 'init' # method not executed so far ("" if method is successful, "any string" if method needs to be executed again)

        phases[self.name] = self

    def run(self, middleware_data):
        '''
        run the current phase
        - returns a phase (maybe next phase if method was successful)
        '''

        #method has to return empty string! (string is otherwise the log message)
        if self.name in middleware_data['phases'].keys() and middleware_data['phases'][self.name] is True:
            logger.info("running phase: " + self.name)
            self.msg = self.method(middleware_data)

            if self.msg is None or self.msg in "":
                self._set_msg('init')
                return self._get_next(middleware_data)

            #we received a msg therefore we run again the same method
            return self

        else:
            #select next phase and therefore next method
            self._set_msg('init')
            return self._get_next(middleware_data)

    def get_name(self):
        return self.name

    def get_msg(self):
        return self.msg

    def _set_msg(self, msg):
        self.msg = msg

    def _get_next(self, middleware_data):
        #select the next if the next is executable
        if self.next_phase_key in phases.keys() and middleware_data['phases'][self.next_phase_key] is True:
            logger.info("select next phase and set to init: " + self.next_phase_key)
            phases[self.next_phase_key]._set_msg('init')
            return phases[self.next_phase_key]

        #return the next of the next one if it is not executable
        if self.next_phase_key in phases.keys():
            logger.info("select next of next phase: " + self.next_phase_key)
            return phases[self.next_phase_key]._get_next(middleware_data)

        #return none phase
        logger.info("no next phase: " + self.next_phase_key)
        self._set_msg('init')
        return None
