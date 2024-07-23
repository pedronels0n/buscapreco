import os
import sqlite3
from datetime import date
import pandas as pd
from app import app

def inicializar_db():
    db_file = 'banco.db'

# Verificar se o arquivo existe
    if os.path.exists(db_file):
        banco = sqlite3.connect('banco.db')
        cursor = banco.cursor()
        print(f'O banco de dados {db_file} existe.')
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS pesquisa (
                       codigo INTEGER PRIMARY KEY,
                       sku INTEGER,
                       descricao TEXT,
                       complemento TEXT,
                       preco_unitario REAL,
                       preco_atacado REAL,
                       pricing TEXT,
                       data TEXT
                       )
                       """)
        banco.commit()
        cursor.close()
        banco.close()
        
        
    else:
        banco = sqlite3.connect('banco.db')
        cursor = banco.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS produtos (
                       codigo INTEGER PRIMARY KEY,
                       sku INTEGER,
                       descricao TEXT,
                       complemento TEXT
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE pesquisa (
                       codigo INTEGER PRIMARY KEY,
                       sku INTEGER,
                       descricao TEXT,
                       complemento TEXT,
                       preco_unitario REAL,
                       preco_atacado REAL,
                       pricing TEXT,
                       data TEXT
                       )
                       """)
        
        banco.commit()
        cursor.close()
        print(f'o Banco de dados foi criado: {db_file}')


def add_produto(codigo_barras, codigo_interno, descricao, complemento, preco_unitario, preco_atacado, data, pricing):
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Consulta para contar o número de registros com o mesmo código de barras
    cursor.execute(f"SELECT * FROM {pricing} WHERE codigo = ?", (codigo_barras,))
    resultado = cursor.fetchone()
    # Verifica se o resultado é maior que zero (ou seja, já existe um produto com esse código)
    if resultado is not None:
        cursor.execute(f"""
                UPDATE {pricing}
                SET descricao = ?,
                    sku = ?,
                    complemento = ?,
                    preco_unitario = ?,
                    preco_atacado = ?,
                    data = ?,
                    pricing = ?
                WHERE codigo = ?
            """, (descricao, codigo_interno, complemento, preco_unitario, preco_atacado, data, pricing, codigo_barras))
            
            # Confirmar a transação de atualização
        banco.commit()
        print(f"Já existe um produto com código de barras {codigo_barras}.")
        print(f"Dados do produto com código {codigo_barras} atualizados com sucesso.")
    else:
        cursor.execute(f"""
                       INSERT INTO {pricing} (codigo, sku, descricao, complemento, preco_unitario, preco_atacado, data, pricing)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (codigo_barras, codigo_interno, descricao, complemento, preco_unitario, preco_atacado, data, pricing))
        banco.commit()
        print(f"Produto: {codigo_barras}, inserido com sucesso.") 
    #ENCERRANDO CONEXOES
    cursor.close()
    banco.close()


def consulta_produto(codigo_barras):
        banco = sqlite3.connect('banco.db')
        cursor = banco.cursor()

        cursor.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
        produto = cursor.fetchone()  # Recupera o primeiro (e único) registro
        cursor.close()
        banco.close()

        return produto

def consulta_ultimo_preco(tabela, codigo_barras):
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()
    cursor.execute(f"SELECT * FROM {tabela} WHERE codigo = {codigo_barras}")
    produto = cursor.fetchone()
    cursor.close()
    banco.close()
    if produto is not None:
        print(produto[4], produto[5])
        return produto
    else:
        produto = [0, 0, 0, 0, 0, 0]
        return produto

def obter_produtos():
    conn = sqlite3.connect('banco.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pesquisa")
    produtos = cursor.fetchall()  # Recupera todos os registros
    cursor.close()
    conn.close()
    return produtos


def obter_excel(mercado):
    EXPORTS_DIR = os.path.join(app.root_path, 'exports')
    
    if not os.path.exists(EXPORTS_DIR):
        os.makedirs(EXPORTS_DIR)
     
    banco = sqlite3.connect('banco.db')
    df = pd.read_sql_query(f'SELECT * FROM {mercado}', banco)
    
    data = date.today()
    os.path.join(EXPORTS_DIR, f'Pesquisa_{mercado}_{data}.xlsx')
    excel_file = os.path.join(EXPORTS_DIR, f'Pesquisa_{mercado}_{data}.xlsx')
    df.to_excel(excel_file, index=False, engine='openpyxl')
    banco.close()
    return excel_file

def limpar_dados(nome_tabela):
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()
    cursor.execute(f'DELETE FROM {nome_tabela}')
    banco.commit()
    cursor.close()
    banco.close()


    



