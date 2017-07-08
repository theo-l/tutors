#!/usr/bin/env python
# encoding:utf-8

from fabric.api import (env, task, hosts)
# from fabric.contrib.console import confirm

from host_config import HOSTConfig
from require_config import OSRequirement, PYRequirement
from util import os as os_util

HOST_CONFIGS = [
    #       (host_string, password, host_name, host_role_name)
    ('vagrant@192.168.33.10:22', 'vagrant', 'test', 'test'),
   ('vagrant@192.168.33.20:22', 'vagrant', 'prod', 'prod'),
]

# System software dependencies
OS_REQUIREMENTS = (
    'nginx',
    'git',
    'python-dev',
    'python3-dev',
    'python-pip',
    'python3-pip'
)

Python_requirement = (
    'Django==1.10',
)

python_virtualenv = {
    'python_version':'3.6.0',
    'virtualenv_path':'~/workspace/'
}

config = HOSTConfig(HOST_CONFIGS)
config.setup_fabric_env(env)

os_require = OSRequirement(OS_REQUIREMENTS)
py_require = PYRequirement(packages=Python_requirement, virtualenv_config=python_virtualenv)


########################################
# tasks for test environment host
########################################
@task
@hosts(config.test_hosts)
def upgrade_test_hosts():
    os_util.update_system()


@task
def setup_env():
    """
    This task is used to build the server's initial environment
    """
    run('ls -alh')


@task
@hosts(config.test_hosts)
def setup_Test():
    os_require.install()
    py_require.install()


@task
@hosts(config.test_hosts)
def reset_Test():
    os_require.uninstall()
########################################
# tasks for production host
########################################


@task
@hosts(config.prod_hosts)
def upgrade_prod_hosts():
    os_util.update_system()


@task
@hosts(config.prod_hosts)
def setup_Prod():
    os_require.install()

,qa
@task
@hosts(config.prod_hosts)
def reset_Prod():
    os_require.uninstall()

########################################
# tasks for all hosts
########################################


@task
@hosts(config.all_hosts)
def upgrade_all_hosts():
    os_util.update_system()


@task
@hosts(config.all_hosts)
def setup_ALL():
    os_require.install()
    py_require.install()


@task
@hosts(config.all_hosts)
def reset_ALL():
    os_require.uninstall()
    py_require.uninstall()

