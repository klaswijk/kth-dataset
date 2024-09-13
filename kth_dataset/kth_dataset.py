import numpy as np
import requests
from pathlib import Path
from io import BytesIO
from PIL import Image
from sklearn.utils import check_random_state


def _download(path):
    url = "https://github.com/klaswijk/kth-dataset/blob/main/kth_logo.png?raw=true"
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(path)


def _load(path):
    image = Image.open(path)
    array = np.array(image).sum(-1)  # Sum over the color channels
    array = array < array.max()  # Convert to binary image
    x = np.argwhere(array).astype(float)
    x[:, [0, 1]] = x[:, [1, 0]]
    x[:, 0] = x[:, 0] / array.shape[0]
    x[:, 1] = 1 - x[:, 1] / array.shape[1]
    x = (x - x.mean(0)) / x.std(0)
    return x


def make_kth_dataset(
    n_samples, *, noise=0.0, path=".", download=False, random_state=None
):
    path = Path(path).expanduser() / "kth_logo.png"
    if not path.exists():
        if download:
            _download(path)
        else:
            raise FileNotFoundError(
                f"File not found: {path}. Set download=True to download."
            )
    x = _load("kth_logo.png")
    assert n_samples <= len(x), f"Maximum n_samples of the dataset is {len(x)}"
    generator = check_random_state(random_state)
    generator.shuffle(x)
    if noise > 0:
        x += generator.normal(0, noise, x.shape)
    x = x[:n_samples]
    y = np.zeros(n_samples)
    return x, y


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.animation import FFMpegWriter

    # Save gif
    x, _ = make_kth_dataset(10_000, download=True, random_state=0)
    fig, ax = plt.subplots(constrained_layout=True, figsize=(4, 4))
    writer = FFMpegWriter(fps=30)
    with writer.saving(fig, "kth_scatter.gif", dpi=300):
        for i in range(0, 10_000, 50):
            ax.clear()
            ax.scatter(x[:i, 0], x[:i, 1], s=3, color="#000061")
            ax.set_xlim(-2.5, 2.5)
            ax.set_ylim(-2.5, 2.5)
            ax.set_aspect("equal")
            ax.margins(0, 0)
            writer.grab_frame()

    # Save png
    plt.savefig("kth_scatter.png", dpi=300)
