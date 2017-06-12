#!/usr/bin/env python
# encoding:utf-8

from fabric.api import (env, task, local, settings, abort, run, hosts, roles)
from fabric.contrib.console import confirm

from util import os as os_util


"""
Hello fab
"""
# If a fabfile contains 1 @task decorator, then the plain function will not considered as task, only the function which 
# decorated by @task
@task
def hello():
    print('hello fab')


"""
Task arguments, task's argument can be passed in the following ways:
    1. fab task_name:arg_name=value
    2. fab task_name:value #fabric will guess the args value

"""
@task
def hello_args(name='Fabfile'):
    print("Hello {}".format(name))

"""
Local commands which can run in local machine not remote
    - local: can execute local shell command
"""
@task
def local_cmd():
    local('ls')

"""
Failure handing (warn_only setting option)
"""
@task
def handle_fail():
    with settings(warn_only=True): # settings is a context manager used to setting env for a specific block of code
        result = local('cmd_fail', capture=True) # 'capture' param indicate return the command value 
    if result.failed and not confirm("task failed, continue anyway?"):
        abort('task aborted at user request!') # terminate the task


"""
Remote connection
"""
from  host_config import *
env.hosts = ALL_HOSTS 
env.passwords = HOST_PASSWORDS
env.roledefs.update(ROLE_HOST_STRING_MAP)
test_hosts = NAME_HOST_STRING_MAP['test']
prod_hosts = NAME_HOST_STRING_MAP['prod']
all_hosts = ALL_HOSTS

# System software dependencies
os_requirements = (
        'nginx',
        )


os_require = os_util.OSUtil(os_requirements)



"""
Environment variables
"""
@task
#@hosts(test_hosts)
@roles('prod','test')
def show_env_vars():
    for key, value in env.items():
        if 'role' in key:
            print("{} := {}".format(key, value))
    
    role_name = HOST_STRING_ROLE_MAP[env.host_string]
    print(role_name)
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
@hosts(test_hosts)
def upgrade_test_hosts():
    os_util.update_system()

@task
def setup_env():
    """
    This task is used to build the server's initial environment
    """
    run('ls -alh')


@task
@hosts(test_hosts)
def install_test_os_requirement():
    os_require.install_os_requirement()
    
@task
@hosts(test_hosts)
def remove_test_os_requirement():
    os_require.remove_os_requirement()
########################################
# tasks for production host
########################################
@task
@hosts(prod_hosts)
def upgrade_prod_hosts():
    os_util.update_system()


@task
@hosts(prod_hosts)
def install_prod_os_requirement():
    os_require.install_os_requirement()

@task
@hosts(prod_hosts)
def remove_prod_os_requirement():
    os_require.remove_os_requirement()

########################################
# tasks for all hosts
########################################
@task
@hosts(all_hosts)
def upgrade_all_hosts():
    os_util.update_system()


@task
@hosts(all_hosts)
def install_all_os_requirement():
    os_require.install_os_requirement()


@task
@hosts(all_hosts)
def remove_all_os_requirement():
    os_require.remove_os_requirement()
