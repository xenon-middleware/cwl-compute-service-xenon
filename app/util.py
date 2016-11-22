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
import os

def issequence(obj):
    """ True if given object is a list or a tuple. """
    return isinstance(obj, (list, tuple))

def expandfilename(filename):
    """ Joins sequences of filenames as directories, and expands variables and
        user directory. """
    if issequence(filename):
        filename = os.path.join(*filename)
    return os.path.expandvars(os.path.expanduser(filename))


def expandfilenames(filenames):
    """ Runs expandfilename on each item of a given list. """
    if not issequence(filenames):
        filenames = [filenames]
    return [expandfilename(fname) for fname in filenames]