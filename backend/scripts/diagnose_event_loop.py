import asyncio
import sys

print("Python version:", sys.version)
print("Platform:", sys.platform)
policy = asyncio.get_event_loop_policy()
print("Policy:", type(policy).__name__)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
print("Loop:", type(loop).__name__)
try:
    async def test():
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", "print('SUBPROCESS_OK')",
            stdout=asyncio.subprocess.PIPE
        )
        out, _ = await proc.communicate()
        print("Asyncio Subprocess Output:", out.decode().strip())
    loop.run_until_complete(test())
except Exception as e:
    print("Asyncio Subprocess Failed:", type(e).__name__, e)
finally:
    loop.close()

# Also test uvicorn default event loop or selector loop
import selectors
selector_loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
try:
    async def test_selector():
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-c", "print('SUBPROCESS_OK')"
        )
        await proc.communicate()
    selector_loop.run_until_complete(test_selector())
except Exception as e:
    print("SelectorEventLoop Subprocess Failed (Expected):", type(e).__name__, e)
finally:
    selector_loop.close()
