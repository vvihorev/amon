import json
from urllib import request


class Amon:
    def __init__(self, url="http://localhost:8000", max_chart_len=200):
        self.url = url
        request.urlopen(request.Request(
            f"{self.url}/config",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "max_chart_len": max_chart_len,
            }).encode()
        ))

    def configure(self, max_chart_len=None, begin_at_zero=None):
        options = {}
        if max_chart_len is not None:
            options["max_chart_len"] = max_chart_len
        if begin_at_zero is not None:
            options["begin_at_zero"] = begin_at_zero

        request.urlopen(request.Request(
            f"{self.url}/config",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(options).encode()
        ))

    def create_chart(self, chart_id: str):
        request.urlopen(request.Request(
            f"{self.url}/chart",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "chart_id": chart_id,
            }).encode()
        ))

    def push_data(
        self,
        chart_id: str,
        label: str,
        labels: list,
        data: list,
        border_color: str = "rgb(75, 192, 192",
    ):
        request.urlopen(request.Request(
            f"{self.url}/data",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "chart_id": chart_id,
                "label": label,
                "labels": labels,
                "border_color": border_color,
                "data": data,
            }).encode()
        ))
