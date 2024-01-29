import pyodbc
from Guardian import ConexaoPortal
from Guardian.Tabelas_Portal import Tabelas_Portal
from Models.DadosEmpresa import DadosEmpresa


class DadosEmpresaDAO:
    def buscar_empresas(self):
        
        empresas = []

        query = (
            "SELECT nrCNPJEmpresa, RazaoSocialEmpresa, UsernameRSData, PasswordRSData, UsernameCliente, PasswordCliente, COD_EMPRESA, COD_FILIAL, NOME_FANTASIA, "
            "RSDATA_DOW, REGISTRO_TXT, LOG_OCORRENCIA, LOG_EMAIL, LOG_ROTINA, LOG_AUDITORIA, "
            "insertEmpresas, insertEmpregados, transferEmpregados, insertEmpregadosTurnos, insertFerias, "
            "transfCargo, transfSetor, "
            "getAfastamentos, getRestricaoDemi, "
            "insertCargosRH, insertSetoresRH, DIAS_LOG, LOGIN "
            "FROM " + Tabelas_Portal.DadosEmpresa + " "
            "WHERE STATUS = 'ATIVO' "
            "AND COD_EMPRESA = 'EPI' "
        )

        # Conexao com o banco
        servidor, banco, login, senha = ConexaoPortal.obter_informacoes_conexao()
        connection_string = f'DRIVER={{SQL Server}};SERVER={servidor};DATABASE={banco};UID={login};PWD={senha}'

        with pyodbc.connect(connection_string) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    empresa = DadosEmpresa()
                    empresa.insertEmpregados = row.insertEmpregados == 'S'
                    empresa.insertEmpresas = row.insertEmpresas == 'S'
                    empresa.transferEmpregados = row.transferEmpregados == 'S'
                    empresa.transfCargo = row.transfCargo == 'S'
                    empresa.transfSetor = row.transfSetor == 'S'
                    empresa.insertEmpregadosTurnos = row.insertEmpregadosTurnos == 'S'
                    empresa.insertFerias = row.insertFerias == 'S'
                    empresa.getAfastamentos = row.getAfastamentos == 'S'
                    empresa.getRestricaoDemi = row.getRestricaoDemi == 'S'
                    empresa.insertCargosRH = row.insertCargosRH == 'S'
                    empresa.insertSetoresRH = row.insertSetoresRH == 'S'

                    empresa.RsDataDownload = row.RSDATA_DOW == 'S'
                    empresa.LogTxt = row.REGISTRO_TXT == 'S'
                    empresa.LogOcorrencia = row.LOG_OCORRENCIA == 'S'
                    empresa.LogRotina = row.LOG_ROTINA == 'S'
                    empresa.LogAuditoria = row.LOG_AUDITORIA == 'S'

                    empresa.CNPJEmpresa = row.nrCNPJEmpresa
                    empresa.RazaoSocialEmpresa = row.RazaoSocialEmpresa
                    empresa.UserRsData = row.UsernameRSData
                    empresa.PasswordRsData = row.PasswordRSData
                    empresa.UserCliente = row.UsernameCliente
                    empresa.PasswordCliente = row.PasswordCliente
                    empresa.CodEmpresa = row.COD_EMPRESA
                    empresa.CodFilial = row.COD_FILIAL
                    empresa.DIAS_LOG = row.DIAS_LOG
                    empresa.NomeFantasia = row.NOME_FANTASIA
                    empresa.LogEmail = row.LOG_EMAIL
                    empresa.Email = row.LOGIN

                    empresas.append(empresa)

        return empresas