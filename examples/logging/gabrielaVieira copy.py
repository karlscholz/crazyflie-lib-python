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
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.

"""
Swarm
"""

import time
import csv
import datetime
import numpy as np

import cflib.crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.syncLogger import SyncLogger

# Change uris and sequences according to your setup
URI1 = 'radio://0/80/2M/E7E7E7E7E0'
URI2 = 'radio://0/80/2M/E7E7E7E7E1'

# Inútil. Esta aqui apenas para enviar uma informação, que não será utilizada. A trajetória já está armazenada no CF
sequence1 = [
    (-0.7,-1.2,0.8,2),
    (-0.7,0.0,0.8,2),
]
sequence2 = [
    (-0.7,0.0,0.8,2),
    (-0.7,1.5,0.8,2),
]

seq_args = {
    URI1: [sequence1],
    URI2: [sequence2],    
}

# List of URIs, comment the one you do not want to fly
uris = {
    URI1,
    URI2,    
}

x1_vetor = []
y1_vetor = []
z1_vetor = []
x2_vetor = []
y2_vetor = [] 
z2_vetor = []
roll1_vetor = []
pitch1_vetor = []
yaw1_vetor = []
roll2_vetor = []
pitch2_vetor = []
yaw2_vetor = []
leitura = 0

def wait_for_position_estimator(scf):
    print('Waiting for estimator to find position...')

    log_config = LogConfig(name='Kalman Variance', period_in_ms=100)
    log_config.add_variable('kalman.varPX', 'float')
    log_config.add_variable('kalman.varPY', 'float')
    log_config.add_variable('kalman.varPZ', 'float')

    var_y_history = [1000] * 10
    var_x_history = [1000] * 10
    var_z_history = [1000] * 10

    threshold = 0.001

    with SyncLogger(scf, log_config) as logger:
        for log_entry in logger:
            data = log_entry[1]

            var_x_history.append(data['kalman.varPX'])
            var_x_history.pop(0)
            var_y_history.append(data['kalman.varPY'])
            var_y_history.pop(0)
            var_z_history.append(data['kalman.varPZ'])
            var_z_history.pop(0)

            min_x = min(var_x_history)
            max_x = max(var_x_history)
            min_y = min(var_y_history)
            max_y = max(var_y_history)
            min_z = min(var_z_history)
            max_z = max(var_z_history)

            # print("{} {} {}".
            #       format(max_x - min_x, max_y - min_y, max_z - min_z))

            if (max_x - min_x) < threshold and (
                    max_y - min_y) < threshold and (
                    max_z - min_z) < threshold:
                break


def reset_estimator(scf):
    cf = scf.cf
    cf.param.set_value('kalman.resetEstimation', '1')
    time.sleep(0.1)
    cf.param.set_value('kalman.resetEstimation', '0')

    wait_for_position_estimator(cf)
    

def activate_high_level_commander(scf):
    scf.cf.param.set_value('commander.enHighLevel', '1')


def activate_controller(scf):
    # 1-PID 2-Mellinger
    controller = 2
    scf.cf.param.set_value('stabilizer.controller', controller)

def run_sequence(scf, args_dict=seq_args):

    global x1_vetor
    global y1_vetor
    global z1_vetor
    global x2_vetor
    global y2_vetor
    global z2_vetor
    global leitura
    global roll1_vetor 
    global pitch1_vetor
    global yaw1_vetor
    global roll2_vetor
    global pitch2_vetor
    global yaw2_vetor

    if scf.cf.link_uri == 'radio://0/80/2M/E7E7E7E7E0':
        total_duration = 12.8
        zi = 0.5
        yi = 0.3
        xi = 0.58

    if scf.cf.link_uri == 'radio://0/80/2M/E7E7E7E7E1':
        total_duration = 12.7
        zi = 0.5
        yi = 0.5
        xi = 0.21

    trajectory_id = 1
    commander = scf.cf.high_level_commander

    commander.takeoff(zi, 2.0)
    time.sleep(2.0)

    commander.go_to(xi,yi,zi,0.0,2.0, relative = False)
    time.sleep(2.0)

    leitura = 1
    relative = True
    commander.start_trajectory(trajectory_id, 1.0, relative)
    time.sleep(total_duration)
    
    leitura = 0
    commander.land(0.0, 2.0)
    time.sleep(8.0)
    commander.stop()


    x1_vetor = str(x1_vetor)
    y1_vetor = str(y1_vetor)
    z1_vetor = str(z1_vetor)
    x2_vetor = str(x2_vetor)
    y2_vetor = str(y2_vetor)
    z2_vetor = str(z2_vetor)
    roll1_vetor = str(roll1_vetor)
    pitch1_vetor = str(pitch1_vetor)
    yaw1_vetor = str(yaw1_vetor)
    roll2_vetor = str(roll2_vetor)
    pitch2_vetor = str(pitch2_vetor)
    yaw2_vetor = str(yaw2_vetor)

    arquivo1 = open('Eixo_X1.txt', 'w')
    arquivo1.write(x1_vetor)
    arquivo1.close()

    arquivo2 = open('Eixo_Y1.txt', 'w')
    arquivo2.write(y1_vetor)
    arquivo2.close()

    arquivo3 = open('Eixo_Z1.txt', 'w')
    arquivo3.write(z1_vetor)
    arquivo3.close()

    arquivo4 = open('Eixo_Roll1.txt', 'w')
    arquivo4.write(roll1_vetor)
    arquivo4.close()

    arquivo5 = open('Eixo_Pitch1.txt', 'w')
    arquivo5.write(pitch1_vetor)
    arquivo5.close()

    arquivo6 = open('Eixo_Yaw1.txt', 'w')
    arquivo6.write(yaw1_vetor)
    arquivo6.close()

    arquivo7 = open('Eixo_X2.txt', 'w')
    arquivo7.write(x2_vetor)
    arquivo7.close()

    arquivo8 = open('Eixo_Y2.txt', 'w')
    arquivo8.write(y2_vetor)
    arquivo8.close()

    arquivo9 = open('Eixo_Z2.txt', 'w')
    arquivo9.write(z2_vetor)
    arquivo9.close()

    arquivo10 = open('Eixo_Roll2.txt', 'w')
    arquivo10.write(roll1_vetor)
    arquivo10.close()

    arquivo11 = open('Eixo_Pitch2.txt', 'w')
    arquivo11.write(pitch1_vetor)
    arquivo11.close()

    arquivo12 = open('Eixo_Yaw2.txt', 'w')
    arquivo12.write(yaw1_vetor)
    arquivo12.close()

def sensores_angulos1(scf):

    if scf.cf.link_uri == 'radio://0/80/2M/E7E7E7E7E0':

    # The definition of the logconfig can be made before connecting
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')

        scf.cf.log.add_config(lg_stab)
    # This callback will receive the data
        lg_stab.data_received_cb.add_callback(start_angles_printing1)
    # Start the logging
        lg_stab.start()

    if scf.cf.link_uri == 'radio://0/80/2M/E7E7E7E7E1':

    # The definition of the logconfig can be made before connecting
        lg_stab = LogConfig(name='Stabilizer', period_in_ms=100)
        lg_stab.add_variable('stabilizer.roll', 'float')
        lg_stab.add_variable('stabilizer.pitch', 'float')
        lg_stab.add_variable('stabilizer.yaw', 'float')

        scf.cf.log.add_config(lg_stab)
    # This callback will receive the data
        lg_stab.data_received_cb.add_callback(start_angles_printing2)
    # Start the logging
        lg_stab.start()


# Estimação Posição Angular
def start_angles_printing1(timestamp, data, logconf):

    global roll1_vetor
    global pitch1_vetor
    global yaw1_vetor
    global leitura
    
    """Callback froma the log API when data arrives"""
    roll = data['stabilizer.roll']
    pitch = data['stabilizer.pitch']
    yaw = data['stabilizer.yaw']

    if leitura == 1:
        
        roll1_vetor.append(roll)
        pitch1_vetor.append(pitch)
        yaw1_vetor.append(yaw)

# Estimação Posição Angular
def start_angles_printing2(timestamp, data, logconf):

    global roll2_vetor
    global pitch2_vetor
    global yaw2_vetor
    global leitura
    
    """Callback froma the log API when data arrives"""
    roll = data['stabilizer.roll']
    pitch = data['stabilizer.pitch']
    yaw = data['stabilizer.yaw']

    if leitura == 1:
        
        roll2_vetor.append(roll)
        pitch2_vetor.append(pitch)
        yaw2_vetor.append(yaw)




def position_callback1(timestamp, data, logconf):

    global x1_vetor
    global y1_vetor
    global z1_vetor
    global leitura

    x1 = data['kalman.stateX']
    y1 = data['kalman.stateY']
    z1 = data['kalman.stateZ']

    if leitura == 1:
        x1_vetor.append(x1)
        y1_vetor.append(y1)
        z1_vetor.append(z1)  

def position_callback2(timestamp, data, logconf):

    global x2_vetor
    global y2_vetor
    global z2_vetor
    global leitura
    
    x2 = data['kalman.stateX']
    y2 = data['kalman.stateY']
    z2 = data['kalman.stateZ']

    if leitura == 1:
        x2_vetor.append(x2)
        y2_vetor.append(y2)
        z2_vetor.append(z2)  
 
     
def start_position_printing(scf):
   
    if scf.cf.link_uri == 'radio://0/80/2M/E7E7E7E7E0':
       
        log_conf = LogConfig(name='Position', period_in_ms=100)
        log_conf.add_variable('kalman.stateX', 'float')
        log_conf.add_variable('kalman.stateY', 'float')
        log_conf.add_variable('kalman.stateZ', 'float')

        scf.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(position_callback1)
        log_conf.start()

    if scf.cf.link_uri == 'radio://0/80/2M/E7E7E7E7E1':
         
        log_conf = LogConfig(name='Position', period_in_ms=100)
        log_conf.add_variable('kalman.stateX', 'float')
        log_conf.add_variable('kalman.stateY', 'float')
        log_conf.add_variable('kalman.stateZ', 'float')

        scf.cf.log.add_config(log_conf)
        log_conf.data_received_cb.add_callback(position_callback2)
        log_conf.start()

if __name__ == '__main__':
    cflib.crtp.init_drivers(enable_debug_driver=False)
    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:

        swarm.parallel_safe(activate_high_level_commander)
        swarm.parallel_safe(activate_controller)
        swarm.parallel_safe(reset_estimator)
        swarm.parallel_safe(start_position_printing)
        swarm.parallel_safe(sensores_angulos1)
        swarm.parallel_safe(run_sequence, args_dict=seq_args)


