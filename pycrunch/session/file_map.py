from collections import defaultdict


class TestMap:
    def __init__(self):
        # filename -> test_fqn[]
        self.map = defaultdict(set)

    def did_found_tests_in_file(self, filename, test_names, module_name):
        if len(test_names) <= 0:
            return

        new_list = {f'{module_name}:{test}' for test in test_names}
        self.map[filename] = new_list

    def get_immutable_tests_for_file(self, filename):
        return list(self.map.get(filename, set()))

    def file_did_removed(self, filename):
        self.map.pop(filename)

    def test_exist(self, filename, fqn):
        return fqn in self.map[filename]


test_map = TestMap()