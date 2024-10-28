"""
1. Create an empty directory where the `metrics` file will be stored.
2. Point the metrics exporter to the created directory: `Exporter("./mydir/metrics")`.
3. Run `python -m http.server` from the created directory to expose metrics to Prometheus.

See __main__ for a usage example of the Exporter.
"""
import time
from pathlib import Path
from threading import Thread


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Metric:
    seen_metrics = set()
    COUNTER = "counter"
    GAUGE = "gauge"

    def __init__(self, name, m_type, help):
        base = name.split("{")[0]
        self.name = name
        self.m_type = m_type
        self.value = None
        self.text = f"# HELP {base} {help}\n# TYPE {base} {self.m_type}\n{self.name}"

    def __str__(self):
        if self.value is None:
            return ""
        return f"{self.text} {self.value}\n"

    def update(self, value):
        self.value = value


class Exporter(metaclass=Singleton):
    def __init__(self, metrics_file_path="metrics", export_period=2, debug=False):
        self.metrics_file_path = Path(metrics_file_path)
        if not self.metrics_file_path.exists():
            self.metrics_file_path.touch()
        self.metrics = {}
        self.intervals = {}
        self.last_write = time.time()
        self.export_period = export_period
        self.debug = debug

    def timer_start(self, key: str):
        self.intervals[key] = time.time()

    def timer_stop(self, key: str):
        if key not in self.intervals:
            return
        length = time.time() - self.intervals[key]
        stat = f"Execution time `{key}`: {length:.6f} seconds"
        if self.debug:
            print("\033[1;32mDEBUG: ", stat, "\x1b[0m", flush=True)

        if key in self.metrics:
            self.metrics[key].update(length)
        else:
            self.metrics[key] = Metric(
                key, Metric.GAUGE, "Automatically generated timer metric."
            )
        self.try_write_to_file()

    def try_write_to_file(self):
        ts = time.time()
        if ts - self.last_write <= self.export_period:
            return
        Thread(target=self._write_to_file).start()

    def _write_to_file(self):
        if self.debug:
            print("\033[1;32mDEBUG: Writing metrics to file\x1b[0m", flush=True)
        self.metrics_file_path.write_text(
            "\n".join(list(map(str, self.metrics.values())))
        )
        self.last_write = time.time()

    def counter_inc(self, key, value=1):
        if key not in self.metrics:
            metric = Metric(
                key, Metric.COUNTER, "Automatically generated counter metric."
            )
            metric.value = 0
            self.metrics[key] = metric
        metric = self.metrics[key]
        metric.update(metric.value + value)
        if self.debug:
            print(
                f"\033[1;32mDEBUG: Increment `{metric.name}` to {metric.value}\x1b[0m",
                flush=True,
            )
        self.try_write_to_file()


if __name__ == "__main__":
    e = Exporter(metrics_file_path="metrics", debug=True)

    while True:
        e.timer_start('test{loop="outer"}')

        for i in range(3):
            e.counter_inc('iter_count{loop="inner"}')

        time.sleep(1)
        e.counter_inc('iter_count{loop="outer"}')

        e.timer_stop('test{loop="outer"}')
        print()
