from src.raspi.lib import log

logger = log.getLogger("SoulTrain.controlflow.phases.phase")

phases = {}

class Phase(object):
    def __init__(self, name, method, next_phase_key):
        self.name = name
        self.method = method
        self.next_phase_key = next_phase_key
        self.msg = "init"

        phases[self.name] = self

    def run(self, middleware_data):
        '''
        run the current phase
        - returns a phase (maybe next phase if method was successful)
        '''

        #method has to return empty string! (string is otherwise the log message)
        result = "" #suppose we don't have to run the method
        if self.name in middleware_data['phases'].keys() and middleware_data['phases'][self.name] is True:
            logger.info("running phase: " + self.name)
            result = self.method(middleware_data)

        self.msg = result

        if result in "":
            if self.next_phase_key in phases.keys():
                logger.info("select next phase: " + self.next_phase_key)
                return phases[self.next_phase_key]

            logger.info("no next phase: " + self.next_phase_key)
            return None

        logger.info("still not finished: " + self.next_phase_key)
        return self

    def get_name(self):
        return self.name

    def get_msg(self):
        return self.msg
