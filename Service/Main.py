

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
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Main, cls).__new__(cls)
            cls._instance.init()
        return cls._instance
    
    def init(self):
        self.IdCiclo = None
        self.IdProcessamento = 0
        self.NomeCliente = None
        self.LogTxtHabilitado = True
        self.LogOcorrenciaHabilitado = True
        self.LogEmailHabilitado = False
        self.LogRotinaHabilitado = True
        self.LogAuditoriaHabilitado = False
        self.RegistroRotina = None
        self.TipoEnvio = None
        self.Username = None
        self.Password = None
        self.DiasLog = 0

    def ExecucaoServico(self):
        try:
            self.IdCiclo = datetime.now().strftime("%Y%m%d%H%M%S")
            ServiceConfig.CarregarConfiguracoes()
            self.IdProcessamento = IdProcessamentoDAO.IniciarProcessamento()

            # dados_empresa_dao = DadosEmpresaDAO()
            # empresas = dados_empresa_dao.buscar_empresas()

            self.buscar_dados_global()

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

            if self.RegistroRotina == "C" or self.RegistroRotina == "R":
                Guardian_LogTxt.LogControle(TipoControle.Ciclo_Iniciado) 
                GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Iniciado, self.IdProcessamento, "")

            EpiController.Executar()

            if self.RegistroRotina == "C" or self.RegistroRotina == "R":
                Guardian_LogTxt.LogControle(TipoControle.Ciclo_Finalizado)
                GuardianLog.Log_Rotina("", ServiceConfig.NomeServico, Tipo.Finalizado, self.IdProcessamento, "")
        except Exception as ex:
            Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
            GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao executar o serviço.", str(ex), ex.args[0], self.IdProcessamento, "")

    def buscar_dados_global(self):
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
                        self.RegistroRotina = row[0]
                        self.TipoEnvio = row[1]
                        self.DiasLog = int(row[2])
                        self.Username = row[3]
                        self.Password = row[4]
                        # Faça o que precisar com os dados

        except Exception as ex:
            Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, f"Erro : {ex}")
            GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico, "Erro ao executar ao buscar dados globais.", str(ex), ex.args[0], self.IdProcessamento, "")

                
    