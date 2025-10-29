import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Load the data
# file_path = "SMI_300_data_object.csv"  #for object bundle
# file_path = "SMI_300_data_sky_LHS.csv"  #for LHS sky bundle
file_path = "SMI_300_data_sky_RHS.csv"  #for RHS sky bundle


data = pd.read_csv(file_path)

# Define group colors (consistent with your earlier specification)
group_colors = {
    1: "#1f77b4",
    2: "#2ca02c",
    3: "#9467bd",
    4: "#17becf",
    5: "#e377c2",
    6: "#8c564b",
    7: "#d62728",
    8: "#ff7f0e",
}

# === 1. Plot fiber positions colored by Group ===
def plot_by_group(data, radius_mm):
    fig, ax = plt.subplots(figsize=(8, 8))
    for _, row in data.iterrows():
        color = group_colors.get(row["Group"], "gray")
        circle = plt.Circle((row["X location in mm"], row["Y location in mm"]),
                            radius = radius_mm, color=color, ec="black", lw=0.5)
        ax.add_patch(circle)
        ax.text(row["X location in mm"], row["Y location in mm"], f"{row['Fiber ID']:.0f}",
                ha='center', va='center', fontsize=6, color='white', weight='bold')
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X location (mm)")
    ax.set_ylabel("Y location (mm)")
    ax.set_title("Fiber positions colored by Group")
    ax.set_xlim(data["X location in mm"].min()-1, data["X location in mm"].max()+1)
    ax.set_ylim(data["Y location in mm"].min()-1, data["Y location in mm"].max()+1)

    # === Add legend with counts ===
    patches = []
    for grp, color in group_colors.items():
        count = len(data[data["Group"] == grp])
        patches.append(mpatches.Patch(color=color, label=f"Group {grp} (n={count})"))
    ax.legend(handles=patches, loc='upper right', fontsize=6)
    plt.show()


# === 2. Plot fiber positions colored by Non-telecentricity (with colorbar) ===
def plot_by_telecentricity(data, radius_mm):
    fig, ax = plt.subplots(figsize=(8, 8))
    tele_vals = data["Non-telecentricity in degree"]
    
    # Fixed colorbar range
    norm = plt.Normalize(vmin=-0.05, vmax=0.30)
    cmap = plt.cm.viridis  # or plt.cm.gray_r

    for _, row in data.iterrows():
        color = cmap(norm(row["Non-telecentricity in degree"]))
        circle = plt.Circle((row["X location in mm"], row["Y location in mm"]),
                            radius=radius_mm, color=color, ec="black", lw=0.5)
        ax.add_patch(circle)
        ax.text(row["X location in mm"], row["Y location in mm"], f"{row['Fiber ID']:.0f}",
                ha='center', va='center', fontsize=6, color='white', weight='bold')

    # Colorbar with fixed limits
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label="Non-telecentricity (degree)")

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("X location (mm)")
    ax.set_ylabel("Y location (mm)")
    ax.set_title("Fiber positions shaded by Non-telecentricity")
    ax.set_xlim(data["X location in mm"].min() - 1, data["X location in mm"].max() + 1)
    ax.set_ylim(data["Y location in mm"].min() - 1, data["Y location in mm"].max() + 1)
    plt.show()

# === 3. Histogram of Non-telecentricity for each group (custom bin edges) ===
def plot_telecentricity_hist(data, bins=None):
    fig, ax = plt.subplots(figsize=(8, 6))

    if bins is None:
        bins = 12

    # Sort group keys and split into first half (solid) and second half (dotted)
    group_keys = sorted(group_colors.keys())
    half_point = len(group_keys) // 2

    for i, grp in enumerate(group_keys):
        subset = data[data["Group"] == grp]
        if not subset.empty:
            linestyle = '-' if i < half_point else ':'
            count = len(subset)
            ax.hist(subset["Non-telecentricity in degree"], bins=bins,
                    histtype='step', linewidth=2,
                    linestyle=linestyle, color=group_colors[grp], label=f"Group {grp} (n={count})")

    ax.set_xlabel("Δθ (degree)")
    ax.set_ylabel("N")
    ax.set_title("Distribution of Non-telecentricity by Group")
    ax.legend(fontsize=8, ncol=4, loc="upper center")
    plt.show()


# === Example usage ===
plot_by_group(data, radius_mm=0.185)
plot_by_telecentricity(data, radius_mm=0.185)
plot_telecentricity_hist(data, bins=np.arange(0, 0.401, 0.005))
