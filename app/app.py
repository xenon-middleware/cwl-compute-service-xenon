#!/usr/bin/env python3

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


import bottle
from bottle import (post, get, run, delete, request, response, HTTPResponse,
                    static_file, hook)

app = bottle.app()
app.compute_resource = create_xenon_compute_resource()

# TODO get from swagger.json basepath
prefix = ''

@hook('before_request')
def strip_path():
    request.environ['PATH_INFO'] = request.environ['PATH_INFO'].rstrip('/')

@get(prefix+'/')
def get_root():
    response.status = 200
    return '''{
        "cwl-compute-service-xenon": {
            "version": "0.0.1"
        }
    }'''

@get(prefix+'/api')
def get_swagger():
    return static_file('swagger.yml', root='api')

@get(prefix + '/jobs')
def get_jobs():
    return '[]'

@post(prefix + '/jobs')
def post_job():
    body = dict(request.json)
    response.status = 201
    return body

@post(prefix + '/jobs/<jobId>/cancel')
def cancel_job_by_id(jobId):
    return 'cancelling'

@delete(prefix + '/jobs/<jobId>')
def delete_job_by_id(jobId):
    response.status = 200
    return 'deleting'

@get(prefix + '/jobs/<jobId>')
def get_job_by_id(jobId):
    return 'here is a job by its id'

@get(prefix + '/jobs/<jobId>/log')
def get_job_log_by_id(jobId):
    return 'this is the log'
