import io
from collections import OrderedDict

from coverage import Coverage



class CoverageRunForSingleFile:
    def __init__(self, filename, lines, arcs, analysis):
        self.analysis = analysis
        self.arcs = arcs
        self.lines = lines
        self.filename = filename

    def as_json(self):
        return OrderedDict(filename=self.filename, lines_covered=self.lines, analysis=self.analysis, arcs=self.arcs,)

class CoverageRun:
    def __init__(self, entry_point, time_elapsed, test_metadata, execution_result):
        self.test_metadata = test_metadata
        self.time_elapsed = time_elapsed
        self.entry_point = entry_point
        self.execution_result = execution_result
        self.percentage_covered = -1
        self.files = []


    def parse_lines(self, cov):
        output_file = io.StringIO()
        self.percentage_covered = round(cov.report(file=output_file), 2)
        coverage_data = cov.get_data()

        for f in coverage_data.measured_files():
            lines = coverage_data.lines(f)
            arcs = coverage_data.arcs(f)
            analysis = cov.analysis2(f)
            self.files.append(CoverageRunForSingleFile(f, lines, arcs, analysis))

    def as_json(self):
        files_ = [x.as_json() for x in self.files]
        return dict(
            percentage_covered=self.percentage_covered,
            entry_point=self.entry_point,
            time_elapsed=round(self.time_elapsed * 1000, 2),
            test_metadata=self.test_metadata,
            files=files_,
            status=self.execution_result.status,
            captured_output=self.execution_result.captured_output,
        )


def serialize_test_run(cov : Coverage, entry_file, time_elapsed, test_metadata, execution_result):
    run_results = CoverageRun(entry_file, time_elapsed, test_metadata, execution_result)
    run_results.parse_lines(cov)
    return run_results




def serialize_test_set_state(test_set):

    from pycrunch.session.state import TestState

    def serialize_test(test_state: TestState):
        discovered_test = test_state.discovered_test
        execution_result = test_state.execution_result
        return dict(
            fqn=discovered_test.fqn,
            module=discovered_test.module,
            filename=discovered_test.filename,
            name=discovered_test.name,
            state=execution_result.status,
        )

    return dict(
        tests=[serialize_test(v) for (k, v) in test_set.items()],
        )