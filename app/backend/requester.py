from datetime import datetime
import json
import aiohttp

from app.common.constants import TELEGRAM_SENDER_HOST, TELEGRAM_SENDER_PORT
from app.backend.response import Response


class Requester:
    def __init__(self):
        self.sender_url = f"http://{TELEGRAM_SENDER_HOST}:{TELEGRAM_SENDER_PORT}"
        
    async def _post(self, url: str, data: dict) -> Response:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as response:
                status = response.status
                text = await response.text()
        return Response(status, text)

    async def _delete(self, url: str) -> Response:
        async with aiohttp.ClientSession() as session:
            async with session.delete(url=url) as response:
                status = response.status
                print(status)
                text = await response.text()
        return Response(status, text)

    async def send_notification_post(
        self, 
        deed_id: int, 
        telegram_id: int,
        deed_name: str,
        deed_time: datetime
    ) -> Response:
        url = self.sender_url + f"/notifications/{deed_id}/"
        data = {
            'telegram_id': telegram_id,
            'deed_name': deed_name,
            'deed_time': deed_time,
        }
        response = await self._post(url, data)
        return response

    async def send_notifocation_delete(
        self,
        deed_id
    ) -> Response:
        print('hi!')
        url = self.sender_url + f"/notifications/{deed_id}/"
        response = await self._delete(url)
        return response
