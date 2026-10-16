import unittest

from gwf.backends.base import Status
from gwf_torque_backend.torque import TorqueBackend


class QueueParsingTests(unittest.TestCase):
    def setUp(self):
        # Parsing does not need a live queue or the persistent tracking store.
        self.backend = TorqueBackend.__new__(TorqueBackend)

    def test_running_and_waiting_jobs(self):
        states = {"R": Status.RUNNING}
        states.update({state: Status.SUBMITTED for state in ("H", "Q", "T", "W")})
        for state, expected in states.items():
            with self.subTest(state=state):
                xml = (
                    "<Data><Job><Job_Id>123.server</Job_Id>"
                    "<job_state>{}</job_state></Job></Data>".format(state)
                )
                self.assertEqual(
                    self.backend.parse_queue_output(xml), {"123.server": expected}
                )

    def test_finished_and_unrecognized_jobs(self):
        xml = """<Data>
          <Job><Job_Id>1.server</Job_Id><job_state>C</job_state></Job>
          <Job><Job_Id>2.server</Job_Id><job_state>E</job_state></Job>
          <Job><Job_Id>3.server</Job_Id><job_state>?</job_state></Job>
        </Data>"""
        self.assertEqual(
            self.backend.parse_queue_output(xml),
            {job: Status.UNKNOWN for job in ("1.server", "2.server", "3.server")},
        )

    def test_empty_queue(self):
        self.assertEqual(self.backend.parse_queue_output("<Data/>"), {})


if __name__ == "__main__":
    unittest.main()
