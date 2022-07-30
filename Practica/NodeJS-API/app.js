const express = require('express');
const mysql = require('mysql');

const bodyParser = require('body-parser');

const PORT = process.env.PORT || 3000;

const app = express();

app.use(bodyParser.json());

// MySql
// const connection = mysql.createConnection({
//   host: 'database-1.ct4jfvgo8r4m.us-east-1.rds.amazonaws.com',
//   user: 'admin',
//   password: 'admin12345',
//   database: 'sys'
// });

// Route
app.get('/', (req, res) => {
  res.send('Welcome to my API!');
});

// --------------------------------------------USUARIOS------------------------------------------------
app.get('/getUsuarios', (req, res) => {
  const sql = 'SELECT * FROM usuario';

  // connection.query(sql, (error, results) => {
  //   if (error) throw error;
  //   if (results.length > 0) {
  //     res.json(results);
  //   } else {
  //     res.send('Not result');
  //   }
  // });
});

app.post('/login', (req, res) => {
    const { usuario, contrasena } = req.body;
    const sql = `SELECT * FROM usuario WHERE usuario = "${usuario}" AND contrasena = "${contrasena}"`;
    console.log("SSSSSS");
    res.send('Not result');
    
  });

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));