import requests


class Amon:
    def __init__(self, url="http://localhost:8000", max_chart_len=200):
        self.url = url
        requests.post(
            self.url + "/config",
            json={
                "max_chart_len": max_chart_len,
            },
        )

    def configure(self, max_chart_len=None, begin_at_zero=None):
        options = {}
        if max_chart_len is not None:
            options["max_chart_len"] = max_chart_len
        if begin_at_zero is not None:
            options["begin_at_zero"] = begin_at_zero

        requests.post(self.url + "/config", json=options)

    def create_chart(self, chart_id: str):
        requests.post(
            self.url + "/chart",
            json={
                "chart_id": chart_id,
            },
        )

    def push_data(
        self,
        chart_id: str,
        label: str,
        labels: list,
        data: list,
        border_color: str = "rgb(75, 192, 192",
    ):
        requests.post(
            self.url + "/data",
            json={
                "chart_id": chart_id,
                "label": label,
                "labels": labels,
                "border_color": border_color,
                "data": data,
            },
        )
