from datetime import datetime
from enum import Enum

from Guardian_log.LogDAO import LogDAO
from Guardian_log.LogOcorrencia import LogOcorrencia
from Guardian_log.LogRotina import LogRotina




class Tipo(Enum):
    Iniciado = 'Iniciado'
    Finalizado = 'Finalizado'

class Acao(Enum):
    Cadastro = 'Cadastro'
    Atualizacao = 'Atualização'
    Delecao = 'Deleção'
    Importacao = 'Importação'
    DelecaoAntigo = 'DeleçãoAntigo'
    Atendido = 'Atendido'
    Integracao = 'Integração'

class Status(Enum):
    Sucesso = 'Sucesso'
    Falha = 'Falha'

class GuardianLog:
    def Log_Rotina(sigla_rotina, nome_rotina, tipo, id_proc, cnpj):
        from Config.Service_Config import ServiceConfig
        from Service.Main import Main

        main = Main()
        if main.LogRotinaHabilitado == True:
            log_rotina = LogRotina()
            log_rotina.IdProc = str(id_proc)
            log_rotina.IdLog = datetime.now().strftime("%Y%m%d%H%M%S") + sigla_rotina
            log_rotina.IdCiclo = main.IdCiclo
            log_rotina.Rotina = nome_rotina
            log_rotina.Tipo = tipo
            log_rotina.Data = datetime.now().strftime("%Y%m%d")
            log_rotina.Hora = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            log_rotina.Aplicacao = ServiceConfig.NomeServico
            log_rotina.Cliente = cnpj

            log_dao = LogDAO()
            log_dao.RegistrarLogRotina(log_rotina)

    @staticmethod
    def Log_RotinaDelet(sigla_rotina, nome_rotina, tipo, id_proc, cnpj):
        from Config.Service_Config import ServiceConfig
        from Service.Main import Main

        main = Main()
        if main.LogRotinaHabilitado == True:
            log_rotina = LogRotina()
            log_rotina.IdProc = str(id_proc)
            log_rotina.IdLog = datetime.now().strftime("%Y%m%d%H%M%S")
            log_rotina.IdCiclo = main.IdCiclo
            log_rotina.Rotina = f"{sigla_rotina}/{nome_rotina}"
            log_rotina.Tipo = tipo
            log_rotina.Data = datetime.now().strftime("%Y%m%d")
            log_rotina.Hora = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            log_rotina.Aplicacao = ServiceConfig.NomeServico
            log_rotina.Cliente = cnpj

            log_dao = LogDAO()
            log_dao.RegistrarLogRotina(log_rotina)

    @staticmethod
    def Log_Ocorrencia(nome_rotina, descricao, descricao_tecnica, informacoes_adicionais, id_proc, cnpj):
            from Config.Service_Config import ServiceConfig
            from Service.Main import Main

            main = Main()
            if main.LogOcorrenciaHabilitado == True:
                log_ocorrencia = LogOcorrencia()
                log_ocorrencia.IdProc = id_proc
                log_ocorrencia.NomeRotina = nome_rotina
                log_ocorrencia.Data = datetime.now().strftime("%Y%m%d")
                log_ocorrencia.Hora = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                log_ocorrencia.Descricao = descricao.replace("'", "|")
                log_ocorrencia.DescricaoTecnica = descricao_tecnica.replace("'", "|")
                log_ocorrencia.InformacaoAdicional = informacoes_adicionais.replace("'", "|")
                log_ocorrencia.Aplicacao = ServiceConfig.NomeServico
                log_ocorrencia.Cliente = cnpj

                log_dao = LogDAO()
                log_dao.RegistrarLogOcorrencia(log_ocorrencia)