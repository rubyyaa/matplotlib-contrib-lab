"""
===========================================
Damped Sinusoid with Exponential Envelope
===========================================

A damped sinusoid models the free response of many physical systems:
RLC circuits, mechanical oscillators, and acoustic resonators. This
example plots the oscillation alongside its exponential decay envelope.
"""

import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 2, 1000)

frequency = 5.0       # Hz
damping = 2.0         # 1/s
amplitude = 1.0

signal = amplitude * np.exp(-damping * t) * np.sin(2 * np.pi * frequency * t)
envelope_upper = amplitude * np.exp(-damping * t)
envelope_lower = -amplitude * np.exp(-damping * t)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, signal, color="steelblue", linewidth=1.2, label="Damped sinusoid")
ax.plot(t, envelope_upper, "--", color="coral", linewidth=0.9, label="Envelope")
ax.plot(t, envelope_lower, "--", color="coral", linewidth=0.9)
ax.fill_between(t, envelope_lower, envelope_upper, alpha=0.08, color="coral")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Damped Sinusoid: $A e^{-\\alpha t} \\sin(2\\pi f t)$")
ax.legend(loc="upper right")
ax.set_xlim(0, 2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules
#    is shown in this example:
#
#    - `matplotlib.axes.Axes.plot` / `matplotlib.pyplot.plot`
#    - `matplotlib.axes.Axes.fill_between` / `matplotlib.pyplot.fill_between`
#    - `matplotlib.pyplot.subplots`
#
# .. tags::
#
#    plot-type: line
#    level: beginner
