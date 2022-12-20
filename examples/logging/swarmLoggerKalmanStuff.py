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
    x = data['my_RL_POS.myRLX']
    y = data['my_RL_POS.myRLY']
    z = data['my_RL_POS.myRLYaw']

    rlP00 = data['RL_A.rlP00']
    rlP01 = data['RL_A.rlP01']
    rlP02 = data['RL_A.rlP02']
    rlP10 = data['RL_A.rlP10']
    rlP11 = data['RL_A.rlP11']
    rlP12 = data['RL_A.rlP12']

    rlP20 = data['RL_B.rlP20']
    rlP21 = data['RL_B.rlP21']
    rlP22 = data['RL_B.rlP22']
    rlXp0 = data['RL_B.rlXp0']
    rlYp0 = data['RL_B.rlYp0']
    rlYa0 = data['RL_B.rlYa0']

    rlXp1 = data['RL_C.rlXp1']
    rlYp1 = data['RL_C.rlYp1']
    rlYa1 = data['RL_C.rlYa1']

    update = data['UWB_A.update']
    distance = data['UWB_A.distance']
    velX = data['UWB_A.velX']
    velY = data['UWB_A.velY']
    gyroZ = data['UWB_A.gyroZ']
    height = data['UWB_A.height']
    myVelX = data['UWB_B.myVelX']
    myVelY = data['UWB_B.myVelY']
    myGyroZ = data['UWB_B.myGyroZ']
    myHeight = data['UWB_B.myHeight']

    #print('{}: pos: ({},{},{}) for {}'.format(timestamp, x, y, z, uri))
    with open(desktopPath+timestampProgramStart+'_cf-swarm_positions.csv', 'a') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow([timestamp, uri, x, y, z, rlP00, rlP01, rlP02, rlP10, rlP11, rlP12, rlP20, rlP21, rlP22, rlXp0, rlYp0, rlYa0, rlXp1, rlYp1, rlYa1, update, distance, velX, velY, gyroZ, height, myVelX, myVelY, myGyroZ, myHeight])
    csvfile.close()

    global rlCoordinates
    rlCoordinates[int(uri[-1])] = [x,y]

def start_position_printing(scf):
   
    #if scf.cf.link_uri == 'radio://0/80/2M':
           
    pos_conf = LogConfig(name='pos_conf', period_in_ms=500)
    pos_conf.add_variable('my_RL_POS.myRLX', 'float')
    pos_conf.add_variable('my_RL_POS.myRLY', 'float')
    pos_conf.add_variable('my_RL_POS.myRLYaw', 'float')
    try:
        scf.cf.log.add_config(pos_conf)
        pos_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
        pos_conf.start()
    except BaseException as e:
        print(e)
    

    A_RL_conf = LogConfig(name='A_RL_conf', period_in_ms=500)
    A_RL_conf.add_variable('RL_A.rlP00', 'float')
    A_RL_conf.add_variable('RL_A.rlP01', 'float')
    A_RL_conf.add_variable('RL_A.rlP02', 'float')
    A_RL_conf.add_variable('RL_A.rlP10', 'float')
    A_RL_conf.add_variable('RL_A.rlP11', 'float')
    A_RL_conf.add_variable('RL_A.rlP12', 'float')
    try:
        scf.cf.log.add_config(A_RL_conf)
        A_RL_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
        A_RL_conf.start()
    except BaseException as e:
        print(e)
    
    B_RL_conf = LogConfig(name='B_RL_conf', period_in_ms=500)
    B_RL_conf.add_variable('RL_B.rlP20', 'float')
    B_RL_conf.add_variable('RL_B.rlP21', 'float')
    B_RL_conf.add_variable('RL_B.rlP22', 'float')
    B_RL_conf.add_variable('RL_B.rlXp0', 'float')
    B_RL_conf.add_variable('RL_B.rlYp0', 'float')
    B_RL_conf.add_variable('RL_B.rlYa0', 'float')
    try:
        scf.cf.log.add_config(B_RL_conf)
        B_RL_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
        B_RL_conf.start()
    except BaseException as e:
        print(e)

    C_RL_conf = LogConfig(name='C_RL_conf', period_in_ms=500)
    C_RL_conf.add_variable('RL_C.rlXp1', 'float')
    C_RL_conf.add_variable('RL_C.rlYp1', 'float')
    C_RL_conf.add_variable('RL_C.rlYa1', 'float')
    try:
        scf.cf.log.add_config(B_RL_conf)
        B_RL_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
        B_RL_conf.start()
    except BaseException as e:
        print(e)
    
    A_UWB_conf = LogConfig(name='UWB_conf', period_in_ms=500)
    A_UWB_conf.add_variable('UWB_A.update', 'uint16_t')
    A_UWB_conf.add_variable('UWB_A.distance', 'uint16_t')
    A_UWB_conf.add_variable('UWB_A.velX', 'float')
    A_UWB_conf.add_variable('UWB_A.velY', 'float')
    A_UWB_conf.add_variable('UWB_A.gyroZ', 'float')
    A_UWB_conf.add_variable('UWB_A.height', 'float')
    try:
        scf.cf.log.add_config(A_UWB_conf)
        A_UWB_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
        A_UWB_conf.start()
    except BaseException as e:
        print(e)

    B_UWB_conf = LogConfig(name='UWB_conf', period_in_ms=500)
    B_UWB_conf.add_variable('UWB_B.myVelX', 'float')
    B_UWB_conf.add_variable('UWB_B.myVelY', 'float')
    B_UWB_conf.add_variable('UWB_B.myGyroZ', 'float')
    B_UWB_conf.add_variable('UWB_B.myHeight', 'float')
    try:
        scf.cf.log.add_config(B_UWB_conf)
        B_UWB_conf.data_received_cb.add_callback(lambda t, d, l: position_callback(scf.cf.link_uri, t, d, l))
        B_UWB_conf.start()
    except BaseException as e:
        print(e)

    print("Hey1 Jude")
    
    print(f"Logging started for {scf.cf.link_uri}")
    with open(desktopPath+timestampProgramStart+'_cf-swarm_positions_rawdata.csv', 'a') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        writer.writerow(["timestamp", "uri", "x", "y", "z", "rlP00", "rlP01", "rlP02", "rlP10", "rlP11", "rlP12", "rlP20", "rlP21", "rlP22", "rlXp0", "rlYp0", "rlYa0", "rlXp1", "rlYp1", "rlYa1", "update", "distance", "velX", "velY", "gyroZ", "height", "myVelX", "myVelY", "myGyroZ", "myHeight"])
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