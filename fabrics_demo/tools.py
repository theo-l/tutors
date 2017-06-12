#!/usr/bin/env python
# encoding:utf-8

from fabric.api import run

class OS:


    PKG_INSTALL_CMD = 'sudo {} install {}'
    PKG_REMOVE_CMD = 'sudo {} remove {}'

    def __init__(self, pkg_tool_name=None, packages=None):
        """
        Configuare system package tool name
        package dependencies
        """

        if pkg_tool_name is not None:
            self.pkg_tool_name = pkg_tool_name
        else:
            import platform
            dist = platform.linux_distribution()
            if dist[0] =='debian':
                self.pkg_tool_name = 'apt-get'
            else:
                self.pkg_tool_name = 'apt-get'

        self.packages = packages or []


    def packages(self, packages=None):
        """
        Install system package dependencies
        """
        for pkg in packages:
            run(self.pkg_install_cmd.format(self.pkg_tool_name, pkg))

    def nopackages(self, packages=None):
        """
        Remove system package dependencies
        """
        pass



