# CWL Compute Service using Xenon
#
# Copyright 2015 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from .util import expandfilenames
import yaml
import os
import logging

class Config(object):
    """
    Manages configuration, divided up in sections.

    A list of additional configurators contains the actual configuration. Later
    configurators in the list will overwrite those of earlier ones.
    Configurators must implement the section() and sections() methods.
    """
    def __init__(self, configurators=None):
        if configurators is None:
            configurators = []
        self.configurators = configurators
        self._sections = {}

    def add_section(self, name, keyvalue):
        """
        Add (overwrite) the configuration of a section.

        Parameters
        ----------
        name : str
            section name
        keyvalue : dict
            keys with values of the section
        """
        self._sections[name] = self.dict_value_expandvar(keyvalue)

    def section(self, name):
        """ Get the dict of key-values of config section.
        @param name: section name. Use 'DEFAULT' for default (unnamed) section.
        @raise KeyError: if section does not exist
        """
        values = {}
        for cfg in self.configurators:
            try:
                values.update(cfg.section(name))
            except KeyError:
                pass

        try:
            values.update(self._sections[name])
        except KeyError:
            if len(values) == 0:
                raise  # otherwise, it was found in one of the sub-configs.

        return values

    def sections(self):
        """ The set of configured section names. """
        sections = set(self._sections.keys())
        for cfg in self.configurators:
            sections |= cfg.sections()

        return sections

    def dict_value_expandvar(self, d):
        """ Expand all environment variables of given dict.
        Uses os.path.expandvars internally. Only applies to str values.
        @param d: dict to expand values of. """

        for key in d:
            try:
                d[key] = os.path.expandvars(d[key])
            except TypeError:
                pass  # d[key] is not a string
        return d


class FileConfig(object):
    """
    Manages configuration, divided up in sections.

    Configuration can be read from a yaml config file. Those files are
    divided into sections, where the first entries fall in the DEFAULT section.
    Within each section, entries are stored as key-value pairs with unique
    keys.
    """
    DEFAULT_FILENAMES = [
        "config.yml", ("..", "config.yml"), ("~", ".simcity_client")]

    def __init__(self, filenames=None):
        if filenames is None:
            filenames = FileConfig.DEFAULT_FILENAMES

        filenames = expandfilenames(filenames)

        success = False
        for file in filenames:
            if os.path.exists(file):
                with open(file, 'r') as ymlfile:
                    self.config = yaml.load(ymlfile)
                    success = True

            logging.info("Tried config file: ", file, ": ", success)

        if not success:
            raise ValueError(
            "No valid configuration files could be found: tried " +
            str(filenames))

    def section(self, name):
        """ Get key-values of a config section.
        @param name: str name of the config section
        @return: dict of key-values
        """
        try:
            return self.dict_value_expandvar(self.config[name])
        except NoSectionError:
            raise KeyError()

    def sections(self):
        """ The set of configured section names, including DEFAULT. """
        return frozenset(['DEFAULT'] + self.config.keys())