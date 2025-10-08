---
layout: post
title: Catalogue of LR Schedulers
---


```python
from pathlib import Path
import os
from collections import defaultdict

from IPython.display import HTML, Image
import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera
import torch.optim as optim
import torch

ROOT = Path("./assets/img/")

if not os.path.exists(ROOT):
    os.makedirs(ROOT)
```


```python
def get_dummy_optimizer(lr):
    return optim.SGD([torch.tensor(0)], lr=lr)
```

# StepLR


```python
def step_lr():

    optimizer = get_dummy_optimizer(lr=1.)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.1)

    epochs = np.arange(0, 200)
    
    lr_arr = []
    for epoch in epochs:
        lr = scheduler.get_last_lr()
        lr_arr.append(lr)
        
        optimizer.step()
        scheduler.step()

    lr_arr = np.array(lr_arr)

    fig, (ax, ax_log) = plt.subplots(1, 2, figsize=(12,5))

    fig.suptitle("StepLR")

    ax.set_xlabel("epoch")
    ax.set_ylabel("lr")

    ax_log.set_xlabel("epoch")
    ax_log.set_ylabel("lr (log-scale)")

    ax_log.set_yscale("log")

    camera = Camera(fig)
    for epoch in epochs:
        ax.scatter(epoch, lr_arr[epoch], color="royalblue")
        ax.plot(epochs[:epoch+1], lr_arr[:epoch+1], color="royalblue")

        ax_log.scatter(epoch, lr_arr[epoch], color="royalblue")
        ax_log.plot(epochs[:epoch+1], lr_arr[:epoch+1], color="royalblue")
        
        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "steplr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

step_lr()
```




<img src="{{ '/assets/2025-10-08-lr_schedule/img/steplr.gif' | relative_url }}"/>



# ExponentialLR


```python
def exp_lr():

    epochs = np.arange(0, 200)
    gammas = [0.9, 0.95, 0.99]
    
    lr_dict = defaultdict(list)
    for gamma in gammas:
        
        optimizer = get_dummy_optimizer(lr=1.)
        scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=gamma)

        for epoch in epochs:
            lr = scheduler.get_last_lr()
            lr_dict[gamma].append(lr)
            
            optimizer.step()
            scheduler.step()

    fig, (ax, ax_log) = plt.subplots(1, 2, figsize=(12,5))

    fig.suptitle("ExponentialLR")

    ax.set_xlabel("epoch")
    ax.set_ylabel("lr")

    ax_log.set_xlabel("epoch")
    ax_log.set_ylabel("lr (log-scale)")

    ax_log.set_yscale("log")
    
    colors = {
        0.9: "royalblue",
        0.95: "orangered",
        0.99: "forestgreen",
    }
    
    camera = Camera(fig)
    for epoch in epochs:

        lines = []
        log_lines = []
        
        for gamma in lr_dict.keys():

            lr_arr = np.array(lr_dict[gamma])
            
            ax.scatter(epoch, lr_arr[epoch], color=colors[gamma])
            line, = ax.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                            color=colors[gamma], label=r"$\gamma=%s$" % gamma)
            
            
            ax_log.scatter(epoch, lr_arr[epoch], color=colors[gamma])
            log_line, = ax_log.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                            color=colors[gamma], label=r"$\gamma=%s$" % gamma)
            
            lines.append(line)
            log_lines.append(log_line)

        ax.legend(handles=lines)
        ax_log.legend(handles=log_lines)
        
        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "explr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

exp_lr()
```

    /tmp/ipykernel_14/3603444625.py:68: UserWarning: Creating legend with loc="best" can be slow with large amounts of data.
      anim.save(gif_path, writer="pillow", fps=30)





<img src="{{ '/assets/2025-10-08-lr_schedule/img/explr.gif' | relative_url }}"/>



# PolynomialLR


```python
def poly_lr():

    epochs = np.arange(0, 200)
    powers = [1., 2., 3., 4., 5.]
    
    lr_dict = defaultdict(list)
    for power in powers:
        
        optimizer = get_dummy_optimizer(lr=1.)
        scheduler = optim.lr_scheduler.PolynomialLR(optimizer, power=power, 
                                                    total_iters=150)

        for epoch in epochs:
            lr = scheduler.get_last_lr()
            lr_dict[power].append(lr)
            
            optimizer.step()
            scheduler.step()

    fig, ax = plt.subplots(1, 1, figsize=(5,5))

    fig.suptitle("PolynomialLR")

    ax.set_xlabel("epoch")
    ax.set_ylabel("lr")
    
    colors = {
        1.: "royalblue",
        2.: "orangered",
        3.: "forestgreen",
        4.: "mediumblue",
        5.: "crimson",
    }
    
    camera = Camera(fig)
    for epoch in epochs:

        lines = []
        
        for power in lr_dict.keys():

            lr_arr = np.array(lr_dict[power])
            
            ax.scatter(epoch, lr_arr[epoch], color=colors[power])
            line, = ax.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                            color=colors[power], label=f"power={power}")
            
            
            lines.append(line)

        ax.legend(handles=lines)
        
        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "polylr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

poly_lr()
```




<img src="{{ '/assets/2025-10-08-lr_schedule/img/polylr.gif' | relative_url }}"/>



# CyclicLR


```python
def cyclic_lr():

    base_lr = 0.1
    max_lr = 1.

    modes = ["triangular", "triangular2", "exp_range"]
    
    epochs = np.arange(0, 200)

    fig, axes = plt.subplots(1, 3, figsize=(18,5))

    lr_dict = defaultdict(list)
    
    for mode in ["triangular", "triangular2"]:
        
        optimizer = get_dummy_optimizer(lr=1.)
        scheduler = optim.lr_scheduler.CyclicLR(optimizer, mode=mode, 
                                                step_size_up=50, base_lr=base_lr, max_lr=max_lr)

        for epoch in epochs:
            
            lr = scheduler.get_last_lr()
            lr_dict[mode].append(lr)
            
            optimizer.step()
            scheduler.step()


    mode = "exp_range"
    gammas = [0.99, 0.98, 0.97]
    lr_exp_range_dict = defaultdict(list)

    for gamma in gammas:
        optimizer = get_dummy_optimizer(lr=1.)
        scheduler = optim.lr_scheduler.CyclicLR(optimizer, mode=mode, gamma=gamma,
                                                step_size_up=50, 
                                                base_lr=base_lr, max_lr=max_lr)

        for epoch in epochs:
            
            lr = scheduler.get_last_lr()
            lr_exp_range_dict[gamma].append(lr)
            
            optimizer.step()
            scheduler.step()

    fig.suptitle("CyclicLR")

    for idx, ax in enumerate(axes):
        ax.set_xlabel("epoch")
        ax.set_ylabel("lr")

        mode = modes[idx]
        ax.set_title(mode)
    
    exp_range_colors = {
        0.99: "royalblue",
        0.98: "orangered",
        0.97: "forestgreen",
    }
    
    camera = Camera(fig)

    for epoch in epochs:
        for idx, mode in enumerate(["triangular", "triangular2"]):
            ax = axes[idx]

            lr_arr = np.array(lr_dict[mode])
            
            ax.scatter(epoch, lr_arr[epoch], color="royalblue")
            ax.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                            color="royalblue")
        
        ax = axes[2]
        lines = []
        for gamma in gammas:
            color = exp_range_colors[gamma]

            lr_arr = np.array(lr_exp_range_dict[gamma])

            ax.scatter(epoch, lr_arr[epoch], color=color)
            line,  = ax.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                            color=color, label=r"$\gamma=%s$" % gamma)

            lines.append(line)
            
        ax.legend(handles=lines)
        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "cycliclr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

cyclic_lr()
```




<img src="{{ '/assets/2025-10-08-lr_schedule/img/cycliclr.gif' | relative_url }}"/>



# OneCycleLR


```python
def onecycle_lr():

    max_lr = 1.
    
    max_epochs = 200
    epochs = np.arange(0, max_epochs)

    fig, axes = plt.subplots(1, 1, figsize=(5,5))

    lr_dict = defaultdict(list)

    for threephase in [True, False]:

        optimizer = get_dummy_optimizer(lr=1.)
        scheduler = optim.lr_scheduler.OneCycleLR(optimizer, max_lr=max_lr, total_steps=max_epochs,
                                                  three_phase=threephase,)

        for epoch in epochs:
            
            lr = scheduler.get_last_lr()
            lr_dict[threephase].append(lr)
            
            optimizer.step()
            scheduler.step()

    fig.suptitle("OneCycleLR")

    axes.set_xlabel("epoch")
    axes.set_ylabel("lr")
    
    camera = Camera(fig)

    colors = {
        True: 'royalblue',
        False: 'orangered',
    }

    for epoch in epochs:
        
        lines = []
        for threephase in [True, False]:
            
            lr_arr = np.array(lr_dict[threephase])

            color = colors[threephase]
            axes.scatter(epoch, lr_arr[epoch], color=color)
            line, = axes.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                            color=color, label=("three_phase" if threephase else "two_phase"))
            
            lines.append(line)
        
        axes.legend(handles=lines)

        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "onecyclelr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

onecycle_lr()
```




<img src="{{ '/assets/2025-10-08-lr_schedule/img/onecyclelr.gif' | relative_url }}"/>




```python
def cosanneal_lr():
    
    max_epochs = 200
    epochs = np.arange(0, max_epochs)

    fig, axes = plt.subplots(1, 1, figsize=(5,5))

    lr_arr = []

    optimizer = get_dummy_optimizer(lr=1.)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max_epochs)

    for epoch in epochs:
        
        lr = scheduler.get_last_lr()
        lr_arr.append(lr)
        
        optimizer.step()
        scheduler.step()

    lr_arr = np.array(lr_arr)
    
    fig.suptitle("CosineAnnealingLR")

    axes.set_xlabel("epoch")
    axes.set_ylabel("lr")
    
    camera = Camera(fig)

    color = "royalblue"
    
    for epoch in epochs:
        
        axes.scatter(epoch, lr_arr[epoch], color=color)
        line, = axes.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                        color=color,)
    

        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "cosanneallr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

cosanneal_lr()
```




<img src="{{ '/assets/2025-10-08-lr_schedule/img/cosanneallr.gif' | relative_url }}"/>




```python
def coswarm_lr():
    
    max_epochs = 200
    epochs = np.arange(0, max_epochs)

    T_0 = 50
    T_mult = 3
    
    fig, axes = plt.subplots(1, 1, figsize=(5,5))

    lr_arr = []

    optimizer = get_dummy_optimizer(lr=1.)
    scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(optimizer, T_0=T_0, T_mult=T_mult)

    for epoch in epochs:
        
        lr = scheduler.get_last_lr()
        lr_arr.append(lr)
        
        optimizer.step()
        scheduler.step()

    lr_arr = np.array(lr_arr)
    
    fig.suptitle("CosineAnnealingWarmRestarts")

    axes.set_xlabel("epoch")
    axes.set_ylabel("lr")
    
    camera = Camera(fig)

    color = "royalblue"
    
    for epoch in epochs:
        
        axes.scatter(epoch, lr_arr[epoch], color=color)
        line, = axes.plot(epochs[:epoch+1], lr_arr[:epoch+1], 
                        color=color,)
    

        camera.snap()

    anim = camera.animate()
    plt.close()

    gif_path = ROOT / "coswarmlr.gif"  
    anim.save(gif_path, writer="pillow", fps=30)
    return Image(url=gif_path)

coswarm_lr()
```




<img src="{{ '/assets/2025-10-08-lr_schedule/img/coswarmlr.gif' | relative_url }}"/>


