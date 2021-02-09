#!/usr/bin/python

from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import download, unzip, check_md5

import os
import shutil

class Python2Conan(ConanFile):
    name        = "python2"
    version     = "2.7.13"
    url         = "https://github.com/python/cpython"
    license     = "Python 2 License"
    description = "Python 2 Package"
    settings    = "os", "compiler", "build_type", "arch"
    generators  = "virtualenv"

    def source(self):
        zip_name = "python2.7.13-release.zip"
        download("https://github.com/python/cpython/archive/v2.7.13.zip", zip_name)
        check_md5(zip_name, "c31795e30d95b082627aaa9368fe65fc")
        unzip(zip_name)
        shutil.move("cpython-2.7.13", self.name)
        os.unlink(zip_name)

    def build(self):
        install_path = os.path.join(self.conanfile_directory, "install")

        os.chdir(self.name)
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("chmod +x configure")
            self.run("chmod +x install-sh")
            self.run("chmod +x Parser/asdl_c.py")
            self.run("./configure --prefix " + install_path)
            self.run("make")
            #self.run("make test")
            self.run("make install")

    def package(self):
        self.copy("*", dst="bin",     src="install/bin",     keep_path=True)
        self.copy("*", dst="include", src="install/include", keep_path=True)
        self.copy("*", dst="lib",     src="install/lib",     keep_path=True)
        self.copy("*", dst="share",   src="install/share",   keep_path=True)

    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.PYTHONPATH.append(self.package_folder)
