import asyncio
import time

COEFF = 0.001


async def land(plant, soaking_time, germination_time, survival_time):
    print(f'0 Beginning of sowing the {plant} plant')

    print(f"1 Soaking of the {plant} started")
    await asyncio.sleep(soaking_time * COEFF)
    print(f"2 Soaking of the {plant} is finished")

    print(f"7 Application of fertilizers for {plant}")
    await asyncio.sleep(3 * COEFF)
    print(f"7 Fertilizers for the {plant} have been introduced")

    print(f"8 Treatment of {plant} from pests")
    await asyncio.sleep(5 * COEFF)
    print(f"8 The {plant} is treated from pests")

    print(f"3 Shelter of the {plant} is supplied")
    await asyncio.sleep(COEFF * germination_time)

    print(f"4 Shelter of the {plant} is removed")
    print(f"5 The {plant} has been transplanted")
    await asyncio.sleep(survival_time * COEFF)

    print(f"6 The {plant} has taken root")
    print(f"9 The seedlings of the {plant} are ready")


async def sowing(*data):
    tasks = []
    for i in data:
        plant = i[0]
        soaking_time = i[1]
        germination_time = i[2]
        survival_time = i[3]
        tasks.append(asyncio.create_task(land(plant, soaking_time, germination_time, survival_time)))
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time.time()
    data = [('carrot', 7, 18, 2), ('cabbage', 2, 6, 10), ('onion', 5, 12, 7)]
    asyncio.run(sowing(*data))
    print(time.time() - t0)
