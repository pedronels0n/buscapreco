from app import app
from flask import render_template, request, send_file
import json
import urllib.request
import xml.etree.ElementTree as ET
from .database import *
from datetime import date


#Rota INDEX - Pagina Principal 
@app.route('/')
def pricing():
    return render_template('pricing.html')

@app.route('/index',  methods=['POST'])
def index():
    mercado = request.form.get('supermercado')
    return render_template('index.html', mercado=mercado)



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
    mercado = str(request.form.get('mercado'))
    data = date.today()

    add_produto(codigo_barras, codigo_interno, descricao, complemento, preco_unitario, preco_atacado, data, mercado)


    print(f'Descricao:{descricao}')
    print(f'SKU:{codigo_interno}')
    print(f'Complemento: {complemento}')
    print(f'Codigo:{codigo_barras}') 
    print(f'Unidade:{preco_unitario}')
    print(f'Atacado:{preco_atacado}')
    print(f'Na data: {data}')
    print(f'Mercado:{mercado}')
    return render_template('index.html', mercado=mercado)


#Rota para buscar o codigo de barras fornecido
@app.route('/codigo', methods=['GET'])
def consultar_produto_por_codigo_barra():
    #Utilizamos um arquivo xml como fonte de dados
    #para obter informacoes essenciais do produto
    codigo_barras = request.args.get('codigo_barras')
    mercado = request.args.get('mercado')
    produto = consulta_produto(codigo_barras)
    if produto:
        codigo_barras = produto[0]
        codigo_interno = produto[1]
        descricao = produto[2]
        complemento = produto[3]
        preco = consulta_ultimo_preco(mercado, codigo_barras)
        preco_unitario = preco[4]
        preco_atacado = preco[5]
        return render_template('buscar.html', descricao=descricao, codigo_barras=codigo_barras, codig_interno=codigo_interno , complemento=complemento, mercado=mercado, preco_unitario=preco_unitario, preco_atacado=preco_atacado)
    
    #API para Codigo de Barras
    #Configuracao de API da Cosmos
    headers ={
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

    return render_template('buscar.html', descricao=descricao, codigo_barras=codigo_barras, mercado=mercado)




@app.route('/pricing')
@app.route('/pricing.html')
def mercado():
    return render_template('pricing.html')
#Lista de produtos inseridos no baanco

@app.route('/produtos')
def listar_produtos():
    produtos = obter_produtos()

    if produtos:
        return render_template('produtos.html', produtos=produtos)
    else:
        return "Nenhum produto encontrado."

@app.route('/relatorio')
def relatorios():
    return render_template('relatorio.html')

@app.route('/export_excel', methods=['POST'])
def excel():
    mercado = request.form.get('mercado')
    pricing = obter_excel(mercado)
    data = date.today()
    return send_file(pricing, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=(f'Pesquisa {mercado}_{data}.xlsx'))

@app.route('/limpar/<nome_tabela>')
def limpar_tabela(nome_tabela):
    limpar_dados(nome_tabela)
    return f'Tabela {nome_tabela} limpa'


