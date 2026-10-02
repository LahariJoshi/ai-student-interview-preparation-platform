import asyncio
import subprocess
import sys
import selectors

print("Testing asyncio.to_thread with subprocess inside SelectorEventLoop...")

selector_loop = asyncio.SelectorEventLoop(selectors.SelectSelector())
try:
    async def run_in_selector():
        def sync_worker():
            p = subprocess.run(
                [sys.executable, "-c", "print('SELECTOR_THREAD_SUBPROCESS_WORKS')"],
                capture_output=True,
                text=True,
            )
            return p.stdout.strip()

        return await asyncio.to_thread(sync_worker)

    result = selector_loop.run_until_complete(run_in_selector())
    print("Result:", result)
    assert result == "SELECTOR_THREAD_SUBPROCESS_WORKS"
    print("SUCCESS: Subprocess in worker thread works seamlessly inside SelectorEventLoop!")
finally:
    selector_loop.close()
