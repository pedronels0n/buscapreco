from app import app
from flask import render_template, request
import json
import urllib.request

#Rota INDEX - Pagina Principal 
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



#Rota BUSCAR - Pagina Secundaria
@app.route('/contato')
def contato():
    return render_template('contato.html')



#Rota BUSCAR - Pagina Secundaria
@app.route('/buscar', methods=['GET'])
#Criando funcao para receber o codigo enviado via GET
#da pagina Index.html
def buscador():

    codigo_barras = request.args.get('codigo_barras')
    
    #API para Codigo de Barras
    #Configuracao de API da Cosmos
    headers = {
          'X-Cosmos-Token': 'WN0U_hsymg5d1x8_7XKwDQ',
          'Content-Type': 'application/json',
          'User-Agent': 'Cosmos-API-Request'
      }

    req      = urllib.request.Request(f'https://api.cosmos.bluesoft.com.br/gtins/{codigo_barras}.json', None, headers)
    response = urllib.request.urlopen(req)
    data     = json.loads(response.read().decode('utf-8'))
    #Filtrando as informacoes Essenciais
    #para retonar ao Cliente
    descricao = data['description']
    foto = data['thumbnail']

    return render_template('buscar.html', descricao=descricao, codigo_barras=codigo_barras, foto=foto)

@app.route('/salvar_precos', methods=['POST'])
def salvar_preco():
    #Capturando dos dados do formulario
    codigo_barras = request.form.get('codigo_barras_hidden')
    preco_unitario = float(request.form.get('preco_unitario').replace(',', '.'))
    preco_atacado = float(request.form.get('preco_atacado').replace(',', '.'))
    descricao = request.form.get('descricao')


    print(f'Descricao:{descricao}')
    print(f'Codigo:{codigo_barras}')
    print(f'Unidade:{preco_unitario}')
    print(f'Atacado:{preco_atacado}')
    return render_template('index.html')