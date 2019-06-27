import io
from pathlib import Path

import logging

import yaml

logger = logging.getLogger(__name__)

class Configuration:
    def __init__(self):
        self.discovery_exclusions = ()
        self.working_directory = Path('.')
        self.runtime_engine = 'pytest'
        self.available_engines = ['simple', 'pytest']

    def runtime_engine_will_change(self, new_engine):
        self.throw_if_not_supported_engine(new_engine)
        self.runtime_engine = new_engine

    def throw_if_not_supported_engine(self, new_engine):
        if new_engine not in self.available_engines:
            raise Exception(f'engine {new_engine} not available. Possible options: {self.available_engines}')

    def load_runtime_configuration(self):
        joinpath = self.working_directory.joinpath('.discovery.yaml')
        print(str(joinpath.absolute()))
        print(joinpath)
        with io.open(joinpath, encoding='utf-8') as f:
            x = yaml.safe_load(f)
            discovery = x.get('discovery', None)
            if discovery:
                exc = discovery.get('exclusions', None)
                if not hasattr(exc, "__len__"):
                    raise Exception('.discovery.yaml: discovery->exclusions should be array')
                self.discovery_exclusions = tuple(exc)
            print(x)
            print(f)


config = Configuration()