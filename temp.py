import json
import time

import httpx

start_time = time.perf_counter()
x = httpx.post(
    url="http://localhost:11434/api/chat",
    timeout=60,
    json={
        "model": "qwen3:4b",
        "options": {
            # "num_ctx": 5,
        },
        "messages": [
            {
                "role": "user",
                "content": "write me a haiku about rubiks cubes",
            }
        ],
        "stream": False,
    },
)
end_time = time.perf_counter()

print(
    json.dumps(
        x.json(),
        indent=4,
    )
)

print(f"seconds elapsed: {end_time-start_time}")
