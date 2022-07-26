from gwf.backends.base import PbsLikeBackendBase
from gwf.backends.exceptions import BackendError
from gwf.backends.utils import call

from gwf.utils import retry


class TorqueBackend(PbsLikeBackendBase):

    @retry(on_exc=BackendError)
    def call_queue_command(self):
        return call('qstat', '-f', '--xml')
