import logging
import aiohttp
from config import API_SECRET, API_URL

logging.basicConfig(level=logging.INFO)

async def check_is_admin(telegram_id: int) -> bool:
    """Send request to Django backend and check if user is admin"""
    headers = {"Authorization": f"Bearer {API_SECRET}"}
    async with aiohttp.ClientSession() as session:
        try:
            url = f"{API_URL}api/auth/check-admin/?telegram_id={telegram_id}"
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("is_admin", False)
                else:
                    error_text = await resp.text()
                    logging.error(f"Check admin error {resp.status}: {error_text}")
                    return False
        except Exception as e:
            logging.error(f"Admin check request failed: {e}")
            return False
        
async def get_admins_from_django():
    url = f"{API_URL}api/auth/all-admins/"
    headers = {"Authorization": f"Bearer {API_SECRET}"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"Failed to fetch admins: {response.status} {await response.text()}")
                return []

async def create_user_in_django(user_data: dict):
    headers = {"Authorization": f"Bearer {API_SECRET}"}
    async with aiohttp.ClientSession() as session:
        try:
            print(headers)
            url = f"{API_URL}api/auth/users/"
            async with session.post(url, json=user_data, headers=headers) as resp:
                if resp.status == 201:
                    return await resp.json()
                else:
                    error_text = await resp.text()
                    logging.error(f"Django API error {resp.status}: {error_text}")
                    return None
        except Exception as e:
            logging.error(f"Request failed: {e}")
            return None
        
async def get_user_info(telegram_id):
    headers = {"Authorization": f"Bearer {API_SECRET}"}
    async with aiohttp.ClientSession() as session:
        try:
            url = f"{API_URL}api/auth/user-info/"
            async with session.get(f"{url}?telegram_id={telegram_id}", headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, list):
                        return data[0] if data else None
                    return data
                else:
                    error_text = await resp.text()
                    logging.error(f"Django API error {resp.status}: {error_text}")
                    return None
        except Exception as e:
            logging.error(f"Request failed: {e}")
            return None

async def update_user_status(telegram_id: int, approve: bool):
    url = f"{API_URL}api/auth/user-{'approve' if approve else 'reject'}/{telegram_id}/"
    headers = {"Authorization": f"Bearer {API_SECRET}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            return response.status == 200