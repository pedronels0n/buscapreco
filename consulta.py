import xml.etree.ElementTree as ET

def ler_xml(nome_arquivo):
    tree = ET.parse(nome_arquivo)
    root = tree.getroot()
    return root
def consultar_produto_por_sku(xml_root, sku):
    produto = xml_root.find(f".//produto[@sku='{sku}']")
    if produto is not None:
        descricao = produto.find('descricao').text
        complemento = produto.find('complemento').text
        embalagens = produto.findall('embalagem')
        codigos_barras = [emb.find('codigo_barra').text for emb in embalagens]

        return {
            'sku': sku,
            'descricao': descricao,
            'complemento': complemento,
            'codigos_barras': codigos_barras
        }
    else:
        return None
def consultar_produto_por_codigo_barra(xml_root, codigo_barra):
    for produto in xml_root.findall('produto'):
        for embalagem in produto.findall('embalagem'):
            if embalagem.find('codigo_barra').text == codigo_barra:
                codig_interno = produto.get('sku')
                descricao = produto.find('descricao').text
                complemento = produto.find('complemento').text
                
                return {
                    'codigo_interno': codig_interno,
                    'descricao': descricao,
                    'complemento': complemento,
                    'codigo_barra': codigo_barra
                }
    
    return None

# Exemplo de uso
if __name__ == '__main__':
    arquivo_xml = 'produtos.xml'  # Substitua pelo nome do seu arquivo XML
    xml_root = ler_xml(arquivo_xml)
    
    codigo_de_barras = '7896105181767'
    produto2 = consultar_produto_por_codigo_barra(xml_root, codigo_de_barras)
    if produto2:
        print(f"Codigo_Interno: {produto2['codigo_interno']}")
        print(f"Descrição: {produto2['descricao']}")
        print(f"Complemento: {produto2['complemento']}")
        print(f"Códigos de Barras: {', '.join(produto2['codigos_barras'])}")
    else:
        print(f"Produto com SKU {sku_produto} não encontrado.")