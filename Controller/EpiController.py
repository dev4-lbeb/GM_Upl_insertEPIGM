from datetime import datetime
import delta_sharing
from Config.GuardianLog import GuardianLog, Tipo
from Config.Service_Config import ServiceConfig
from DAO import EpiDAO
from Guardian import ConexaoPortal
from Guardian.Guardian_LogTxt import Guardian_LogTxt
from Service.Main import Main


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
    try:
        if Main.RegistroRotina == "R":
            GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Iniciado, Main.IdProcessamento, "")

        lista_retornada = PegarRegistros()

        # Conexao com o banco
        servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
        connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'
        # Cria um cursor a partir da conexão
        cursor = connection_string.cursor()
        try:
            # Loop para inserir cada linha no SQL Server
            for valores_da_linha in lista_retornada:
                sql_insert = f'''INSERT INTO insertEstoque 
                            (idFilial, descricaoFilial, codItem, descItem, quantidade, DataEntradaMidd, 
                            DataSaidaMidd, Reenvios, DataReenvio, rsExp, codEmpresa, codFilial,
                            cnpjCliente, status)
                            VALUES 
                            ({valores_da_linha[0]}, '{valores_da_linha[1]}', {valores_da_linha[2]}, 
                            '{valores_da_linha[3]}', {valores_da_linha[4]}, '{datetime.now().strftime('%d/%m/%Y')}', 
                            '', {0}, '', 
                            '', '', '',
                            '', '')'''

            cursor.execute(sql_insert)

            # Confirme as alterações no banco de dados
            connection_string.commit()
        except Exception as ex:
            GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, f"Erro na query de insert: {str(sql_insert)}", ex, ex.args[0], Main.IdProcessamento, "")
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            connection_string.close()

        if Main.RegistroRotina == "R":
            GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Finalizado, Main.IdProcessamento, "")

    except Exception as ex:
        Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao salvar os registros vindos do GM.", ex, ex.args[0], Main.IdProcessamento, "")

        
    


def PegarRegistros():
    FILE = 'configDataBricks.share'
    try:
        client = delta_sharing.SharingClient(FILE)

        print(client.list_all_tables())

        df = delta_sharing.load_as_pandas(f'{FILE}#rs-data-sharing.rsdata.sample_table')

        # Especificando o caminho do arquivo CSV
        csv_path = 'exportar\exp.csv'

        # Salvando o DataFrame como um arquivo CSV
        df.to_csv(csv_path, index=False)

        # Convertendo o DataFrame para uma string
        df_string = df.to_string(index=False)

        # Especificando o caminho do arquivo de texto
        txt_path = 'exportar\exp.txt'

        # Salvando a string em um arquivo de texto
        with open(txt_path, 'w') as file:
            file.write(df_string)

        lista_de_novos_valores = []
        # Loop pelas linhas e colunas do DataFrame
        for indice, linha in df.iterrows():
            # Lista para armazenar os valores da linha atual
            valores_da_linha = []

            for nome_coluna, valor in linha.items():
            # Adiciona cada valor da coluna à lista
                valores_da_linha.append(valor)
        
            # Adiciona a lista de valores da linha à lista principal
            lista_de_novos_valores.append(valores_da_linha)
        
        return lista_de_novos_valores
    except Exception as ex:
        Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao conectar ao GM e pegar os dados.", ex, ex.args[0], Main.IdProcessamento, "")
