#!/usr/bin/env python
# encoding:utf-8

from fabric.api import run

def update_system():
    run('sudo apt-get update; sudo apt-get upgrade')

class OSUtil:

    def __init__(self, requirements):
        self.requirements = requirements

    def install_os_requirement(self):
        for requirement in self.requirements:
            run('sudo apt-get install {}'.format(requirement))
    
    def remove_os_requirement(self):
        for requirement in self.requirements:
            run('sudo apt-get remove {}'.format(requirement))
