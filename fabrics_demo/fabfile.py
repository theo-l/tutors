#!/usr/bin/env python
# encoding:utf-8

from fabric.api import (env, task, local, settings, abort, run, hosts, roles)
from fabric.contrib.console import confirm

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

config = HOSTConfig(HOST_CONFIGS)
config.setup_fabric_env(env)

os_require = OSRequirement(OS_REQUIREMENTS)
py_require = PYRequirement(Python_requirement)


@task
def hello():
    """
    Hello fab
    """
    # If a fabfile contains 1 @task decorator, then the plain function will not considered as task, only the function which
    # decorated by @task
    print('hello fab')


@task
def hello_args(name='Fabfile'):
    """
    Task arguments, task's argument can be passed in the following ways:
        1. fab task_name:arg_name=value
        2. fab task_name:value #fabric will guess the args value

    """
    print("Hello {}".format(name))


@task
def local_cmd():
    """
    Local commands which can run in local machine not remote
        - local: can execute local shell command
    """
    local('ls')


@task
def handle_fail():
    """
    Failure handing (warn_only setting option)
    """
    with settings(warn_only=True):  # settings is a context manager used to setting env for a specific block of code
        result = local('cmd_fail', capture=True)  # 'capture' param indicate return the command value
    if result.failed and not confirm("task failed, continue anyway?"):
        abort('task aborted at user request!')  # terminate the task


@task
@roles(config.all_hosts)
def show_env_vars():
    for key, value in env.items():
        if 'role' in key:
            print("{} := {}".format(key, value))

    run('ls -alh')


"""
Test @roles decorator
"""


@task
@roles('test')
def show_role_env():
    pass


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
