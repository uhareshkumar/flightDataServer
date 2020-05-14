const express = require('express');
const router = express.Router();
const spawn = require("child_process").spawn;

router.post('/getFlights', async(req, res) => {

    const {
        dateInNum, month, year,
        fromAirportCity, fromAirportCode, fromCountryName, fromCountryCode,
        toAirportCity, toAirportCode, toCountryName, toCountryCode
    } = req.body;

    var process = await spawn('python',["./searchFlights.py", 
                            dateInNum, month, year,
                            fromAirportCity, fromAirportCode, fromCountryName, fromCountryCode,
                            toAirportCity, toAirportCode, toCountryName, toCountryCode] ); 
    
    process.stdout.on('data', function(data) {
        const scrapeResult = data.toString().split('\n'); 
        const flightData = {
            paytmUrl: scrapeResult[0],
            yatraUrl: scrapeResult[1],
            goibiboUrl: scrapeResult[2],
            details: []
        };

        for(let i=3; i<scrapeResult.length-1; i = i+ 7) {
            
            var cars = [scrapeResult[i+4], scrapeResult[i+5], scrapeResult[i+6]];

            for(let j=0;j<3;j++) {
            	cars[j] = cars[j].replace(/,/g,'');
                cars[j] = cars[j].replace('Not Found','1111111111');
               	cars[j] = parseInt(cars[j]);
            }

            var paytmPrice = cars[0];
            var yatraPrice = cars[1];
            var goibiboPrice = cars[2];

            var bestPrice = {
            	price: paytmPrice,
                company: 'paytm',
                url: flightData.paytmUrl,
                priceInString: scrapeResult[i+4]
            }

            if(bestPrice.price >= yatraPrice) {
               	bestPrice.price = yatraPrice;
                bestPrice.company = 'yatra';
                bestPrice.url = flightData.yatraUrl;
                bestPrice.priceInString = scrapeResult[i+5];  
            }
            if(bestPrice.price > goibiboPrice){
            	bestPrice.price = goibiboPrice;
                bestPrice.company = 'goibibo';
                bestPrice.url = flightData.goibiboUrl;
                bestPrice.priceInString = scrapeResult[i+6];
            }

            flightData.details[flightData.details.length] = {
                flightName: scrapeResult[i],
                departureTime: scrapeResult[i+1],
                arrivalTime: scrapeResult[i+2],
                duration: scrapeResult[i+3],
                paytmPrice: scrapeResult[i+4],
                yatraPrice: scrapeResult[i+5],
                goibiboPrice: scrapeResult[i+6],
                bestPrice: bestPrice
            };
        }
        
        res.send(flightData);        
    });
});

module.exports = router;