#!/usr/bin/env python
# encoding:utf-8

def build_role_or_name_to_hoststring_map(roles_or_names, map_type='role'):
    data ={}
    for role_or_name in roles_or_names:
        addresses =[]
        for host in HOST_CONFIGS:
            if map_type == 'role' and host[3] == role_or_name:
                addresses.append(host[0])
            elif map_type == 'name' and host[2] == role_or_name:
                addresses.append(host[0])
        data[role_or_name] = addresses
    return data



HOST_CONFIGS =[
#       (host_string, password, host_name, host_role_name) 
            ('vagrant@192.168.33.10:22','vagrant', 'test','test'),
            ('vagrant@192.168.33.20:22','vagrant', 'prod','prod'),
        ]

ALL_HOSTS = [host[0] for host in HOST_CONFIGS]
# all host names should be unique
HOST_NAMES = [host[2] for host in HOST_CONFIGS]

# all role names should be unique
HOST_ROLES = set([host[3] for host in HOST_CONFIGS])

# {host_string:password,...}
HOST_PASSWORDS = {host[0]:host[1] for host in HOST_CONFIGS}

# host_address->host_role_name
# used to find 'role_name' of 'host_address'
HOST_STRING_ROLE_MAP ={host[0]:host[3] for host in HOST_CONFIGS}
ROLE_HOST_STRING_MAP = build_role_or_name_to_hoststring_map(HOST_ROLES,'role')

# host_string - > host_name
HOST_STRING_NAME_MAP = {host[0]:host[2] for host in HOST_CONFIGS}
NAME_HOST_STRING_MAP = build_role_or_name_to_hoststring_map(HOST_NAMES,'name')




if __name__ == "__main__":
    print('host configs:', HOST_CONFIGS)
    print('host names:',HOST_NAMES)
    print('host roles:', HOST_ROLES)
    print('host passwords:',HOST_PASSWORDS)
    print('host_string -> role: ',HOST_STRING_ROLE_MAP)
    print('role -> host_string:',ROLE_HOST_STRING_MAP)
    print('host_string -> name:',HOST_STRING_NAME_MAP)
    print('name -> host_strings:', NAME_HOST_STRING_MAP)

