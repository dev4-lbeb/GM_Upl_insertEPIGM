

import os


class Guardian_TxtFile:
    def DefinirArquivo(self, caminho, nome_arquivo):
        try:
            caminho_completo = os.path.join(caminho, nome_arquivo)
            if not os.path.exists(caminho_completo):
                with open(caminho_completo, 'w') as arquivo:
                    arquivo.write("-------------------------------------------------------------------------------------------------------\n")
        except Exception as ex:
            raise ex

    def DefinirTexto(self, caminho, nome_arquivo, texto):
        try:
            self.DefinirArquivo(caminho, nome_arquivo)

            caminho_completo = os.path.join(caminho, nome_arquivo)
            with open(caminho_completo, 'a') as arquivo:
                arquivo.write("\n" + texto)
        except Exception as ex:
            raise ex
