const axios = require('axios');

// Configura a URL base para o JSON Server
const API_URL = 'http://localhost:3009';

/**
 * Função GET: Obter todos os registros de uma coleção
 * @param {string} collection - Nome da coleção (ex: 'reservations')
 * @returns {Promise} - Dados da resposta
 */
async function getAll(collection) {
  try {
    const response = await axios.get(`${API_URL}/${collection}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao obter ${collection}:`, error);
    throw error;
  }
}

/**
 * Função GET por ID: Obter um registro específico de uma coleção
 * @param {string} collection - Nome da coleção (ex: 'reservations')
 * @param {number} id - ID do registro
 * @returns {Promise} - Dados da resposta
 */
async function getById(collection, id) {
  try {
    const response = await axios.get(`${API_URL}/${collection}/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao obter ${collection} com ID ${id}:`, error);
    throw error;
  }
}

/**
 * Função POST: Criar um novo registro em uma coleção
 * @param {string} collection - Nome da coleção (ex: 'reservations')
 * @param {Object} data - Dados do novo registro
 * @returns {Promise} - Dados da resposta
 */
async function create(collection, data) {
  try {
    const response = await axios.post(`${API_URL}/${collection}`, data);
    return response.data;
  } catch (error) {
    console.error(`Erro ao criar novo registro em ${collection}:`, error);
    throw error;
  }
}

/**
 * Função PUT: Atualizar um registro existente em uma coleção
 * @param {string} collection - Nome da coleção (ex: 'reservations')
 * @param {number} id - ID do registro a ser atualizado
 * @param {Object} data - Dados para atualizar
 * @returns {Promise} - Dados da resposta
 */
async function update(collection, id, data) {
  try {
    const response = await axios.put(`${API_URL}/${collection}/${id}`, data);
    return response.data;
  } catch (error) {
    console.error(`Erro ao atualizar ${collection} com ID ${id}:`, error);
    throw error;
  }
}

/**
 * Função DELETE: Remover um registro de uma coleção
 * @param {string} collection - Nome da coleção (ex: 'reservations')
 * @param {number} id - ID do registro a ser removido
 * @returns {Promise} - Dados da resposta
 */
async function remove(collection, id) {
  try {
    const response = await axios.delete(`${API_URL}/${collection}/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Erro ao remover ${collection} com ID ${id}:`, error);
    throw error;
  }
}

// Exporta as funções para uso em outros arquivos
module.exports = {
  getAll,
  getById,
  create,
  update,
  remove
};
