


from datetime import datetime
from enum import Enum
import os
from Guardian.Guardian_TxtFile import Guardian_TxtFile



class TipoControle(Enum):
    Servico_Iniciado = 1
    Servico_Finalizado = 2
    Ciclo_Iniciado = 3
    Ciclo_Finalizado = 4

class Guardian_LogTxt:
    @staticmethod
    def LogAplicacao(rotina, descricao):
        from Service.Main import Main

        main = Main()
        try:
            if main.LogTxtHabilitado == True:
                 # Obtenha o diretório do script atual
                script_dir = os.path.dirname(os.path.abspath(__file__))

                # Navegue para o diretório pai (raiz do projeto)
                root_dir = os.path.dirname(script_dir)

                log_directory = os.path.join(root_dir, "Log")
                if not os.path.exists(log_directory):
                    os.makedirs(log_directory)

                texto_registro = ""
                if rotina:
                    texto_registro += datetime.now().strftime("%d/%m/%Y | %H:%M:%S.%f") + " | " + rotina
                if descricao:
                    texto_registro += "\n=> " + descricao

                guardian_txt = Guardian_TxtFile()
                guardian_txt.DefinirTexto(log_directory, f"Guardian_Log_ERRO_{main.IdCiclo}.txt", texto_registro)
        except Exception as ex:
            excecao_txt = str(ex)

    @staticmethod
    def LogControle(tipo_controle):
        from Service.Main import Main
        from Config.Service_Config import ServiceConfig

        main = Main()
        try:
            if main.LogTxtHabilitado == True:
                rotina = ServiceConfig.NomeServico
                descricao = tipo_controle.name.replace("_", " ")

                # Obtenha o diretório do script atual
                script_dir = os.path.dirname(os.path.abspath(__file__))

                # Navegue para o diretório pai (raiz do projeto)
                root_dir = os.path.dirname(script_dir)

                log_directory = os.path.join(root_dir, "Log")
                if not os.path.exists(log_directory):
                    os.makedirs(log_directory)

                texto_registro = ""
                if rotina:
                    texto_registro += f"{datetime.now().strftime('%d/%m/%Y | %H:%M:%S.%f')} | {rotina}"
                if descricao:
                    texto_registro += f"\n=> {descricao}"

                guardian_txt = Guardian_TxtFile()
                guardian_txt.DefinirTexto(log_directory, f"Guardian_Log_{main.IdCiclo}.txt", texto_registro)
        except Exception as ex:
            excecao_txt = str(ex)
