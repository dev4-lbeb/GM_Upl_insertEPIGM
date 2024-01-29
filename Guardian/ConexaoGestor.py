class ConexaoGestor:
    Banco = None
    Login = None
    Senha = None
    Servidor = None

def obter_informacoes_conexao():
    return ConexaoGestor.Servidor, ConexaoGestor.Banco, ConexaoGestor.Login, ConexaoGestor.Senha