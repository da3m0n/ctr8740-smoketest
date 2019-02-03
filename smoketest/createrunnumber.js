const fs = require('fs');
const path = require('path');
const http = require('http');
const process = require('process');

let getDateRunInfo = (dateFolder) => {

    let logs = process.cwd() + "/logs";
    let dateRunInfo = [];
    let res = {};

    res[dateFolder] = {maxNumber: 0};

        console.log("getting run info exists", path.join(logs, dateFolder));
    if (fs.existsSync(path.join(logs, dateFolder))) {
        let lastRunNumbers = fs.readdirSync(path.join(logs,dateFolder));
        let max =  lastRunNumbers.reduce(function (c, x) {

            if (/^\d+$/.test(x)) {
                return Math.max(c, parseInt(x));
            }
            return c
        }, 0);
        res[dateFolder] = {maxNumber: max};
    }

    console.log('res', res);
    return res;
};

let makeDate = () => {
    let date = new Date();
    let day = date.getDate();
    let month = date.getMonth();
    let year = date.getFullYear();
    let monthNames = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ];

    function pad(n) {
        return n < 10 ? '0' + n : n;
    }

    return pad(day) + '_' + monthNames[month] + '_' + year;

};

// Create an instance of the http server to handle HTTP requests
let dateRunInfo = getDateRunInfo(makeDate());

let app = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/plain'});

    if (req.url === '/next') {
        let currentDate =  makeDate();
        if (dateRunInfo[currentDate] === undefined) {
            dateRunInfo = getDateRunInfo(currentDate);
        }
        dateRunInfo[currentDate].maxNumber++;
        res.end('' + currentDate + '/' + dateRunInfo[currentDate].maxNumber);
    }
    else {
        res.end('no number');
    }
});


// Start the server on port 3000
app.listen(3000, '127.0.0.1');
console.log('Node server running on port 3000');