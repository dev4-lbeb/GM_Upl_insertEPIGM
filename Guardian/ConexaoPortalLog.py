class ConexaoPortalLog:
    Banco = None
    Login = None
    Senha = None
    Servidor = None

def obter_informacoes_conexao():
    return ConexaoPortalLog.Servidor, ConexaoPortalLog.Banco, ConexaoPortalLog.Login, ConexaoPortalLog.Senha