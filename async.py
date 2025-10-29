import asyncio

async def step1():
    await asyncio.sleep(1)  # 模拟耗时操作
    print("step1 done")
    return "data1"

async def step2(data):
    await asyncio.sleep(1)
    print(f"step2 done with {data}")
    return "data2"

async def step3(data):
    await asyncio.sleep(1)
    print(f"step3 done with {data}")

async def main():
    result1 = await step1()
    result2 = await step2(result1)
    await step3(result2)

asyncio.run(main())
