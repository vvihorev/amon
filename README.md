# amon
 
Single page sidecar to throw your real-time charts at.

![image](https://github.com/user-attachments/assets/ee768a5b-5095-4789-8648-0e317e61cff6)

1. Build and run the `amon` container.

```bash
docker build . -t amon
docker run -d --name=amon -p 8000:8000 amon
```

2. Open the `amon` home page in a browser: http://localhost:8000

3. Use the `Amon` class to create charts and push data to them from your python code.

Run and see `example.py` for more details.

