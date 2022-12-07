#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2019 Bitcraze AB
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
Simple example of a synchronized swarm choreography using the High level
commander.

The swarm takes off and flies a synchronous choreography before landing.
The take-of is relative to the start position but the Goto are absolute.
The sequence contains a list of commands to be executed at each step.

This example is intended to work with any absolute positioning system.
It aims at documenting how to use the High Level Commander together with
the Swarm class to achieve synchronous sequences.
"""
import threading
import time
from collections import namedtuple
from queue import Queue

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
"""
The layout of the positions:
    x2      x1      x0

y3  9              3

            ^ Y
            |
y2  8       5       2
            |
[my desk]   +------> X

y1  7       4       1



y0  6               0
"""

z0 = 1
z = 2

x0 = 1.28
x1 = 0.35
x2 = -0.64

y0 = -1.45
y1 = -0.5
y2 = 0.47
y3 = 1.55

# Time for one step in second
STEP_TIME = 1

# Possible commands, all times are in seconds
Takeoff = namedtuple('Takeoff', ['height', 'time'])
Land = namedtuple('Land', ['time'])
Goto = namedtuple('Goto', ['x', 'y', 'z', 'time'])
# RGB [0-255], Intensity [0.0-1.0]
Ring = namedtuple('Ring', ['r', 'g', 'b', 'intensity', 'time'])
# Reserved for the control loop, do not use in sequence
Quit = namedtuple('Quit', [])

uris = 0
sequence = 0

if True: #swith one or all
    uris = [
    'radio://0/80/2M/E7E7E7E710', #0
    ]

    sequence = [
        # Step, CF_id,  action
        (0,    0,      Takeoff(0.5, 2)),
        (2,    0,      Goto(x1, y1, 1, 4)),
        (6,    0,      Goto(x0, y0, 2, 6)),
        (12,   0,      Goto(x2, y0, 0.5, 4)),
        (16,   0,      Goto(x2, y3, 4, 6)),
        (22,   0,      Goto(x0, y3, 2, 2)),
        (24,   0,      Goto(x0, y3, 2, 2)),
        (26,   0,      Goto(x1, y1, 0.4, 4)),
        (30,   0,      Goto(x1, y1, 0.4, 4)),
        (34,   0,      Land(2)),
    ]
else:
    uris = [#maximum of 3 per CrazyRadio -> you need at least 4 CrazyRadios on different channels
    'radio://0/80/2M/E7E7E7E710', #0
    'radio://0/80/2M/E7E7E7E711', #1
    'radio://0/80/2M/E7E7E7E712', #2
    'radio://0/80/2M/E7E7E7E713', #3
    'radio://0/80/2M/E7E7E7E714', #4
    'radio://0/80/2M/E7E7E7E715', #5
    'radio://0/80/2M/E7E7E7E716', #6
    'radio://0/80/2M/E7E7E7E717', #7
    'radio://0/80/2M/E7E7E7E718', #8
    'radio://0/80/2M/E7E7E7E719', #9
    ]
    slowerFactor = 2
    baseHeight = 0.5
    sequence = [
        # Step, CF_id,  action
        #Takeoff
        (0,    0,      Takeoff(1, 2*slowerFactor)),
        (0,    1,      Takeoff(1, 2*slowerFactor)),
        (0,    2,      Takeoff(1, 2*slowerFactor)),
        (0,    3,      Takeoff(1, 2*slowerFactor)),
        (0,    4,      Takeoff(1, 2*slowerFactor)),
        (0,    5,      Takeoff(1, 2*slowerFactor)),
        (0,    6,      Takeoff(1, 2*slowerFactor)),
        (0,    7,      Takeoff(1, 2*slowerFactor)),
        (0,    8,      Takeoff(1, 2*slowerFactor)),
        (0,    9,      Takeoff(1, 2*slowerFactor)),
        #Square Step1 hold Position
        (2*slowerFactor,    0,      Goto(x0, y0, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    1,      Goto(x0, y1, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    2,      Goto(x0, y2, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    3,      Goto(x0, y3, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    4,      Goto(x1, y1, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    5,      Goto(x1, y2, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    6,      Goto(x2, y0, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    7,      Goto(x2, y1, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    8,      Goto(x2, y2, 1+baseHeight, 2*slowerFactor)),
        (2*slowerFactor,    9,      Goto(x2, y3, 1+baseHeight, 2*slowerFactor)),
        #Square Step2 move right and up
        (4*slowerFactor,    0,      Goto(x0, y0-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    1,      Goto(x0, y1-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    2,      Goto(x0, y2-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    3,      Goto(x0, y3-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    4,      Goto(x1, y1-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    5,      Goto(x1, y2-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    6,      Goto(x2, y0-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    7,      Goto(x2, y1-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    8,      Goto(x2, y2-1, 2+baseHeight, 2*slowerFactor)),
        (4*slowerFactor,    9,      Goto(x2, y3-1, 2+baseHeight, 2*slowerFactor)),
        #Square Step 3 move back
        (6*slowerFactor,    0,      Goto(x0-1, y0-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    1,      Goto(x0-1, y1-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    2,      Goto(x0-1, y2-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    3,      Goto(x0-1, y3-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    4,      Goto(x1-1, y1-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    5,      Goto(x1-1, y2-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    6,      Goto(x2-1, y0-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    7,      Goto(x2-1, y1-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    8,      Goto(x2-1, y2-1, 2+baseHeight, 2*slowerFactor)),
        (6*slowerFactor,    9,      Goto(x2-1, y3-1, 2+baseHeight, 2*slowerFactor)),
        #Square Step 3 move left and down slowly
        (8*slowerFactor,    0,      Goto(x0-1, y0, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    1,      Goto(x0-1, y1, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    2,      Goto(x0-1, y2, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    3,      Goto(x0-1, y3, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    4,      Goto(x1-1, y1, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    5,      Goto(x1-1, y2, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    6,      Goto(x2-1, y0, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    7,      Goto(x2-1, y1, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    8,      Goto(x2-1, y2, .5+baseHeight, 4*slowerFactor)),
        (8*slowerFactor,    9,      Goto(x2-1, y3, .5+baseHeight, 4*slowerFactor)),
        #Square Step 4 move forward and up
        (12*slowerFactor,    0,      Goto(x0, y0, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    1,      Goto(x0, y1, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    2,      Goto(x0, y2, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    3,      Goto(x0, y3, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    4,      Goto(x1, y1, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    5,      Goto(x1, y2, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    6,      Goto(x2, y0, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    7,      Goto(x2, y1, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    8,      Goto(x2, y2, 1+baseHeight, 2*slowerFactor)),
        (12*slowerFactor,    9,      Goto(x2, y3, 1+baseHeight, 2*slowerFactor)),
        #Pyramid Step 1 hold position
        (14*slowerFactor,    0,      Goto(x0, y0, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    1,      Goto(x0, y1, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    2,      Goto(x0, y2, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    3,      Goto(x0, y3, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    4,      Goto(x1, y1, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    5,      Goto(x1, y2, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    6,      Goto(x2, y0, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    7,      Goto(x2, y1, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    8,      Goto(x2, y2, 1+baseHeight, 2*slowerFactor)),
        (14*slowerFactor,    9,      Goto(x2, y3, 1+baseHeight, 2*slowerFactor)),
        #Pyramid Step 2 move to position
        (16*slowerFactor,    0,      Goto(x0+1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    1,      Goto(x0, y1, 1.5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    2,      Goto(x0, y2, 1.5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    3,      Goto(x0+1, y3+1, .5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    4,      Goto(x1, y1, 2.5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    5,      Goto(x1, y2, 2.5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    6,      Goto(x2-1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    7,      Goto(x2, y1, 1.5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    8,      Goto(x2, y2, 1.5+baseHeight, 3*slowerFactor)),
        (16*slowerFactor,    9,      Goto(x2-1, y3+1, .5+baseHeight, 3*slowerFactor)),
        #Pyramid Step 3 move in cw and ccw square 1
        (19*slowerFactor,    6,      Goto(x0+1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    2,      Goto(x0, y1, 1.5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    8,      Goto(x0, y2, 1.5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    0,      Goto(x0+1, y3+1, .5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    4,      Goto(x1+1, y1, 2.5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    5,      Goto(x1, y2-1, 2.5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    9,      Goto(x2-1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    1,      Goto(x2, y1, 1.5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    7,      Goto(x2, y2, 1.5+baseHeight, 3*slowerFactor)),
        (19*slowerFactor,    3,      Goto(x2-1, y3+1, .5+baseHeight, 3*slowerFactor)),
        #Pyramid Step 4 move in cw and ccw square 2
        (22*slowerFactor,    9,      Goto(x0+1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    8,      Goto(x0, y1, 1.5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    7,      Goto(x0, y2, 1.5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    6,      Goto(x0+1, y3+1, .5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    4,      Goto(x1+1, y1+1, 2.5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    5,      Goto(x1+1, y2-1, 2.5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    3,      Goto(x2-1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    2,      Goto(x2, y1, 1.5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    1,      Goto(x2, y2, 1.5+baseHeight, 3*slowerFactor)),
        (22*slowerFactor,    0,      Goto(x2-1, y3+1, .5+baseHeight, 3*slowerFactor)),
        #Pyramid Step 5 move in cw and ccw square 3
        (25*slowerFactor,    3,      Goto(x0+1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    7,      Goto(x0, y1, 1.5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    1,      Goto(x0, y2, 1.5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    9,      Goto(x0+1, y3+1, .5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    4,      Goto(x1, y1+1, 2.5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    5,      Goto(x1+1, y2, 2.5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    0,      Goto(x2-1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    8,      Goto(x2, y1, 1.5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    2,      Goto(x2, y2, 1.5+baseHeight, 3*slowerFactor)),
        (25*slowerFactor,    6,      Goto(x2-1, y3+1, .5+baseHeight, 3*slowerFactor)),
        #Pyramid Step 6 move back to original position
        (28*slowerFactor,    0,      Goto(x0+1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    1,      Goto(x0, y1, 1.5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    2,      Goto(x0, y2, 1.5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    3,      Goto(x0+1, y3+1, .5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    4,      Goto(x1, y1, 2.5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    5,      Goto(x1, y2, 2.5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    6,      Goto(x2-1, y0-1, .5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    7,      Goto(x2, y1, 1.5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    8,      Goto(x2, y2, 1.5+baseHeight, 3*slowerFactor)),
        (28*slowerFactor,    9,      Goto(x2-1, y3+1, .5+baseHeight, 3*slowerFactor)),
        #Pyramid Step 7 stay in pyramid position 
        (31*slowerFactor,    0,      Goto(x0+1, y0-1, .5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    1,      Goto(x0, y1, 1.5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    2,      Goto(x0, y2, 1.5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    3,      Goto(x0+1, y3+1, .5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    4,      Goto(x1, y1, 2.5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    5,      Goto(x1, y2, 2.5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    6,      Goto(x2-1, y0-1, .5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    7,      Goto(x2, y1, 1.5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    8,      Goto(x2, y2, 1.5+baseHeight, 1*slowerFactor)),
        (31*slowerFactor,    9,      Goto(x2-1, y3+1, .5+baseHeight, 1*slowerFactor)),
        #Landing Step 1 move in normal formation
        (32*slowerFactor,    0,      Goto(x0, y0, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    1,      Goto(x0, y1, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    2,      Goto(x0, y2, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    3,      Goto(x0, y3, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    4,      Goto(x1, y1, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    5,      Goto(x1, y2, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    6,      Goto(x2, y0, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    7,      Goto(x2, y1, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    8,      Goto(x2, y2, 1.5, 2*slowerFactor)),
        (32*slowerFactor,    9,      Goto(x2, y3, 1.5, 2*slowerFactor)),
        #Landing Step 1 move in normal formation
        (34*slowerFactor,    0,      Goto(x0, y0, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    1,      Goto(x0, y1, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    2,      Goto(x0, y2, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    3,      Goto(x0, y3, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    4,      Goto(x1, y1, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    5,      Goto(x1, y2, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    6,      Goto(x2, y0, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    7,      Goto(x2, y1, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    8,      Goto(x2, y2, 0.5, 2*slowerFactor)),
        (34*slowerFactor,    9,      Goto(x2, y3, 0.5, 2*slowerFactor)),
        #Landing Step 3 final Land
        (36*slowerFactor,    0,      Land(2)),
        (36*slowerFactor,    1,      Land(2)),
        (36*slowerFactor,    2,      Land(2)),
        (36*slowerFactor,    3,      Land(2)),
        (36*slowerFactor,    4,      Land(2)),
        (36*slowerFactor,    5,      Land(2)),
        (36*slowerFactor,    6,      Land(2)),
        (36*slowerFactor,    7,      Land(2)),
        (36*slowerFactor,    8,      Land(2)),
        (36*slowerFactor,    9,      Land(2)),
    ]


def activate_high_level_commander(scf):
    scf.cf.param.set_value('commander.enHighLevel', '1')


def activate_mellinger_controller(scf, use_mellinger):
    controller = 1
    if use_mellinger:
        controller = 2
    scf.cf.param.set_value('stabilizer.controller', str(controller))


def set_ring_color(cf, r, g, b, intensity, time):
    cf.param.set_value('ring.fadeTime', str(time))

    r *= intensity
    g *= intensity
    b *= intensity

    color = (int(r) << 16) | (int(g) << 8) | int(b)

    cf.param.set_value('ring.fadeColor', str(color))


def crazyflie_control(scf):
    cf = scf.cf
    control = controlQueues[uris.index(cf.link_uri)]

    activate_mellinger_controller(scf, False)

    commander = scf.cf.high_level_commander

    # Set fade to color effect and reset to Led-ring OFF
    set_ring_color(cf, 0, 0, 0, 0, 0)
    cf.param.set_value('ring.effect', '14')

    while True:
        command = control.get()
        if type(command) is Quit:
            return
        elif type(command) is Takeoff:
            commander.takeoff(command.height, command.time)
        elif type(command) is Land:
            commander.land(0.0, command.time)
        elif type(command) is Goto:
            commander.go_to(command.x, command.y, command.z, 0, command.time)
        elif type(command) is Ring:
            set_ring_color(cf, command.r, command.g, command.b,
                           command.intensity, command.time)
            pass
        else:
            print('Warning! unknown command {} for uri {}'.format(command, cf.uri))


def control_thread():
    pointer = 0
    step = 0
    stop = False

    while not stop:
        print('Step {}:'.format(step))
        while sequence[pointer][0] <= step:
            cf_id = sequence[pointer][1]
            command = sequence[pointer][2]

            print(' - Running: {} on {}'.format(command, cf_id))
            controlQueues[cf_id].put(command)
            pointer += 1

            if pointer >= len(sequence):
                print('Reaching the end of the sequence, stopping!')
                stop = True
                break

        step += 1
        time.sleep(STEP_TIME)

    for ctrl in controlQueues:
        ctrl.put(Quit())


if __name__ == '__main__':
    controlQueues = [Queue() for _ in range(len(uris))]

    cflib.crtp.init_drivers()
    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel_safe(activate_high_level_commander)
        swarm.reset_estimators()

        print('Starting sequence!')

        threading.Thread(target=control_thread).start()

        swarm.parallel_safe(crazyflie_control)

        time.sleep(1)
