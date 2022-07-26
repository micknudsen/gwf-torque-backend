from xml.etree import ElementTree

from gwf.backends.base import PbsLikeBackendBase, Status
from gwf.backends.exceptions import BackendError
from gwf.backends.utils import call

from gwf.utils import retry


class TorqueBackend(PbsLikeBackendBase):

    @retry(on_exc=BackendError)
    def call_queue_command(self):
        return call('qstat', '-f', '--xml')

    def parse_queue_output(self, stdout):
        job_states = {}
        root = ElementTree.fromstring(stdout)
        for job in root.iter('Job'):
            job_id = job.find('Job_Id').text
            state = job.find('job_state').text
            if state == 'R':
                job_state = Status.RUNNING
            elif state in ['H', 'Q', 'T', 'W']:
                job_state = Status.SUBMITTED
            else:
                job_state = Status.UNKNOWN
            job_states[job_id] = job_state
        return job_states
