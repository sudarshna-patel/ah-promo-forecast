set PYTHONPATH=%cd%

podman build -t promo-forecast-app .
podman run -p 8000:8000 -p 5000:5000 promo-forecast-app

# dev
podman run --rm -p 5000:5000 -p 8000:8000 -v %cd%:/app promo-forecast-app
podman run --rm --memory="5g" -p 5000:5000 -p 8000:8000 -v %cd%:/app promo-forecast-app



Great question! To make sure your running **Podman container** picks up code changes without rebuilding the image every time, you can use **volume mounting** to map your local code directory into the container. This way, code edits on your host are reflected immediately in the container.

Here’s how to do it:

---

### ✅ 1. **Edit your `uvicorn` command** to enable auto-reload

Update your `CMD` in the `Containerfile`:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

> ⚠️ Note: `--reload` is for **development only** — it enables hot reloading when files change.

---

### ✅ 2. **Mount your local code into the container** using Podman

Assuming your local code is in `./fastapi-app`:

```bash
podman run --rm -p 8000:8000 \
  -v $(pwd)/app:/app/app \
  fastapi-app
```

Explanation:
- `--rm`: Removes container after you stop it.
- `-v $(pwd)/app:/app/app`: Mounts your local `app` folder into the container.
- You can also mount `requirements.txt` if needed.

---

### 🛠 Pro Tip: Create a development-specific container script

You can create a script like `run-dev.sh`:

```bash
#!/bin/bash
podman run --rm -p 8000:8000 \
  -v $(pwd)/app:/app/app \
  fastapi-app
```

---

### 💡 Bonus: Use Docker/Podman Compose (optional)

If the project grows, you might want to use **`podman-compose`** with volume mounts, networks, etc.

---

Let me know if you want a ready-to-go `docker-compose.yml` (works with Podman too)!