import os
import sqlite3


def inicializar_db():
    db_file = 'banco.db'

# Verificar se o arquivo existe
    if os.path.exists(db_file):
        print(f'O banco de dados {db_file} existe.')
    else:
        banco = sqlite3.connect('banco.db')
        cursor = banco.cursor()
        cursor.execute("""
                       CREATE TABLE produtos (
                       codigo INTEGER PRIMARY KEY,
                       sku INTEGER,
                       descricao TEXT,
                       complemento TEXT,
                       preco_unitario REAL,
                       preco_atacado REAL
                       )
                       """)
        
        cursor.execute("""
                       CREATE TABLE pesquisa (
                       codigo INTEGER PRIMARY KEY,
                       sku INTEGER,
                       descricao TEXT,
                       complemento TEXT,
                       preco_unitario REAL,
                       preco_atacado REAL
                       )
                       """)
        
        banco.commit()
        cursor.close()
        print(f'o Banco de dados foi criado: {db_file}')


def add_produto(codigo_barras, codigo_interno, descricao, complemento, preco_unitario, preco_atacado):
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Consulta para contar o número de registros com o mesmo código de barras
    cursor.execute("SELECT 1 FROM pesquisa WHERE codigo = ?", (codigo_barras,))
    resultado = cursor.fetchone()
    # Verifica se o resultado é maior que zero (ou seja, já existe um produto com esse código)
    if resultado:
        cursor.execute("""
                UPDATE pesquisa
                SET descricao = ?,
                    complemento = ?,
                    preco_unitario = ?,
                    preco_atacado = ?
                WHERE codigo = ?
            """, (descricao, complemento, preco_unitario, preco_atacado, codigo_barras))
            
            # Confirmar a transação de atualização
        banco.commit()
        print(f"Já existe um produto com código de barras {codigo_barras}.")
        print(f"Dados do produto com código {codigo_barras} atualizados com sucesso.")
    else:
        cursor.execute("""
                       INSERT INTO pesquisa (codigo, sku, descricao, complemento, preco_unitario, preco_atacado)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, (codigo_barras, codigo_interno, descricao, complemento, preco_unitario, preco_atacado))
        banco.commit()
        print(f"Produto: {codigo_barras}, inserido com sucesso.") 
    #ENCERRANDO CONEXOES
    cursor.close()
    banco.close()