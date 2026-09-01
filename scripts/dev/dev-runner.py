import subprocess, os, time, urllib.request, sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(ROOT_DIR)

# 1. Ensure docker compose postgres is up
try:
    subprocess.run(['docker', 'compose', '-f', 'docker-compose.dev.yml', 'up', '-d'], check=True)
    print('PostgreSQL docker container is up.')
except Exception as e:
    print('Docker warning:', e)

# 2. Backend Server on PORT 3001
print('1. Starting Backend Server on PORT 3001...')
server_dir = os.path.join(ROOT_DIR, 'server')
s_proc = subprocess.Popen(
    ['node', '--env-file=.env', 'dist/main.js'],
    cwd=server_dir,
    stdout=open(os.path.join(ROOT_DIR, 'server.log'), 'w'),
    stderr=subprocess.STDOUT
)
print('Backend spawned, PID:', s_proc.pid)

# 3. Frontend Client on PORT 5173
print('2. Starting Frontend Client on PORT 5173...')
client_dir = os.path.join(ROOT_DIR, 'client')
vite_bin = os.path.join(client_dir, 'node_modules', '.bin', 'vite.cmd')
c_proc = subprocess.Popen(
    [vite_bin, '--host', '--port', '5173'],
    cwd=client_dir,
    stdout=open(os.path.join(ROOT_DIR, 'client.log'), 'w'),
    stderr=subprocess.STDOUT
)
print('Frontend spawned, PID:', c_proc.pid)

# 4. Wait for backend to be ready
print('3. Waiting for Backend to be ready...')
for i in range(25):
    time.sleep(1)
    try:
        req = urllib.request.Request('http://127.0.0.1:3001/api/v1/auth/setup-status')
        with urllib.request.urlopen(req, timeout=2) as resp:
            if resp.status == 200:
                print(f'Backend Ready at second {i+1}!')
                break
    except Exception:
        pass

# 5. Verify Frontend & Proxied API
time.sleep(2)
try:
    with urllib.request.urlopen('http://localhost:5173/', timeout=5) as resp:
        print(f'Frontend UI is LIVE at http://localhost:5173/ (HTTP {resp.status})')
except Exception as e:
    print('Frontend UI check:', e)

try:
    with urllib.request.urlopen('http://localhost:5173/api/v1/auth/setup-status', timeout=5) as resp:
        print(f'Proxied API via Frontend: HTTP {resp.status}')
except Exception as e:
    print('Frontend Proxied API check:', e)

print('\n===================================================')
print(' CAO SACH LOCAL DEV DA SAN SANG!')
print(' -> Truy cap: http://localhost:5173')
print('===================================================\n')
sys.stdout.flush()

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    print('\nStopping dev servers...')
    s_proc.terminate()
    c_proc.terminate()

