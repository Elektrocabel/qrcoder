from multiprocessing import Pool, Manager
import pyqrcode
import fileinput
from time import sleep
from uploader import upload
import imgkit
import os


def generate(q, data):
    i = 0
    for s in data:
        i += 1
        img = pyqrcode.create(s)
        code = img.png_as_base64_str(scale=6)
        index_str = ''
        for line in fileinput.FileInput('index.html'):
            index_str += line.replace('{{ qr_code }}', code)
        filename = f'img{os.getpid()}-{i}.jpg'
        imgkit.from_string(index_str, filename)
        q.put(filename)


def send(q, count):
    for _ in range(count):
        sleep(1)
        filename = q.get()
        upload(filename)


if __name__ == '__main__':
    n = int(input('how many coupons do you need?\n'))
    coupons = []

    with open('data.txt', 'r') as f:
        for _ in range(n):
            coupon = f.readline()
            if coupon == '':
                raise ValueError('it is too many!')
            coupons.append(coupon)

    queue = Manager().Queue()

    pool = Pool(processes=3)

    pool.apply(generate, (queue, coupons[:n//2]))
    pool.apply(generate, (queue, coupons[n//2:]))

    pool.apply(send, (queue, n))

    pool.close()
    pool.join()
