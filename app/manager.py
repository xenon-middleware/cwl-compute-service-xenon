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

from .xenon_compute_resource import XenonComputeResource 

class Manager:
    def __init__(self, config):
        self._jobs = {}

        # Load the configuration
        if isinstance(config, Config):
            self._config = config
        else:
            self._config = Config()
            self._config.configurators.append(FileConfig(config))
        
    def create_xenon_compute_resource(host_id, host_cfg):
        self._computer = XenonComputeResource(
                    host=host_cfg['host'],
                    jobdir=host_cfg['path'],
                    prefix=host_id + '-',
                    max_time=host_cfg.get('max_time', 1440),
                    properties=host_cfg)