#!/usr/bin/env python3
# -----------------------------------------------------------
# plot_ep.py  –  robust loader for EP1_N#.dat / EP2_N#.dat
# -----------------------------------------------------------
import os
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler          # <-- provides the colour-cycle helper

# -----------------------------------------------------------
# GLOBAL SETTINGS
chain_sizes0   = [2, 3, 4, 5, 6, 7, 8]
chain_sizes   = [2, 4, 6, 8, 10, 12, 14, 16]
ep1_pattern   = "EP1_N{}.dat"
ep2_pattern   = "EP2_N{}.dat"
output_name   = "EP_summary3.pdf"

# 🎨  COLOUR PALETTE (first two define the paper’s theme)
colors = [
    (33/255, 64/255, 154/255),   # theme blue
    'firebrick',                 # theme red
    '#a9bcd0',                   # desaturated blue-grey
    'goldenrod',                 # warm gold
    'mistyrose',                 # light rose
    '#D8DBE2',                   # pastel grey-blue
    'slategray',                 # extra tone for the 7th line
]
plt.rc('axes', prop_cycle=cycler('color', colors))

# -----------------------------------------------------------
def parse_token(tok: str) -> float:
    """Turn '0.5' or '1/2' into a float."""
    tok = tok.strip()
    if "/" in tok:
        return float(Fraction(tok))
    return float(tok)

def load_dat(fname: str) -> np.ndarray:
    """Read two-column files that contain the data."""
    if not os.path.isfile(fname):
        raise FileNotFoundError(f"Expected file not found: {fname}")
    rows = []
    with open(fname) as fh:
        for line in fh:
            if line.strip():
                vals = [parse_token(t) for t in line.split()]
                rows.append(vals)
    return np.asarray(rows, dtype=float)

# -----------------------------------------------------------
ep1_data = {N: load_dat(ep1_pattern.format(N)) for N in chain_sizes}
ep2_data = {N: load_dat(ep2_pattern.format(N)) for N in chain_sizes}

# -----------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10, 6), sharex=True, sharey=True)

# -------- Case 1 ------------------------------------------------
ax1 = axes[0]
for N, data in ep1_data.items():
    ax1.plot(data[:, 0], data[:, 1], label=f"N = {int(N/2)}", marker='o')
ax1.set_title("Case 1", fontsize=16)
ax1.set_xlabel("M / 2N", fontsize=16)
ax1.set_ylabel("EPs / 2N", fontsize=16)
ax1.grid(True)
ax1.legend(fontsize=13)
ax1.tick_params(labelsize=14)

# -------- Case 2 ------------------------------------------------
ax2 = axes[1]
for N, data in ep2_data.items():
    ax2.plot(data[:, 0], data[:, 1], label=f"N = {int(N/2)}", marker='o')
ax2.set_title("Case 2", fontsize=16)
ax2.set_xlabel("M / 2N", fontsize=16)
ax2.grid(True)
ax2.legend(fontsize=13)
ax2.tick_params(labelsize=14)
#---------------------------------
panelz = ['a', 'b']
axes0= [ax1, ax2]
for ax, label in zip(axes0, panelz):
    ax.text(0.05, 1.10, label, transform=ax.transAxes, fontsize=18, fontweight='bold', va='top', ha='right')
# -----------------------------------------------------------
#fig.suptitle("EP/N vs. M/N")
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.savefig(output_name) #, dpi=400)
print(f"Figure written to: {output_name}")
plt.show()
