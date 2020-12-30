#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .config import Configuration
except (ValueError, ImportError) as e:
    raise Exception('You may need to run w1fit3kAl1 from the root directory (which includes README.md)', e)

from .util.color import Color

import os
import sys


class Wifite(object):

    def __init__(self):
        '''
        Initializes Wifite. Checks for root permissions and ensures dependencies are installed.
        '''

        self.print_banner()

        Configuration.initialize(load_interface=False)

        if os.getuid() != 0:
            Color.pl('{!} {R}error: {O}w1fit3kAl1{R} must be run as {O}root{W}')
            Color.pl('{!} {R}re-run with {O}sudo{W}')
            Configuration.exit_gracefully(0)

        from .tools.dependency import Dependency
        Dependency.run_dependency_check()


    def start(self):
        '''
        Starts target-scan + attack loop, or launches utilities dpeending on user input.
        '''
        from .model.result import CrackResult
        from .model.handshake import Handshake
        from .util.crack import CrackHelper

        if Configuration.show_cracked:
            CrackResult.display()

        elif Configuration.check_handshake:
            Handshake.check()

        elif Configuration.crack_handshake:
            CrackHelper.run()

        else:
            Configuration.get_monitor_mode_interface()
            self.scan_and_attack()

            
    def print_banner(self):
        Color.pl(r' {W}{G}{W}')
    
        '''Displays ASCII art of the highest caliber.'''
        Color.pl(r' {G}w1fit3kAl1 {D}%s{W}' % Configuration.version)
        Color.pl(r' {W}{D}automated WIFI program for penetration and testing f0r Kali-Linux-2020.x{W}')
        Color.pl(r' {C}{D}https://github.com/nu11secur1ty/w1f1t3kAl1{W}')
        Color.pl('')
        
        Color.pl(r' {W}{G}---------------------------------------------------------{W}')
        Color.pl(r' {W}{G}         88       88       eeee                     88   {W}')
        Color.pl(r' {W}{G}e   e  e  8   eeee 8 eeeee    8  e   e  eeeee e      8   {W}')
        Color.pl(r' {W}{G}8   8  8  8   8    8   8      8  8   8  8   8 8      8   {W}')
        Color.pl(r' {W}{G}8e  8  8  8   8eee 8   8e  eee8  8eee8e 8eee8 8e     8   {W}')
        Color.pl(r' {W}{G}88  8  8 8888 88  8888 88    88  88   8 88  8 88    8888 {W}')
        Color.pl(r' {W}{G}88ee8ee8 8888 88  8888 88 eee88  88   8 88  8 88eee 8888 {W}')
        Color.pl('')
        
    def scan_and_attack(self):
        '''
        1) Scans for targets, asks user to select targets
        2) Attacks each target
        '''
        from .util.scanner import Scanner
        from .attack.all import AttackAll

        Color.pl('')

        # Scan
        s = Scanner()
        targets = s.select_targets()

        # Attack
        attacked_targets = AttackAll.attack_multiple(targets)

        Color.pl('{+} Finished attacking {C}%d{W} target(s), exiting' % attacked_targets)


##############################################################


def entry_point():
    try:
        w1fit3kAl1 = Wifite()
        w1fit3kAl1.start()
    except Exception as e:
        Color.pexception(e)
        Color.pl('\n{!} {R}Exiting{W}\n')

    except KeyboardInterrupt:
        Color.pl('\n{!} {O}Interrupted, Shutting down...{W}')

    Configuration.exit_gracefully(0)


if __name__ == '__main__':
    entry_point()
