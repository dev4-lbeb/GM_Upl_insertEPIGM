
import pyodbc
from datetime import datetime
from Config.GuardianLog import GuardianLog, Tipo

from Config.Service_Config import ServiceConfig
from Controller import EpiController
from DAO.DadosEmpresaDAO import DadosEmpresaDAO
from DAO.IdProcessamentoDAO import IdProcessamentoDAO
from Guardian import ConexaoPortal
from Guardian.Guardian_LogTxt import Guardian_LogTxt, TipoControle


class Main:
    IdCiclo = None
    IdProcessamento = 0
    NomeCliente = None
    LogTxtHabilitado = False
    LogOcorrenciaHabilitado = False
    LogEmailHabilitado = False
    LogRotinaHabilitado = False
    LogAuditoriaHabilitado = False
    RegistroRotina = None
    TipoEnvio = None
    Username = None
    Password = None
    DiasLog = 0

    def ExecucaoServico(self):
        try:
            Main.IdCiclo = datetime.now().strftime("%Y%m%d%H%M%S")
            ServiceConfig.CarregarConfiguracoes()
            Main.IdProcessamento = IdProcessamentoDAO.IniciarProcessamento()

            # dados_empresa_dao = DadosEmpresaDAO()
            # empresas = dados_empresa_dao.buscar_empresas()

            buscar_dados_global()

            # Adicione o código abaixo ao loop no qual você está iterando sobre as empresas
            # for dados_empresa in empresas:
            #     # ATRIBUIÇÃO DE VALOR PARA AS PROPRIEDADES DE CONTROLE
            #     Main.NomeCliente = dados_empresa.NomeFantasia
            #     Main.LogTxtHabilitado = dados_empresa.LogTxt
            #     Main.LogOcorrenciaHabilitado = dados_empresa.LogOcorrencia
            #     Main.LogRotinaHabilitado = dados_empresa.LogRotina
            #     Main.LogAuditoriaHabilitado = dados_empresa.LogAuditoria
            # if Main.RegistroRotina == "C" or Main.RegistroRotina == "R":
            #     Guardian_LogTxt.LogControle(TipoControle.Ciclo_Iniciado)
            #     GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Iniciado, Main.IdProcessamento, dados_empresa.CNPJEmpresa)

            # if Main.RegistroRotina == "C" or Main.RegistroRotina == "R":
            #     Guardian_LogTxt.LogControle(TipoControle.Ciclo_Finalizado)
            #     GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Finalizado, Main.IdProcessamento, dados_empresa.CNPJEmpresa)

            if Main.RegistroRotina == "C" or Main.RegistroRotina == "R":
                Guardian_LogTxt.LogControle(TipoControle.Ciclo_Iniciado)
                GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Iniciado, Main.IdProcessamento, "")

            EpiController.Executar()

            if Main.RegistroRotina == "C" or Main.RegistroRotina == "R":
                Guardian_LogTxt.LogControle(TipoControle.Ciclo_Finalizado)
                GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Finalizado, Main.IdProcessamento, "")
        except Exception as ex:
            Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
            GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao executar o serviço.", ex, ex.args[0], Main.IdProcessamento, "")

def buscar_dados_global():
    # BUSCAR DADOS DE CONFIG GLOBAL
    try:
        # Conexao com o banco
        servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
        connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'

        query = "SELECT REGISTRO_ROTINA, TIPO_DE_ENVIO, DIAS_LOG, LOGIN_RSDATA, SENHA_RSDATA FROM CONFIG_GLOBAL"

        with pyodbc.connect(connection_string) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    Main.RegistroRotina = row[0]
                    Main.TipoEnvio = row[1]
                    Main.DiasLog = int(row[2])
                    Main.Username = row[3]
                    Main.Password = row[4]
                    # Faça o que precisar com os dados

    except Exception as ex:
        Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
        GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao executar ao buscar dados globais.", ex, ex.args[0], Main.IdProcessamento, "")

                
    