# 20220614
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
"""
Version of the AutonomousSequence.py example connecting to 10 Crazyflies.
The Crazyflies go straight up, hover a while and land but the code is fairly
generic and each Crazyflie has its own sequence of setpoints that it files
to.

The layout of the positions:
    x2      x1      x0

y3  10              4

            ^ Y
            |
y2  9       6       3
            |
[ich]       +------> X

y1  8       5       2



y0  7               1

"""
import time

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm

# Change uris and sequences according to your setup
URI1 = 'radio://0/80/2M/E7E7E7E701'
URI2 = 'radio://0/80/2M/E7E7E7E703'
URI3 = 'radio://0/80/2M/E7E7E7E704'
URI4 = 'radio://0/80/2M/E7E7E7E705'
URI5 = 'radio://0/80/2M/E7E7E7E706'
URI6 = 'radio://0/80/2M/E7E7E7E708'
URI7 = 'radio://0/80/2M/E7E7E7E709'
URI8 = 'radio://0/80/2M/E7E7E7E70A'
URI9 = 'radio://0/80/2M/E7E7E7E70B'
URI10 = 'radio://0/80/2M/E7E7E7E70C'


z0 = 1
z = 2

x0 = 3.5
x1 = 2.5
x2 = 1.5

y0 = 1.5
y1 = 2.5
y2 = 3.5
y3 = 4.5

takeoffIncrementTime = 0.5
quickIncrementTime = 1.0
middleIncrementTime = 3.0
longIncrementTime = 5.0

#    x   y   z  time
sequence1 = [
    #Takeoff
    (x0, y0, z0/2, takeoffIncrementTime),
    (x0, y0, z0, takeoffIncrementTime),
    (x0, y0, z, middleIncrementTime),
    #Sqaure
    (x0, y0-1, z, middleIncrementTime),
    (x0-1, y0-1, z, middleIncrementTime),
    (x0-1, y0, z, middleIncrementTime),
    (x0, y0, z, longIncrementTime),
    #Pyramid
    (x0+.5, y0-.5, z-.5, quickIncrementTime),
    (x0+1, y0-1, z-1, longIncrementTime),  
    #Normal
    (x0, y0, z, middleIncrementTime),
    #Landing
    (x0, y0, z0, middleIncrementTime),
    (x0, y0, z0/2, quickIncrementTime),
]

sequence2 = [
    #Takeoff
    (x0, y1, z0/2, takeoffIncrementTime),
    (x0, y1, z0, takeoffIncrementTime),
    (x0, y1, z, middleIncrementTime),
    #Sqaure
    (x0, y1-1, z, middleIncrementTime),
    (x0-1, y1-1, z, middleIncrementTime),
    (x0-1, y1, z, middleIncrementTime),
    (x0, y1, z, longIncrementTime),
    #Pyramid
    (x0, y1, z, quickIncrementTime),
    (x0, y1, z, longIncrementTime),
    #Normal
    (x0, y1, z, middleIncrementTime),
    #Landing
    (x0, y1, z0, middleIncrementTime),
    (x0, y1, z0/2, quickIncrementTime),
]

sequence3 = [
    #Takeoff
    (x0, y2, z0/2, takeoffIncrementTime),
    (x0, y2, z0, takeoffIncrementTime),
    (x0, y2, z, middleIncrementTime),
    #Sqaure
    (x0, y2-1, z, middleIncrementTime),
    (x0-1, y2-1, z, middleIncrementTime),
    (x0-1, y2, z, middleIncrementTime),
    (x0, y2, z, longIncrementTime),
    #Pyramid
    (x0, y2, z, quickIncrementTime),
    (x0, y2, z, longIncrementTime),
    #Normal
    (x0, y2, z, middleIncrementTime),
    #Landing
    (x0, y2, z0, middleIncrementTime),
    (x0, y2, z0/2, quickIncrementTime),
]

sequence4 = [
    #Takeoff
    (x0, y3, z0/2, takeoffIncrementTime),
    (x0, y3, z0, takeoffIncrementTime),
    (x0, y3, z, middleIncrementTime),
    #Sqaure
    (x0, y3-1, z, middleIncrementTime),
    (x0-1, y3-1, z, middleIncrementTime),
    (x0-1, y3, z, middleIncrementTime),
    (x0, y3, z, longIncrementTime),
    #Pyramid
    (x0+.5, y3+.5, z-.5, quickIncrementTime),
    (x0+1, y3+1, z-1, longIncrementTime),
    #Normal
    (x0, y3, z, middleIncrementTime),
    #Landing
    (x0, y3, z0, middleIncrementTime),
    (x0, y3, z0/2, quickIncrementTime),
]

sequence5 = [
    #Takeoff
    (x1, y1, z0/2, takeoffIncrementTime),
    (x1, y1, z0, takeoffIncrementTime),
    (x1, y1, z, middleIncrementTime),
    #Sqaure
    (x1, y1-1, z, middleIncrementTime),
    (x1-1, y1-1, z, middleIncrementTime),
    (x1-1, y1, z, middleIncrementTime),
    (x1, y1, z, longIncrementTime),
    #Pyramid
    (x1, y1, z+.5, quickIncrementTime),
    (x1, y1, z+1, longIncrementTime),
    #Normal
    (x1, y1, z, middleIncrementTime),
    #Landing
    (x1, y1, z0, middleIncrementTime),
    (x1, y1, z0/2, quickIncrementTime),
]

sequence6 = [
    #Takeoff
    (x1, y2, z0/2, takeoffIncrementTime),
    (x1, y2, z0, takeoffIncrementTime),
    (x1, y2, z, middleIncrementTime),
    #Sqaure
    (x1, y2-1, z, middleIncrementTime),
    (x1-1, y2-1, z, middleIncrementTime),
    (x1-1, y2, z, middleIncrementTime),
    (x1, y2, z, longIncrementTime),
    #Pyramid
    (x1, y2, z+.5, quickIncrementTime),
    (x1, y2, z+1, longIncrementTime),
    #Normal
    (x1, y2, z, middleIncrementTime),
    #Landing
    (x1, y2, z0, middleIncrementTime),
    (x1, y2, z0/2, quickIncrementTime),
]

sequence7 = [
    #Takeoff
    (x2, y0, z0/2, takeoffIncrementTime),
    (x2, y0, z0, takeoffIncrementTime),
    (x2, y0, z, middleIncrementTime),
    #Sqaure
    (x2, y0-1, z, middleIncrementTime),
    (x2-1, y0-1, z, middleIncrementTime),
    (x2-1, y0, z, middleIncrementTime),
    (x2, y0, z, longIncrementTime),
    #Pyramid
    (x2-.5, y0-.5, z-.5, quickIncrementTime),
    (x2-1, y0-1, z-1, longIncrementTime),
    #Normal
    (x2, y0, z, middleIncrementTime),
    #Landing
    (x2, y0, z0, middleIncrementTime),
    (x2, y0, z0/2, quickIncrementTime),
]

sequence8 = [
    #Takeoff
    (x2, y1, z0/2, takeoffIncrementTime),
    (x2, y1, z0, takeoffIncrementTime),
    (x2, y1, z, middleIncrementTime),
    #Sqaure
    (x2, y1-1, z, middleIncrementTime),
    (x2-1, y1-1, z, middleIncrementTime),
    (x2-1, y1, z, middleIncrementTime),
    (x2, y1, z, longIncrementTime),
    #Pyramid
    (x2, y1, z, quickIncrementTime),
    (x2, y1, z, longIncrementTime),
    #Normal
    (x2, y1, z, middleIncrementTime),
    #Landing
    (x2, y1, z0, middleIncrementTime),
    (x2, y1, z0/2, quickIncrementTime),
]

sequence9 = [
    #Takeoff
    (x2, y2, z0/2, takeoffIncrementTime),
    (x2, y2, z0, takeoffIncrementTime),
    (x2, y2, z, middleIncrementTime),
    #Sqaure
    (x2, y2-1, z, middleIncrementTime),
    (x2-1, y2-1, z, middleIncrementTime),
    (x2-1, y2, z, middleIncrementTime),
    (x2, y2, z, longIncrementTime),
    #Pyramid
    (x2, y2, z, quickIncrementTime),
    (x2, y2, z, longIncrementTime),
    #Normal
    (x2, y2, z, middleIncrementTime),
    #Landing
    (x2, y2, z0, middleIncrementTime),
    (x2, y2, z0/2, quickIncrementTime),
]

sequence10 = [
    #Takeoff
    (x2, y3, z0/2, takeoffIncrementTime),
    (x2, y3, z0, takeoffIncrementTime),
    (x2, y3, z, middleIncrementTime),
    #Sqaure
    (x2, y3-1, z, middleIncrementTime),
    (x2-1, y3-1, z, middleIncrementTime),
    (x2-1, y3, z, middleIncrementTime),
    (x2, y3, z, longIncrementTime),
    #Pyramid
    (x2-.5, y3+.5, z-.5, quickIncrementTime),
    (x2-1, y3+1, z-1, longIncrementTime),
    #Normal
    (x2, y3, z, middleIncrementTime),
    #Landing
    (x2, y3, z0, middleIncrementTime),
    (x2, y3, z0/2, quickIncrementTime),
]

seq_args = {
    URI1: [sequence1],
    URI2: [sequence2],
    URI3: [sequence3],
    URI4: [sequence4],
    URI5: [sequence5],
    URI6: [sequence6],
    URI7: [sequence7],
    URI8: [sequence8],
    URI9: [sequence9],
    URI10: [sequence10],
}

# List of URIs, comment the one you do not want to fly
uris = {
    URI1,
    URI2,
    URI3,
    URI4,
    URI5,
    URI6,
    URI7,
    URI8,
    URI9,
    URI10
}#


def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)


def take_off(cf, position):
    take_off_time = 1.0
    sleep_time = 0.1
    steps = int(take_off_time / sleep_time)
    vz = position[2] / take_off_time

    print(vz)

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)


def land(cf, position):
    landing_time = 1.0
    sleep_time = 0.1
    steps = int(landing_time / sleep_time)
    vz = -position[2] / landing_time

    print(vz)

    for _ in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)

    cf.commander.send_stop_setpoint()
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def run_sequence(scf, sequence):
    try:
        cf = scf.cf

        take_off(cf, sequence[0])
        for position in sequence:
            print('Setting position of Crazyflie {}'.format(cf.link_uri) + ' to {}'.format(position))
            end_time = time.time() + position[3]
            while time.time() < end_time:
                cf.commander.send_position_setpoint(position[0],
                                                    position[1],
                                                    position[2], 0)
                time.sleep(0.1)
        land(cf, sequence[-1])
    except Exception as e:
        print(e)


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

        swarm.parallel(run_sequence, args_dict=seq_args)
