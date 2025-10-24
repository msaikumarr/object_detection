# Video Processing and Object Counting with Streamlit frontend
# Video Processing and Object Counting (Streamlit frontend)

This project runs YOLOv8-based object detection and counting with a simple Streamlit frontend.

Example result (object counts):

```json
{
    "laptop": 2,
    "bottle": 2,
    "cell phone": 2,
    "chair": 1,
    "car": 1,
    "keyboard": 1
}
```

## Quick start (Windows PowerShell) — the easy way

1. Create and activate a virtual environment (if you don't have one):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
# If PowerShell blocks script execution, run (one-time):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2. Install dependencies from `requirements.txt`:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the Streamlit frontend:

```powershell
streamlit run src/app.py
```

If you see an error like "ModuleNotFoundError: No module named 'ultralytics'", it means the `ultralytics` package (YOLOv8) isn't installed in the active environment. The previous `pip install -r requirements.txt` step should install it, but if it fails, install it directly:

```powershell
pip install ultralytics
# If you need a specific PyTorch build (CPU-only example):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
# then re-install ultralytics if needed:
pip install ultralytics
```

Notes:
- The project already contains `requirements.txt` with `ultralytics` and `streamlit` listed.
- If you plan to use a GPU, install the appropriate GPU build of `torch` before `ultralytics` (see https://pytorch.org/get-started/locally/).

## Deploying (quick option)
If you want a one-click public demo, push this repository to GitHub and use Streamlit Community Cloud (recommended for quick demos). Point Streamlit Cloud to `src/app.py` as the app entrypoint.

For a container-based deploy (Render, Heroku, Docker), I can add a simple Dockerfile and instructions — tell me which you prefer.

### Deploying with Netlify (recommended proxy flow)

Netlify cannot run a long-lived Streamlit server directly. The recommended approach is:

1. Deploy the Streamlit app (container) to a container host (Render, Railway, Fly, Heroku, etc.) and note the public URL such as `https://your-backend.example.com`.
2. Use Netlify to serve a small static landing site and proxy all requests to the backend URL. The repo includes a `public/index.html` and `netlify.toml` with a proxy redirect rule.

Quick steps:

- Edit `public/index.html` and `netlify.toml` and replace `https://YOUR_BACKEND_URL_HERE` with your backend URL from step (1).
- Commit and push to GitHub.
- On Netlify: New site → Import from GitHub → choose this repo.
    - Base directory: leave blank
    - Build command: leave blank
    - Publish directory: `public`

Netlify will publish the static site and proxy incoming requests to your Streamlit backend.

If you'd like a proxy that reads the backend URL from Netlify environment variables (so you don't have to commit it into the repo), I can scaffold a small Netlify Function (serverless) to forward requests to `process.env.BACKEND_URL` instead — tell me if you want that.
