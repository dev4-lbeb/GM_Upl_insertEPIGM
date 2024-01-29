
import pyodbc

from Guardian.Guardian_LogTxt import Guardian_LogTxt
from Guardian import ConexaoPortalLog
from Guardian.Tabelas_Guardian import Tabelas_Guardian

class LogDAO:
    def RegistrarLogRotina(self, log_rotina):
        
        query = f"""
            INSERT INTO {Tabelas_Guardian.LogRotina}
            (ID_PROC, ID_LOG, ID_CICLO, ROTINA, TIPO, DATA, HORA, APLICACAO, CLIENTE)
            VALUES (
                '{log_rotina.IdProc}',
                '{log_rotina.IdLog}',
                '{log_rotina.IdCiclo}',
                '{log_rotina.Rotina}',
                '{log_rotina.Tipo}',
                '{log_rotina.Data}',
                '{log_rotina.Hora}',
                '{log_rotina.Aplicacao}',
                '{log_rotina.Cliente}'
            )
        """

        try:
            # Conexao com o banco
            servidor, banco, login, senha = ConexaoPortalLog.obter_informacoes_conexao()
            connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'

            # Estabelece a conexão
            connection = pyodbc.connect(connection_string)
            # Cria um cursor a partir da conexão
            cursor = connection.cursor()

            # Execute a consulta SQL com parâmetros para o INSERT
            cursor.execute(query)
            connection.commit()
        except Exception as ex:
            Guardian_LogTxt.LogAplicacao("Registrar Log Rotina ",f"Erro Erro: {ex}\nQuery: {query}")

    def RegistrarLogOcorrencia(self, log_ocorrencia):
        query = f"""
            INSERT INTO {Tabelas_Guardian.LogOcorrencia}
            (ID_PROC, NOME_ROTINA, DATA, HORA, DESCRICAO, DESCRICAO_TECNICA, INFORMACAO_ADICIONAL, APLICACAO, CLIENTE, ENVIADOS)
            VALUES (
                '{log_ocorrencia.IdProc}',
                '{log_ocorrencia.NomeRotina}',
                '{log_ocorrencia.Data}',
                '{log_ocorrencia.Hora}',
                '{log_ocorrencia.Descricao.replace("'", "|")}',
                '{log_ocorrencia.DescricaoTecnica.replace("'", "|")}',
                '{log_ocorrencia.InformacaoAdicional.replace("'", "|")}',
                '{log_ocorrencia.Aplicacao}',
                '{log_ocorrencia.Cliente}',
                ''
            )
        """

        try:
             # Conexao com o banco
            servidor, banco, login, senha = ConexaoPortalLog.obter_informacoes_conexao()
            connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'

            # Estabelece a conexão
            connection = pyodbc.connect(connection_string)
            # Cria um cursor a partir da conexão
            cursor = connection.cursor()

            # Execute a consulta SQL com parâmetros para o INSERT
            cursor.execute(query)
            connection.commit()
        except Exception as ex:
            Guardian_LogTxt.LogAplicacao("Registrar Log Ocorrencia ",f"Erro : {ex}\nQuery: {query}")