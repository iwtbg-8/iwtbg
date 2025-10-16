// iwtbg Script
// Backend API Integration

// API Configuration
// Use relative URLs when served from same origin, fallback to localhost
const API_URL = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1') 
    ? window.location.origin 
    : 'http://localhost:5000';

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const downloadBtn = document.getElementById('downloadBtn');
    const videoUrlInput = document.getElementById('videoUrl');
    const formatOptions = document.getElementById('formatOptions');
    const qualityGrid = document.getElementById('qualityGrid');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const result = document.getElementById('result');
    const thumbnail = document.getElementById('thumbnail');
    const videoTitle = document.getElementById('videoTitle');
    const videoDuration = document.getElementById('videoDuration');
    const finalDownloadBtn = document.getElementById('finalDownloadBtn');

    // Helper function to safely parse JSON responses
    async function safeJsonParse(response) {
        // Check if response is ok first
        if (!response.ok) {
            // Try to parse error response if possible, otherwise use status text
            let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            try {
                const text = await response.text();
                if (text) {
                    const errorData = JSON.parse(text);
                    errorMessage = errorData.error || errorMessage;
                }
            } catch (parseError) {
                // Response is not JSON or empty, use status text
            }
            throw new Error(errorMessage);
        }

        // Check content type before parsing as JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await response.text();
            throw new Error(`Server returned non-JSON response: ${text.substring(0, 200)}`);
        }

        // Get response text first to check if it's empty
        const text = await response.text();
        if (!text || text.trim() === '') {
            throw new Error('Server returned empty response');
        }

        try {
            return JSON.parse(text);
        } catch (parseError) {
            throw new Error(`Invalid JSON response: ${parseError.message}`);
        }
    }

    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all FAQ items
            faqItems.forEach(faq => faq.classList.remove('active'));
            
            // Open clicked item if it wasn't active
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Download button click handler
    downloadBtn.addEventListener('click', async function() {
        const url = videoUrlInput.value.trim();
        
        if (!url) {
            showNotification('Please enter a video URL', 'error');
            return;
        }

        if (!isValidUrl(url)) {
            showNotification('Please enter a valid URL', 'error');
            return;
        }

        // Reset UI
        formatOptions.style.display = 'none';
        result.style.display = 'none';
        
        // Show progress
        progressContainer.style.display = 'block';
        progressText.textContent = 'Analyzing video...';
        animateProgress(0, 100, 2000);

        try {
            // Call backend API to analyze video
            const response = await fetch(`${API_URL}/api/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const data = await safeJsonParse(response);

            // Hide progress
            progressContainer.style.display = 'none';
            
            // Show format options with real data
            displayQualityOptions(url, data);
            formatOptions.style.display = 'block';
            
            showNotification('Video analyzed successfully!', 'success');

        } catch (error) {
            progressContainer.style.display = 'none';
            const errorMsg = error.message || 'Unknown error occurred';
            showNotification(`Error: ${errorMsg}`, 'error');
            console.error('Analysis error:', error);
            
            // Log additional details for debugging
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                console.error('Network error - check if server is running on:', API_URL);
                showNotification('Network error - please check if the server is running', 'error');
            }
        }
    });

    // Function to validate URL
    function isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    // Function to animate progress bar
    function animateProgress(start, end, duration) {
        const startTime = Date.now();
        const animate = () => {
            const elapsed = Date.now() - startTime;
            const progress = Math.min((elapsed / duration) * (end - start) + start, end);
            progressFill.style.width = progress + '%';
            
            if (progress < end) {
                requestAnimationFrame(animate);
            }
        };
        animate();
    }

    // Function to display quality options
    function displayQualityOptions(url, videoData) {
        // Build quality options from actual video data
        const qualities = [];
        
        // Add video formats
        if (videoData.formats && videoData.formats.length > 0) {
            const qualityIcons = {
                '2160p': 'fa-crown',
                '1440p': 'fa-gem',
                '1080p': 'fa-star',
                '720p': 'fa-check-circle',
                '480p': 'fa-play-circle',
                '360p': 'fa-mobile-alt',
                '240p': 'fa-mobile-alt',
                '144p': 'fa-mobile-alt'
            };

            videoData.formats.forEach(format => {
                const sizeLabel = format.filesize ? 
                    `~${(format.filesize / (1024 * 1024)).toFixed(0)} MB` : 
                    'Size unknown';
                
                qualities.push({
                    label: format.quality,
                    resolution: format.quality,
                    size: sizeLabel,
                    icon: qualityIcons[format.quality] || 'fa-video',
                    videoData: videoData
                });
            });
        } else {
            // Fallback default qualities
            qualities.push(
                { label: 'Best Quality', resolution: '1080p', size: 'Auto', icon: 'fa-star', videoData },
                { label: 'HD', resolution: '720p', size: 'Auto', icon: 'fa-check-circle', videoData },
                { label: 'SD', resolution: '480p', size: 'Auto', icon: 'fa-play-circle', videoData }
            );
        }

        // Add audio only option
        qualities.push({ 
            label: 'Audio Only', 
            resolution: 'audio', 
            size: 'MP3', 
            icon: 'fa-music',
            videoData 
        });

        qualityGrid.innerHTML = '';
        
        qualities.forEach(quality => {
            const option = document.createElement('div');
            option.className = 'quality-option';
            option.innerHTML = `
                <i class="fas ${quality.icon}"></i>
                <div class="quality-label">${quality.label}</div>
                <div class="quality-size">${quality.resolution}</div>
                <div class="quality-size">${quality.size}</div>
            `;
            
            option.addEventListener('click', () => {
                // Remove selected class from all options
                document.querySelectorAll('.quality-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                
                // Add selected class to clicked option
                option.classList.add('selected');
                
                // Prepare download with real backend
                setTimeout(() => {
                    prepareDownload(quality, url, videoData);
                }, 500);
            });
            
            qualityGrid.appendChild(option);
        });
    }

    // Function to prepare download
    async function prepareDownload(quality, url, videoData) {
        formatOptions.style.display = 'none';
        progressContainer.style.display = 'block';
        progressText.textContent = `Downloading ${quality.label}...`;
        animateProgress(0, 30, 1000);

        try {
            // Call backend API to download video
            const response = await fetch(`${API_URL}/api/download`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    url: url,
                    quality: quality.resolution
                })
            });

            animateProgress(30, 70, 2000);
            const data = await safeJsonParse(response);

            animateProgress(70, 100, 1000);

            setTimeout(() => {
                progressContainer.style.display = 'none';
                
                // Show result with real data
                displayResult(quality, url, videoData, data.filename);
                result.style.display = 'block';
                
                showNotification('Download complete!', 'success');
            }, 1000);

        } catch (error) {
            progressContainer.style.display = 'none';
            const errorMsg = error.message || 'Download failed';
            showNotification(`Download error: ${errorMsg}`, 'error');
            console.error('Download error:', error);
            
            // Log additional details for debugging
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                console.error('Network error - check if server is running on:', API_URL);
                showNotification('Network error - please check if the server is running', 'error');
            }
            
            formatOptions.style.display = 'block';
        }
    }

    // Function to display download result
    function displayResult(quality, url, videoData, filename) {
        thumbnail.src = videoData.thumbnail || 'https://images.unsplash.com/photo-1611162616305-c69b3fa7fbe0?w=400';
        videoTitle.textContent = videoData.title;
        videoDuration.textContent = `Quality: ${quality.label} (${quality.resolution}) • Ready to download`;
        
        // Set up final download button
        finalDownloadBtn.onclick = () => {
            // Download the file from backend
            const downloadUrl = `${API_URL}/api/download-file/${encodeURIComponent(filename)}`;
            window.open(downloadUrl, '_blank');
            showNotification('Download started! Check your browser downloads.', 'success');
        };
    }



    // Notification function
    function showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#6366f1'};
            color: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideIn 0.3s ease;
            max-width: 400px;
            font-weight: 500;
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Remove notification after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 5000);
    }

    // Add notification animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // Add some interactivity on scroll
    window.addEventListener('scroll', () => {
        const header = document.querySelector('.header');
        if (window.scrollY > 50) {
            header.style.background = 'rgba(15, 23, 42, 0.98)';
        } else {
            header.style.background = 'rgba(15, 23, 42, 0.95)';
        }
    });
});

/*
IMPORTANT NOTES FOR PRODUCTION:

1. Backend Implementation Required:
   - This is a frontend demo only
   - You need to implement a backend server (Node.js, Python, etc.)
   - Use libraries like yt-dlp, youtube-dl, or similar
   - Example backend frameworks:
     * Python: Flask/FastAPI + yt-dlp
     * Node.js: Express + ytdl-core or yt-dlp wrapper

2. Backend API Endpoints Needed:
   - POST /api/analyze - Analyze video URL and return metadata
   - POST /api/download - Process and download video
   - GET /api/progress/:id - Check download progress

3. Legal Considerations:
   - Respect copyright laws
   - Add proper terms of service
   - Implement rate limiting
   - Add user agreement before downloads

4. Security Measures:
   - Validate and sanitize all URLs
   - Implement CORS properly
   - Add rate limiting
   - Protect against malicious URLs
   - Use environment variables for sensitive data

5. Performance Optimization:
   - Implement caching for video metadata
   - Use queue system for downloads (Redis, Bull)
   - Consider CDN for static assets
   - Implement proper error handling

6. Additional Features to Consider:
   - User accounts and download history
   - Batch downloads
   - Playlist support
   - Subtitle downloads
   - Format conversion
   - Cloud storage integration
*/
