# 🎬 iwtbg - Setup & Usage Guide

## ✅ Installation Complete!

All video download libraries have been successfully installed:
- ✅ **yt-dlp** (2024.10.7) - The main video download library
- ✅ **Flask** (3.0.0) - Backend web server
- ✅ **Flask-CORS** (4.0.0) - Cross-origin resource sharing
- ✅ **requests** (2.32.5) - HTTP library

## 🚀 How to Start the Application

### Method 1: Using the Startup Script (Recommended)

```bash
cd /home/kali/Desktop/iwtbg
chmod +x start-server.sh
./start-server.sh
```

### Method 2: Manual Start

```bash
cd /home/kali/Desktop/iwtbg
source venv/bin/activate
python3 server.py
```

### Method 3: Direct Python Command

```bash
cd /home/kali/Desktop/iwtbg
venv/bin/python server.py
```

## 🌐 Accessing the Application

Once the server is running:

1. **Backend API**: http://localhost:5000
2. **Frontend Website**: Open `index.html` in your browser

   You can use one of these methods:
   ```bash
   # Method 1: Double-click index.html in file manager
   
   # Method 2: Open with Firefox
   firefox index.html
   
   # Method 3: Open with default browser
   xdg-open index.html
   ```

## 📋 API Endpoints

The backend server provides these endpoints:

- `GET /` - API status and documentation
- `POST /api/analyze` - Analyze a video URL and get metadata
- `POST /api/formats` - Get all available formats for a video
- `POST /api/download` - Download a video in specified quality
- `GET /api/download-file/<filename>` - Download the file

## 🎯 How to Use

1. **Start the backend server** (see above)
2. **Open `index.html`** in your web browser
3. **Paste a video URL** from any supported platform
4. **Click "Download"** to analyze the video
5. **Select quality** from the available options
6. **Download** your video!

## 🎥 Supported Platforms

The application supports **1000+ websites** including:

- YouTube
- Facebook
- Instagram
- Twitter/X
- TikTok
- Vimeo
- Dailymotion
- Twitch
- Reddit
- LinkedIn
- And many more!

## 📁 Project Structure

```
iwtbg/
├── index.html          # Frontend webpage
├── styles.css          # Styles and design
├── script.js           # Frontend JavaScript (with API integration)
├── server.py           # Backend Flask server
├── requirements.txt    # Python dependencies
├── start-server.sh     # Startup script
├── downloads/          # Downloaded videos folder
├── venv/              # Python virtual environment
└── README.md          # Documentation
```

## 🛠️ Testing the API

You can test the API using curl:

```bash
# Test if server is running
curl http://localhost:5000/

# Analyze a video
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'

# Download a video
curl -X POST http://localhost:5000/api/download \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ","quality":"720p"}'
```

## ⚡ Quick Start Example

```bash
# 1. Navigate to project
cd /home/kali/Desktop/iwtbg

# 2. Start server
./start-server.sh

# 3. In another terminal, open the website
firefox index.html
```

## 🔧 Troubleshooting

### Server won't start?
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Port 5000 already in use?
```bash
# Find and kill process using port 5000
sudo lsof -ti:5000 | xargs kill -9

# Or edit server.py and change the port
```

### Frontend can't connect to backend?
- Make sure the backend server is running
- Check that API_URL in script.js matches your backend (default: http://localhost:5000)
- Check browser console for CORS errors

### Download fails?
- Make sure you have write permissions in the downloads folder
- Some videos may be geo-restricted or require authentication
- Check server logs for detailed error messages

## 📝 Important Notes

1. **Legal Usage**: Only download videos you have permission to download
2. **Storage**: Downloaded videos are saved in the `downloads/` folder
3. **Performance**: Download speed depends on your internet connection
4. **Quality**: Available quality options depend on the source video

## 🎨 Customization

### Change Download Location
Edit `server.py`, line 11:
```python
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'your-folder-name')
```

### Change Server Port
Edit `server.py`, last line:
```python
app.run(debug=True, host='0.0.0.0', port=YOUR_PORT)
```

Then update `script.js`:
```javascript
const API_URL = 'http://localhost:YOUR_PORT';
```

## 📚 Additional Resources

- yt-dlp documentation: https://github.com/yt-dlp/yt-dlp
- Flask documentation: https://flask.palletsprojects.com/
- Supported sites list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 🤝 Need Help?

If you encounter any issues:
1. Check the server terminal for error messages
2. Check browser console (F12) for frontend errors
3. Try with a different video URL
4. Make sure all dependencies are installed

---

**Enjoy downloading! 🎉**
