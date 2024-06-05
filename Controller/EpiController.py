from datetime import datetime
import delta_sharing
from Config.GuardianLog import GuardianLog, Tipo
from Config.Service_Config import ServiceConfig
from DAO import EpiDAO
from Guardian import ConexaoPortal
from Guardian.Guardian_LogTxt import Guardian_LogTxt
import pyodbc
from decimal import Decimal
import pandas as pd

class EpiController:
    def __init__(self):
        self._epi_dao = EpiDAO()
        self._status = "E"
        self._erro = ""
        self._nome = "GM_Upl_insertEPIGM"
        self._sigla = "EGMINS"

    @property
    def nome(self):
        return self._nome

    @property
    def sigla(self):
        return self._sigla
    
def Executar():
    from Service.Main import Main

    main = Main()
    try:
        if main.RegistroRotina == "R":
            GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Iniciado, main.IdProcessamento, "")

        # limparTabela()

        chaves_locais = buscar_epi_local()
        
        lista_retornada = PegarRegistros()

        # Filtrar os dados cuja chave não está na lista de chaves
        nova_lista = []
        # Iterar sobre cada tupla em dados
        for dado in lista_retornada:
            # dado[0] é a chave, dado[1] é o valor
            chave = dado[11][1] 
            if chave not in chaves_locais:
                nova_lista.append(dado)
            else:
                print(f"local: {dado[11]}")  # Mostrar o que está sendo excluído
        xml_result = list_to_xml(lista_retornada)

        # Conexao com o banco
        servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
        connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'
        # Cria um cursor a partir da conexão
        connection = pyodbc.connect(connection_string)
        try:
            # Loop para inserir cada linha no SQL Server
            for valores_da_linha in nova_lista:
                xmlEntradaOrigem = "#rs-data-sharing.rsdata.estoque_epi_por_filial"
                xmlRespOrigem = xml_result
                idfilial = valores_da_linha[0][1]
                descricaoFilial = valores_da_linha[1][1]
                idLocalEstoque = valores_da_linha[2][1]
                descricaoLocal = valores_da_linha[3][1]
                idProduto = valores_da_linha[4][1]
                idItem = valores_da_linha[5][1]
                codTamanho = valores_da_linha[7][1]
                descItem = valores_da_linha[6][1]       
                quantidade = valores_da_linha[8][1] if valores_da_linha[8][1] != None else Decimal('0.000000')
                dtMovimento = valores_da_linha[10][1] 
                DataEntradaMidd = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

                sql_insert = f'''INSERT INTO insertEstoqueEntrada 
                            (idFilial, descricaoFilial, idLocalEstoque, 
                            descricaoLocal, idProduto, idItem, codTamanho,
                            descItem, quantidade, dtMovimento, DataEntradaMidd, 
                            DataSaidaMidd, Reenvios, DataReenvio, 
                            rsExp, codEmpresa, codFilial,
                            cnpjCliente, status, idProc,
                            xmlEntradaOrigem, xmlRespOrigem, xmlEntradaDestino, xmlRespDestino)
                            VALUES 
                            ('{idfilial}', '{descricaoFilial}', '{idLocalEstoque}', 
                            '{descricaoLocal}', '{idProduto}', '{idItem}', '{codTamanho}',
                            '{descItem}', {quantidade}, '{dtMovimento}', '{DataEntradaMidd}', 
                            '', {0}, '', 
                            '', '{idfilial}', '{idLocalEstoque}',
                            '', '', {main.IdProcessamento}, 
                            '{xmlEntradaOrigem}', CONVERT(varbinary(MAX),'{xmlRespOrigem}'), '', '')'''
                
                # Cria um cursor a partir da conexão
                cursor = connection.cursor()
                # Execute a consulta SQL com parâmetros para o INSERT
                cursor.execute(sql_insert)
                # Confirme as alterações no banco de dados
                connection.commit() 
                
        except Exception as ex:
            GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, f"Erro na query de insert: {str(sql_insert)}", str(ex), ex.args[0], main.IdProcessamento, "")
        finally:
            # Fechar o cursor e a conexão
            if(len(nova_lista) != 0):
                cursor.close()
                connection.close()

        if main.RegistroRotina == "R":
            GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Finalizado, main.IdProcessamento, "")

    except Exception as ex:
        Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao salvar os registros vindos do GM.", str(ex), ex.args[0], main.IdProcessamento, "")

def PegarRegistros():
    from Service.Main import Main

    FILE = 'configDataBricks.share'
    try:
        client = delta_sharing.SharingClient(FILE)

        shares = client.list_shares()

        for share in shares:
            schemas = client.list_schemas(share)
            for schema in schemas:
                tables = client.list_tables(schema)
                for table in tables:
                    print(f'name = {table.name}, share = {table.share}, schema = {table.schema}')

        print(client.list_all_tables())

        # Definindo as variáveis datainicio e datafim
        # datainicio = "2016-06-16 00:00:00"
        # df = delta_sharing.load_table_changes_as_pandas(f"{FILE}#rs-data-sharing.rsdata.estoque_epi_por_filial", starting_timestamp='2024-05-29T00:00:00Z')
        #df = delta_sharing.load_as_pandas(f"{FILE}#rs-data-sharing.rsdata.estoque_epi_por_filial", timestamp='2024-05-29T10:38:54Z')
        df = delta_sharing.load_as_pandas(f'{FILE}#rs-data-sharing.rsdata.estoque_epi_por_filial')

        # Definir os critérios de filtragem
        quantidade_min = 0.000
        empresa_filtro = 2
        id_filial_filtro = 20        # Exemplo de id_filial a ser filtrado

        data_atual = datetime.now()
        data_entrada = data_atual.strftime('%Y-%m-%d')
        #data_entrada = "2024-06-04"

        # Verificar se as colunas necessárias estão presentes no DataFrame
        colunas_necessarias = ['qtde_entrada', 'dataentrada', 'empresa', 'id_filial']
        if all(col in df.columns for col in colunas_necessarias):
            # Converter a coluna 'dataentrada' para o tipo datetime
            df['dataentrada'] = pd.to_datetime(df['dataentrada'], errors='coerce')

            # Remover linhas onde 'dataentrada' é NaT
            df = df.dropna(subset=['dataentrada'])

            # Filtrar a coluna 'dataentrada' para a data específica (considerando apenas a data, ignorando a hora)
            filtered_df = df[df['dataentrada'].dt.date == pd.to_datetime(data_entrada).date()]

            # Filtrar a coluna 'empresa' pelo valor específico
            filtered_df = filtered_df[filtered_df['empresa'] == empresa_filtro]

            # Filtrar a coluna 'id_filial' pelo valor específico
            filtered_df = filtered_df[filtered_df['id_filial'] == id_filial_filtro]

            # Filtrar a coluna 'quantidade' para valores maiores que 0.000
            filtered_df = filtered_df[filtered_df['qtde_entrada'] > quantidade_min]
        # Especificando o caminho do arquivo CSV - completo
        csv_path = 'exportar\exp.csv'
        # Salvando o DataFrame como um arquivo CSV - completo
        df.to_csv(csv_path, index=False)

        # Especificando o caminho do arquivo CSV - filtrado
        csv_path = 'exportar\expFiltrado.csv'
        # Salvando o DataFrame como um arquivo CSV - filtrado
        filtered_df.to_csv(csv_path, index=False)

        # Convertendo o DataFrame para uma string - completo
        df_string = df.to_string(index=False)
        # Especificando o caminho do arquivo de texto - completo
        txt_path = 'exportar\exp.txt'

        # Salvando a string em um arquivo de texto
        with open(txt_path, 'w') as file:
            file.write(df_string)

        # Convertendo o DataFrame para uma string - filtrado
        df_string = filtered_df.to_string(index=False)
        # Especificando o caminho do arquivo de texto - filtrado
        txt_path = 'exportar\expFiltrado.txt'

        # Salvando a string em um arquivo de texto
        with open(txt_path, 'w') as file:
            file.write(df_string)

        lista_de_novos_valores = []
        # Loop pelas linhas e colunas do DataFrame
        for indice, linha in filtered_df.iterrows():
            # Lista para armazenar os valores da linha atual
            valores_da_linha = []
            chave = ""

            for nome_coluna, valor in linha.items():
            # Adiciona cada valor da coluna à lista
                valores_da_linha.append((nome_coluna, valor))
                if(nome_coluna == "id_filial"):
                    chave += str(valor) + "|"
                if(nome_coluna == "empresa"):
                    chave += str(valor) + "|"
                if(nome_coluna == "id_epi"):
                    chave += str(valor) + "|"
                if(nome_coluna == "id_tamanho"):
                    chave += str(valor) + "|"
                if(nome_coluna == "qtde_entrada"):
                    quantiade = Decimal(valor)
                    valor_normal = valor.normalize()
                    valor_final = int(valor_normal) if valor_normal == valor_normal.to_integral() else float(valor_normal)
                    chave += str(valor_final) + "|"
                if(nome_coluna == "dataentrada"):
                    chave += str(valor)

            # Adiciona a lista de valores da linha à lista principal
            valores_da_linha.append(("chave", chave))
            lista_de_novos_valores.append(valores_da_linha)
        
        return lista_de_novos_valores
    except Exception as ex:
        Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao conectar ao GM e pegar os dados.", str(ex), ex.args[0], Main.IdProcessamento, "")

def buscar_epi_local():
    from Service.Main import Main
    # Conexao com o banco
    servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
    connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'
    # Cria um cursor a partir da conexão
    connection = pyodbc.connect(connection_string)
    lista_de_valores_locais = []

    try:  
        query = "SELECT idFilial, idLocalEstoque, idItem, codTamanho, quantidade, dtMovimento FROM insertEstoqueEntrada"

        with pyodbc.connect(connection_string) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    chave = ""
                    chave += str(row[0]) + "|"
                    chave += str(row[1]) + "|"
                    chave += str(row[2]) + "|"
                    chave += str(row[3]) + "|"
                    chave += str(row[4]) + "|"
                    chave += str(row[5])
                    lista_de_valores_locais.append(chave)
    except Exception as ex:
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, f"Erro na query de busca por epi locais: {str(query)}", str(ex), ex.args[0], Main.IdProcessamento, "")
    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()

    return lista_de_valores_locais

def list_to_xml(lista_de_novos_valores):
    import xml.etree.ElementTree as ET
    root = ET.Element('produtos')

    for linha in lista_de_novos_valores:
        produto = ET.SubElement(root, 'produto')
        for nome_coluna, valor in linha:
            elemento = ET.SubElement(produto, nome_coluna)
            elemento.text = str(valor)

    # Converte o elemento XML para uma string com a devida declaração XML
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_string = xml_declaration + ET.tostring(root, encoding='unicode')
    return xml_string

def limparTabela():
    from Service.Main import Main
    # Conexao com o banco
    servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
    connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'
    # Cria um cursor a partir da conexão
    connection = pyodbc.connect(connection_string)
    try:  
        sql_delet = "DELETE FROM insertEstoqueEntrada"
        # Cria um cursor a partir da conexão
        cursor = connection.cursor()
        # Execute a consulta SQL com parâmetros para o INSERT
        cursor.execute(sql_delet)
        # Confirme as alterações no banco de dados
        connection.commit()        
    except Exception as ex:
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, f"Erro na query de delete: {str(sql_delet)}", str(ex), ex.args[0], Main.IdProcessamento, "")
    finally:
        # Fechar o cursor e a conexão
        cursor.close()
        connection.close()