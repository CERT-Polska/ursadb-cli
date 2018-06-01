import json
import sys
import zmq
import terminal

ANSI = {
    'RED': '\x1b[31m',
    'GREEN': '\x1b[32m',
    'RESET': '\x1b[39m',
}

if len(sys.argv) < 2:
    HOST_URL = "tcp://localhost:9281"
elif len(sys.argv) == 2 and sys.argv[1] not in ['-h', '--help', '/?']:
    HOST_URL = sys.argv[1]
else:
    print('Usage: python ursaclient.py [host url]')
    print('Example:')
    print('    python ursaclient.py')
    print('    python ursaclient.py tcp://localhost:9281')
    sys.exit(1)

context = zmq.Context()
print("[ ] Connecting: {}".format(HOST_URL))

socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.RCVTIMEO, 1000)
socket.connect(HOST_URL)

socket.send('ping;')

while True:
    try:
        socket.recv()
    except zmq.error.Again as e:
        print("{}[!] Connection failed: {}{}".format(ANSI['RED'], str(e), ANSI['RESET']))
    else:
        break


progress_socket = context.socket(zmq.REQ)
progress_socket.connect(HOST_URL)


print("{}[+] Connected{}".format(ANSI['GREEN'], ANSI['RESET']))


def print_progress_bars():
    progress_socket.send('status;')
    result = json.loads(progress_socket.recv())
    tasks = [task for task in result.get('result', {}).get('tasks', [])
             if task.get('work_done') < task.get('work_estimated')]

    for task in tasks:
        frac = float(task['work_done']) / task['work_estimated']
        bar = '#' * int(20 * frac)
        bar = bar + (20 - len(bar)) * '.'
        print 'task {:4} {:3.2f}% [{}]'.format(task['id'], frac * 100, bar)


def do_query(query):
    if not query.endswith(';'):
        query += ';'
    socket.send(query)
    while True:
        try:
            res = json.loads(socket.recv())
            return res
        except Exception as e:
            print_progress_bars()


def main():
    while True:
        query = raw_input('> ').strip()
        res = do_query(query)

        if 'error' in res:
            print '{}ERR {}{}'.format(ANSI['RED'], res.get('error').get('message', '(no error provided)'), ANSI['RESET'])
        else:
            print '{}OK {}{}'.format(ANSI['GREEN'], res, ANSI['RESET'])

        for fname in res.get('result', {}).get('files', []):
            print fname

        print ''


if __name__ == '__main__':
    main()
