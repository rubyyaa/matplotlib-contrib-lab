# Contributing to matplotlib-contrib-lab

This guide explains how to add a gallery example to this repository.
It follows a simplified version of the [matplotlib contribution workflow](https://matplotlib.org/stable/devel/contribute.html).

## Step-by-Step

1. **Fork** this repository on GitHub.
2. **Clone** your fork locally.
3. **Create a branch** named `add-YOUR-TOPIC-example` (e.g., `add-bode-plot-example`).
4. **Write your gallery example** in the appropriate subdirectory under `galleries/examples/`.
5. **Run the tests** to verify your example executes without errors.
6. **Commit** with a descriptive message following the 50-character subject line convention.
7. **Push** your branch and **open a pull request** against the instructor's `main` branch.

## Gallery Example File Format

Every gallery example is a standalone Python script. Follow this structure exactly:

```python
"""
================================
Your Example Title Goes Here
================================

One to three sentences describing what this example demonstrates
and why it is useful for engineers.
"""

import matplotlib.pyplot as plt
import numpy as np

# Your plotting code here (15-30 lines).
# Use numpy to generate data and pyplot to create the visualization.

plt.show()

# %%
#
# .. admonition:: References
#
#    The use of the following functions, methods, classes and modules
#    is shown in this example:
#
#    - `matplotlib.axes.Axes.plot` / `matplotlib.pyplot.plot`
#    - `matplotlib.pyplot.subplots`
#
# .. tags::
#
#    plot-type: line
#    level: beginner
```

### Required Sections

1. **RST docstring** at the top: title with `===` underline, and a 1-3 sentence description.
2. **Imports**: `matplotlib.pyplot as plt` and `numpy as np` at minimum.
3. **Plotting code**: 15-30 lines that generate data and create a visualization.
4. **`plt.show()`**: Must be called so the test runner can verify execution.
5. **References admonition**: List every matplotlib function/method your example uses.
6. **Tags section**: Include `plot-type` (e.g., `line`, `scatter`, `bar`, `stem`, `heatmap`) and `level` (`beginner` or `intermediate`).

### Subdirectories

Place your file in the subdirectory that best matches your topic:

| Subdirectory | Topics |
|---|---|
| `signals/` | FFT, spectrogram, filtering, discrete-time signals |
| `circuits/` | RC/RLC transients, phasor diagrams, impedance |
| `controls/` | Bode plots, Nyquist plots, pole-zero, step response |
| `communications/` | Constellation diagrams, eye diagrams, modulation |
| `sensors/` | Calibration curves, measurement uncertainty |

Create the subdirectory if it doesn't exist yet. Add an empty `__init__.py` if needed.

## Docstring Style

Use **NumPy-style docstrings** for any helper functions in your example:

```python
def compute_transfer_function(frequencies, poles, zeros):
    """Evaluate a transfer function at given frequencies.

    Parameters
    ----------
    frequencies : numpy.ndarray
        Array of frequencies in Hz.
    poles : list of complex
        Pole locations in the s-plane.
    zeros : list of complex
        Zero locations in the s-plane.

    Returns
    -------
    H : numpy.ndarray
        Complex transfer function values.
    """
```

## Running Tests

From the repository root:

```bash
pytest tests/ -v
```

The test runner automatically discovers all `.py` files under `galleries/examples/`
and runs each one. Your example passes if it executes without raising an exception.

## Commit Message Convention

Follow the same convention from Lab 2:

- **Subject line**: 50 characters or fewer, imperative mood ("Add ...", not "Added ...")
- **Blank line** after the subject
- **Body** (optional): explain what and why

Example:
```
Add gallery example: Bode plot of RC low-pass filter

Demonstrates semilogx for magnitude and phase response
of a first-order RC filter. Uses numpy for frequency sweep.
ECE 105 Lab 3 contribution assignment.
```

## AI Tool Disclosure

This project follows matplotlib's policy on generative AI use.

**Acceptable uses of AI tools when contributing:**
- Getting solution ideas for your plotting code
- Understanding existing example code in this repository
- Translating or proofreading your docstrings and PR descriptions

**You must:**
- Understand every line of code you contribute
- Be able to explain your code if asked by the instructor or a reviewer
- Disclose your AI usage honestly in the PR template

**You must not:**
- Submit AI-generated code without reading, testing, and understanding it
- Let AI tools directly create issues or PRs on your behalf
- Copy an AI response verbatim without adapting it to the project conventions

This policy mirrors the real matplotlib project's "Use of Generative AI" guidelines.
