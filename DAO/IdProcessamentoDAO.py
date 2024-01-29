
from datetime import datetime
import pyodbc

class IdProcessamentoDAO:
    @staticmethod
    def IniciarProcessamento():
        from Guardian import ConexaoPortal
        
        codigo = 0

        # Construa a string SQL com placeholders para os parâmetros
        query_insert = f"""INSERT INTO ID_PROCESSAMENTO (Data, Hora) VALUES ('{datetime.now().strftime("%Y%m%d")}', '{datetime.now().strftime("%H:%M")}');"""
        
        query_select = "SELECT SCOPE_IDENTITY() As ID"

        # Preencha os valores para os placeholders
        #valores = (datetime.now().strftime("%Y%m%d"), datetime.now().strftime("%H:%M"))

        try:
            
            # Conexao com o banco
            servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
            connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'

            # Estabelece a conexão
            connection = pyodbc.connect(connection_string)
            # Cria um cursor a partir da conexão
            cursor = connection.cursor()

            # Execute a consulta SQL com parâmetros para o INSERT
            cursor.execute(query_insert)
            
            # Execute a parte do SELECT
            cursor.execute(query_select)
            # Recupere o último ID inserido
            codigo = cursor.fetchone()[0]
            # Confirme as alterações no banco de dados
            connection.commit()
        except Exception as ex:
            # Tratar exceção conforme necessário
            print(f"Erro ao iniciar o processamento: {ex}")
        finally:
            # Fechar o cursor e a conexão
            cursor.close()
            connection.close()

        return codigo
