from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import NearestNeighbors


MODEL_PATH = Path("simulated_sampling_nickel_t3/models/umap_retrained_umap_run3.joblib")

USE_SIMULATED = False
USE_EXPERIMENTAL = True
USE_ROI_ONLY = True


def compute_2nn_id(Z):
    nn = NearestNeighbors(n_neighbors=3, algorithm="auto")
    nn.fit(Z)
    dist, _ = nn.kneighbors(Z)

    r1 = dist[:, 1]
    r2 = dist[:, 2]
    mask = (r1 > 1e-12) & (r2 > r1)
    mu = r2[mask] / r1[mask]

    if len(mu) < 50:
        print("Too few samples for reliable 2NN.")
        return None

    if np.std(mu) < 1e-12:
        print("mu variance is approximately zero; 2NN is invalid.")
        return None

    mu_sorted = np.sort(mu)
    sample_count = len(mu_sorted)
    # Keep the empirical plotting positions below one so the log transform is finite.
    empirical_cdf = np.arange(1, sample_count + 1) / (sample_count + 1)
    x = np.log(mu_sorted)
    y = -np.log(1 - empirical_cdf)
    slope, _intercept = np.polyfit(x, y, 1)
    return slope, x, y


def main():
    bundle = joblib.load(MODEL_PATH)
    simulated = bundle["Z_sim"]
    experimental_roi = bundle.get("Z_roi")
    selected = []

    if USE_SIMULATED:
        print("Using simulated data")
        selected.append(simulated)

    if USE_EXPERIMENTAL:
        if USE_ROI_ONLY:
            print("Using ROI experimental data")
            if experimental_roi is None:
                raise RuntimeError("Z_exp_roi not found.")
            selected.append(experimental_roi)
        else:
            experimental_all = bundle.get("Z_exp_all")
            print("Using full experimental data")
            if experimental_all is None:
                raise RuntimeError("Z_exp_all not found.")
            selected.append(experimental_all)

    if not selected:
        raise RuntimeError("No dataset selected.")

    all_samples = np.vstack(selected)
    print("Total samples used:", len(all_samples))
    result = compute_2nn_id(all_samples)
    if result is None:
        print("2NN estimation failed.")
        return

    dimension, x, y = result
    print(f"\nEstimated intrinsic dimension d = {dimension:.3f}")
    plt.figure(figsize=(6, 5))
    plt.scatter(x, y, s=5, alpha=0.7)
    plt.plot(x, dimension * x, linewidth=2)
    plt.xlabel("log(mu)")
    plt.ylabel("-log(1 - F_emp(mu))")
    plt.title(f"2NN Intrinsic Dimension (d = {dimension:.2f})")
    plt.tight_layout()
    plt.savefig("2nn_id_plot.png", dpi=300)
    plt.close()
    print("Saved 2nn_id_plot.png")


if __name__ == "__main__":
    main()
