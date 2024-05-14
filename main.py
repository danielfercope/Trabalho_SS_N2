import pymysql
from pymysql import Error
from flask import Flask, jsonify, request, send_file
import random
import json
from flask_cors import CORS
import time
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)
CORS(app)


def conectar_bd():
    try:
        conexao = pymysql.connect(
            host='localhost',
            user='root',
            password='admin123',
            database='banco'
        )
        print("Conexão ao banco de dados MySQL bem-sucedida")
        return conexao
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def fisher_yates(arr):
    n = len(arr)
    for i in range(n - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]


def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


@app.route('/create-array', methods=['POST'])
def create_array():
    start_time = time.time()
    array = []
    for i in range(50000):
        array.append(i)
    fisher_yates(array)

    conexao = conectar_bd()
    if conexao:
        cursor = conexao.cursor()
        try:
            array_json = json.dumps(array)
            comando = "INSERT INTO array (array_value) VALUES (%s)"
            cursor.execute(comando, (array_json,))
            conexao.commit()
        except Error as e:
            print(f"Erro ao executar o comando SQL: {e}")
        finally:
            cursor.close()
            conexao.close()

    end_time = time.time()
    execution_time = end_time - start_time
    return jsonify({'array': array, 'execution_time': execution_time})


@app.route('/ordenar-array', methods=['GET'])
def ordenar_array():
    start_time = time.time()
    conexao = conectar_bd()
    if conexao:
        cursor = conexao.cursor()
        try:
            comando = f'SELECT array_value FROM array;'
            cursor.execute(comando)
            array_randomizado = cursor.fetchall()

            array = [json.loads(item[0]) for item in array_randomizado]

            for arr in array:
                quick_sort(arr)

            array_ordenado_json = [json.dumps(arr) for arr in array]
            print(array_ordenado_json)

            end_time = time.time()
            execution_time = end_time - start_time

            return jsonify({'array_ordenado': array_ordenado_json, 'execution_time': execution_time})
        except Error as e:
            print(f"Erro ao executar o comando SQL: {e}")
        finally:
            cursor.close()
            conexao.close()

    return jsonify({'mensagem': 'Erro ao recuperar e ordenar o array.'})

def generate_scatter_plot(data):
    numbers = [int(num.strip()) for num in data.split(',') if num.strip()]
    x = np.arange(len(numbers))
    y = numbers
    plt.scatter(x, y)
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Gráfico de Dispersão')
    plt.grid(True)
    plt.tight_layout()

def generate_line_chart(data):
    numbers = [int(num.strip()) for num in data.split(',') if num.strip()]
    x = np.arange(len(numbers))
    y = numbers
    plt.plot(x, y)
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Gráfico de Linhas')
    plt.grid(True)
    plt.tight_layout()

def generate_bar_chart(data):
    numbers = [int(num.strip()) for num in data.split(',') if num.strip()]
    x = np.arange(len(numbers))
    y = numbers
    plt.bar(x, y)
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Gráfico de Barras')
    plt.grid(True)
    plt.tight_layout()

def generate_bubble_chart(data):
    numbers = [int(num.strip()) for num in data.split(',') if num.strip()]
    x = np.arange(len(numbers))
    y = numbers
    sizes = np.random.randint(10, 100, size=len(numbers))
    plt.scatter(x, y, s=sizes)
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Gráfico de Bolhas')
    plt.grid(True)
    plt.tight_layout()

def generate_dot_plot(data):
    numbers = [int(num.strip()) for num in data.split(',') if num.strip()]
    x = np.arange(len(numbers))
    y = numbers
    plt.plot(x, y, marker='o', linestyle='')
    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Gráfico de Pontos')
    plt.grid(True)
    plt.tight_layout()

@app.route('/gerar-grafico', methods=['POST'])
def gerar_grafico():
    data = request.json
    numbers = data['numbers']
    chart_type = data['chartType']

    if chart_type == 'scatter':
        generate_scatter_plot(numbers)
    elif chart_type == 'line':
        generate_line_chart(numbers)
    elif chart_type == 'bar':
        generate_bar_chart(numbers)
    elif chart_type == 'bubble':
        generate_bubble_chart(numbers)
    elif chart_type == 'dot':
        generate_dot_plot(numbers)
    else:
        return jsonify({'error': 'Tipo de gráfico não suportado'}), 400

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)
    plt.close()

    return send_file(img_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
