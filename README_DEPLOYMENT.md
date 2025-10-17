# 🚨 FIX: "Network error - please check if the server is running"

## Quick Answer

**GitHub Pages can't run Python servers!** You need to:
1. Deploy backend to **Render.com** (free)
2. Update API URL in `script.js`
3. Done!

---

## 📚 Documentation (Read This First!)

### Start Here → `SOLUTION.md`
**Read this first!** Explains the problem and solution in simple terms.

### Follow This → `CHECKLIST.md`
Step-by-step checklist with checkboxes. Estimated time: 15-25 minutes.

### Need Details? → `QUICK_DEPLOY.md`
3-step deployment guide with troubleshooting tips.

### Want More Info? → `DEPLOYMENT_GUIDE.md`
Complete deployment guide with all options and configurations.

### Curious How It Works? → `ARCHITECTURE.md`
Technical explanation of the full-stack architecture.

---

## 🚀 3-Step Quick Fix

### 1. Deploy Backend (Render.com)
```
https://render.com → New Web Service → Connect GitHub
Build: pip install -r requirements.txt
Start: python server_production.py
Instance: Free
```

### 2. Update script.js (Line 6-8)
```javascript
// Change this:
: 'http://localhost:5000';

// To this (use your Render URL):
: 'https://your-app.onrender.com';
```

### 3. Push Changes
```bash
git add script.js
git commit -m "Update API URL for production"
git push origin main
```

**Done!** Visit `https://iwtbg-8.github.io/iwtbg/` in 2-3 minutes.

---

## 📁 Files Reference

| File | Purpose | Need to Edit? |
|------|---------|---------------|
| `script.js` | Frontend code | ✅ **YES** - Update API URL |
| `server.py` | Backend API | ✅ Already updated (CORS) |
| `server_production.py` | Production server | ✅ Already updated |
| `render.yaml` | Render config | ✅ Already created |
| `requirements.txt` | Python dependencies | ❌ No changes needed |
| `index.html` | Frontend UI | ❌ No changes needed |
| `styles.css` | Styling | ❌ No changes needed |

---

## ⚠️ Important: Free Tier Limitation

**Render.com Free Tier:**
- Backend **sleeps** after 15 minutes of inactivity
- First request takes **30-60 seconds** to wake up
- This is normal! Just wait, it will work.

**To fix sleeping:**
- Upgrade to Render Starter: $7/month (24/7 uptime)
- Or keep free tier for testing/personal use

---

## 🐛 Common Issues

### "Network error" after deployment
- ✅ Check: API URL in script.js matches your Render URL
- ✅ Check: Backend is running (visit Render URL directly)
- ✅ Wait: 30-60 seconds on first request (free tier wake-up)

### Backend won't start on Render
- Check Render Dashboard → Logs for errors
- Verify all files committed and pushed to GitHub

### GitHub Pages not updating
- Wait 2-3 minutes after push
- Clear browser cache (Ctrl+Shift+R)

---

## 💡 What Changed?

### Files Created/Updated:
1. ✅ `render.yaml` - Render deployment config
2. ✅ `server_production.py` - Updated for cloud deployment
3. ✅ `server.py` - CORS updated for GitHub Pages
4. ✅ `SOLUTION.md` - Problem explanation
5. ✅ `CHECKLIST.md` - Step-by-step guide
6. ✅ `QUICK_DEPLOY.md` - Quick deployment
7. ✅ `DEPLOYMENT_GUIDE.md` - Complete guide
8. ✅ `ARCHITECTURE.md` - Technical details
9. ✅ `config.example.js` - API URL template

### What You Need to Do:
- ✅ Deploy to Render.com (5-10 min)
- ✅ Update `script.js` API URL (1 min)
- ✅ Commit and push (1 min)

**That's it!** 🎉

---

## 📊 Architecture

```
Frontend (GitHub Pages)
https://iwtbg-8.github.io/iwtbg/
│
├─ index.html
├─ script.js ────────────┐
└─ styles.css            │
                         │ HTTPS Request
                         │ (CORS enabled)
                         ▼
Backend (Render.com)
https://your-app.onrender.com
│
├─ server.py
├─ yt-dlp
└─ downloads/
```

---

## 💰 Cost

| Tier | Cost | Features |
|------|------|----------|
| **Free** | $0/mo | Backend sleeps after 15 min |
| **Starter** | $7/mo | 24/7 uptime, no sleeping |
| **Pro** | $25/mo | More RAM, faster processing |

**Recommendation**: Start with free, upgrade if you use it daily.

---

## 🎯 Next Steps

1. [ ] Read `SOLUTION.md` to understand the problem
2. [ ] Follow `CHECKLIST.md` to deploy (15-25 min)
3. [ ] Test your deployment
4. [ ] Add authentication before making public!
5. [ ] Consider upgrading if you want 24/7 uptime

---

## 📞 Need Help?

1. **Read the docs** - Start with `SOLUTION.md`
2. **Check Render logs** - Dashboard → Your Service → Logs
3. **Check browser console** - F12 → Console tab
4. **Test backend directly** - `curl https://your-render-url.onrender.com/api`

---

## ✨ Summary

**Problem:** GitHub Pages can't run Python  
**Solution:** Split deployment (frontend on GitHub, backend on Render)  
**Time:** 15-25 minutes  
**Cost:** Free (with limitations) or $7/month (24/7)  

**You've got this!** 🚀
