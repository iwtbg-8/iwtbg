# Deployment Guide - Full Stack on Render.com

## Problem
GitHub Pages **cannot run Python servers**. It only serves static HTML/CSS/JS files.

## Solution
Deploy backend to **Render.com** (free tier) and frontend to **GitHub Pages**.

## Step-by-Step Deployment

### Part 1: Deploy Backend to Render.com

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub account

2. **Connect Your Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `iwtbg-8/iwtbg`
   - Select the repository

3. **Configure Service**
   ```
   Name: iwtbg
   Region: Choose closest to you
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python server_production.py
   Instance Type: Free
   ```

4. **Add Environment Variables** (Optional)
   ```
   PORT = 10000 (Render auto-assigns this)
   PYTHON_VERSION = 3.11
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - You'll get a URL like: `https://iwtbg.onrender.com`

### Part 2: Update Frontend for Production

6. **Update script.js API URL**
   
   Replace in `script.js` (line 6-8):
   ```javascript
   // OLD (won't work on GitHub Pages):
   const API_URL = window.location.origin.includes('localhost') 
       ? window.location.origin 
       : 'http://localhost:5000';
   
   // NEW (works with Render backend):
   const API_URL = window.location.origin.includes('localhost') 
      ? window.location.origin 
      : 'https://iwtbg.onrender.com';  // Your Render URL
   ```

7. **Commit and Push Changes**
   ```bash
   git add script.js render.yaml server_production.py
   git commit -m "Configure for production deployment"
   git push origin main
   ```

8. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from branch
   - Branch: main, folder: / (root)
   - Save
   - Your site will be at: `https://iwtbg-8.github.io/iwtbg/`

### Part 3: Update CORS Settings

9. **Update server.py CORS**
   
   In `server.py`, ensure CORS allows your GitHub Pages domain and Render backend:
   ```python
   from flask_cors import CORS
   
   CORS(app, resources={
      r"/api/*": {
         "origins": [
            r"https?://localhost(:\\d+)?",
            r"https?://127\\.0\\.0\\.1(:\\d+)?",
            r"https://iwtbg-8\\.github\\.io",  # Your GitHub Pages URL
            r"https://.*\\.onrender\\.com"      # Render subdomains
         ],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"]
      }
   })
   ```

10. **Commit and Push**
    ```bash
    git add server.py
    git commit -m "Add GitHub Pages to CORS"
    git push origin main
    ```
    - Render will auto-redeploy your backend

## Testing

1. **Test Backend** (wait for Render deployment):
   ```bash
   curl https://iwtbg.onrender.com/api
   ```
   Should return API info JSON.

2. **Test Frontend**:
   - Visit: `https://iwtbg-8.github.io/iwtbg/`
   - Try downloading a video
   - Check browser console for errors (F12)

## Important Notes

### ⚠️ Free Tier Limitations

**Render.com Free Tier:**
- Service **spins down after 15 minutes** of inactivity
- First request after spin-down takes 30-60 seconds to wake up
- 750 hours/month (enough for testing)
- Solution: Upgrade to paid tier ($7/month) for 24/7 uptime

**GitHub Pages:**
- 100GB bandwidth/month
- Static files only
- Free forever

### 🔒 Security Recommendations

Before going public, add:
1. **Rate limiting** (prevent abuse)
2. **Authentication** (user accounts)
3. **Usage quotas** (limit downloads per user)
4. **HTTPS only** (already enabled on Render + GitHub Pages)

### 💰 Cost Estimate

**Current Setup (Free):**
- Render: $0 (Free tier, spin-down after 15 min)
- GitHub Pages: $0

**Production Setup (Paid):**
- Render Starter: $7/month (always-on)
- GitHub Pages: $0
- **Total: $7/month**

**With Heavy Usage:**
- Render Pro: $25/month (2GB RAM, faster)
- CDN (Cloudflare): $0-20/month
- **Total: $25-45/month**

## Alternative Deployment Options

If Render doesn't work, try:

### Option 2: Railway.app
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### Option 3: Heroku
- More expensive ($5-7/month minimum)
- But more reliable and faster

### Option 4: PythonAnywhere
- Free tier available
- Easier setup for Python apps
- Limited to 100 seconds/day on free tier

## Troubleshooting

### "Network error" after deployment
- Check Render logs: Dashboard → Logs
- Verify backend URL in script.js matches Render URL
- Check CORS settings include your GitHub Pages domain

### Backend not starting
- Check requirements.txt has all dependencies
- Verify Python version compatibility
- Check Render build logs for errors

### Downloads failing
- Free tier may timeout on large files (>100MB)
- Upgrade to paid tier or use smaller videos

### Frontend not updating
- Clear browser cache (Ctrl+Shift+R)
- Check GitHub Pages build status
- Wait 2-3 minutes after push for Pages to rebuild

## Next Steps

After deployment works:
1. Add custom domain (optional)
2. Implement authentication
3. Add rate limiting
4. Set up monitoring/alerts
5. Configure backup/logging

## Support

If you get stuck:
1. Check Render logs
2. Check browser console (F12)
3. Test backend directly with curl
4. Verify CORS settings
