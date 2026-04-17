"""
=============================
Moving Average Filter Example
=============================

This example shows how a moving average smooths a noisy sinusoidal
signal. It is a simple way to illustrate low-pass filtering in the
time domain.
"""

import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(1965)
t = np.linspace(0, 2, 400)
clean = np.sin(2 * np.pi * t)
noise = rng.normal(0, 0.3, t.size)
signal = clean + noise

window = np.ones(20) / 20
smooth = np.convolve(signal, window, mode="same")

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, signal, color="steelblue", linewidth=1.0, alpha=0.6, label="Noisy signal")
ax.plot(t, clean, color="black", linewidth=1.2, linestyle="--", label="Original sine")
ax.plot(t, smooth, color="coral", linewidth=2.0, label="Moving average")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Moving Average Filter")
ax.set_xlim(0, 2)
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right")

plt.tight_layout()
plt.show()

# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules
#    is shown in this example:
#
#    - `matplotlib.axes.Axes.legend` / `matplotlib.pyplot.legend`
#    - `matplotlib.axes.Axes.plot` / `matplotlib.pyplot.plot`
#    - `matplotlib.pyplot.subplots`
#
# .. tags::
#
#    plot-type: line
#    level: beginner