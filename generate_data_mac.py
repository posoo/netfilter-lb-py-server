import os
import subprocess

DATA_DIR = 'data'

for i in range(10, 31):
    _size_in_bytes = 1 << i
    _bs = ''
    _cnt = -1
    _output_file = os.path.join(DATA_DIR, f'{_size_in_bytes}.bin')
    if _size_in_bytes < (16 << 10):
        _bs = '1k'
        _cnt = _size_in_bytes // (1 << 10)
    elif (16 << 10) <= _size_in_bytes < (1 << 20):
        _bs = '16k'
        _cnt = _size_in_bytes // (16 << 10)
    else:
        _bs = '1m'
        _cnt = _size_in_bytes // (1 << 20)

    subprocess.run([
        'dd',
        'if=/dev/urandom',
        f'of={_output_file}',
        f'bs={_bs}',
        f'count={_cnt}'
    ])

