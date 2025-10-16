## Build for **Snap (Ubuntu, Debian, etc.)**

### Requirements:

You need `snapcraft` installed:

```bash
sudo snap install snapcraft --classic
```

### Folder structure:

Your repo should contain a file named **`snap/snapcraft.yaml`**

### Build:

In your project root:

```bash
snapcraft
```

This will create a file:

```
snakegame_1.0.0_amd64.snap
```

### Test locally:

```bash
sudo snap install snakegame_1.0.0_amd64.snap --dangerous
```

(`--dangerous` allows local testing of unsigned snaps)

### Publish on Snap Store:

1. Create a Snapcraft account: [https://snapcraft.io/account](https://snapcraft.io/account)
2. Register your app name:

   ```bash
   snapcraft register snakegame
   ```
3. Upload:

   ```bash
   snapcraft upload snakegame_1.0.0_amd64.snap --release=stable
   ```

---
By C4L :D