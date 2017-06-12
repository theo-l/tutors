#!/usr/bin/env python
# encoding:utf-8

#from fabric.api import (cd, run, task, env, hosts, roles)
from fabric.api import *
from fabtools import require
import fabtools

from host_confg import *

env.hosts = ALL_HOSTS
env.passwords = HOST_PASSWORDS
test_hosts = NAME_HOST_STRING_MAP['test']
prod_hosts = NAME_HOST_STRING_MAP['prod']
env.roledefs.update(ROLE_HOST_STRING_MAP)

deb_packages = [
       'nginx',
       'redis-server',
        ]

@task
@hosts(ALL_HOSTS)
def setup():

    # system package requires
    require.deb.packages(deb_packages)


    # python requirements
    with require.python.virtualenv('/home/vagrant/env'):
        require.page.package('Django')


@task
@hosts(ALL_HOSTS)
def reset():

    # remove deb packages
    require.deb.nopackages(deb_packages)
