from typing import List, Any

timeline = None

def trace(**kwargs):
    global timeline
    # todo: do not override, existing, create a list of subscribers
    if not timeline:
        # print('trace called, but no timeline injected: ', kwargs)
        return

    # todo: check for accepted types: str, int, dict() ?
    timeline.record(**kwargs)

def inject_timeline(new_timeline):
    global timeline
    # print(timeline)

    timeline = new_timeline
    # print(timeline)


class RecordedVariable:
    def __init__(self, name, value, timestamp):
        self.name = name
        self.value = value
        self.timestamp = timestamp

    def as_json(self):
        return dict(
            ts=self.timestamp,
            name=self.name,
            value=self.value,
        )

class InsightTimeline:
    # Timeline must be viewed as chrome performance timeline or jetbrains timeline profiler UI
    # Timeline represents state of application on each line (ideally)
    # currently - on each call of trace function
    variables: List[RecordedVariable]

    def __init__(self, clock):
        self.variables = []
        self.start_timestamp = None
        self.clock = clock
        pass

    def start(self):
        self.start_timestamp = self.clock.now()

    def as_json(self):
        results = []
        for v in self.variables:
            results.append(v.as_json())
        return results

    def record(self, **kwargs):
        # print(kwargs)
        # print(vars())
        ts = self.clock.now()
        adjusted_time = self.adjust_to_timeline_start(ts)
        for key, value in kwargs.items():
            # print(key + ' - ' + str(value))
            self.variables.append(RecordedVariable(key, value, adjusted_time))

    def adjust_to_timeline_start(self, ts):
        return ts - self.start_timestamp

    def make_safe_for_pickle(self):
        # this is last resort call,
        # consider avoiding it in first place to not lose performance
        import pickle
        for variable in self.variables:
            try:
                pickle.dumps(variable)
            except Exception as e:
                variable.value = \
                    f'This cannot be traced: {str(variable.value)}\n\nConsider removing this trace call for faster test execution.'
