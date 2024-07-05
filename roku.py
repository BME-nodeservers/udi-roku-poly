#!/usr/bin/env python3
"""
Polyglot v3 node server experimental Roku Media Player control.
Copyright (C) 2019,2021 Robert Paauwe
"""
import udi_interface
import sys
from nodes import roku

LOGGER = udi_interface.LOGGER

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start('2.0.6')
        roku.Controller(polyglot)
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
        

