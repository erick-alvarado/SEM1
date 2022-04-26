const express = require('express');
const mysql = require('mysql');

const bodyParser = require('body-parser');

const PORT = process.env.PORT || 3000;

const app = express();

app.use(bodyParser.json());

// MySql
const connection = mysql.createConnection({
  host: 'database-1.ct4jfvgo8r4m.us-east-1.rds.amazonaws.com',
  user: 'admin',
  password: 'admin12345',
  database: 'sys'
});

// Route
app.get('/', (req, res) => {
  res.send('Welcome to my API!');
});

// --------------------------------------------USUARIOS------------------------------------------------
app.get('/getUsuarios', (req, res) => {
  const sql = 'SELECT * FROM usuario';

  connection.query(sql, (error, results) => {
    if (error) throw error;
    if (results.length > 0) {
      res.json(results);
    } else {
      res.send('Not result');
    }
  });
});

app.post('/login', (req, res) => {
    const { usuario, contrasena } = req.body;
    const sql = `SELECT * FROM usuario WHERE usuario = "${usuario}" AND contrasena = "${contrasena}"`;
    connection.query(sql, (error, result) => {
      if (error) throw error;
  
      if (result.length > 0) {
        res.json(result);
      } else {
        res.send('Not result');
      }
    });
  });

  app.post('/acrearUsuario', (req, res) => {
    const sql = 'INSERT INTO usuario SET ?';
  
    const customerObj = {
      usuario: req.body.usuario,
      contrasena: req.body.contrasena,
      nombre: req.body.nombre
    };
  
    connection.query(sql, customerObj, error => {
      if (error) throw error;
      res.send('Usuario created!');
      res.json(result);
    });
  });

//----------------------
app.post('/register', (req, res) => {
    const { usuario, contrasena, nombre } = req.body;
    const sql = `INSERT INTO usuario (usuario, contrasena, nombre) VALUES ("${usuario}","${contrasena}", "${nombre}")`;
    const sql2 = `SELECT id_usuario FROM Usuario WHERE usuario = "${usuario}"`;
    //const sql3 = `INSERT INTO album (nombre, id_usuario) VALUES ("Foto_perfil","${contrasena}", "${nombre}")`;

    connection.query(sql, (error, result) => {
      if (error) throw error;
      res.send('Usuario created!');   
      
      connection.query(sql2, (error, result2) => {
        if (error) throw error; 
        console.log(result2); 
        res.send(result2.body);     
        //res.json(result2.body);    
      });
    });

    

  });


  app.post('/crearUsuario', (req, res) => {
    const { usuario, contrasena, nombre } = req.body;
    const sql = `INSERT INTO usuario (usuario, contrasena, nombre) VALUES ("${usuario}","${contrasena}", "${nombre}")`;
    

    connection.query(sql, (error, result) => {
      if (error) throw error;
      res.send('Usuario created!');      
    });
  });



app.get('/customers/:id', (req, res) => {
  const { id } = req.params;
  const sql = `SELECT * FROM customers WHERE id = ${id}`;
  connection.query(sql, (error, result) => {
    if (error) throw error;

    if (result.length > 0) {
      res.json(result);
    } else {
      res.send('Not result');
    }
  });
});

app.post('/add', (req, res) => {
  //add
  const sql = 'INSERT INTO usuario SET ?';

  const customerObj = {
    usuario: req.body.usuario,
    contrasena: req.body.contrasena,
    nombre: req.body.nombre
  };

  connection.query(sql, customerObj, error => {
    if (error) throw error;
    res.send('Customer created!');
  });
});

app.put('/subir-foto', (req, res) => {
  //update/:id
  const { id } = req.params;
  const { name, city } = req.body;
  const sql = `UPDATE customers SET name = '${name}', city='${city}' WHERE id =${id}`;

  connection.query(sql, error => {
    if (error) throw error;
    res.send('Customer updated!');
  });
});

app.delete('/delete/:id', (req, res) => {
  ///delete/:id
  const { id } = req.params;
  const sql = `DELETE FROM customers WHERE id= ${id}`;

  connection.query(sql, error => {
    if (error) throw error;
    res.send('Delete customer');
  });
});

// Check connect
connection.connect(error => {
  if (error) throw error;
  console.log('Database server running!');
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));