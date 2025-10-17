// Configuration Template for Production Deployment
// Copy this to script.js after deploying to Render.com

// ============================================
// STEP 1: Deploy backend to Render.com
// STEP 2: Copy your Render URL 
// STEP 3: Replace BACKEND_URL below
// ============================================

// API Configuration
const BACKEND_URL = 'https://YOUR-RENDER-URL-HERE.onrender.com';  // ← CHANGE THIS!

const API_URL = window.location.origin.includes('localhost') || window.location.origin.includes('127.0.0.1') 
    ? window.location.origin   // Local development
    : BACKEND_URL;              // Production (Render.com)

// Example:
// const BACKEND_URL = 'https://iwtbg-backend.onrender.com';

// ============================================
// After changing, commit and push:
// git add script.js
// git commit -m "Update API URL for production"
// git push origin main
// ============================================
