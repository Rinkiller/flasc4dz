# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение должно сохраняться в отдельном файле,
# название которого соответствует названию изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
import sys
import requests
import threading
import multiprocessing
import asyncio
import time
from flask import Flask, render_template, redirect, request, url_for, flash, make_response


urls = [
'https://catalog-photo.ru/wp-content/uploads/2023/05/8-45Tv_vbbc-576x1024.jpg',
'https://catalog-photo.ru/wp-content/uploads/2023/05/AJwkJVLpirg-576x1024.jpg',
'https://catalog-photo.ru/wp-content/uploads/2023/05/eLpV9xqoOg-576x1024.jpg',
'https://catalog-photo.ru/wp-content/uploads/2023/05/GuWvEhcRhXk-576x1024.jpg',
'https://catalog-photo.ru/wp-content/uploads/2023/05/mJ-SzFgRlkc-576x1024.jpg',
'https://catalog-photo.ru/wp-content/uploads/2023/05/jZfhRh9nYkE-576x1024.jpg'
]
app = Flask(__name__)
app.secret_key = '77cd032d1d513c1c0efeaa6dbb71cf6d5b4b1a9b0139effcb3ed5125f9b0609e'
line_time = []
file_names = []


def sincron(urls):
    global line_time
    global file_names
    start_time = time.time()
    line_time.append(start_time)
    for url in urls:
        response = requests.get(url)
        filename = 'save/sync_' + url[ url.rfind("/") + 1: ]
        file_names.append(filename)
        with open(filename, "wb") as f:
            f.write(response.content) 
        line_time.append(time.time())
        print(f"Downloaded {url} in {line_time[len(line_time) - 1] - line_time[len(line_time) - 2]:.2f} seconds")
    print(f"Downloaded  all urls in {line_time[len(line_time) - 1] - start_time:.2f} seconds")

   
def load_url(url, start_time, index):
    global line_time
    global file_names
    response = requests.get(url)
    filename = f'save/{index}{url[ url.rfind("/") + 1: ]}'
    file_names.append(filename)
    with open(filename, "wb") as f:
        f.write(response.content)
    line_time.append(time.time())
    print(f"Downloaded {url} in {line_time[len(line_time) - 1] - line_time[len(line_time) - 2]:.2f} seconds")

def treades(urls):
    start_time = time.time()
    global line_time
    line_time.append(start_time)
    threads = []
    for url in urls:
        t = threading.Thread(target=load_url(url, start_time, 'thread_'))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(f"Downloaded  all urls in {time.time() - start_time:.2f} seconds")
 

def processing(urls):
    start_time = time.time()
    global line_time
    line_time.append(start_time)
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=load_url(url, start_time, 'process_'))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
    print(f"Downloaded  all urls in {time.time() - start_time:.2f} seconds")




async def load_url_as(url, start_time, index):
    global line_time
    global file_names
    response = requests.get(url)
    filename = f'save/{index}{url[ url.rfind("/") + 1: ]}'
    file_names.append(filename)
    with open(filename, "wb") as f:
        f.write(response.content)
    line_time.append(time.time())
    print(f"Downloaded {url} in {line_time[len(line_time) - 1] - line_time[len(line_time) - 2]:.2f} seconds")


async def async_met(urls):
    start_time = time.time()
    global line_time
    line_time.append(start_time)
    tasks = []
    for url in urls:
        task = asyncio.create_task(load_url_as(url, start_time, 'async_'))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Downloaded  all urls in {time.time() - start_time:.2f} seconds")

 


def results_canvas(metod):
    global urls
    global line_time
    global file_names
    file_names.append('ALL files')
    result_time_str = []
    for index in range(1,len(line_time)) :
        result_time_str.append(f'{line_time[index] - line_time[index - 1]:.2f}')
    result_time_str.append(f'{line_time[len(line_time) - 1] - line_time[0]:.2f}')
    dict_result = {}
    for index, file, time in zip(range(len(file_names)),  file_names , result_time_str):
        dict_result[index + 1] = [file, time]
    line_time = []
    file_names = []
    urls = [
        'https://catalog-photo.ru/wp-content/uploads/2023/05/8-45Tv_vbbc-576x1024.jpg',
        'https://catalog-photo.ru/wp-content/uploads/2023/05/AJwkJVLpirg-576x1024.jpg',
        'https://catalog-photo.ru/wp-content/uploads/2023/05/eLpV9xqoOg-576x1024.jpg',
        'https://catalog-photo.ru/wp-content/uploads/2023/05/GuWvEhcRhXk-576x1024.jpg',
        'https://catalog-photo.ru/wp-content/uploads/2023/05/mJ-SzFgRlkc-576x1024.jpg',
        'https://catalog-photo.ru/wp-content/uploads/2023/05/jZfhRh9nYkE-576x1024.jpg'
        ]
    return {'dict_result':dict_result, 'metod':metod}

@app.route('/',methods=['GET', 'POST'])
def root():
    context = {'urls': urls}
    return render_template('index.html', **context)

@app.route('/synch',methods=['GET', 'POST'])
def synchron_metod():   
    sincron(urls)
    return render_template('rezults.html', **results_canvas('синхронным'))

@app.route('/oner',methods=['GET', 'POST'])
def oner():
    context = {'urls': urls}
    return render_template('oner.html', **context)


@app.route('/s/<urlss>', methods=['GET', 'POST'])
def synchron_metod_atr(urlss):   
    if not urlss:
        print('нет данных')
        url_for('root')
    else:
        urls = urlss
        sincron(urls)
    return render_template('rezults.html', **results_canvas('синхронным'))

@app.route('/treades',methods=['GET', 'POST'])
def treades_metod():   
    treades(urls)
    return render_template('rezults.html', **results_canvas('многопоточным'))


@app.route('/t/<urlss>', methods=['GET', 'POST'])
def treades_metod_atr(urlss):   
    if not urlss:
        print('нет данных')
        url_for('root')
    else:
        urls = urlss
        treades(urls)
    return render_template('rezults.html', **results_canvas('многопоточным'))

@app.route('/processing',methods=['GET', 'POST'])
def processing_metod():   
    processing(urls)
    return render_template('rezults.html', **results_canvas('многопроцессорным'))


@app.route('/p/<urlss>', methods=['GET', 'POST'])
def processing_metod_atr(urlss):   
    if not urlss:
        print('нет данных')
        url_for('root')
    else:
        urls = urlss
        processing(urls)
    return render_template('rezults.html', **results_canvas('многопроцессорным'))

@app.route('/async',methods=['GET', 'POST'])
def async_metod():   
    async_met(urls)
    return render_template('rezults.html', **results_canvas('асинхронным'))


@app.route('/a/<urlss>', methods=['GET', 'POST'])
def async_metod_atr(urlss):   
    if not urlss:
        print('нет данных')
        url_for('root')
    else:
        urls = urlss
        async_met(urls)
    return render_template('rezults.html', **results_canvas('асинхронным'))

if __name__=="__main__":
    if len(sys.argv) > 2:
        urls = []
        index = 0
        for param in sys.argv:
            if index != 1 and index != 0:
                urls.append(param)
            index += 1
        if sys.argv[1] == 's': sincron(urls)
        elif sys.argv[1] == 't': treades(urls)
        elif sys.argv[1] == 'p': processing(urls)
        elif sys.argv[1] == 'a': asyncio.run(async_met(urls))
        else:
            app.run(debug=True)
    else:
        app.run(debug=True)
    

    # УКАЗАННЫЙ НИЖЕ КОД ПОЗВОЛЯЕТ ПРОВЕРИТЬ РАБОТУ МЕТОДОВ ОТДЕЛЬНО ВЫДАСТ РЕЗУЛЬТАТЫ ЗА КАЖДЫЙ ВАРИАНТ
    # Синхронный метод обработчика
    #sincron(urls)
    # for i in range(1,len(line_time)):
    #     print(f"file№{i} load time = {line_time[i] - line_time[i-1]:.2f}")
    # print(f"Downloaded  all urls in {line_time[len(line_time) - 1] - line_time[0]:.2f} seconds")

    #Мультипроцессорный метод обработчика
    #processing(urls)
    # for i in range(1,len(line_time)):
    #     print(f"file№{i} load time = {line_time[i] - line_time[i-1]:.2f}")
    # print(f"Downloaded  all urls in {line_time[len(line_time) - 1] - line_time[0]:.2f} seconds")

    #Многопоточный метод обработчика
    # treades(urls)
    # for i in range(1,len(line_time)):
    #     print(f"file№{i} load time = {line_time[i] - line_time[i-1]:.2f}")
    # print(f"Downloaded  all urls in {line_time[len(line_time) - 1] - line_time[0]:.2f} seconds")

    # Асинхронный метод обработчика
    # asyncio.run(async_met(urls))
    # for i in range(1,len(line_time)):
    #     print(f"file№{i} load time = {line_time[i] - line_time[i-1]:.2f}")
    # print(f"Downloaded  all urls in {line_time[len(line_time) - 1] - line_time[0]:.2f} seconds")