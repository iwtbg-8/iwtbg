# 🚨 SOLUTION: "Network error - please check if the server is running"

## The Problem

You deployed to **GitHub Pages**, but it only hosts **static files** (HTML/CSS/JS).  
Your Python backend (`server.py`) **cannot run** on GitHub Pages.

```
❌ GitHub Pages = Static files only (no Python, no server)
✅ Need separate backend hosting for Python server
```

---

## The Solution (3 Steps)

### 1. Deploy Backend to Render.com (Free)

Go to: **https://render.com** → Sign up → New Web Service

**Configure:**
- Repository: `iwtbg-8/iwtbg`
- Build Command: `pip install -r requirements.txt`
- Start Command: `python server_production.py`
- Instance Type: **Free**

Click "Create Web Service" and **copy your URL**:
```
Example: https://iwtbg.onrender.com
```

### 2. Update script.js

Open `script.js`, find line 6-8, and change:

**FROM:**
```javascript
const API_URL = window.location.origin.includes('localhost') 
    ? window.location.origin 
    : 'http://localhost:5000';  // ❌ This doesn't work on GitHub Pages
```

**TO:**
```javascript
const API_URL = window.location.origin.includes('localhost') 
    ? window.location.origin 
   : 'https://iwtbg.onrender.com';  // ✅ Your Render URL
```

### 3. Commit and Push

```bash
git add script.js server.py server_production.py
git commit -m "Configure for production deployment"
git push origin main
```

GitHub Pages will auto-update in 2-3 minutes.  
Render will auto-deploy your backend.

---

## Testing

1. **Test Backend** (wait 2-3 minutes after Render deployment):
   ```bash
   curl https://iwtbg.onrender.com/api
   ```
   Should return JSON with API info.

2. **Test Frontend**:
   - Visit: `https://iwtbg-8.github.io/iwtbg/`
   - Paste a video URL
   - Click download
   - **First time**: Wait 30-60 seconds (backend waking up)

---

## ⚠️ Important Notes

### Free Tier Behavior
- Backend **sleeps** after 15 minutes of no activity
- **First request** takes 30-60 seconds to wake up
- Show "Loading..." message to users
- Subsequent requests are fast

### To Fix Sleeping
- **Option 1**: Upgrade to Render Starter ($7/month) → 24/7 uptime
- **Option 2**: Use ping service (free) → https://uptimerobot.com

### What You Built
```
Frontend (GitHub Pages)        Backend (Render.com)
https://iwtbg-8.github.io  →   https://yourapp.onrender.com
     │                                    │
     ├─ index.html                       ├─ server.py
     ├─ script.js  ───────HTTPS──────→   ├─ yt-dlp
     └─ styles.css                       └─ downloads/
```

---

## Files Created for You

✅ `DEPLOYMENT_GUIDE.md` - Detailed deployment instructions  
✅ `QUICK_DEPLOY.md` - 3-step quick start  
✅ `ARCHITECTURE.md` - How everything works  
✅ `render.yaml` - Render.com configuration  
✅ `config.example.js` - API URL configuration template  
✅ Updated `server_production.py` - Works with Render  
✅ Updated `server.py` - CORS configured for production  

---

## Troubleshooting

**Still getting "Network error"?**

1. **Check backend is running:**
   ```bash
   curl https://your-render-url.onrender.com/api
   ```
   If it returns JSON → backend is working!

2. **Check API URL in script.js:**
   - Open `script.js`
   - Look at line 6-8
   - Should be your Render URL, not `localhost`

3. **Wait for wake-up (free tier):**
   - First request takes 30-60 seconds
   - Be patient, it will work!

4. **Clear browser cache:**
   - Press `Ctrl + Shift + R` (hard refresh)
   - Or clear cache in DevTools

5. **Check browser console:**
   - Press F12 → Console tab
   - Look for errors
   - CORS errors? Update server.py CORS settings

---

## What's Next?

After it's working:

1. ✅ Test thoroughly with different video URLs
2. ⏳ Add authentication (before making public)
3. ⏳ Add rate limiting (prevent abuse)
4. ⏳ Consider upgrading to paid tier ($7/month)
5. ⏳ Monitor usage and costs

---

## Cost Summary

**Current (Free):**
- Frontend: $0 (GitHub Pages)
- Backend: $0 (Render Free Tier)
- **Total: $0/month** ⚠️ Backend sleeps

**Recommended (Production):**
- Frontend: $0 (GitHub Pages)
- Backend: $7/month (Render Starter)
- **Total: $7/month** ✅ 24/7 uptime

---

## Need Help?

1. Read `QUICK_DEPLOY.md` for step-by-step
2. Read `ARCHITECTURE.md` to understand how it works
3. Check Render logs if backend fails
4. Check browser console (F12) for frontend errors

**You're almost there! Just deploy the backend to Render.com and update the API URL.** 🚀
