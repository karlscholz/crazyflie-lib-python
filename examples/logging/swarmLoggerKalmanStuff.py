# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017-2018 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

#20221213KS

"""
"""
import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

from cflib.crazyflie.log import LogConfig
import logging
import csv
import datetime

import numpy as np
from matplotlib import pyplot as plt

import os
desktopPath = os.path.join(os.environ['USERPROFILE'])+"\\" # Get the desktop path on WINDOWS

timestampProgramStart = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

rlCoordinates = np.array([
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ], dtype = float)

# List of URIs, comment the one you do not want to fly
#CHECK THE USB DEVICE NUMBER IF YOU'RE USING IT WITH CFCLIENT
uris = {
    #'radio://0/80/2M/E7E7E7E7E0', #comment out to be able to connect via cfclient
    'radio://1/80/2M/E7E7E7E7E1', 
    #'radio://1/80/2M/E7E7E7E7E2',
    #'radio://1/80/2M/E7E7E7E7E3',
}

def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print(f"Parameters downloaded for{scf.cf.link_uri}")

def position_callback(uri, timestamp, data, logconf):
    rlP00 = data['AA_relativelocalization.rlP00']
    rlP01 = data['AA_relativelocalization.rlP01']
    rlP02 = data['AA_relativelocalization.rlP02']
    rlP10 = data['AA_relativelocalization.rlP10']
    rlP11 = data['AA_relativelocalization.rlP11']
    rlP12 = data['AA_relativelocalization.rlP12']
    rlP20 = data['AA_relativelocalization.rlP20']
    rlP21 = data['AA_relativelocalization.rlP21']
    rlP22 = data['AA_relativelocalization.rlP22']
    rlXp0 = data['AA_relativelocalization.rlXp0']
    rlYp0 = data['AA_relativelocalization.rlYp0']
    rlYa0 = data['AA_relativelocalization.rlYa0']
    rlXp1 = data['AA_relativelocalization.rlXp1']
    rlYp1 = data['AA_relativelocalization.rlYp1']
    rlYa1 = data['AA_relativelocalization.rlYa1']

    update = data['AA_ranging.update']
    distance = data['AA_ranging.distance']
    velX = data['AA_ranging.velX']
    velY = data['AA_ranging.velY']
    gyroZ = data['AA_ranging.gyroZ']
    height = data['AA_ranging.height']
    myVelX = data['AA_ranging.myVelX']
    myVelY = data['AA_ranging.myVelY']
    myGyroZ = data['AA_ranging.myGyroZ']
    myHeight = data['AA_ranging.myHeight']

    #print('{}: pos: ({},{},{}) for {}'.format(timestamp, x, y, z, uri))
    with open(desktopPath+timestampProgramStart+'_cf-swarm_positions.csv', 'a') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow([timestamp, uri, rlP00, rlP01, rlP02, rlP10, rlP11, rlP12, rlP20, rlP21, rlP22, rlXp0, rlYp0, rlYa0, rlXp1, rlYp1, rlYa1, update, distance, velX, velY, gyroZ, height, myVelX, myVelY, myGyroZ, myHeight])
    csvfile.close()

    global rlCoordinates
    rlCoordinates[int(uri[-1])] = [x,y]

def start_position_printing(scf):
   
    #if scf.cf.link_uri == 'radio://0/80/2M':
           
    log_conf = LogConfig(name='Kalmanstuff', period_in_ms=500)
    log_conf.add_variable('AA_relativelocalization.rlP00', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP01', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP02', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP10', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP11', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP12', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP20', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP21', 'float')
    log_conf.add_variable('AA_relativelocalization.rlP22', 'float')
    log_conf.add_variable('AA_relativelocalization.rlXp0', 'float')
    log_conf.add_variable('AA_relativelocalization.rlYp0', 'float')
    log_conf.add_variable('AA_relativelocalization.rlYa0', 'float')
    log_conf.add_variable('AA_relativelocalization.rlXp1', 'float')
    log_conf.add_variable('AA_relativelocalization.rlYp1', 'float')
    log_conf.add_variable('AA_relativelocalization.rlYa1', 'float')
    
    log_conf.add_variable('AA_ranging.update', 'uint16')
    log_conf.add_variable('AA_ranging.distance', 'uint16')
    log_conf.add_variable('AA_ranging.velX', 'float')
    log_conf.add_variable('AA_ranging.velY', 'float')
    log_conf.add_variable('AA_ranging.gyroZ', 'float')
    log_conf.add_variable('AA_ranging.height', 'float')
    log_conf.add_variable('AA_ranging.myVelX', 'float')
    log_conf.add_variable('AA_ranging.myVelY', 'float')
    log_conf.add_variable('AA_ranging.myGyroZ', 'float')
    log_conf.add_variable('AA_ranging.myHeight', 'float')


    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
    log_conf.start()
    print(f"Logging started for {scf.cf.link_uri}")
    with open(desktopPath+timestampProgramStart+'_cf-swarm_positions.csv', 'a') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow("timestamp, uri, rlP00, rlP01, rlP02, rlP10, rlP11, rlP12, rlP20, rlP21, rlP22, rlXp0, rlYp0, rlYa0, rlXp1, rlYp1, rlYa1, update, distance, velX, velY, gyroZ, height, myVelX, myVelY, myGyroZ, myHeight")
    csvfile.close()
    

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers()

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # If the copters are started in their correct positions this is
        # probably not needed. The Kalman filter will have time to converge
        # any way since it takes a while to start them all up and connect. We
        # keep the code here to illustrate how to do it.
        # swarm.reset_estimators()

        # The current values of all parameters are downloaded as a part of the
        # connections sequence. Since we have 10 copters this is clogging up
        # communication and we have to wait for it to finish before we start
        # flying.
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)
        swarm.parallel(start_position_printing)
        print("logging...")
        plt.ion()
        d = 5
        while(True):
            #while(True) not just for plot, but also to keep the programm running for the callback function
            plt.axis([d, -d, -d, d]) # horizontal axis is inverted, cause Y axis of aircraft increases to the left when X goes forward and Z up
            
            E0XCoord, E0YCoord = rlCoordinates[0]
            plt.scatter(E0XCoord,E0YCoord, color='black', label='E0')
            E1XCoord, E1YCoord = rlCoordinates[1]
            plt.scatter(E1XCoord,E1YCoord, color='red', label='E1')
            E2XCoord, E2YCoord = rlCoordinates[2]
            plt.scatter(E2XCoord,E2YCoord, color='green', label='E2')
            E3XCoord, E3YCoord = rlCoordinates[3]
            plt.scatter(E3XCoord,E3YCoord, color='blue', label='E3')
            
            plt.legend()
            plt.pause(.32)
            plt.clf()