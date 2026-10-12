import sys
import time
import requests

COUNT = 10

if len(sys.argv) != 2:
    print(f"Использование: python {sys.argv[0]} <URL>")
    sys.exit(1)

url = sys.argv[1]
times = []
total_bytes = 0

for i in range(COUNT):
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        data = response.content
    except requests.RequestException as error:
        print(f"Запрос {i + 1} не удался: {error}")
        sys.exit(1)

    elapsed = time.perf_counter() - start
    downloaded = len(data)
    times.append(elapsed)
    total_bytes += downloaded

    speed_mbps = downloaded * 8 / elapsed / 1_000_000
    print(
        f"{i + 1}: {downloaded / 1_000_000:.2f} MB за {elapsed:.2f} с "
        f"({speed_mbps:.2f} Мбит/с)"
    )

average_time = sum(times) / len(times)
average_bytes = total_bytes / COUNT
average_speed = average_bytes * 8 / average_time / 1_000_000

print(f"\nСреднее время запроса: {average_time:.2f} с")
print(f"Средний объём загрузки: {average_bytes / 1_000_000:.2f} MB")
print(f"Средняя скорость: {average_speed:.2f} Мбит/с")