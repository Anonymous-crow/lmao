import asyncio

def async_loop(f):
    loop = asyncio.get_event_loop()
    def decorated(*args, **kwargs):
        loop.run_until_complete(f(*args, **kwargs))
    return decorated

class Async:
    @async_loop
    async def function(self, word):
        print(word)
        await asyncio.sleep(1.0)

a=Async()
a.function("hello_world")
