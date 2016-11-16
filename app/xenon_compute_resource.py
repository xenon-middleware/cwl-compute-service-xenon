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

try:
    import xenon
    from xenon import java
    xenon_support = True
except ImportError:
    xenon_support = False

if not xenon_support:
    raise EnvironmentError("Xenon not installed. Install "
                            "with pip install -U '.[xenon]'")

class XenonComputeResource():
    """ Submits job using Xenon. """
    def __init__(self, host, prefix, jobdir, max_time=1440,
                 properties=None):
        try:
            xenon.init(log_level='INFO')
        except ValueError:
            pass  # xenon is already initialized

        self.max_time = max_time
        urlsplit = self.host.split('://')
        if len(urlsplit) != 2:
            raise ValueError("host must contain a scheme and a "
                             "hostname, syntax `scheme://host`.")
        self.scheme, self.hostname = urlsplit
        if properties is not None:
            self.private_key = properties.get('private-key')
            self.password = properties.get('password')

            self.xenon_properties = xenon.conversions.dict_to_HashMap({
                key[len('xenon-property-'):]: value
                for key, value in properties.items()
                if key.startswith('xenon-property-')
            })

            self.scheduler_properties = xenon.conversions.dict_to_HashMap({
                key[len('scheduler-property-'):]: value
                for key, value in properties.items()
                if key.startswith('scheduler-property-')
            })
        else:
            self.xenon_properties = None
            self.scheduler_properties = None
            self.private_key = None
            self.password = None

    def _do_submit(self, job, command):
        """ Submit a command with given job metadata. """
        with xenon.Xenon(self.xenon_properties) as x:
            try:
                jobs = x.jobs()
                desc = xenon.jobs.JobDescription()
                desc.addEnvironment('SIMCITY_JOBID', job.id)
                desc.setMaxTime(int(self.max_time))
                desc.setWorkingDirectory(self.jobdir)
                desc.setStdout("stdout_" + job.id + ".txt")
                desc.setStderr("stderr_" + job.id + ".txt")

                scheduler = self.scheduler(x)

                if scheduler.isOnline():
                    desc.setExecutable("/bin/sh")
                    if len(command) == 1:
                        command_str = "'{0}'".format(command[0])
                    else:
                        command_str = "'{0}' '{1}'".format(
                            command[0], "' '".join(command[1:]))
                    desc.setArguments([
                        "-c", "nohup {0} >'{1}' 2>'{2}' &"
                        .format(command_str, desc.getStdout(),
                                desc.getStderr())])
                    job = jobs.submitJob(scheduler, desc)
                    print("Waiting for submission to finish...")
                    jobs.waitUntilDone(job, 0)
                    print("Done.")
                else:
                    desc.setExecutable(command[0])
                    desc.setArguments(command[1:])
                    job = jobs.submitJob(scheduler, desc)

                return job.getIdentifier()
            except xenon.exceptions.XenonException as ex:
                raise IOError(ex.javaClass(),
                              "Cannot submit job with Xenon: {0}"
                              .format(ex.message()))

    def kill(self, job):
        """
        Stop a started job.
        """
        self.check_job(job)

        with xenon.Xenon(self.xenon_properties) as x:
            try:
                for xjob in self.jobs(x):
                    if xjob.getIdentifier() == job['batch_id']:
                        x.jobs().cancelJob(xjob)
                        return archive_job(job)
            except xenon.exceptions.XenonException as ex:
                raise IOError(ex.javaClass(),
                              "Cannot kill job with Xenon: {0}"
                              .format(ex.message()))
        return None

    def status(self, jobs):
        """
        Get the status of a list of running jobs, one of:
        Adapter.{DONE, RUNNING, PENDING}

        @raise ValueError: if job does not contain 'host_section' and
            'batch_id' attributes.
        """
        for job in jobs:
            self.check_job(job)

        with xenon.Xenon(self.xenon_properties) as x:
            xjobs = self.jobs(x)
            return [XenonAdapter.single_status(job, xjobs, x) for job in jobs]

    def scheduler(self, x):
        """ Get a Xenon Scheduler. """
        credential = None
        if (self.private_key is not None or
                self.password is not None):
            cred = x.credentials()
            if self.password is not None:
                password = java.lang.String(self.password).toCharArray()
            else:
                password = None

            if self.private_key is not None:
                credential = cred.newCertificateCredential(
                    'ssh', self.private_key, None, password,
                    None)
            else:
                credential = cred.newPasswordCredential(
                    'ssh', None, password, None)

        return x.jobs().newScheduler(self.scheme, self.hostname, credential,
                                     self.scheduler_properties)

    def jobs(self, x):
        """ Get a list of Xenon Job objects. """
        return x.jobs().getJobs(self.scheduler(x), [])

    @staticmethod
    def single_status(job, xjobs, x):
        """
        Get the status of a single job, given a list of Xenon Job objects.
        @param job: SIM-CITY Job
        @param xjobs: list of Xenon Job objects
        @param x: Xenon
        @return one of Adapter.{DONE, RUNNING, PENDING}.
        """
        try:
            for xjob in xjobs:
                if xjob.getIdentifier() == job['batch_id']:
                    xstatus = x.jobs().getJobStatus(xjob)

                    if xstatus.isRunning():
                        return Adapter.RUNNING
                    elif xstatus.isDone():
                        return Adapter.DONE
                    else:
                        return Adapter.PENDING
            return Adapter.DONE
        except xenon.exceptions.XenonException:
            return None