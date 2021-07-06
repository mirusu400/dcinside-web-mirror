import dc_api
# 프로그래밍 갤러리 글 무한 크롤링
import asyncio
import dc_api
import json
_json = {}
async def run():
    global _json
    async with dc_api.API() as api:
        async for i in api.board(board_id="raycity", num=10):
            print(i.title)
            print(i.image_available)
        

asyncio.run(run())