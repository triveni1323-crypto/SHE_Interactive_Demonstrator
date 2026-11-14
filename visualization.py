"""Plotting helpers for the SHE demonstrator."""
import matplotlib.pyplot as plt

def noise_growth_figure(p: int = 101, initial_noise: int = 3, levels: int = 4):
    noises = [initial_noise]
    for _ in range(levels):
        noises.append(noises[-1] ** 2)
    fig, ax = plt.subplots()
    ax.plot(range(len(noises)), noises, marker="o")
    ax.axhline(p / 2, linestyle="--", label="p/2 correctness boundary")
    ax.set_yscale("symlog")
    ax.set_xlabel("Multiplication depth")
    ax.set_ylabel("Illustrative residual magnitude")
    ax.set_title("Noise growth under repeated squaring")
    ax.legend()
    fig.tight_layout()
    return fig
