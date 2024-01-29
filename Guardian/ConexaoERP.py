class ConexaoERP:
    Banco = None
    Login = None
    Senha = None
    Servidor = None

def obter_informacoes_conexao():
    return ConexaoERP.Servidor, ConexaoERP.Banco, ConexaoERP.Login, ConexaoERP.Senha