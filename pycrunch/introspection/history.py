from collections import deque


def serialize_intervals(root_interval):
    intervals_dict = [
        serialize_intervals(interval) for interval in root_interval.intervals
    ]

    events = [
        dict(name=evt.name, timestamp=evt.relative_timestamp())
        for evt in root_interval.events
    ]

    return [
        dict(
            name=root_interval.name,
            events=events,
            intervals=intervals_dict,
            start=root_interval.started_at,
            end=root_interval.stopped_at,
            duration=root_interval.duration(),
        )
    ]


class ExecutionHistory:
    def __init__(self):
        self.timelines = deque(maxlen=100)

    def save(self, timeline):
        self.timelines.append(timeline)

    def to_json(self):
        my_copy = self.timelines.copy()
        results = [
            dict(
                timeline_name=x.name,
                duration=x.duration(),
                intervals=serialize_intervals(x.root),
            )
            for x in my_copy
        ]

        return dict(results=results)


execution_history = ExecutionHistory()