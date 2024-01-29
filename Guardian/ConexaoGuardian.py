class ConexaoGuardian:
    Banco = None
    Login = None
    Senha = None
    Servidor = None

def obter_informacoes_conexao():
    return ConexaoGuardian.Servidor, ConexaoGuardian.Banco, ConexaoGuardian.Login, ConexaoGuardian.Senha