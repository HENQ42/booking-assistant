from flask import Flask, request, jsonify
from functions import reservation_detector, data_extractor

app = Flask(__name__)

@app.route('/process-email', methods=['POST'])
def process_email():
    # Obtendo o conteúdo do e-mail enviado na requisição
    data = request.get_json()
    email_content = data.get('email_content', '')

    # Verificar se o e-mail é uma solicitação de reserva
    is_reservation = reservation_detector(email_content)
    print("É uma reserva?", is_reservation)

    if is_reservation in 'Sim':
        # Extrair dados da reserva
        reservation_data = data_extractor(email_content)
        print("dados da reserva: ", reservation_data, "\n")

        #verificação de extração
        if reservation_data == "Negado":
            return jsonify({
                "status": "success",
                "is_reservation": False,
                "message": "O e-mail foi negado na extração."
            })

        # Retornar os dados extraídos como JSON
        return jsonify({
            "status": "success",
            "is_reservation": True,
            "reservation_data": reservation_data
        })
    else:
        return jsonify({
            "status": "success",
            "is_reservation": False,
            "message": "O e-mail não está relacionado a uma reserva."
        })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)