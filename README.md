# matplotlib-contrib-lab

A simplified matplotlib-style gallery for ECE 105 students to practice the open-source contribution workflow: fork, branch, commit, and pull request.

This repository mirrors the structure of the real [matplotlib](https://github.com/matplotlib/matplotlib) gallery but is scoped for a single lab session. Each gallery example is a self-contained Python script that generates an ECE-themed visualization.

## Quick Start

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/matplotlib-contrib-lab.git
cd matplotlib-contrib-lab

# Install dependencies in your ece105 environment
mamba activate ece105
pip install matplotlib numpy pytest

# Run the tests
pytest tests/ -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution guide, including:

- How to create a gallery example
- File format and docstring requirements
- How to run tests
- PR template and AI disclosure policy

## Gallery Structure

```
galleries/examples/
    signals/           # Signal processing visualizations
    circuits/          # Circuit analysis visualizations
    controls/          # Control systems visualizations
    communications/    # Digital communications visualizations
    sensors/           # Sensor and measurement visualizations
```

## License

BSD 3-Clause. See [LICENSE](LICENSE).
