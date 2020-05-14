const express = require('express');
const bodyParser =  require('body-parser');  
const cors = require('cors');
const getFlightsRouter = require('./router/getFlights');

const app = express();
app.use(bodyParser.json());
app.use(cors());
app.use(getFlightsRouter);


app.listen(3001, () =>  { 
    console.log('server running on port 3001'); 
});