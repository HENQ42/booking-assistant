# main.py

import os
from functions import reservation_detector, data_extractor

def main():
    # Exemplo de e-mail
    email_content = """
        Data do email: 22/10/24
Boa tarde,

Conforme conversamos pelo whatsapp, solicito reserva como segue:

Ciente que o pagamento será efetuado amanhã

 

Hotel Vitória 

R. Guajajaras, 251 - Xinguara, PA, 68555-160

1x quarto duplo com café da manhã

Estacionamento incluso

Diária: R$ 200,00

23/10 a 04/11

 

Srs. REINALDO JORGE MONTEIRO BARBOS

ISAAC PANTOJA DOS SANTOS

Por favor, informar dados bancários para pagamento.

Não trabalhamos com PIX.

 

Nossos dados para emissão da nota fiscal:

Razão Social: ICOMON TECNOLOGIA LTDA.

C.N.P.J.: 02.137.309/0001‐53

Insc. Estadual: 116.591.820‐110

Endereço: 

Rua: Agrimensor Sugaya, 400

Bairro: Itaquera 

Município/Cidade: São Paulo 

Estado: São Paulo

CEP: 08260‐030

Desde já agradeço e no aguardo de retorno para providenciar o pagamento

 

 

 

 

Atenciosamente, 
    """

    # Verificar se o e-mail é uma solicitação de reserva
    is_reservation = reservation_detector(email_content)

    #debug
    # print("is_reservation: ", is_reservation)

    if is_reservation in 'Sim':
        # Extrair dados da reserva
        reservation_data = data_extractor(email_content)

        #debug
        # print("reservation_data: ", reservation_data)

        # Exibir os dados extraídos
        print("\nDados da Reserva Extraídos:")
        for key, value in reservation_data.items():
            print(f"{key}: {value}")

        # Aqui você pode adicionar lógica para processar a reserva,
        # como atualizar o sistema interno, enviar confirmações, etc.
    else:
        print("O e-mail não está relacionado a uma reserva.")

if __name__ == "__main__":
    main()