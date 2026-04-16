"""
=================================
RC Circuit Step Response
=================================

The voltage across a capacitor in a series RC circuit responds to a
step input as v(t) = V_in * (1 - exp(-t / RC)). This example plots
the charging curve for several time-constant values, illustrating how
component values affect the transient response.
"""

import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 5, 500)
v_in = 5.0  # step voltage in volts

tau_values = [0.2, 0.5, 1.0, 2.0]
colors = ["#e63946", "#457b9d", "#2a9d8f", "#e9c46a"]

fig, ax = plt.subplots(figsize=(8, 5))

for tau, color in zip(tau_values, colors):
    v_cap = v_in * (1 - np.exp(-t / tau))
    ax.plot(t, v_cap, color=color, linewidth=1.5,
            label=f"$\\tau$ = {tau} s")

ax.axhline(y=v_in, color="gray", linestyle=":", linewidth=0.8,
           label=f"$V_{{in}}$ = {v_in} V")
ax.axhline(y=0.632 * v_in, color="gray", linestyle="--", linewidth=0.6,
           alpha=0.5)
ax.text(4.6, 0.632 * v_in + 0.1, "63.2%", fontsize=8, color="gray",
        ha="right")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Capacitor Voltage (V)")
ax.set_title("RC Circuit Step Response: $v(t) = V_{in}(1 - e^{-t/\\tau})$")
ax.legend(loc="lower right", fontsize=9)
ax.set_xlim(0, 5)
ax.set_ylim(0, v_in * 1.1)
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
#    - `matplotlib.axes.Axes.axhline`
#    - `matplotlib.axes.Axes.text`
#    - `matplotlib.pyplot.subplots`
#
# .. tags::
#
#    plot-type: line
#    level: beginner
