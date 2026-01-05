import asyncio
from aade_publicity_search import AadeClient

async def main():
    client = AadeClient(
        username="username",
        password="password"
    )

    data = await client.get_vat_info("123456789")
    print(data)

asyncio.run(main())