import xml.etree.ElementTree as ET
import sqlite3

def ler_xml(nome_arquivo):
    tree = ET.parse(nome_arquivo)
    root = tree.getroot()
    return root

def inicializar_banco():
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        
        # Criar tabela produtos se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                codigo_barras TEXT PRIMARY KEY,
                sku TEXT,
                descricao TEXT,
                complemento TEXT
            )
        ''')
        
        conn.commit()
        return conn, cursor
    
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        return None, None

def adicionar_produto(conn, cursor, sku, descricao, complemento, codigos_barras):
    try:
        for codigo in codigos_barras:
            cursor.execute('''
                INSERT INTO produtos (codigo_barras, sku, descricao, complemento)
                VALUES (?, ?, ?, ?)
            ''', (codigo, sku, descricao, complemento))
        
        conn.commit()
        print(f"Produtos adicionados com sucesso para o SKU {sku}")
    
    except sqlite3.IntegrityError:
        print(f"Erro: código de barras duplicado para o SKU {sku}. Ignorando inserção.")
    
    except sqlite3.Error as e:
        print(f"Erro ao inserir produtos: {e}")
        conn.rollback()


# Exemplo de uso
if __name__ == '__main__':
    arquivo_xml = 'produtos.xml'  # Substitua pelo nome do seu arquivo XML
    xml_root = ler_xml(arquivo_xml)
    
    conn, cursor = inicializar_banco()
    
    if conn and cursor:
        try:
            for produto in xml_root.findall('produto'):
                sku = produto.get('sku')
                descricao = produto.find('descricao').text
                complemento = produto.find('complemento').text
                codigos_barras = [emb.find('codigo_barra').text for emb in produto.findall('embalagem')]
                
                adicionar_produto(conn, cursor, sku, descricao, complemento, codigos_barras)
        
        except Exception as e:
            print(f"Erro ao processar XML ou inserir produtos: {e}")
        
cursor.close()

conn.close()