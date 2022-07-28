from xml.etree import ElementTree

from gwf.backends.base import PbsLikeBackendBase, Status
from gwf.backends.exceptions import BackendError
from gwf.backends.utils import call

from gwf.utils import ensure_trailing_newline, retry


class TorqueBackend(PbsLikeBackendBase):

    option_defaults = {
        'cores': 1,
        'memory': '1gb',
        'walltime': '01:00:00',
        'account': None
    }

    @retry(on_exc=BackendError)
    def call_queue_command(self):
        return call('qstat', '-f', '--xml')

    def parse_queue_output(self, stdout):
        """
        C	Job is completed after having run.
        E	Job is exiting after having run.
        H	Job is held.
        Q	Job is queued, eligible to run or routed.
        R	Job is running.
        T	Job is being moved to new location.
        W	Job is waiting for its execution time (-a option) to be reached.
        """
        job_states = {}
        root = ElementTree.fromstring(stdout)
        for job in root.iter('Job'):
            job_id = job.find('Job_Id').text.split('.')[0]
            state = job.find('job_state').text
            if state == 'R':
                job_state = Status.RUNNING
            elif state in ['H', 'Q', 'T', 'W']:
                job_state = Status.SUBMITTED
            else:
                job_state = Status.UNKNOWN
            job_states[job_id] = job_state
        return job_states

    @retry(on_exc=BackendError)
    def call_submit_command(self, script, dependencies):
        args = []
        if dependencies:
            args.append('-W afterok:{}'.format(':'.join(dependencies)))
        return call('qsub', *args, input=script)

    @retry(on_exc=BackendError)
    def call_cancel_command(self, job_id):
        return call('qdel', job_id)

    def compile_script(self, target):

        out = []

        out.append(f'#PBS -N {target.name}')
        out.append(f'#PBS -W group_list={target.options["account"]}')
        out.append(f'#PBS -A {target.options["account"]}')
        out.append(f'#PBS -l nodes=1:ppn={target.options["cores"]}')
        out.append(f'#PBS -l mem={target.options["memory"]}')
        out.append(f'#PBS -l walltime={target.options["walltime"]}')
        out.append(f'#PBS -o {self.log_manager.stdout_path(target)}')
        out.append(f'#PBS -e {self.log_manager.stderr_path(target)}')

        out.append(f'cd {target.working_dir}')

        out.append(ensure_trailing_newline(target.spec))

        return '\n'.join(out)
