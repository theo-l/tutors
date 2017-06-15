#!/usr/bin/env python
# encoding:utf-8


class HOSTConfig:

    def __init__(self, host_configs, *args, **kwargs):
        """
        host_configs = [
            (host_string, password, host_name, host_role)
        ]
        """
        self.host_configs = host_configs
        self.all_host_strings = []
        self.all_host_names = []
        self.all_host_roles = []
        self.host_string_password_map = {}
        self.host_string_name_map = {}
        self.host_string_role_map = {}
        for host in host_configs:
            self.all_host_strings.append(host[0])
            self.all_host_names.append(host[2])
            self.all_host_roles.append(host[3])
            self.host_string_password_map[host[0]] = host[1]
            self.host_string_name_map[host[0]] = host[2]
            self.host_string_role_map[host[0]] = host[3]

        self.name_host_string_map = self.build_role_or_name_hoststring_map(self.host_string_name_map)
        self.role_host_string_map = self.build_role_or_name_hoststring_map(self.host_string_role_map)

        for name in self.all_host_names:
            setattr(self, '{}_hosts'.format(name), self.name_host_string_map[name])

        setattr(self, 'all_hosts', self.all_host_strings)

        for role in self.all_host_roles:
            setattr(self, '{}_roles'.format(role), self.role_host_string_map[role])

        setattr(self, 'all_roles', self.all_host_strings)

    def build_role_or_name_hoststring_map(self, reverse_data=None):
        if reverse_data is None:
            return

        data = {}
        for host_string, role_or_name in reverse_data.items():
            if role_or_name not in data:
                data[role_or_name] = []
            data[role_or_name].append(host_string)
        return data

    def setup_fabric_env(self, env):
        """
        setup fabric environment variable: 'env'
        """
        env.hosts = self.all_host_strings
        env.passwords = self.host_string_password_map
        env.roledefs.update(self.role_host_string_map)


if __name__ == '__main__':

    HOST_CONFIGS = [
        #       (host_string, password, host_name, host_role_name)
        ('vagrant@192.168.33.10:22', 'vagrant', 'test', 'test'),
        ('vagrant@192.168.33.20:22', 'vagrant', 'prod', 'prod'),
    ]

    config = HOSTConfig(HOST_CONFIGS)

    print(config.test_hosts)
