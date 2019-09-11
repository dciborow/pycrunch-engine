import time

from pycrunch.api import shared
from pycrunch.pipeline.abstract_task import AbstractTask
from pycrunch.session.file_map import test_map


class FileRemovedTask(AbstractTask):
    def __init__(self, file):
        self.file = file
        self.timestamp = time.time()

    def run(self):
        from pycrunch.session import state
        shared.pipe.push(event_type='file_modification',
                         modified_file=self.file,
                         ts=self.timestamp,
                         )

        test_map.file_did_removed(self.file)
        from pycrunch.discovery.simple import TestSet
        state.engine.test_discovery_will_become_available(TestSet())