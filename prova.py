import asyncio

async def task_a():
    print("A")
    await asyncio.sleep(2)
    print("A dopo 2 secondi")


async def task_b():
    print("B")
    await asyncio.sleep(1)
    print("B dopo 1 secondo")


async def main():
    
    await asyncio.create_task(task_a())
    await asyncio.create_task(task_b())


asyncio.run(main())