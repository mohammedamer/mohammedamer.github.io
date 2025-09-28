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
    # On Spring Simulation

    I would like to investigate some spring physics. First let's consider the one dimensional case. The spring force can be modeled as:

    $$
    F = -kx
    $$

    where $k$ is the spring constant. Using Newton's second law:

    $$
    \begin{align*}
    F &= ma\\
    ma &= -kx\\
    a &= -\frac{k}{m}x
    \end{align*}
    $$

    If we define $\omega^2 = \frac{k}{m}$, then we have:

    $$
    \begin{align*}
    \frac{d^2{x}}{dt^2} = -\omega^2x
    \end{align*}
    $$

    which is a second-order differential equation. A solution is:

    $$
    x = A\cos(\omega t+\phi)
    $$

    where $A$ and $\phi$ are amplitude and phase, respectively, which are constants that can be determined by initial conditions. The velocity and acceleration can be determined by differentiating the position equation:

    $$
    v = -A\omega\sin(\omega t+\phi)\\
    a = -A\omega^2\cos(\omega t + \phi)
    $$

    What this looks like:
    """
    )
    return


@app.cell
def _():
    from IPython.display import HTML
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from celluloid import Camera
    return Camera, np, patches, plt


@app.cell
def _(Camera, ROOT, mo, np, patches, plt):
    def spring1d():

        omega = 1 # rad/sec
        A = 0.1 # m

        T = 3*1/omega*2*np.pi

        t = np.linspace(0, T, 100)
        x = A*np.cos(omega*t)

        fig, (ax_mass, ax_graph) = plt.subplots(1, 2, figsize=(12,5))

        ax_graph.set_xlabel("t")
        ax_graph.set_ylabel("x")

        ax_graph.set_xlim((0, T))
        ax_graph.set_ylim((-0.2,0.2))

        xmin = -0.2
        xmax = 0.2
        ymin = -0.1
        ymax = 1.0

        ax_mass.set_xlim((xmin, xmax))
        ax_mass.set_ylim((ymin, ymax))
        ax_mass.set_yticks([])

        mass_width = 0.08
        mass_height = 0.2

        wall_x = -0.19

        camera = Camera(fig)

        for idx, ti in enumerate(t):

            ax_mass.hlines(0, xmin, xmax, color="black")
            ax_mass.vlines(0, ymin, ymax, color="black", linestyle="dashed")
            ax_mass.vlines(wall_x, ymin, ymax, color="black")

            _x = x[idx]-mass_width/2.

            rect = patches.Rectangle((_x, 0.01), 0.08, 0.2, linewidth=1, edgecolor='black', facecolor='none')
            ax_mass.add_patch(rect)

            ax_mass.hlines(mass_height/2., wall_x, _x, color="black")

            x_line, = ax_graph.plot(t[:idx+1], x[:idx+1], color="royalblue", label="x")
            ax_graph.scatter(ti, x[idx], color="royalblue")

            camera.snap()

        anim = camera.animate()

        gif_path = ROOT / "spring1d.gif"  
        anim.save(gif_path, writer="pillow", fps=30)
        return mo.image(gif_path, width=600)

    spring1d()
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    This is the infamous **harmonic osillation**. As the mass is displaced from the spring equilibrium position, the restoring force increases. This decelerates the mass till it stops completely and reverse direction and starts accelerating in the other direction. As the mass crosses the equilibrium position, a restoring force kicks in in the other direction and so on.

    As you may imagine, this will continue for eternity if not disturbed, which is not in agreement with our everyday experience of the physical world. Hence, this is an idealization (at least for the macro phenomenon) that lives only in a platonic realm. In reality, in addition to the restoring force, there are also resitive forces, such as friction, whcih interfere with that happening.

    We can add the contribution of resitive force as:

    $$
    F = -kx - b v
    $$

    where $b$ is a constant. The resistive force is represented by the second term, which depends on velocity. So, when the object is not moving, it does not experience a resistive force (which is reasonable) and the magnitude of the force will depend on the speed of the object (so higher speed $\rightarrow$ larger resistance).

    Same way, using Newton second law to deduce the equation of motion:

    $$
    \frac{d^2x}{dt^2} + \frac{b}{m} \frac{dx}{dt} + \frac{k}{m} x = 0 
    $$

    When the resistive force is weaker than the restoring force, we get the **underdamped oscillator**:

    $$
    x(t) = A e^{-\frac{b}{2m} t} \cos(\omega t + \phi) 
    $$
    """
    )
    return


@app.cell
def _(Camera, ROOT, mo, np, patches, plt):
    def damped_spring1d():

        k = 1
        m = 1
        omega = np.sqrt(k/m) # rad/sec
        A = 0.1 # m
        b = 0.2

        T = 5*1/omega*2*np.pi

        t = np.linspace(0, T, 100)
        x = A*np.exp(-b/(2*m)*t)*np.cos(omega*t)

        fig, (ax_mass, ax_graph) = plt.subplots(1, 2, figsize=(12,5))

        ax_graph.set_xlabel("t")
        ax_graph.set_ylabel("x")

        ax_graph.set_xlim((0, T))
        ax_graph.set_ylim((-0.2,0.2))

        xmin = -0.2
        xmax = 0.2
        ymin = -0.1
        ymax = 1.0

        ax_mass.set_xlim((xmin, xmax))
        ax_mass.set_ylim((ymin, ymax))
        ax_mass.set_yticks([])

        mass_width = 0.08
        mass_height = 0.2

        wall_x = -0.19

        camera = Camera(fig)

        for idx, ti in enumerate(t):

            ax_mass.hlines(0, xmin, xmax, color="black")
            ax_mass.vlines(0, ymin, ymax, color="black", linestyle="dashed")
            ax_mass.vlines(wall_x, ymin, ymax, color="black")

            _x = x[idx]-mass_width/2.

            rect = patches.Rectangle((_x, 0.01), 0.08, 0.2, linewidth=1, edgecolor='black', facecolor='none')
            ax_mass.add_patch(rect)

            ax_mass.hlines(mass_height/2., wall_x, _x, color="black")

            x_line, = ax_graph.plot(t[:idx+1], x[:idx+1], color="royalblue", label="x")
            ax_graph.scatter(ti, x[idx], color="royalblue")

            camera.snap()

        anim = camera.animate()

        gif_path = ROOT / "damped_spring1d.gif"  
        anim.save(gif_path, writer="pillow", fps=30)
        return mo.image(gif_path, width=600)

    damped_spring1d()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    Let's consider simulations in 2D. First, let's assume a mass fixed to ceiling by a spring and free to move in two dimensions under the influence of the spring force and gravity. Let the mass poition be represented by the vector $\textbf{r}$, the fixation point is the origin, gravity acceleration is $\textbf{g} = -g \hat{\textbf{j}}$, where $g = 9.8$, and the unstretched spring length is $l$. Then:

    $$
    \frac{d^2\textbf{r}}{dt^2} = -\frac{k}{m}(|\textbf{r}| - l) \textbf{r} + \frac{1}{m} \textbf{g}
    $$

    To solve numerically, we may represent the previous motion equation as:

    $$
    \begin{align*}
    |\textbf{r}| &= \sqrt{x^2 + y^2}\\\\
    \frac{d\textbf{v}}{dt} &= -\frac{k}{m}(|\textbf{r}| - l) \textbf{r} + \frac{1}{m} \textbf{g} \\\\
    \frac{d\textbf{r}}{dt} &= \textbf{v}
    \end{align*}
    $$
    """
    )
    return


@app.cell
def _(Camera, ROOT, mo, np, plt):
    from scipy.integrate import odeint

    def hanged_spring2d():

        k = 1
        m = 1
        g = np.array([0, -9.8])

        l = 1

        r0 = np.array([1, 1.5])
        v0 = np.array([0, 0.])

        s0 = np.concat((r0, v0))
    
        def motion_fn(s, t):

            r0, v0 = s[:2], s[2:]
        
            r_abs = np.linalg.norm(r0)
        
            dv = -k/m*(r_abs - l)*r0 + 1/m*g
            dr = v0

            return np.concat([dr, dv])
    
        t = np.linspace(0, 10, 100)

        sol = odeint(motion_fn, s0, t)

        fig, (ax_mass, ax_graph) = plt.subplots(1, 2, figsize=(12,5))

        # ax_graph.set_xlim((-1, 1))
        # ax_graph.set_ylim((-20, 0))
    
        camera = Camera(fig)

        for t_idx in range(len(sol)):

            v = sol[:t_idx+1, 2:]
            ax_graph.plot(v[:, 0], v[:, 1], color="royalblue")

            camera.snap()

        anim = camera.animate()

        gif_path = ROOT / "hanged_spring2d.gif"  
        anim.save(gif_path, writer="pillow", fps=30)
        return mo.image(gif_path, width=600)

    hanged_spring2d()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
