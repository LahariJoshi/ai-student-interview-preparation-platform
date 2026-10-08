import asyncio
import os
import sys

# Ensure backend in sys.path
sys.path.insert(0, os.path.abspath("backend"))

from app.modules.coding.services.evaluation_service import run_subprocess_sync

def test_minimal_subprocess():
    print("Testing minimal synchronous subprocess...")
    rc, stdout, stderr, timed_out, elapsed_ms = run_subprocess_sync(
        cmd=[sys.executable, "-c", "print('SUBPROCESS_OK')"],
        timeout_sec=5.0,
    )
    print(f"RC: {rc}, stdout: '{stdout.strip()}', stderr: '{stderr.strip()}', timed_out: {timed_out}, elapsed_ms: {elapsed_ms}")
    assert rc == 0
    assert stdout.strip() == "SUBPROCESS_OK"
    assert timed_out is False
    print("MINIMAL SUBPROCESS PASS!")

async def test_minimal_subprocess_async():
    print("Testing minimal subprocess via asyncio.to_thread...")
    rc, stdout, stderr, timed_out, elapsed_ms = await asyncio.to_thread(
        run_subprocess_sync,
        cmd=[sys.executable, "-c", "import sys; sys.stdout.write('ASYNC_THREAD_OK')"],
        timeout_sec=5.0,
    )
    print(f"Async RC: {rc}, stdout: '{stdout.strip()}', stderr: '{stderr.strip()}', timed_out: {timed_out}, elapsed_ms: {elapsed_ms}")
    assert rc == 0
    assert stdout.strip() == "ASYNC_THREAD_OK"
    assert timed_out is False
    print("ASYNC TO_THREAD SUBPROCESS PASS!")

if __name__ == "__main__":
    test_minimal_subprocess()
    asyncio.run(test_minimal_subprocess_async())
