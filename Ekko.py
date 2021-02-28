"""Ekko é uma ferramenta para manipulação de pings em Python e somente a sistemas operacionais Windows.(Por Enquanto!!!)
"""

import subprocess
import re
import time
import datetime

# https://stackoverflow.com/questions/46476677/python-subprocess-check-output-decoding-specials-characters

class Ekko_Pings:
    """Essa classe automatiza pings. Ela cria loops com o método subprocess_ping. Possui a intenção de
    obter o tempo de emparelhamento de devices, tempo de perda de energia de capacitores e tamanho de bytes
    suportados por cada device na rede.
    """

    def __init__(self, ip, package="32", number_of_messages=None, timer=1, number_of_sucessful_responses=1,
                 number_of_problematic_messages=4):

        """
        ip -> Ip do device (Ipv4 ou Ipv6).

        package -> Tamanho do pacote enviado em bytes.

        number_of_messages -> Controlador do numero de pings enviados. Caso seja default(None) pings infinitos.

        timer -> Controla o tempo entre cada ping.

        number_of_sucessful_responses -> Controla os loops através da quantidade de respostas respondidas pelo device.

        number_of_problematic_messages -> Controla os loops através da quantidade de respostas problematicas dadas
        pelo device.


        :param ip: String
        :param package: String
        :param number_of_messages: Int or None
        :param timer: Int
        :param number_of_sucessful_responses: Int
        :param number_of_problematic_messages: Int
        """

        assert type(ip) is str, "ip must be a Str"
        assert type(package) is str, "package must be a Str"
        assert type(number_of_messages) is int or number_of_messages is None, "number must be a Int or None"
        assert type(timer) is int, "timer must be a Int"
        assert type(number_of_problematic_messages) is int, "number_of_problematic_messages must be a Int"
        assert type(number_of_sucessful_responses) is int , "number_of_sucessful_responses must be a Int"

        self.ip = ip
        self.package = package
        self.number_of_messages = number_of_messages
        self.timer = timer
        self.start_time = list()
        self.problematic_messages = []
        self.first_successful_responses = []
        self.number_of_problematic_messages = number_of_problematic_messages
        self.number_of_sucessful_responses = number_of_sucessful_responses

    def subprocess_ping(self):
        """Esse método cria um subprocess(ping único), trata a resposta tirando as estatisticas, mata o
        subprocesso e chama um temporizador.

        :return: Str
        """
        process = subprocess.Popen(f'ping /n 1 /l {self.package} {self.ip}',
                                   stdout=subprocess.PIPE,
                                   encoding="437", close_fds=True)
        response = process.stdout.read()

        # gambiarra
        response = re.sub(r'.* Pacotes:.*', '', response, re.M)
        response = re.sub(r'.* perda.*', '', response, re.M)
        response = re.sub(r'Estatísticas.*', '', response, re.M)
        response = re.sub(r'Aproximar.*', '', response, re.M)
        response = re.sub(r'.* Máximo.*', '', response, re.M)
        response = re.sub(r'\n{6}|\n{4}', '', response, re.M)
        # gambiarra

        process.kill()
        response += datetime.datetime.now().strftime('%H:%M:%S')
        time.sleep(self.timer)
        return response

    def check_pairing_time(self):
        """Esse método checa o tempo de emparelhamento de um device através das respostas dos pings. Se um device
         for ligado ao mesmo tempo em que o método check_pairing_time for chamado o tempo de emparelhamento será
         obtido através do atributo first_successful_responses.

        :return: Void
        """

        c = 0
        time_is_over = "Esgotado o tempo limite do pedido."
        unreachable_host = "Host de destino inacessível."
        general_failure = "Falha geral."

        self.start_time = ['( Start: ', self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')']

        print('Começou: ', self.ip)

        if self.number_of_messages:
            for i in range(0, self.number_of_messages):
                response = self.subprocess_ping()
                time.sleep(self.timer)
                if time_is_over in response or unreachable_host in response or general_failure in response:
                    c += 1
                    self.first_successful_responses.append(['(', response, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])
                    if c == self.number_of_sucessful_responses:
                        print('Terminado: ', self.ip)
                        break

        else:
            while True:
                response = self.subprocess_ping()
                time.sleep(self.timer)
                if time_is_over not in response and unreachable_host not in response\
                        and general_failure not in response:

                    c += 1
                    self.first_successful_responses.append(['(', response, self.ip,
                                                            datetime.datetime.now().strftime('%H:%M:%S'), ')'])

                    if c == self.number_of_sucessful_responses:
                        print('Terminado: ', self.ip)
                        break

    def check_shutdown_time(self):
        """Esse método checa o tempo de desligamento de um device através das respostas dos pings. Se um device
         for desligado ao mesmo tempo em que o método check_shutdown_time for chamado o tempo de respostas
         problematicas pode indicar o tempo de desligamento do device, através do atributo
         number_of_problematic_messages.

        :return: Void
        """
        response = str()
        time_is_over = "Esgotado o tempo limite do pedido."
        unreachable_host = "Host de destino inacessível."
        general_failure = "Falha geral."
        c = 0

        self.start_time = ['( Start: ', self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')']

        if self.number_of_messages:
            for i in range(0, self.number_of_messages):
                response = self.subprocess_ping()
                time.sleep(1)
                if time_is_over in response or unreachable_host in response or general_failure in response:
                    c += 1

                    if time_is_over in response:
                        self.problematic_messages.append(['(', time_is_over, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])

                    if unreachable_host in response:
                        self.problematic_messages.append(['(', unreachable_host, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])

                    if general_failure in response:
                        self.problematic_messages.append(['(', general_failure, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])
                    if c == 5:
                        break

        else:
            while True:
                response += self.subprocess_ping()
                if time_is_over in response or unreachable_host in response or general_failure in response:
                    c += 1

                    if time_is_over in response:
                        self.problematic_messages.append(['(', time_is_over, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])

                    if unreachable_host in response:
                        self.problematic_messages.append(['(', unreachable_host, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])

                    if general_failure in response:
                        self.problematic_messages.append(['(', general_failure, self.ip, datetime.datetime.now().strftime('%H:%M:%S'), ')'])

                    if c == 4:
                        break

