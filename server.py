from flask import Flask, request, jsonify, send_file, send_from_directory, abort
from flask_cors import CORS
import yt_dlp
import os
import json
import re
import logging
from urllib.parse import urlparse, quote
from pathlib import Path
from datetime import datetime
import hashlib
import time
from collections import deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='.')

# CORS configuration with more security (allow GH Pages, Render, and local dev)
CORS(app, resources={
    r"/api/*": {
        # Use regex patterns for origins to properly match ports/subdomains
        "origins": [
            r"https?://localhost(:\d+)?",
            r"https?://127\.0\.0\.1(:\d+)?",
            r"https://iwtbg-8\.github\.io",
            r"https://.*\.onrender\.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
MAX_FILESIZE = 20 * 1024 * 1024 * 1024  # 20GB max file size
ALLOWED_DOMAINS = []  # Empty means all domains allowed
DOWNLOAD_DIR = os.path.join(os.getcwd(), 'downloads')
CACHE_TTL = 24 * 3600  # 24 hours cache (increased)
RATE_LIMIT_WINDOW = 10 * 60  # 10 minutes window (for 1000 requests)
RATE_LIMIT_MAX = 1000  # Max 1000 requests per IP per 10 minutes (very generous)

# In-memory caches and rate limit storage
analyze_cache = {}  # url -> (timestamp, data)
formats_cache = {}  # url -> (timestamp, data)
rate_limit_map = {}  # ip -> deque[timestamps]

# Create downloads directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)
    logger.info(f"Created download directory: {DOWNLOAD_DIR}")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_valid_url(url):
    """Validate URL format and check for suspicious patterns"""
    try:
        result = urlparse(url)
        
        # Check basic URL structure
        if not all([result.scheme, result.netloc]):
            return False
        
        # Only allow http and https
        if result.scheme not in ['http', 'https']:
            return False
        
        # Block localhost and private IPs to prevent SSRF
        blocked_hosts = ['localhost', '127.0.0.1', '0.0.0.0', '::1']
        hostname = result.netloc.split(':')[0].lower()
        
        if hostname in blocked_hosts:
            logger.warning(f"Blocked localhost/private IP: {result.netloc}")
            return False
        
        # Check for private IP ranges (basic check)
        if (hostname.startswith('192.168.') or 
            hostname.startswith('10.') or 
            hostname.startswith('172.16.') or
            hostname.startswith('172.17.') or
            hostname.startswith('172.18.') or
            hostname.startswith('172.19.') or
            hostname.startswith('172.20.') or
            hostname.startswith('172.21.') or
            hostname.startswith('172.22.') or
            hostname.startswith('172.23.') or
            hostname.startswith('172.24.') or
            hostname.startswith('172.25.') or
            hostname.startswith('172.26.') or
            hostname.startswith('172.27.') or
            hostname.startswith('172.28.') or
            hostname.startswith('172.29.') or
            hostname.startswith('172.30.') or
            hostname.startswith('172.31.')):
            logger.warning(f"Blocked private IP range: {result.netloc}")
            return False
        
        return True
    except Exception as e:
        logger.error(f"URL validation error: {e}")
        return False

def sanitize_text(text):
    """Sanitize text to prevent XSS and other injection attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = str(text)
    text = re.sub(r'[<>"\']', '', text)
    text = text.strip()
    
    return text[:500]  # Limit length

def sanitize_filename(filename):
    """Sanitize filename to prevent directory traversal and ensure safety"""
    # Remove any directory components
    filename = os.path.basename(filename)
    
    # Remove any dangerous characters
    filename = re.sub(r'[^\w\s\-\.]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:250] + ext
    
    return filename

def get_client_ip():
    """Get client IP considering proxies (X-Forwarded-For)."""
    xff = request.headers.get('X-Forwarded-For', '')
    if xff:
        # Take the first IP in the list
        return xff.split(',')[0].strip()
    return request.remote_addr or 'unknown'

def is_rate_limited(ip):
    """Basic fixed-window rate limiter using a sliding deque."""
    now = time.time()
    dq = rate_limit_map.get(ip)
    if dq is None:
        dq = deque()
        rate_limit_map[ip] = dq
    # Evict old timestamps
    while dq and now - dq[0] > RATE_LIMIT_WINDOW:
        dq.popleft()
    if len(dq) >= RATE_LIMIT_MAX:
        return True
    dq.append(now)
    return False

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def home():
    """Serve the main frontend page"""
    try:
        return send_file('index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return jsonify({'error': 'Frontend not found'}), 404

@app.route('/api')
def api_info():
    """API status and information"""
    return jsonify({
        'status': 'running',
        'version': '1.0.1',
        'message': 'iwtbg API is active',
        'endpoints': {
            '/api/analyze': {
                'methods': ['POST'],
                'description': 'Analyze video URL',
                'body': {'url': 'string (required)'}
            },
            '/api/download': {
                'methods': ['POST'],
                'description': 'Download video',
                'body': {'url': 'string (required)', 'quality': 'string (e.g., "720p", "1080p")'}
            },
            '/api/formats': {
                'methods': ['POST'],
                'description': 'Get available formats',
                'body': {'url': 'string (required)'}
            },
            '/api/download-file/<filename>': {
                'methods': ['GET'],
                'description': 'Download the file'
            }
        }
    })

@app.route('/api/analyze', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def analyze_video():
    """Analyze video URL and return metadata"""
    if request.method == 'OPTIONS':
        return '', 204
    
    if request.method != 'POST':
        # Return 405 for any method other than POST or OPTIONS
        return method_not_allowed(None)
    
    try:
        # Rate limiting
        client_ip = get_client_ip()
        if is_rate_limited(client_ip):
            return jsonify({'error': 'Too many requests. Please try again later.'}), 429

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate and sanitize URL
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # URL length is now unlimited for flexibility
        
        logger.info(f"Analyzing URL: {url[:100]}... (ip={client_ip})")

        # Cache check
        cached = analyze_cache.get(url)
        if cached:
            ts, payload = cached
            if time.time() - ts < CACHE_TTL:
                logger.info("Returning cached analysis result")
                return jsonify(payload)

        # yt-dlp options for extracting info only with proper headers
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'socket_timeout': 60,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'nocheckcertificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash', 'translated_subs']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
            },
            'noplaylist': True,
            'geo_bypass': True,
            'sleep_interval': 2,
            'max_sleep_interval': 5,
        }

        # Retry mechanism for anti-bot issues
        max_retries = 5
        info = None
        for attempt in range(max_retries + 1):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    break  # Success, exit retry loop
            except yt_dlp.utils.DownloadError as e:
                msg = str(e)
                if "Sign in to confirm you're not a bot" in msg or 'not a bot' in msg:
                    if attempt < max_retries:
                        wait_time = (2 ** attempt) + (attempt * 2)  # More aggressive backoff
                        logger.warning(f"Anti-bot challenge on attempt {attempt + 1}, waiting {wait_time}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"YouTube anti-bot challenge persisted after {max_retries + 1} attempts")
                        return jsonify({
                            'error': 'YouTube is blocking automated requests for this video',
                            'message': 'This video is temporarily unavailable. Please try again later or use a different video.',
                            'technical': 'Anti-bot verification required'
                        }), 503  # Service Unavailable
                else:
                    # Other download errors, don't retry
                    logger.exception(f"Download error: {e}")
                    return jsonify({'error': f'Failed to analyze video: {str(e)}'}), 400
            except Exception as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    logger.warning(f"Unexpected error on attempt {attempt + 1}, waiting {wait_time}s: {e}")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.exception(f"Unexpected error in analyze_video: {e}")
                    return jsonify({'error': 'Failed to analyze video. Please check the URL and try again.'}), 500

        # Check if we got info after all retries
        if info is None:
            return jsonify({'error': 'Failed to analyze video after multiple attempts.'}), 500

        try:
            # Process the extracted info
            # Extract available formats
            formats = []
            if 'formats' in info and info['formats']:
                seen_qualities = set()
                for f in info['formats']:
                    height = f.get('height')
                    if height and isinstance(height, int):
                        quality_label = f"{height}p"
                        if quality_label not in seen_qualities:
                            filesize = f.get('filesize') or f.get('filesize_approx')
                            formats.append({
                                'quality': quality_label,
                                'height': height,
                                'ext': f.get('ext', 'mp4'),
                                'filesize': filesize,
                                'format_id': f.get('format_id')
                            })
                            seen_qualities.add(quality_label)
            
            # Sort formats by quality (highest first) - ensure height is valid
            formats.sort(key=lambda x: x.get('height', 0), reverse=True)
            
            # Sanitize title to prevent XSS
            title = sanitize_text(info.get('title', 'Unknown Title'))
            description = sanitize_text(info.get('description', ''))[:200]
            if description and len(info.get('description', '')) > 200:
                description += '...'
            
            logger.info(f"Successfully analyzed: {title}")
            
            payload = {
                'success': True,
                'title': title,
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'uploader': sanitize_text(info.get('uploader', 'Unknown')),
                'view_count': info.get('view_count', 0),
                'formats': formats[:6],  # Return top 6 quality options
                'description': description
            }
            # Store in cache
            analyze_cache[url] = (time.time(), payload)
            return jsonify(payload)
            
        except Exception as e:
            logger.exception(f"Error processing video info: {e}")
            return jsonify({'error': 'Failed to process video information. Please try again.'}), 500
    
    except Exception as e:
        logger.exception(f"Unexpected error in analyze_video outer handler: {e}")
        return jsonify({'error': 'Failed to analyze video. Please check the URL and try again.'}), 500

@app.route('/api/formats', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def get_formats():
    """Get all available formats for a video"""
    if request.method == 'OPTIONS':
        return '', 204
    
    if request.method != 'POST':
        return method_not_allowed(None)
    
    try:
        # Rate limiting
        client_ip = get_client_ip()
        if is_rate_limited(client_ip):
            return jsonify({'error': 'Too many requests. Please try again later.'}), 429

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        logger.info(f"Fetching formats for: {url[:100]}... (ip={client_ip})")

        # Cache check
        cached = formats_cache.get(url)
        if cached:
            ts, payload = cached
            if time.time() - ts < CACHE_TTL:
                logger.info("Returning cached formats result")
                return jsonify(payload)
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 60,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'nocheckcertificate': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash', 'translated_subs']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
            },
            'noplaylist': True,
            'geo_bypass': True,
            'sleep_interval': 1,
            'max_sleep_interval': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            try:
                # Organize formats by quality
                video_formats = []
                audio_formats = []
                
                for f in info.get('formats', []):
                    format_info = {
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'quality': f.get('format_note', 'Unknown'),
                        'filesize': f.get('filesize') or f.get('filesize_approx'),
                        'tbr': f.get('tbr')
                    }
                    
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        format_info['type'] = 'video+audio'
                        format_info['resolution'] = f"{f.get('height')}p" if f.get('height') else 'Unknown'
                        video_formats.append(format_info)
                    elif f.get('vcodec') != 'none':
                        format_info['type'] = 'video'
                        format_info['resolution'] = f"{f.get('height')}p" if f.get('height') else 'Unknown'
                        video_formats.append(format_info)
                    elif f.get('acodec') != 'none':
                        format_info['type'] = 'audio'
                        format_info['abr'] = f.get('abr')
                        audio_formats.append(format_info)
                
                payload = {
                    'success': True,
                    'video_formats': video_formats,
                    'audio_formats': audio_formats
                }
                # Store in cache
                formats_cache[url] = (time.time(), payload)
                return jsonify(payload)
                
            except Exception as e:
                logger.exception(f"Error processing formats: {e}")
                return jsonify({'error': 'Failed to process video formats. Please try again.'}), 500
            
    except Exception as e:
        logger.exception(f"Error in get_formats: {e}")
        return jsonify({'error': f'Failed to get formats: {str(e)}'}), 500

@app.route('/api/download', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def download_video():
    """Download video in specified quality"""
    if request.method == 'OPTIONS':
        return '', 204
    
    if request.method != 'POST':
        return method_not_allowed(None)
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400
            
        url = data.get('url')
        quality = data.get('quality', '720p')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # URL length is now unlimited
        
        # Sanitize quality parameter
        if not re.match(r'^\d+p$|^audio$', quality):
            quality = '720p'
        
        logger.info(f"Downloading URL: {url[:100]}... Quality: {quality}")
        
        # Generate safe filename base
        safe_filename = f"download_{hashlib.md5(url.encode()).hexdigest()[:8]}"
        
        # Common yt-dlp options to bypass restrictions
        common_opts = {
            'quiet': False,
            'no_warnings': True,
            'socket_timeout': 120,
            'retries': 10,
            'fragment_retries': 10,
            'concurrent_fragment_downloads': 10,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'nocheckcertificate': True,
            'outtmpl': os.path.join(DOWNLOAD_DIR, f'{safe_filename}_%(title).100s.%(ext)s'),
            'restrictfilenames': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'web'],
                    'skip': ['hls', 'dash', 'translated_subs']
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Sec-Fetch-Mode': 'navigate',
            },
            'noplaylist': True,
            'geo_bypass': True,
            'sleep_interval': 2,
            'max_sleep_interval': 5,
        }
        
        # Configure download options based on quality
        if quality == 'audio':
            ydl_opts = {
                **common_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            # Extract resolution number (e.g., '1080p' -> '1080')
            resolution = quality.replace('p', '') if quality else '720'
            
            # Simplified format selector for better compatibility and speed
            ydl_opts = {
                **common_opts,
                'format': f'best[height<={resolution}]',  # Simpler format selection
                'merge_output_format': 'mp4',
            }
        
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Handle audio conversion
            if quality == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            # Check file exists and size
            if os.path.exists(filename):
                filesize = os.path.getsize(filename)
                if filesize > MAX_FILESIZE:
                    os.remove(filename)
                    logger.warning(f"File exceeds max size: {filesize} bytes")
                    return jsonify({'error': 'File size exceeds maximum limit (500MB)'}), 413
            else:
                return jsonify({'error': 'Download completed but file not found'}), 500
            
            logger.info(f"Download completed: {os.path.basename(filename)} ({filesize} bytes)")
            
            return jsonify({
                'success': True,
                'message': 'Video downloaded successfully',
                'filename': os.path.basename(filename),
                'title': sanitize_text(info.get('title', 'Unknown')),
                'filesize': filesize
            })
            
    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e)
        logger.exception(f"Download error: {error_msg}")
        
        # Provide more helpful error messages
        if '403' in error_msg or 'Forbidden' in error_msg:
            error_msg = "Access denied. This video may be restricted, age-restricted, or require sign-in. Try a different video or quality."
        elif 'Private video' in error_msg:
            error_msg = "This is a private video and cannot be downloaded."
        elif 'Video unavailable' in error_msg:
            error_msg = "Video is unavailable or has been removed."
        elif 'sign in' in error_msg.lower():
            error_msg = "This video requires authentication. Try a public video instead."
            
        return jsonify({'error': f'Download failed: {error_msg}'}), 400
    except Exception as e:
        logger.exception(f"Unexpected error in download_video: {e}")
        return jsonify({'error': 'Download failed. Please try again or use a different video.'}), 500

@app.route('/api/download-file/<filename>', methods=['GET'])
def download_file(filename):
    """Serve the downloaded file"""
    try:
        # Sanitize filename to prevent directory traversal
        safe_filename = sanitize_filename(filename)
        file_path = os.path.join(DOWNLOAD_DIR, safe_filename)
        
        # Verify the file is in the downloads directory (prevent path traversal)
        real_path = os.path.realpath(file_path)
        real_download_dir = os.path.realpath(DOWNLOAD_DIR)
        
        if not real_path.startswith(real_download_dir):
            logger.warning(f"Directory traversal attempt: {filename}")
            return jsonify({'error': 'Invalid filename'}), 403
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            logger.info(f"Serving file: {safe_filename}")
            return send_file(file_path, as_attachment=True, download_name=safe_filename)
        else:
            logger.warning(f"File not found: {safe_filename}")
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.exception(f"Error serving file {filename}: {e}")
        return jsonify({'error': 'Failed to download file'}), 500

# ============================================================================
# STATIC FILE SERVING (Catch-all route - must be last!)
# ============================================================================

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS, etc.)"""
    # Don't catch API routes - let Flask handle method errors properly
    if path.startswith('api/') or path == 'api':
        abort(404)  # This will trigger Flask's normal routing/error handling
        
    try:
        # Prevent directory traversal attacks
        safe_path = Path(path).resolve()
        base_path = Path('.').resolve()
        
        # Check if the resolved path is within the base directory
        if not str(safe_path).startswith(str(base_path)):
            logger.warning(f"Directory traversal attempt: {path}")
            return jsonify({'error': 'Access denied'}), 403
            
        # Only serve specific file types
        allowed_extensions = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf'}
        if safe_path.suffix.lower() not in allowed_extensions:
            logger.warning(f"Disallowed file type: {path}")
            return jsonify({'error': 'File type not allowed'}), 403
            
        return send_from_directory('.', path)
    except Exception as e:
        logger.exception(f"Error serving static file {path}: {e}")
        return jsonify({'error': 'File not found'}), 404

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.exception(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({'error': 'Request entity too large'}), 413

@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 Method Not Allowed errors"""
    # Get allowed methods from the error object if available
    allowed_methods = []
    if error and hasattr(error, 'valid_methods'):
        allowed_methods = list(error.valid_methods - {'HEAD', 'OPTIONS'})
    
    return jsonify({
        'error': 'Method not allowed',
        'message': f'This endpoint does not support {request.method} requests',
        'allowed_methods': allowed_methods if allowed_methods else ['POST']
    }), 405

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 iwtbg API Server Starting...")
    print("=" * 60)
    print(f"📁 Download directory: {DOWNLOAD_DIR}")
    print(f"🌐 Server running on: http://localhost:5000")
    print(f"📊 Max file size: {MAX_FILESIZE / (1024*1024*1024):.0f}GB")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  GET  /                 - Frontend website")
    print("  GET  /api              - API status")
    print("  POST /api/analyze      - Analyze video URL")
    print("  POST /api/formats      - Get available formats")
    print("  POST /api/download     - Download video")
    print("  GET  /api/download-file/<filename> - Serve downloaded file")
    print("=" * 60)
    print("\n⚠️  Development Server - Use server_production.py for production")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
