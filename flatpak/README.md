## Build for **Flatpak (universal Linux)**

### Requirements:

Install Flatpak tooling:

```bash
sudo apt install flatpak flatpak-builder
```

### Build:

```bash
flatpak-builder build-dir snakegame.flatpak.yaml --force-clean
```

This builds it into `build-dir/`.

To **create a distributable bundle**:

```bash
flatpak-builder --repo=repo build-dir snakegame.flatpak.yaml
flatpak build-bundle repo snakegame.flatpak com.c4l.SnakeGame 1.0.0
```

### Test locally:

```bash
flatpak install snakegame.flatpak
flatpak run com.c4l.SnakeGame
```

### Publish on Flathub:

1. Create an account: [https://flathub.org](https://flathub.org)
2. Fork their [submission repo](https://github.com/flathub/flathub)
3. Submit your `.yaml` manifest and metadata according to their [submission guide](https://github.com/flathub/flathub/wiki/App-Submission).

---
By C4L :D
