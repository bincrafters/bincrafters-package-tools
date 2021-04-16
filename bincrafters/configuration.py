import os
import yaml


class GlobalConfiguration(object):
    def __init__(self, path):
        if not os.path.exists(path):
            self.config_yml = {}
            return

        with open(path, 'r') as yaml_file:
            self.config_yml = yaml.safe_load(yaml_file)
            if not self.config_yml:
                self.config_yml = {}

    @property
    def conan_configuration_sources(self):
        return self.config_yml.get("conan_configuration_sources", [])
