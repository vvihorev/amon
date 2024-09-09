import time
import math
from amon import Amon

mon = Amon(max_chart_len=20)

# Create a chart and push data to it, the chart updates in real time
mon.create_chart(chart_id="1")
for i in range(-10, 10):
    mon.push_data("1", "Sigmoid", [i], [1 / (1 + math.exp(-i))])

# Plot multiple series on the same chart
for i in range(-10, 10):
    mon.push_data("1", "Inverse Sigmoid", [i], [1 + -1 / (1 + math.exp(-i))], border_color='rgb(120, 0, 0)')

# Configure all new charts
mon.configure(begin_at_zero=False)

# Old data will be dropped automatically
mon.create_chart("2")
for i in range(-20, 20):
    mon.push_data("2", "Quadratic Function", [i], [2*i**2 + 3*i - 10], border_color='rgb(0, 120, 0)')
    time.sleep(0.1)

