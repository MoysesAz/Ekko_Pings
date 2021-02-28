import re


a="""
Disparando 192.168.1.16 com 32 bytes de dados:
Resposta de 192.168.1.16: bytes=32 tempo=94ms TTL=64

Estatísticas do Ping para 192.168.1.16:
    Pacotes: Enviados = 1, Recebidos = 1, Perdidos = 0 (0% de
             perda),
Aproximar um n�mero redondo de vezes em milissegundos:
    M�nimo = 94ms, M�ximo = 94ms, M�dia = 94ms

Disparando 192.168.1.16 com 32 bytes de dados:
Esgotado o tempo limite do pedido.

Estatísticas do Ping para 192.168.1.16:
    Pacotes: Enviados = 1, Recebidos = 0, Perdidos = 1 (100% de
             perda),

"""
a = re.sub(r'.* Pacotes:.*', '', a, re.M)
a = re.sub(r'.* perda.*', '', a, re.M)
a = re.sub(r'Estatísticas.*', '', a, re.M)
a = re.sub(r'Aproximar.*', '', a, re.M)
a = re.sub(r'.* M.*', '', a, re.M)
a = re.sub(r'\n{1}', '', a, re.M)

print(a)
#print(re.sub(r'(^.*Pacotes.* | ^.+Aproximar.*)', 'oi', a, re.M))
#print(re.sub(r'Estatísticas.*(\n).*(\n).*(\n)$', 'oi', a, re.M))

a = 'oi'
print(a is str)
assert a is str
print(a)