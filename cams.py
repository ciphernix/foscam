#!/usr/bin/python
import datetime
import urllib2
import sys
from settings import *
from Foscam import Foscam
from simplisafe import SimpliSafe


def get_exceptions():
    '''Returns a list of dates for which the cam should not be on.
    dates should be stored one per lind in the format m-d-yyyy, e.g.: 2-16-2015'''
    
    try:
        with open('date_except', 'r') as efile:
            dates = []
            for line in efile.readlines():
                dates.append(line.strip())
        return dates
    except IOError as error:
        print('Unable to open exception file: {0}'.format(error))
        return []
        
   
def is_workhours():
    '''Returns true if working hours.
    Working hours are defined as 7:45am to 6:45PM Mon-Friday.
    '''

    now = datetime.datetime.now()
    weekday = now.weekday()
    hour = now.hour 
    minute = now.minute 
    #return True
    
    str_now = '{month}-{day}-{year}'.format(month=now.month, day=now.day, year=now.year)
    date_exceptions = get_exceptions()
    if str_now in date_exceptions:
        print('Found exception {0}'.format(str_now))
        return False 
    if weekday < 5: #is monday - Friday
        if hour >= 6 and hour <= 18: 
            if hour == 6 and minute < 45: 
                return False
            elif hour == 18 and minute > 05: 
                return False
            else:
                return True
    return False

def alarm_is_on():
    '''Returns True is alarm is not in off of home mode.'''
    
    try:
        alarm = SimpliSafe()
        alarm.login(ALARM_USER, ALARM_PASSWORD)
        alarm.get_location()
        state = alarm.get_state()
        alarm.logout()
        state = state.lower()
        if state == 'off':
            return False
        if state == 'home':
            return False
        return True 
    except Exception as why:
        print "Error getting alarm status {0}".format(why)
        return True


def main():
    '''Main function.''' 
    cam_list = []
    for cam_name in CAMERAS.keys():
        cam = Foscam(cam_name, CAM_USER, CAM_PASSWORD, port=CAMERAS[cam_name]['port'])
        cam_list.append(cam)
     
    if is_workhours() or alarm_is_on():
        #Make sure camera is on
        print "Turning on motion detection on all cameras."
        for cam in cam_list:
            if not cam.is_motion_on():
                cam.motion_on()
    else:
        #Make sure camera is off
        print "Turning off motion detection on all cameras."
        for cam in cam_list:
            if cam.is_motion_on():
                cam.motion_off()


if __name__ == "__main__":
    main()

