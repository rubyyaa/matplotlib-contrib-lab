"""Generate publication-quality sensor data visualizations.

This script creates synthetic temperature sensor data using NumPy
and produces scatter, histogram, and box plot visualizations saved
as PNG files.

Usage
-----
    python generate_plots.py
"""

import matplotlib.pyplot as plt
import numpy as np

# Create a function generate_data(seed) that returns sensor_a, sensor_b,
# and timestamps arrays with the same parameters as in the notebook.
# Use NumPy-style docstring with Parameters and Returns sections.


def generate_data(seed):
    """Generate synthetic sensor temperature data and timestamps.

    Parameters
    ----------
    seed : int
        Seed used to initialize NumPy's random number generator for
        reproducible results.

    Returns
    -------
    sensor_a : numpy.ndarray
        Array of shape (200,) containing Sensor A temperature readings in
        degrees Celsius, sampled from a normal distribution with mean 25.0
        and standard deviation 3.0.
    sensor_b : numpy.ndarray
        Array of shape (200,) containing Sensor B temperature readings in
        degrees Celsius, sampled from a normal distribution with mean 27.0
        and standard deviation 4.5.
    timestamps : numpy.ndarray
        Array of shape (200,) containing timestamps in seconds sampled
        uniformly from 0.0 to 10.0.
    """
    rng = np.random.default_rng(seed)
    n_readings = 200

    sensor_a = rng.normal(loc=25.0, scale=3.0, size=n_readings)
    sensor_b = rng.normal(loc=27.0, scale=4.5, size=n_readings)
    timestamps = rng.uniform(low=0.0, high=10.0, size=n_readings)

    return sensor_a, sensor_b, timestamps

# Create plot_scatter(sensor_a, sensor_b, timestamps, ax) that draws
# the scatter plot from the notebook onto the given Axes object.
# NumPy-style docstring. Modifies ax in place, returns None.


def plot_scatter(sensor_a, sensor_b, timestamps, ax):
    """Plot sensor temperature readings versus time on an existing Axes.

    Parameters
    ----------
    sensor_a : numpy.ndarray
        Array of shape (200,) with Sensor A temperature readings in
        degrees Celsius.
    sensor_b : numpy.ndarray
        Array of shape (200,) with Sensor B temperature readings in
        degrees Celsius.
    timestamps : numpy.ndarray
        Array of shape (200,) with timestamp values in seconds.
    ax : matplotlib.axes.Axes
        Existing Matplotlib Axes to draw the scatter plot on. The axes are
        modified in place.

    Returns
    -------
    None
        This function updates ``ax`` directly and does not create or return
        a new figure or axes.
    """
    ax.scatter(
        timestamps,
        sensor_a,
        color="tab:blue",
        alpha=0.75,
        s=28,
        label="Sensor A",
    )
    ax.scatter(
        timestamps,
        sensor_b,
        color="tab:orange",
        alpha=0.75,
        s=28,
        label="Sensor B",
    )

    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (\N{DEGREE SIGN}C)")
    ax.set_title("Sensor Temperature vs Time")
    ax.legend()
    ax.grid(alpha=0.25)

    return None


def plot_histogram(sensor_a, sensor_b, ax):
    """Plot overlaid histograms for two sensor temperature distributions.

    Parameters
    ----------
    sensor_a : numpy.ndarray
        Array of shape (200,) containing Sensor A temperature readings in
        degrees Celsius.
    sensor_b : numpy.ndarray
        Array of shape (200,) containing Sensor B temperature readings in
        degrees Celsius.
    ax : matplotlib.axes.Axes
        Existing Matplotlib Axes to draw the histogram visualization on.
        The axes are modified in place.

    Returns
    -------
    None
        This function updates ``ax`` directly and does not return any
        Matplotlib objects.
    """
    ax.hist(sensor_a, bins=30, alpha=0.5, color="tab:blue", label="Sensor A")
    ax.hist(sensor_b, bins=30, alpha=0.5, color="tab:orange", label="Sensor B")

    mean_a = sensor_a.mean()
    mean_b = sensor_b.mean()
    ax.axvline(
        mean_a,
        color="tab:blue",
        linestyle="--",
        linewidth=2,
        label=f"Sensor A mean: {mean_a:.2f} C",
    )
    ax.axvline(
        mean_b,
        color="tab:orange",
        linestyle="--",
        linewidth=2,
        label=f"Sensor B mean: {mean_b:.2f} C",
    )

    ax.set_xlabel("Temperature (\N{DEGREE SIGN}C)")
    ax.set_ylabel("Count")
    ax.set_title("Temperature Distribution: Sensor A vs Sensor B")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    return None


def plot_boxplot(sensor_a, sensor_b, ax):
    """Plot side-by-side box plots for two sensor temperature datasets.

    Parameters
    ----------
    sensor_a : numpy.ndarray
        Array of shape (200,) containing Sensor A temperature readings in
        degrees Celsius.
    sensor_b : numpy.ndarray
        Array of shape (200,) containing Sensor B temperature readings in
        degrees Celsius.
    ax : matplotlib.axes.Axes
        Existing Matplotlib Axes to draw the box plot visualization on.
        The axes are modified in place.

    Returns
    -------
    None
        This function updates ``ax`` directly and does not return any
        Matplotlib objects.
    """
    overall_mean = np.concatenate([sensor_a, sensor_b]).mean()

    ax.boxplot([sensor_a, sensor_b], tick_labels=["Sensor A", "Sensor B"])
    ax.axhline(
        overall_mean,
        color="gray",
        linestyle="--",
        linewidth=2,
        label=f"Overall mean: {overall_mean:.2f} C",
    )

    ax.set_ylabel("Temperature (deg C)")
    ax.set_title("Sensor Temperature Distribution Comparison")
    ax.legend()
    ax.grid(axis="y", alpha=0.25)

    return None

# Create main() that generates data, creates a 1x3 subplot figure,
# calls each plot function, adjusts layout, and saves as sensor_analysis.png
# at 150 DPI with tight bounding box.


def main():
    """Generate synthetic sensor data and save a four-panel analysis figure.

    Parameters
    ----------
    None

    Returns
    -------
    None
        Creates a 2x2 figure containing scatter, histogram, and box plot
        visualizations plus a summary statistics panel, then saves it as
        ``sensor_analysis.png``.
    """
    sensor_a, sensor_b, timestamps = generate_data(seed=1234)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plot_scatter(sensor_a, sensor_b, timestamps, axes[0, 0])
    plot_histogram(sensor_a, sensor_b, axes[0, 1])
    plot_boxplot(sensor_a, sensor_b, axes[1, 0])

    stats_ax = axes[1, 1]
    stats_ax.axis("off")
    stats_text = (
        "Summary Statistics\n\n"
        f"Sensor A mean: {sensor_a.mean():.2f} C\n"
        f"Sensor A std:  {sensor_a.std(ddof=1):.2f} C\n\n"
        f"Sensor B mean: {sensor_b.mean():.2f} C\n"
        f"Sensor B std:  {sensor_b.std(ddof=1):.2f} C\n\n"
        f"Combined mean: {np.concatenate([sensor_a, sensor_b]).mean():.2f} C"
    )
    stats_ax.text(0.05, 0.95, stats_text, va="top", fontsize=11)

    fig.tight_layout()
    fig.savefig("sensor_analysis.png", dpi=150, bbox_inches="tight")

    return None


if __name__ == '__main__':
    main()
