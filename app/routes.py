from app import app
from flask import render_template, request
import json
import urllib.request
import xml.etree.ElementTree as ET

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

@app.route('/salvar_precos', methods=['POST'])
def salvar_preco():
    #Capturando dos dados do formulario
    codigo_barras = str(request.form.get('codigo_barras_hidden'))
    codigo_interno = str(request.form.get('codigo_interno'))
    complemento = str(request.form.get('complemento'))
    preco_unitario = float(request.form.get('preco_unitario').replace(',', '.'))
    preco_atacado = float(request.form.get('preco_atacado').replace(',', '.'))
    descricao = str(request.form.get('descricao'))


    print(f'Descricao:{descricao}')
    print(f'SKU:{codigo_interno}')
    print(f'Complemento: {complemento}')
    print(f'Codigo:{codigo_barras}')
    print(f'Unidade:{preco_unitario}')
    print(f'Atacado:{preco_atacado}')
    return render_template('index.html')


#Rota para buscar o codigo de barras fornecido
@app.route('/codigo', methods=['GET'])
def consultar_produto_por_codigo_barra():
    #Utilizamos um arquivo xml como fonte de dados
    #para obter informacoes essenciais do produto
    codigo_barra = request.args.get('codigo_barras')
    tree = ET.parse('produtos.xml')
    xml_root = tree.getroot()
    for produto in xml_root.findall('produto'):
        for embalagem in produto.findall('embalagem'):
            if embalagem.find('codigo_barras').text == codigo_barra:
                codig_interno = produto.get('sku')
                descricao = produto.find('descricao').text
                complemento = produto.find('complemento').text
                
                return render_template('buscar.html', descricao=descricao, codigo_barras=codigo_barra, codigo_interno=codig_interno, complemento=complemento)
            #Caso nao contenha no arquivo
            #criamos uma contigencia utilizando 
            #uma api da cosmos para buscar a descricao do produto
            else:
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

                return render_template('buscar.html', descricao=descricao, codigo_barras=codigo_barras)
    return None