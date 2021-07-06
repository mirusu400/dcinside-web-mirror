import dc_api
# 프로그래밍 갤러리 글 무한 크롤링
import asyncio
import dc_api
import json
_json = {}
async def run():
    global _json
    async with dc_api.API() as api:
        _json = await api.gallery()
        

asyncio.run(run())
print(_json)
with open("gallerys.json", "w", encoding="utf-8") as f:
    json.dump(_json, f, ensure_ascii=False, indent=4)