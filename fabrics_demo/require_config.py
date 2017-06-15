# -*- coding: utf-8 -*-
# @Author: theo-l
# @Date:   2017-06-12 19:31:07
# @Last Modified by:   theo-l
# @Last Modified time: 2017-06-12 20:30:54

"""
Here is the configuration file to configurate requirement dependencies
"""
import six
import platform
from fabric.api import run, cd

pkg_tools = {
    'debian': 'apt-get',
    'fedora': 'yum',
}


class Requirement:

    def __init__(self, *args, **kwargs):
        pass

    def install(self, name=None):
        """
        istall a specified package with the given name all all packages if not given
        """
        if name and not isinstance(name, six.string_types):
            raise ValueError('name should be a string/unicode value!')

        install_names = [name] if name is not None else self._packages

        for name in install_names:
            run('{} {}'.format(self.install_cmd, name))

    def upgrade(self, name=None):
        if name and not isinstance(name, six.string_types):
            raise ValueError('name should be a string/unicode value!')
        upgrade_names = [name] if name is not None else self._packages
        for name in upgrade_names:
            run('{} {}'.format(self.update_cmd, name))

    def uninstall(self, name=None):
        """
        unistall a specified package with the given name all all packages if not given
        """
        if name and not isinstance(name, six.string_types):
            raise ValueError('name should be a string/unicode value!')

        uninstall_names = [name] if name is not None else self._packages
        for name in uninstall_names:
            run('{} {}'.format(self.uninstall_cmd, name))


class OSRequirement(Requirement):

    def __init__(self, packages, *args, **kwargs):
        self._packages = packages
        self._init_pkg_tool()
        super(OSRequirement, self).__init__(*args, **kwargs)

    def _init_pkg_tool(self):
        dist = platform.linux_distribution()
        self.pkg_tool = pkg_tools[dist[0]]
        self.install_cmd = 'sudo {} install '.format(self.pkg_tool)
        self.uninstall_cmd = 'sudo {} remove '.format(self.pkg_tool)
        self.update_cmd = ''


class PYRequirement(Requirement):

    def __init__(self, packages=None, virtualenv_config=None, *args, **kwargs):
        """
        virtualenv_config = {
                'python_version':'3.6.0',
                'virtualenv_path':'/home/name/virtualenv/'
        }
        """
        self._packages = packages or []
        self._virtualenv_config = virtualenv_config or {}
        self._config_virtualenv()
        self._init_pkg_tool()
        super(PYRequirement, self).__init__(*args, **kwargs)

    def _config_virtualenv(self):
        if not self._virtualenv_config:
            self.using_virtual_env = False
            return
        else:
            self.using_virtual_env = True
            # todo here is the place to config python virtual env
            self.virtualenv_path = self._virtualenv_config['virtualenv_path']
            pass

    def _init_pkg_tool(self):
        self.install_cmd = 'pip install ' if self.using_virtual_env else 'sudo pip install '
        self.uninstall_cmd = ' pip uninstall ' if self.using_virtual_env else 'sudo pip uninstall '

    def install(self):
        if self.using_virtual_env:
            with cd(self.virtualenv_path):
                super(PYRequirement, self).install()
        super(PYRequirement, self).install()

    def uninstall(self):
        if self.using_virtual_env:
            with cd(self.virtualenv_path):
                super(PYRequirement, self).uninstall()
        super(PYRequirement, self).uninstall()
