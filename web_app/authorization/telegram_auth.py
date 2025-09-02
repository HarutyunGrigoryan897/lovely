import hashlib
import hmac
import json
from urllib.parse import unquote
from django.contrib.auth import login
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from authorization.models import CustomUser


def verify_telegram_web_app_data(init_data: str, bot_token: str) -> dict:

    try:
        # Parse the init data
        parsed_data = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                parsed_data[key] = unquote(value)
        
        # Extract hash and remove it from data for verification
        received_hash = parsed_data.pop('hash', '')
        
        # Sort the remaining data and create data-check-string
        data_check_arr = []
        for key in sorted(parsed_data.keys()):
            data_check_arr.append(f"{key}={parsed_data[key]}")
        data_check_string = '\n'.join(data_check_arr)
        
        # Create secret key from bot token
        secret_key = hmac.new("WebAppData".encode(), bot_token.encode(), hashlib.sha256).digest()
        
        # Calculate expected hash
        expected_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
        
        # Verify hash
        if not hmac.compare_digest(expected_hash, received_hash):
            return None
            
        # Parse user data
        user_data = json.loads(parsed_data.get('user', '{}'))
        return user_data
        
    except Exception as e:
        print(f"Error verifying Telegram data: {e}")
        return None


@method_decorator(csrf_exempt, name='dispatch')
class TelegramWebAppAuthView(View):
    """
    Handle Telegram Web App authentication
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            init_data = data.get('initData', '')
            
            if not init_data:
                return JsonResponse({'error': 'Missing initData'}, status=400)
            
            # Verify the Telegram Web App data
            user_data = verify_telegram_web_app_data(init_data, settings.BOT_TOKEN)
            
            if not user_data:
                return JsonResponse({'error': 'Invalid Telegram data'}, status=400)
            
            # Get existing user
            telegram_id = user_data.get('id')
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            username = user_data.get('username', f'tg_user_{telegram_id}')
            
            try:
                user = CustomUser.objects.get(telegram_id=telegram_id)
                
                # Update user info
                user.first_name = first_name
                user.last_name = last_name
                if not user.username.startswith('tg_user_'):
                    user.username = username
                user.save()
                
            except CustomUser.DoesNotExist:
                return JsonResponse({'error': 'User not found. Please contact administrator.'}, status=404)
            
            login(request, user)
            
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'telegram_id': user.telegram_id,
                    'is_telegram_user': True,
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CheckAuthStatusView(View):
    """
    Check if user is authenticated (works for both Telegram and regular users)
    """
    
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'telegram_id': getattr(request.user, 'telegram_id', None),
                    'is_telegram_user': bool(getattr(request.user, 'telegram_id', None)),
                }
            })
        else:
            return JsonResponse({'authenticated': False})


class UserInfoView(View):
    """
    Get current user information
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        
        user = request.user
        return JsonResponse({
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'telegram_id': getattr(user, 'telegram_id', None),
                'is_telegram_user': bool(getattr(user, 'telegram_id', None)),
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
            }
        })
