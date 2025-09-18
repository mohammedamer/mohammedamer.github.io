import marimo

__generated_with = "0.15.5"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import marimo as mo

    ROOT = Path("authoring/spring")
    return ROOT, mo


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
    from IPython.display import HTML
    import numpy as np
    import matplotlib.pyplot as plt
    from celluloid import Camera
    return Camera, np, plt


@app.cell
def _(Camera, ROOT, mo, np, plt):
    def spring1d():

        omega = 1 # rad/sec
        A = 0.1 # m

        T = 10

        t = np.linspace(0, T, 100)
        x = A*np.cos(omega*t)

        fig = plt.figure()
        ax = plt.subplot()

        ax.set_xlabel("t")
        ax.set_ylabel("x")

        ax.set_xlim((0, T))
        ax.set_ylim((-0.2,0.2))

        camera = Camera(fig)
        for idx, ti in enumerate(t):
            ax.plot(t[:idx+1], x[:idx+1], color="royalblue")
            ax.scatter(ti, x[idx], color="royalblue")
            camera.snap()

        anim = camera.animate()

        gif_path = ROOT / "spring1d.gif"  
        anim.save(gif_path, writer="pillow", fps=30)
        return mo.image(gif_path, width=600)

    spring1d()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
