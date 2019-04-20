from datetime import datetime
from queue import Queue
import time

from pycrunch.api import shared
from pycrunch.api.serializers import serialize_coverage
from pycrunch.pipeline.abstract_task import AbstractTask
from pycrunch.runner.simple_test_runner import SimpleTestRunner
from pycrunch.session.combined_coverage import combined_coverage, CombinedCoverage


def serialize_combined_coverage(combined: CombinedCoverage):
    return [
        dict(filename=x.filename, lines_with_entrypoints=
        compute_lines(x)) for x in combined.files.values()
    ]


def compute_lines(x):
    result = dict()
    for (line_number, entry_points) in x.lines_with_entrypoints.items():
        result[line_number] = list(entry_points)

    zzz = {line_number:list(entry_points) for (line_number, entry_points) in x.lines_with_entrypoints.items()}
    return zzz

    # return result


class RunTestTask(AbstractTask):

    def __init__(self, tests, entry_point):
        self.entry_point = entry_point
        self.timestamp = shared.timestamp()
        self.tests = tests

    def run(self):
        runner = SimpleTestRunner()
        results = runner.run(self.tests)
        combined_coverage.add_multiple_results(results)
        shared.pipe.push(event_type='test_run_completed',
                         coverage=dict(all_runs=results),
                         data=self.tests,
                         timings=dict(start=self.timestamp, end=shared.timestamp()),
                         ),

        serialized = serialize_combined_coverage(combined_coverage)
        shared.pipe.push(event_type='combined_coverage_updated',
                         combined_coverage=serialized,

                         timings=dict(start=self.timestamp, end=shared.timestamp()),
                         ),
        pass;

# https://stackoverflow.com/questions/45369128/python-multithreading-queue