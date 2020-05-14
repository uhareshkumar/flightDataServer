const express = require('express');
const bodyParser =  require('body-parser');  

const getFlightsRouter = require('./router/getFlights');

const app = express();
app.use(bodyParser.json());
app.use(getFlightsRouter);

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    next();
});

app.listen(3001, () =>  { 
    console.log('server running on port 3001'); 
});