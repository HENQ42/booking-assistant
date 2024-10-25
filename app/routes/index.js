const express = require('express');
const axios = require('axios');
const router = express.Router();

// Rota para exibir a página inicial com as reservas
router.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://localhost:5005/reservations');
    // console.log("response: ", response); //debug

    const reservations = response.data;
    console.log("reservations: ", reservations);//debug

    res.render('main/index', { reservations }); // Renderiza a view index.ejs com as reservas
  } catch (error) {
    console.error('Erro ao obter reservas:', error);
    res.render('index', { reservations: [] }); // Renderiza uma página vazia em caso de erro
  }
});

module.exports = router;