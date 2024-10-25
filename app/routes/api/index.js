const express = require('express');
const axios = require('axios');
const router = express.Router();

const JSON_SERVER_URL = 'http://localhost:5005/reservations';
const REPLY_EMAIL_URL = 'http://localhost:5004/reply_email';

// Endpoint para receber os dados da confirmação de reserva
router.post('/queue_email', async (req, res) => {
  const { message_id, subject, from_email, sent_date, reservation_details } = req.body;

  console.log("infos: ", req.body);

  // Validação dos dados recebidos
  if (!message_id || !from_email || !sent_date) {
    return res.status(400).json({ error: "Todos os campos 'message_id', 'subject', 'from_email', 'sent_date' e 'reservation_details' são obrigatórios." });
  }

  // Estrutura de dados a ser armazenada no json-server
  const reservationData = {
    id: message_id,
    subject: subject,
    from_email: from_email,
    sent_date: sent_date,
    reservation_details: reservation_details,
    createdAt: new Date().toISOString()
  };

  try {
    // Enviar os dados para o json-server
    const response = await axios.post(JSON_SERVER_URL, reservationData);
    res.status(201).json({ success: true, data: response.data });
  } catch (error) {
    console.error("Erro ao salvar no json-server:", error.message);
    res.status(500).json({ error: "Não foi possível armazenar os dados da reserva." });
  }
});


// Rota para confirmar a reserva
router.post('/confirm-reservation', async (req, res) => {
  const { reservationId } = req.body;

  if (!reservationId) {
    return res.status(400).json({ error: "O campo 'reservationId' é obrigatório." });
  }

  try {
    // Enviar requisição POST para o serviço de confirmação de e-mail
    const response = await axios.post(REPLY_EMAIL_URL, { message_id: reservationId });

    // Verificar se a resposta foi bem-sucedida
    if (response.status === 200) {
      res.status(200).json({ success: true, message: `Reserva ${reservationId} confirmada com sucesso.` });
    } else {
      console.error(`Erro ao confirmar a reserva ${reservationId}: Código de status ${response.status}`);
      res.status(500).json({ error: "Não foi possível confirmar a reserva. Tente novamente." });
    }
  } catch (error) {
    console.error(`Erro ao confirmar a reserva ${reservationId}:`, error.message, error.response?.data);
    res.status(500).json({ error: "Não foi possível confirmar a reserva. Tente novamente." });
  }
});


// Rota para rejeitar a reserva
router.post('/reject-reservation', async (req, res) => {
  const { reservationId } = req.body;

  if (!reservationId) {
    return res.status(400).json({ error: "O campo 'reservationId' é obrigatório." });
  }

  try {
    // Enviar requisição DELETE para o json-server
    const response = await axios.delete(`${JSON_SERVER_URL}/${reservationId}`);

    // Verificar se o DELETE foi bem-sucedido
    if (response.status === 200) {
      res.status(200).json({ success: true, message: `Reserva ${reservationId} rejeitada com sucesso.` });
    } else {
      console.error(`Erro ao rejeitar a reserva ${reservationId}: Código de status ${response.status}`);
      res.status(500).json({ error: "Não foi possível rejeitar a reserva. Tente novamente." });
    }
  } catch (error) {
    console.error(`Erro ao rejeitar a reserva ${reservationId}:`, error.message, error.response?.data);
    res.status(500).json({ error: "Não foi possível rejeitar a reserva. Tente novamente." });
  }
});

module.exports = router;
