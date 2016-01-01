import requests


class FoscamExcept(Exception):
    pass

class Foscam(object):
    '''Class to manage Foscam FI8910W Securitty Camera. May work with others
    foscam models. This is based on their CGI API.
    Foscam CGI API documentation: http://www.foscam.es/descarga/ipcam_cgi_sdk.pdf.'''

    def __init__(self, hostname, username, password, port=80):
        '''Init foscam object.'''

        self.hostname   = hostname
        self.username   = username
        self.password   = password
        self.port       = port
        self.parameters = {}
        self.__get_params()


    def __get_params(self):
        '''Get camera's paremets.'''

        url = "http://{host}:{port}/get_params.cgi".format(host=self.hostname,
                                                           port=self.port)
        url_params = {'user' : self.username,
                      'pwd'  : self.password }
        get_request = requests.get(url, params=url_params)
        if get_request.status_code != 200:
            raise FoscamExcept('Got a non 200 response from camera while trying to get parameters.')

        raw_params  = get_request.text.split(';\n')
        for param in raw_params:
            param_list = param.split("=")
            if len(param_list) > 1:
                name = param_list[0]
                if 'var ' in name:
                    name = name[4:]
                value = param_list[1]
                self.parameters[name] = value 

    def is_motion_on(self):
        '''Returns True if camera motion detection is armed.
        Uses self.paremeters['alarm_motion_armed'] to determine if camera is arrmed.
        '''

        if 'alarm_motion_armed' in self.parameters:
            return bool(int(self.parameters['alarm_motion_armed']))
        return False
    
    def motion_on(self):
        '''Turns on motion detection.'''

        url = "http://{host}:{port}/set_alarm.cgi".format(host=self.hostname, port=self.port)
        params = {'user'            : self.username,
                  'pwd'             : self.password,
                  'motion_armed'    : 1
                  }
        alarm_request = requests.get(url, params=params)
        if alarm_request.status_code == 200:
            print "{hostname} : Got 200 status code for alarm on.".format(hostname=self.hostname)
            self.__get_params()
            if self.is_motion_on():
                print "{hostname} : Confirmed alarm is on.".format(hostname=self.hostname)
                return True
            print "{hostname} : Warning Unable to confirmed alarm is On.".format(hostname=self.hostname)
        else:
            print "{hostname} : Warning alarm was not enabled  : HTTP {code} ".format(hostname=self.hostname, code=alarm_request.status_code)
        return False
        

    def motion_off(self):
        '''Turns on motion detection.'''

        url = "http://{host}:{port}/set_alarm.cgi".format(host=self.hostname, port=self.port)
        params = {'user'            : self.username,
                  'pwd'             : self.password,
                  'motion_armed'    : 0
                  }
        alarm_request = requests.get(url, params=params)
        if alarm_request.status_code == 200:
            print "{hostname} : Got 200 status code for alarm off.".format(hostname=self.hostname)
            self.__get_params()
            if not self.is_motion_on():
                print "{hostname} : Confirmed alarm is Off.".format(hostname=self.hostname)
                return True
            print "{hostname} : Warning Unable to confirmed alarm is Off.".format(hostname=self.hostname)
        else:
            print "{hostname} : Unable to disable alarm : HTTP {code} ".format(hostname=self.hostname, code=alarm_request.status_code)
        return False
        

