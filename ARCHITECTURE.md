# Architecture - Full Stack Deployment

## Why GitHub Pages Doesn't Work Alone

```
❌ WRONG (What you tried):
┌─────────────────────┐
│   GitHub Pages      │
│  (Static Files)     │
│                     │
│  index.html         │
│  script.js  ──X──→  server.py (Can't run Python!)
│  styles.css         │
└─────────────────────┘
```

**Problem**: GitHub Pages only serves static files (HTML, CSS, JS). It cannot run Python, Node.js, or any backend code.

---

## Correct Architecture (Split Deployment)

```
✅ CORRECT:

Frontend (GitHub Pages - Free)
┌─────────────────────┐
│ iwtbg-8.github.io   │
│                     │
│  📄 index.html      │
│  📜 script.js       │────────┐
│  🎨 styles.css      │        │
└─────────────────────┘        │
                               │
                               │ HTTPS Request
                               │ (CORS Enabled)
                               │
                               ▼
Backend (Render.com - Free/Paid)
┌─────────────────────┐
│ yourapp.onrender.com│
│                     │
│  🐍 server.py       │
│  📦 yt-dlp          │
│  💾 downloads/      │
└─────────────────────┘
```

---

## How It Works

### 1️⃣ User Visits Website
```
User → https://iwtbg-8.github.io/iwtbg/
       ↓
     GitHub Pages serves HTML/CSS/JS
       ↓
     Browser loads and runs JavaScript
```

### 2️⃣ User Clicks Download
```
Browser JavaScript (script.js)
       ↓
     Makes HTTPS request to:
     https://yourapp.onrender.com/api/download
       ↓
     Render.com server processes request
       ↓
     Downloads video with yt-dlp
       ↓
     Sends file back to browser
```

### 3️⃣ File Download
```
Render.com → User's Browser → User's Computer
```

---

## File Organization

```
Your Repository (GitHub):
├── index.html          → Deployed to GitHub Pages
├── script.js           → Deployed to GitHub Pages
├── styles.css          → Deployed to GitHub Pages
├── server.py           → Deployed to Render.com
├── server_production.py → Deployed to Render.com
├── requirements.txt    → Used by Render.com
└── render.yaml         → Render.com configuration
```

---

## Deployment Platforms Comparison

| Platform | Frontend | Backend | Cost | Uptime |
|----------|----------|---------|------|--------|
| **GitHub Pages** | ✅ Yes | ❌ No | Free | 99.9% |
| **Render.com** | ✅ Yes | ✅ Yes | Free*/Paid | 99%* |
| **Vercel** | ✅ Yes | ⚠️ Serverless only | Free | 99.9% |
| **Netlify** | ✅ Yes | ⚠️ Serverless only | Free | 99.9% |
| **Heroku** | ✅ Yes | ✅ Yes | Paid only | 99.9% |
| **Railway** | ✅ Yes | ✅ Yes | Free*/Paid | 99% |

*Free tier has limitations (sleeping, resource limits)

---

## Why This Split Approach?

### ✅ Advantages
1. **GitHub Pages**: Free, fast CDN, unlimited bandwidth for static files
2. **Render.com**: Can run Python, handle video processing
3. **Separation**: Frontend updates don't require backend restart
4. **Scalability**: Can upgrade backend independently

### ❌ Disadvantages
1. **Free Tier**: Backend sleeps after 15 minutes (30-60s wake time)
2. **CORS**: Must configure cross-origin requests
3. **Two Deployments**: More complex than single deployment

---

## Alternative: All-in-One Deployment

If you don't want split deployment, use **Render.com for everything**:

```
All-in-One (Render.com only):
┌─────────────────────┐
│ yourapp.onrender.com│
│                     │
│  📄 index.html      │
│  📜 script.js       │
│  🎨 styles.css      │
│  🐍 server.py       │
└─────────────────────┘
```

**Pros**: Simpler, no CORS issues, single deployment
**Cons**: Uses backend resources for static files, less efficient

To do this:
1. Just deploy to Render.com
2. Skip GitHub Pages entirely
3. Update `script.js` to use relative URLs

---

## Cost Breakdown

### Free Tier (Good for testing)
- Frontend (GitHub Pages): $0
- Backend (Render Free): $0
- **Total: $0/month**
- ⚠️ Backend sleeps after 15 min

### Production (Recommended)
- Frontend (GitHub Pages): $0
- Backend (Render Starter): $7/month
- **Total: $7/month**
- ✅ 24/7 uptime

### Heavy Usage
- Frontend (GitHub Pages): $0
- Backend (Render Pro): $25/month
- CDN (Cloudflare): $5-20/month
- **Total: $30-45/month**
- ✅ 2GB RAM, faster processing

---

## Security Considerations

### Current Setup
- ✅ HTTPS (both platforms)
- ✅ CORS configured
- ❌ No authentication
- ❌ No rate limiting
- ❌ Public access

### Before Going Public
Add these features:
1. **User Authentication** (Firebase, Auth0, or custom)
2. **Rate Limiting** (Flask-Limiter)
3. **Usage Quotas** (Database tracking)
4. **Input Validation** (Already done)
5. **Monitoring** (Sentry, LogRocket)

---

## Next Steps

1. ✅ Deploy backend to Render.com
2. ✅ Update API URL in script.js
3. ✅ Enable GitHub Pages
4. ⏳ Test thoroughly
5. ⏳ Add authentication (before public launch)
6. ⏳ Add rate limiting
7. ⏳ Monitor usage and costs

---

## Support Resources

- **Render Docs**: https://render.com/docs
- **GitHub Pages**: https://pages.github.com/
- **Flask CORS**: https://flask-cors.readthedocs.io/
- **yt-dlp**: https://github.com/yt-dlp/yt-dlp

---

## Common Issues

### "Mixed Content" Error
- **Cause**: Trying to load HTTP content from HTTPS page
- **Fix**: Use HTTPS for backend URL (Render provides this)

### "CORS Policy" Error
- **Cause**: Backend not allowing requests from frontend domain
- **Fix**: Add frontend domain to CORS origins in server.py

### "Network Error" / "Failed to Fetch"
- **Cause 1**: Backend is sleeping (free tier)
- **Fix**: Wait 60 seconds, retry
- **Cause 2**: Backend crashed or not running
- **Fix**: Check Render logs

### Downloads Fail on Large Files
- **Cause**: Free tier has timeout limits
- **Fix**: Upgrade to paid tier or implement chunked streaming
