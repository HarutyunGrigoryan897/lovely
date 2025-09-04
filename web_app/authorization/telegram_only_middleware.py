from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.conf import settings
import json


class TelegramOnlyMiddleware(MiddlewareMixin):
    """
    Middleware to restrict access to Telegram Web App users only
    """
    
    ALLOWED_URLS = [
        '/api/auth/telegram-auth/',
        '/api/auth/auth-status/',
        '/admin/',  # Keep admin accessible
        '/static/',  # Static files
        '/media/',   # Media files
        '/api/auth/users/',
        '/api/auth/user-info/',
        '/api/auth/check-admin/',
        '/api/auth/user-profile/',
        '/api/auth/all-admins/',
        '/api/auth/user-approve/<telegram_id>/', 
        '/api/auth/user-reject/<telegram_id>/'
    ]
    
    def process_request(self, request):
        # Allow static files and media
        if any(request.path.startswith(url) for url in self.ALLOWED_URLS):
            return None
        
        # Development bypass - set this in your .env file if you want to bypass Telegram requirement during development
        if settings.DEBUG and getattr(settings, 'BYPASS_TELEGRAM_AUTH', False):
            return None
        
        # Check for Telegram Bot API requests (server-to-server from your bot)
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            api_secret = getattr(settings, 'API_SECRET', None)
            if token == api_secret:
                # This is a valid bot API request, allow it
                return None
            
        # Check if user agent indicates Telegram Web App
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # More comprehensive Telegram Web App detection
        telegram_indicators = [
            'TelegramBot' in user_agent,
            'tgWebApp' in user_agent.lower(),
            request.META.get('HTTP_SEC_FETCH_SITE') == 'cross-site',
            request.META.get('HTTP_SEC_FETCH_MODE') == 'navigate',
            request.META.get('HTTP_REFERER', '').startswith('https://web.telegram.org'),
            # Check for specific Telegram Web App headers
            'tg_colorscheme' in request.GET,
            'tgWebAppData' in request.GET,
            'tgWebAppVersion' in request.GET,
            # Common Telegram Web App user agents
            'telegram' in user_agent.lower(),
        ]
        
        is_telegram_webapp = any(telegram_indicators)
        
        # Also check if user is already authenticated via Telegram
        is_telegram_authenticated = (
            request.user.is_authenticated and 
            hasattr(request.user, 'telegram_id') and 
            request.user.telegram_id is not None
        )
        
        # Debug logging (remove in production)
        if settings.DEBUG:
            print(f"TelegramOnlyMiddleware Debug:")
            print(f"  Path: {request.path}")
            print(f"  User authenticated: {request.user.is_authenticated}")
            print(f"  Has telegram_id: {hasattr(request.user, 'telegram_id') if request.user.is_authenticated else 'N/A'}")
            print(f"  Telegram ID: {getattr(request.user, 'telegram_id', 'N/A') if request.user.is_authenticated else 'N/A'}")
            print(f"  Is Telegram WebApp: {is_telegram_webapp}")
            print(f"  Is Telegram Authenticated: {is_telegram_authenticated}")
            print(f"  User Agent: {user_agent[:100]}")
        
        # For API requests, return JSON error
        if request.path.startswith('/api/'):
            if not is_telegram_webapp and not is_telegram_authenticated:
                return JsonResponse({
                    'error': 'Access denied. This service is only available through Telegram Web App.',
                    'code': 'TELEGRAM_REQUIRED'
                }, status=403)
            return None
        
        # For regular page requests - allow if either from Telegram OR already authenticated
        if not is_telegram_webapp and not is_telegram_authenticated:
            # Return a page explaining that Telegram is required
            return HttpResponse(self.get_telegram_required_page(), content_type='text/html')
        
        # Allow access if from Telegram or already authenticated
        return None
    
    def get_telegram_required_page(self):
        """
        Return HTML page with button to open Telegram bot
        """
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to Gold Shop - Open in Telegram</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        .logo {
            width: 100px;
            height: 100px;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 30px;
            color: white;
            font-size: 50px;
            box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
        }
        h1 {
            color: #333;
            margin-bottom: 15px;
            font-size: 32px;
            font-weight: 700;
        }
        .subtitle {
            color: #666;
            font-size: 18px;
            margin-bottom: 30px;
            font-weight: 300;
        }
        p {
            color: #777;
            line-height: 1.6;
            margin-bottom: 20px;
            font-size: 16px;
        }
        .telegram-button {
            display: inline-block;
            background: linear-gradient(45deg, #0088cc, #0099dd);
            color: white;
            padding: 18px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 18px;
            margin: 30px 0;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(0, 136, 204, 0.3);
            position: relative;
            overflow: hidden;
        }
        .telegram-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 25px rgba(0, 136, 204, 0.4);
        }
        .telegram-button:before {
            content: '📱';
            margin-right: 10px;
            font-size: 20px;
        }
        .features {
            margin: 40px 0;
            text-align: left;
            background: #f8f9fa;
            padding: 25px;
            border-radius: 15px;
        }
        .feature {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        .feature:last-child {
            margin-bottom: 0;
        }
        .feature-icon {
            width: 24px;
            height: 24px;
            background: #4CAF50;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: white;
            font-size: 14px;
            font-weight: bold;
        }
        .feature-text {
            color: #555;
            font-weight: 500;
        }
        .download-link {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }
        .download-link a {
            color: #0088cc;
            text-decoration: none;
            font-weight: 500;
        }
        .download-link a:hover {
            text-decoration: underline;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .telegram-button:hover {
            animation: pulse 0.6s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">⌚</div>
        <h1>Gold Shop</h1>
        <p class="subtitle">Luxury Timepiece Collection</p>
        <p>Experience our exclusive watch collection through our secure Telegram platform.</p>
        
        <a href="https://t.me/gold_shop_development_bot" class="telegram-button">
            Open Gold Shop Bot
        </a>
        
        <div class="features">
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <div class="feature-text">Secure Telegram authentication</div>
            </div>
            <div class="feature">
                <div class="feature-icon">✨</div>
                <div class="feature-text">Personalized shopping experience</div>
            </div>
            <div class="feature">
                <div class="feature-icon">🔔</div>
                <div class="feature-text">Instant notifications and updates</div>
            </div>
            <div class="feature">
                <div class="feature-icon">💎</div>
                <div class="feature-text">Exclusive luxury timepiece collection</div>
            </div>
        </div>
        
        <div class="download-link">
            <p style="font-size: 14px; color: #999; margin: 0;">
                Don't have Telegram? <a href="https://telegram.org/" target="_blank">Download it here</a>
            </p>
        </div>
    </div>
</body>
</html>
        """
