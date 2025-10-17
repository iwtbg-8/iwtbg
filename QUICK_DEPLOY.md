# Quick Deployment Instructions

## 🚀 Deploy in 3 Steps

### Step 1: Deploy Backend to Render.com (5 minutes)

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect GitHub repo: `iwtbg-8/iwtbg`
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python server_production.py`
   - **Instance Type**: Free
5. Click "Create Web Service"
6. **Copy your Render URL** (e.g., `https://iwtbg.onrender.com`)

### Step 2: Update Frontend API URL

Edit `script.js` line 6-8, replace with your Render URL:

```javascript
const API_URL = window.location.origin.includes('localhost') 
    ? window.location.origin 
    : 'https://YOUR-RENDER-URL-HERE.onrender.com';  // ← CHANGE THIS
```

### Step 3: Push and Enable GitHub Pages

```bash
# Commit changes
git add script.js server.py server_production.py render.yaml
git commit -m "Configure for production deployment"
git push origin main

# Enable GitHub Pages:
# Go to: https://github.com/iwtbg-8/iwtbg/settings/pages
# Set Source: "Deploy from branch" → main → / (root)
```

### Done! 🎉

**Your app will be live at:**
- Frontend: `https://iwtbg-8.github.io/iwtbg/`
- Backend: `https://your-app.onrender.com`

---

## ⚠️ Important Notes

### First Load (Render Free Tier)
- Backend sleeps after 15 min of inactivity
- **First request takes 30-60 seconds to wake up**
- Show "Loading..." message to users

### To Keep Backend Always On
- Upgrade to Render Starter plan ($7/month)
- Or use a ping service (free): https://uptimerobot.com

---

## 🐛 Troubleshooting

**"Network error" after deployment:**
1. Check if backend is running: Visit `https://your-render-url.onrender.com/api`
2. Verify API_URL in script.js matches your Render URL
3. Wait 60 seconds (backend might be waking up)
4. Check browser console (F12) for CORS errors

**Backend won't start:**
- Check Render logs: Dashboard → Your Service → Logs
- Verify all dependencies in requirements.txt

**Still not working?**
- Clear browser cache (Ctrl+Shift+R)
- Test backend with curl: `curl https://your-render-url.onrender.com/api`
- Check CORS settings in server.py

---

## 📊 What You Get (Free Tier)

✅ Fully functional video downloader
✅ HTTPS encryption (secure)
✅ Global CDN (GitHub Pages)
✅ Unlimited frontend traffic
✅ 750 hours/month backend uptime

❌ Backend sleeps after 15 min idle
❌ Limited to 512MB RAM
❌ Slower download speeds on free tier

**Upgrade to $7/month for:**
- 24/7 uptime (no sleeping)
- Faster performance
- More RAM/resources
