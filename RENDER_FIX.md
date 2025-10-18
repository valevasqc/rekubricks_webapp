# Render Deployment Fix

## Problem
Waitress was causing queue overflow issues on Render with 5000+ products loading.

## Solution
Switched from Waitress to Gunicorn (industry standard for Flask production deployments).

## Steps to Update on Render

### Option 1: Update via Render Dashboard (Recommended)

1. Go to your Render dashboard: https://dashboard.render.com
2. Click on your `rekubricks` service
3. Go to **Settings**
4. Find **Build & Deploy** section
5. Update the **Start Command** to:
   ```
   gunicorn --config gunicorn_config.py app:app
   ```
6. Click **Save Changes**
7. Render will automatically redeploy

### Option 2: Create render.yaml (Alternative)

If you prefer infrastructure as code, create a `render.yaml` file in your repo root with:

```yaml
services:
  - type: web
    name: rekubricks
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --config gunicorn_config.py app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

Then commit and push. Render will auto-detect and use this configuration.

## What Changed

1. **Added `gunicorn` to requirements.txt**
2. **Created `gunicorn_config.py`** - Optimized configuration:
   - 2 workers (good for free tier)
   - 120s timeout (handles large Excel load)
   - Proper logging
   - SSL headers for HTTPS

3. **Simplified `app.py`** - Removed Waitress, now just pure Flask
   - Gunicorn handles the WSGI server in production
   - `python app.py` still works for local dev

## Expected Result

After deployment:
- ✅ No more queue depth warnings
- ✅ Fast startup (< 30 seconds)
- ✅ Stable under load
- ✅ Proper HTTPS handling

## Testing

Once deployed, check:
1. Visit https://rekubricks.onrender.com
2. Check Render logs - should see:
   ```
   [INFO] Starting gunicorn 23.0.0
   [INFO] Listening at: http://0.0.0.0:10000
   [INFO] Using worker: sync
   [INFO] Booting worker with pid: [number]
   ```
3. No queue warnings or timeout errors

## Rollback (if needed)

If something goes wrong, change Start Command back to:
```
python app.py
```

But this shouldn't be necessary - Gunicorn is more stable than Waitress for Flask apps.
