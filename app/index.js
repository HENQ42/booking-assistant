const express = require('express');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

const app = express();

// Middleware para lidar com dados de formulário
app.use(express.urlencoded({ extended: true }));
app.use(express.json()); // Suporte para JSON, se necessário

// Configuração do EJS como view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Servir arquivos estáticos da pasta 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Caminho para a pasta 'routes'
const routesDir = path.join(__dirname, 'routes');

// Verificar se existe um 'index.js' diretamente dentro de 'routes'
const rootRoutePath = path.join(routesDir, 'index.js');
if (fs.existsSync(rootRoutePath)) {
  const rootRoute = require(rootRoutePath);
  app.use('/', rootRoute);
}

// Função para obter todas as pastas dentro de 'routes'
function getDirectories(source) {
  return fs.readdirSync(source).filter(name => {
    const fullPath = path.join(source, name);
    return fs.lstatSync(fullPath).isDirectory();
  });
}

// Obter todas as pastas em 'routes'
const routeFolders = getDirectories(routesDir);

// Mapear cada rota dinamicamente
routeFolders.forEach(folder => {
  const routePath = `/${folder}`; // Define o caminho da rota, ex: '/user', '/admin'
  const route = require(path.join(routesDir, folder, 'index.js')); // Importa o index.js da pasta
  app.use(routePath, route); // Usa o roteador para a rota específica
});

// Porta configurada no arquivo .env ou padrão para 3000
// const PORT = process.env.PORT || 3000;
const PORT = 5001;
app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
