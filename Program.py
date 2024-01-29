from Service.Main import Main

class Program:
    @staticmethod
    def Main():
        main_instance = Main()
        main_instance.ExecucaoServico()

if __name__ == "__main__":
    Program.Main()