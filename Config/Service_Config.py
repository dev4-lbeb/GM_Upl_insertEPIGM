

import traceback
from xml.dom import minidom

from Guardian.ConexaoERP import ConexaoERP
from Guardian.ConexaoGestor import ConexaoGestor
from Guardian.ConexaoGuardian import ConexaoGuardian

from Guardian.ConexaoPortal import ConexaoPortal
from Guardian.ConexaoPortalLog import ConexaoPortalLog






class ServiceConfig:
    Status = False
    NomeServico = "GM_Dow_insertLocalEstoque"
    NomeCliente = "GM"
    DelayCiclo = 5
    DataValidade = 0
    UploadHoraInicio = None
    DelayUpload = 2
    UploadHoraFim = None
    DataUpload = None
    EmailValidacao = None
    TipoUpload = None
    ValorUpload = None
    TopRegistros = None

     # Define o arquivo de configuração com base no modo de depuração
    ArquivoConfig = "Portal_Config_Debug.xml" if __debug__ else "Portal_Config.xml"

    @staticmethod
    def CarregarConfiguracoes():
        try:
            with open("ArquivosConfig/" + ServiceConfig.ArquivoConfig, 'r', encoding='utf') as f:
                xml = minidom.parse(f)
                servidor = xml.getElementsByTagName("Servidor")
                banco = xml.getElementsByTagName("Banco")
                login = xml.getElementsByTagName("Login")
                senha = xml.getElementsByTagName("Senha")

            
            # Encontrar o elemento <Conexao>
            # conexao = config.find(".//Configuracoes/Conexao")

            # Configurações para ConexaoPortal
            ConexaoPortal.Servidor = servidor[0].firstChild.data
            ConexaoPortal.Banco = banco[0].firstChild.data
            ConexaoPortal.Login = login[0].firstChild.data
            ConexaoPortal.Senha = senha[0].firstChild.data

            # Configurações para ConexaoPortalLog
            ConexaoPortalLog.Servidor = servidor[1].firstChild.data
            ConexaoPortalLog.Banco = banco[1].firstChild.data
            ConexaoPortalLog.Login = login[1].firstChild.data
            ConexaoPortalLog.Senha = senha[1].firstChild.data

            # Configurações para ConexaoGuardian
            ConexaoGuardian.Servidor = servidor[2].firstChild.data
            ConexaoGuardian.Banco = banco[2].firstChild.data
            ConexaoGuardian.Login = login[2].firstChild.data
            ConexaoGuardian.Senha = senha[2].firstChild.data

            # Configurações para ConexaoGuardian
            ConexaoERP.Servidor = servidor[3].firstChild.data
            ConexaoERP.Banco = banco[3].firstChild.data
            ConexaoERP.Login = login[3].firstChild.data
            ConexaoERP.Senha = senha[3].firstChild.data

            # Configurações para ConexaoGuardian
            ConexaoGestor.Servidor = servidor[4].firstChild.data
            ConexaoGestor.Banco = banco[4].firstChild.data
            ConexaoGestor.Login = login[4].firstChild.data
            ConexaoGestor.Senha = senha[4].firstChild.data
            return True
        except Exception as ex:
            from Config.GuardianLog import GuardianLog
            from Guardian.Guardian_LogTxt import Guardian_LogTxt
            Guardian_LogTxt.LogAplicacao(ServiceConfig.NomeServico, "Erro ao executar a busca das configurações." + str(ex) + traceback.format_exc())
            GuardianLog.Log_Ocorrencia(ServiceConfig.NomeServico,"Erro ao executar a busca das configurações.", str(ex), ex, "", "")
            return False

