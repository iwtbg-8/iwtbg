# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### ❌ Error: HTTP 403 Forbidden

This error occurs when YouTube or other platforms block download requests. Here are solutions:

#### **Solution 1: Try Different Quality**
- Some quality options may work better than others
- Try selecting "Best Quality" instead of specific resolutions
- Audio-only downloads often work better

#### **Solution 2: Use Different Videos**
YouTube has been implementing stricter anti-bot measures. Some videos may not be downloadable due to:
- Age restrictions
- Regional restrictions
- Copyright protection
- Bot detection

**Recommended alternatives:**
- Try videos from other platforms (Vimeo, Dailymotion, etc.)
- Try older or less popular YouTube videos
- Use publicly available educational content

#### **Solution 3: Test with Known Working URLs**

Try these test URLs that usually work:
```
# Vimeo (usually works well)
https://vimeo.com/148751763

# Archive.org (open access videos)
https://archive.org/details/BigBuckBunny_124

# Dailymotion
https://www.dailymotion.com/video/x8atvre
```

#### **Solution 4: Update yt-dlp**
```bash
cd /home/kali/Desktop/iwtbg
source venv/bin/activate
pip install --upgrade yt-dlp
```

#### **Solution 5: Use YouTube Cookies (Advanced)**

For age-restricted or member-only content:

1. **Export cookies from your browser:**
   - Install a browser extension like "Get cookies.txt"
   - Visit YouTube while logged in
   - Export cookies to a file `cookies.txt`

2. **Place cookies file:**
   ```bash
   # Copy your cookies.txt to the project folder
   cp ~/Downloads/cookies.txt /home/kali/Desktop/iwtbg/
   ```

3. **Update server.py** to use cookies:
   ```python
   # Add to common_opts in the download function:
   'cookiefile': os.path.join(os.getcwd(), 'cookies.txt'),
   ```

### ❌ Error: Failed to Fetch

**Cause:** Frontend can't connect to backend

**Solution:**
1. Make sure server is running: `./start-server.sh`
2. Access via: http://localhost:5000 (NOT by opening index.html directly)
3. Check if port 5000 is available: `lsof -i :5000`

### ❌ Video Analysis Works But Download Fails

**Cause:** Platform allows metadata extraction but blocks actual downloads

**Solutions:**
1. Try lower quality (480p or 360p)
2. Try audio-only format
3. Try a different video from the same platform
4. Some platforms require authentication

### ❌ Downloads Folder is Empty

**Check:**
```bash
ls -la /home/kali/Desktop/iwtbg/downloads/
```

**Solution:**
- Make sure you clicked the final download button
- Check browser's download folder (files may be served directly)
- Check server terminal for error messages

### ❌ Server Won't Start

**Error: Port already in use**
```bash
# Kill existing process
sudo lsof -ti:5000 | xargs kill -9

# Or use a different port (edit server.py)
```

**Error: Module not found**
```bash
# Reinstall dependencies
cd /home/kali/Desktop/iwtbg
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ FFmpeg Errors (for audio conversion)

**Install FFmpeg:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Platform-Specific Notes

### YouTube
- **Current Status:** Increasingly difficult due to bot detection
- **Best Practices:**
  - Use "best" quality option instead of specific resolutions
  - Try audio-only downloads
  - Consider using cookies for restricted content
- **Alternatives:** Try unlisted or educational videos

### Facebook
- **Requirements:** May need authentication for some videos
- **Works Best:** Public videos from pages

### Instagram
- **Works Well:** Public posts and reels
- **May Fail:** Private accounts, stories

### TikTok
- **Usually Works:** Public videos
- **Note:** Watermark may be present

### Vimeo
- **Generally Reliable:** Good success rate
- **Recommended:** Best platform for testing

### Twitter/X
- **Works:** Most public videos
- **Note:** Quality may be limited

## Testing the Application

### 1. Test Backend API Directly

```bash
# Test server status
curl http://localhost:5000/api

# Test video analysis
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://vimeo.com/148751763"}'
```

### 2. Check Server Logs

Watch the terminal where the server is running for detailed error messages.

### 3. Browser Console

Press F12 in your browser and check the Console tab for JavaScript errors.

## Alternative: Command Line Usage

If the web interface isn't working, you can use yt-dlp directly:

```bash
# Activate virtual environment
cd /home/kali/Desktop/iwtbg
source venv/bin/activate

# Download video directly
yt-dlp "VIDEO_URL"

# Download best quality up to 720p
yt-dlp -f "best[height<=720]" "VIDEO_URL"

# Download audio only
yt-dlp -x --audio-format mp3 "VIDEO_URL"

# List available formats
yt-dlp -F "VIDEO_URL"
```

## Best Practices

### ✅ DO:
- Use public, non-restricted content
- Try different platforms (Vimeo, Dailymotion often work better)
- Start with lower quality options
- Test with known working URLs first
- Keep yt-dlp updated

### ❌ DON'T:
- Attempt to download copyrighted content
- Use for piracy
- Download private or restricted videos without permission
- Abuse the service with too many requests

## Getting Help

### 1. Check Logs
```bash
# Server terminal will show detailed errors
# Browser console (F12) shows frontend errors
```

### 2. Update Everything
```bash
cd /home/kali/Desktop/iwtbg
source venv/bin/activate
pip install --upgrade yt-dlp flask flask-cors
```

### 3. Test Different Content

If one video doesn't work:
- Try a different video from the same platform
- Try a different platform
- Use the test URLs provided above

## Known Limitations

1. **YouTube Restrictions:** Due to recent changes, some YouTube videos may fail
2. **Platform Updates:** Websites frequently change, breaking downloaders
3. **Rate Limiting:** Too many requests may trigger blocking
4. **Geographic Restrictions:** Some content is region-locked
5. **Authentication:** Private/premium content requires login

## Legal Notice

⚠️ **Important:** Only download content you have permission to download. Respect copyright laws and platform terms of service.

---

**Need more help?** Check the yt-dlp documentation:
https://github.com/yt-dlp/yt-dlp#usage-and-options
