import concurrent.futures
from Ekko import Ekko_Pings

#dict
ip_3 = Ekko_Pings('2001:db8::3')
ip_4 = Ekko_Pings('2001:db8::4')
ip_5 = Ekko_Pings('2001:db8::5')
ip_6 = Ekko_Pings('2001:db8::6')
ip_7 = Ekko_Pings('2001:db8::7')
ip_8 = Ekko_Pings('2001:db8::8')
ip_9 = Ekko_Pings('2001:db8::9')
ip_a = Ekko_Pings('2001:db8::a')
ip_b = Ekko_Pings('2001:db8::b')
ip_c = Ekko_Pings('2001:db8::c')
moyses = Ekko_Pings('192.168.1.16', number_of_messages=1)
flavia = Ekko_Pings('192.168.1.13', number_of_messages=1)


lista1 = [ip_3]
lista2 = [ip_3, ip_4, ip_5, ip_6, ip_7, ip_8, ip_9]
lista3 = [ip_3, ip_4, ip_5, ip_6, ip_7, ip_8]
lista4 = [ip_3, ip_4, ip_5, ip_6, ip_7]
lista5 = [ip_3, ip_4, ip_5, ip_6]
lista6 = [ip_3, ip_4, ip_5]
lista7 = [ip_3, ip_4]
lista8 = [moyses, flavia]


with concurrent.futures.ThreadPoolExecutor() as executor:
    for i in lista2:
        executor.submit(i.check_pairing_time) #Atenção para parametros colocados com ()

for i in lista2:
    print(i.start_time)
    for j in i.first_successful_responses:
        print(j)


help(Ekko_Pings)