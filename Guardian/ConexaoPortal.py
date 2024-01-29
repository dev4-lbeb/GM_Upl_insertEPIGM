class ConexaoPortal:
    Banco = None
    Login = None
    Senha = None
    Servidor = None

def obter_informacoes_conexao():
    return ConexaoPortal.Servidor, ConexaoPortal.Banco, ConexaoPortal.Login, ConexaoPortal.Senha