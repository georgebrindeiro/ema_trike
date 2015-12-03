#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import sys

def signal_handler(signal, frame):
        global stim_manager
        stim_manager.ccl_stop()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

import ema.modules.stimulator as stimulator

def run():
    global stim_manager

    config_dict = {
        'port': '/dev/ttyUSB0',
        'channel_stim': [1, 2],
        'channel_lf': [],
        'n_factor': 0,
        'freq': 50,
        'ts1': 20,
        'ts2': 3
    }

    config_dict1 = {
        'port': '/dev/ttyUSB0',
        'channel_stim': [1, 2, 5],
        'channel_lf': [5],
        'n_factor': 1,
        'ts1': 50,
        'ts2': 5
    }

    config_dict2 = {
        'port': '/dev/ttyUSB0',
        'channel_stim': [2, 3, 6, 8],
        'channel_lf': [2, 3],
        'n_factor': 2,
        'ts1': 16.5,
        'ts2': 6
    }

    stim_manager = stimulator.Stimulator(config_dict)

    #stim_manager.single_pulse(channel_number = 3, pulse_width = 200, pulse_current = 120)
    #stim_manager.single_pulse(channel_number = 2, pulse_width = 221, pulse_current = 55)
    stim_manager.ccl_initialize()
    # stim_manager.ccl_update(mode = {2: 'single', 3: 'triplet', 6: 'doublet', 8: 'doublet'},
    #                         pulse_width = {2: 100, 3: 200, 6: 300, 8: 400},
    #                         pulse_current = {2: 52, 3: 55, 6: 72, 8: 92})
    # stim_manager.ccl_update(mode = {2: 'single', 3: 'triplet', 6: 'doublet', 8: 'doublet'},
    #                         pulse_width = {2: 100, 3: 200, 6: 300, 8: 400},
    #                         pulse_current = {2: 52, 3: 55, 6: 72, 8: 92})
    stim_manager.ccl_update(mode = {1: 'single', 2: 'single'},
                            pulse_width = {1: 500, 2: 500},
                            pulse_current = {1: 6, 2: 6})

    key = ''
    while key != 'q':
        key = raw_input("Press q to quit")
