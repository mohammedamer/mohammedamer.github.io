import marimo

__generated_with = "0.15.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # On Springs

    I would like to investigate some spring physics. First let's consider the one dimensional case. The spring force can be modeled as:

    $$
    F = -kx
    $$

    where $k$ is the spring constant. Using Newton's second law:

    $$
    \begin{align}
    F &= ma\\
    ma &= -kx\\
    a &= -\frac{k}{m}x
    \end{align}
    $$

    If we define $\omega^2 = \frac{k}{m}$, then we have:

    $$
    \begin{align}
    \frac{d^2{x}}{dt^2} = -\omega^2x
    \end{align}
    $$

    which is a second-order differential equation. A solution is:

    $$
    x = A\cos(\omega t+\phi)
    $$

    where $A$ and $\phi$ are amplitude and phase, respectively, which are constants that can be determined by initial conditions.

    What this looks like:
    """
    )
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
