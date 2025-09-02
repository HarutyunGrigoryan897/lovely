import logging
import aiohttp
from config import API_SECRET, API_URL

logging.basicConfig(level=logging.INFO)

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