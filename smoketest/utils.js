let utils = (function () {

    function loadXMLDoc(filename) {
        return loadDoc(filename, "document")
    }

    function loadDoc(filename, type) {
        let xhttp;

        if (window.ActiveXObject) {
            xhttp = new ActiveXObject("Msxml2.XMLHTTP");
        }
        else {
            xhttp = new XMLHttpRequest();
        }

        try {
            xhttp.open("GET", filename, false);
            if (type) {
                xhttp.responseType = type;
             }
        } catch (err) {
            // console.log('error');
        }

        xhttp.send("");

        return {
            response: xhttp.responseXML ? xhttp.responseXML : xhttp.responseText,
            responseType: xhttp.responseType,
            status: xhttp.status
        };
    }

    function getResult(filename) {
        let xml = loadXMLDoc(filename);

        if (xml.status === 404) {
            return false;
        }
        return xml;

    }

    function displayXMLResult(xml, xsl, elementId) {
        var xsl = loadXMLDoc(xsl);
        // code for IE
        let xsltProcessor = new XSLTProcessor();
        if (xml) {
            xsltProcessor.importStylesheet(xsl.response);
            let resultDocument = xsltProcessor.transformToFragment(xml.response, document);
            document.getElementById(elementId).appendChild(resultDocument);
        } else {
            let p = document.createElement('div');
            document.getElementById(elementId).appendChild(p);
        }

    }

    function getIpAddresses(file) {
        let xml = loadXMLDoc(file),
            xmlDoc = xml.response,
            addressTags = xmlDoc.getElementsByTagName('ipAddress'),
            ipAddresses = [];
        if(addressTags) {
            for (let i = 0; i < addressTags.length; i++) {
                ipAddresses.push({ipAddress: addressTags[i].innerHTML,
                                  location: addressTags[i].attributes.location.value});
            }
        }

        return ipAddresses;
    }

    let getXMLTagValue = (file, tag) => {
        let xml = loadXMLDoc(file),
            xmlDoc = xml.response,
            addressTags = xmlDoc.getElementsByTagName(tag),
            ipAddresses = [];

        for (let i = 0; i < addressTags.length; i++) {
            ipAddresses.push(addressTags[i].innerHTML);
        }

        return ipAddresses;
    }

    let removeEmptyItemsFromArr = (arr) => {
        var newArr = [];

        for(var a in arr) {
            if(arr[a] !== "") {
                newArr.push(arr[a]);
            }
        }
        return newArr;
    };

    var monthMap = {
        'January' : 0,
        'February' : 1,
        'March': 2,
        'April' : 3,
        'May' : 4,
        'June': 5,
        'July': 6,
        'August': 7,
        'September': 8,
        'October': 9,
        'November': 10,
        'December': 11};

    let parseDate = (dStr) => {
        let parts = dStr.split('_');
        return new Date(parseInt(parts[2]), monthMap[parts[1]], parseInt(parts[0])).getTime();
    };

    let getTestRunInfo = (data) => {
        let runInfo = [];
        let runArrays = {};

        if(data !== undefined) {
            let splitDates = data.response.split('\n');
            let newDatesArr = removeEmptyItemsFromArr(splitDates);
            let runNumberArr = [];

            for (let d in newDatesArr) {
                let date = newDatesArr[d].split('/')[0];
                let runNumber = newDatesArr[d].split('/')[1];

                let runs = runArrays[date] = runArrays[date] || [];
                if (runs.length === 0) {
                    runInfo.push({date, runs})
                }
                runs.push (runNumber);
            }
        }

        runInfo.forEach(function (info) {
            info.runs.sort(function (x, y) {
                return parseInt(y) - parseInt(x);
            });

        });

        runInfo.sort(function (x, y) {
            return parseDate(y.date) - parseDate(x.date);
        });
        return runInfo;
    };


    function loadNewResults(date) {
        displayXMLResult("logs/smoketestDatesOrig.xml", 'results.xsl', 'tests');
//        display
    }


    function makeListElem(ulEle, run, date) {
        let ipAddresses = getIpAddresses('/smoketest/logs/' + date + '/' + run + '/' + 'ip-addresses.xml');

        let individualRes = {};
        let perIpResults = [];

        let runNumberContainer = document.createElement('div');
        runNumberContainer.setAttribute('class', 'runNumberContainer');

        let runNumDiv = document.createElement('div');
        runNumDiv.setAttribute('class', 'runNumDiv');

        let totalErrors = 0;
        let totalTests = 0;
        let summary = {};

        ipAddresses.forEach(function (ip) {
            let testResult = loadXMLDoc('/smoketest/' + ip.location +'/' + 'testresult.xml');

            let testResultXml = testResult.response;
            if (!testResultXml.getElementsByTagName) {
                return;
            }
            let errorCountEle = testResultXml.getElementsByTagName('errorCount');
            let totalErrorCountEle = testResultXml.getElementsByTagName('totalTestCount');

            let testCount = parseInt(totalErrorCountEle[0].getAttribute('totalTestCount'));
            let errorCount = parseInt(errorCountEle[0].getAttribute('errorCount'));

            individualRes = {totalErrorCount: errorCount, totalTestCount: testCount};
            perIpResults.push({ip, totalErrorCount: errorCount, totalTestCount: testCount});

            totalErrors += errorCount;
            totalTests += testCount;
            summary = {errors: totalErrors, runs: totalTests};
        });

        if (Object.keys(individualRes).length === 0) {
            return null;
        }

        let testResultDiv = document.createElement('div');
        testResultDiv.setAttribute('class', 'testResultDiv');
        testResultDiv.innerHTML = summary.runs - summary.errors + ' / ' + summary.runs;
        testResultDiv.setAttribute('class', summary.errors > 0 ? 'test-fail' : 'test-pass');

        let runNumEle = document.createElement('p');
        let result = document.createElement('p');

        runNumEle.innerHTML = run;
        // result.innerHTML = individualRes.totalTestCount - individualRes.totalErrorCount + '/' + individualRes.totalTestCount;

        let resContainer = document.createElement('div');
        resContainer.setAttribute('class', 'resContainer');

        runNumDiv.appendChild(runNumEle);
        testResultDiv.appendChild(result);

        resContainer.appendChild(runNumDiv);
        resContainer.appendChild(testResultDiv);
        runNumberContainer.appendChild(resContainer);


        ipAddresses.forEach(function (ip, cnt) {
            let testResultXML = loadXMLDoc('/smoketest/' + ip.location + '/' + 'testresult.xml');
            let testResultXmlResp = testResultXML.response;
            if (!testResultXmlResp.getElementsByTagName) {
                return;
            }

            let screenshots = [];
            screenshots.push(testResultXmlResp.getElementsByTagName('screenshot'));
            let testResult = perIpResults[cnt];
            let ipAndResDiv = document.createElement('div');
            let ipAddressText = document.createElement('p');
            ipAddressText.innerHTML = ip.ipAddress;

            let ipAddressDiv = document.createElement('div');
            ipAddressDiv.setAttribute('class', 'ipAddressDiv');
            ipAddressDiv.appendChild(ipAddressText);

            let perIpResultDiv = document.createElement('div');
            perIpResultDiv.setAttribute('class', 'perIpResultDiv');
            perIpResultDiv.setAttribute('class',  testResult.totalErrorCount > 0 ? 'test-fail' : 'test-pass');
            perIpResultDiv.innerHTML = testResult.totalTestCount - testResult.totalErrorCount + ' / ' +testResult.totalTestCount

            ipAndResDiv.setAttribute('class', 'ipAndResDiv');
            ipAndResDiv.appendChild(ipAddressDiv);
            ipAndResDiv.appendChild(perIpResultDiv);
            runNumberContainer.appendChild(ipAndResDiv);

            if(testResult.totalErrorCount > 0) {
                if (screenshots.length > 0) {
                    let cnt = 0;
                    screenshots.forEach(function (ipScreenShots) {
                        for (let ss = 0; ss < ipScreenShots.length; ss++) {
                            let screenshotPath = ipScreenShots[ss].getAttribute('path');

                            let screenshotDiv = document.createElement('div');
                            let screenshotLink = document.createElement('a');
                            screenshotLink.setAttribute('data-lightbox', screenshotPath.split('/').pop());

                            screenshotLink.setAttribute('href', screenshotPath);
                            screenshotLink.innerHTML = screenshotPath;

                            screenshotDiv.setAttribute('class', 'screenshotDiv');
                            screenshotDiv.appendChild(screenshotLink);
                            runNumberContainer.appendChild(screenshotDiv);
                            cnt++;

                        }
                    });
                }

            }

        });
            if(totalErrors > 0) {
                runNumberContainer.classList.add('smokeTestFail');
                runNumberContainer.classList.remove('smokeTestPass');
            } else {
                runNumberContainer.classList.add('smokeTestPass');
                runNumberContainer.classList.remove('smokeTestFail');
            }

        return runNumberContainer;
    }

    function loadAndDisplayPage(allTests, testRunInfo) {

        let dates = [];

        let rootEle = document.getElementById('accordion');
        let count = 0;

        testRunInfo.forEach(function(obj){
            let summaryInfo = loadXMLDoc('logs/' + obj.date + '/testsummary.xml');
            let xmlDoc = summaryInfo.response;

            let summaryEle = xmlDoc.getElementsByTagName('summary');
            let totalTestCount = summaryEle[0].getAttribute('totalTestCount');
            let totalErrorCount = summaryEle[0].getAttribute('totalErrorCount');

            let defaultPanelEle = document.createElement("div");
            defaultPanelEle.setAttribute('class', 'card');

            let panelHeadingEle = document.createElement("div");
            panelHeadingEle.setAttribute('class', 'card-header');

            let summaryContainer = document.createElement('div');
            summaryContainer.setAttribute('class', 'summary-container');

            let dateContainer = document.createElement('div');
            dateContainer.setAttribute('class', 'date-container');

            let panelTitleEle = document.createElement("h4");
            panelTitleEle.setAttribute('class', 'panel-title');

            let anchorEle = document.createElement("a");
            anchorEle.setAttribute('data-toggle', 'collapse');
            anchorEle.setAttribute('data-parent', '#accordion');
            anchorEle.setAttribute('href', '#collapse' + count);

            let bodyPanelContainer = document.createElement('div');
            bodyPanelContainer.setAttribute('id', 'collapse' + count);
            bodyPanelContainer.setAttribute('class', 'panel-collapse collapse');
            // bodyPanelContainer.setAttribute('class', 'collapse');
            // bodyPanelContainer.setAttribute('class', 'in');  // uncomment to expand
            count++;

            let overallResultContainer = document.createElement('div');
            // overallResultContainer.setAttribute('class', totalErrorCount > 0 ? 'test-fail' : 'test-pass');
            let ret = totalErrorCount > 0 ? 'test-fail' : 'test-pass'
            overallResultContainer.setAttribute('class', 'overall-result-container ' + ret );

            overallResultContainer.innerHTML = totalTestCount - totalErrorCount + ' / ' + totalTestCount;

            summaryContainer.appendChild(dateContainer);
            summaryContainer.appendChild(overallResultContainer);
            dateContainer.appendChild(panelTitleEle);
            panelHeadingEle.appendChild(summaryContainer);
            defaultPanelEle.appendChild(panelHeadingEle);

            anchorEle.innerHTML = obj.date.replace(/_/g, ' ');
            panelTitleEle.appendChild(anchorEle);

            let panelBodyEle = document.createElement('div');
            panelBodyEle.setAttribute('class', 'card-body');

            let panelheaderContainer = document.createElement('div');

            let runNumHeader = document.createElement('div');
            runNumHeader.innerHTML = "Run #";

            let resultHeader = document.createElement('div');
            resultHeader.setAttribute('class', 'resultHeaderDiv');
            resultHeader.innerHTML = "Result (Success / Total)";

            panelheaderContainer.appendChild(runNumHeader);
            panelheaderContainer.appendChild(resultHeader);

            panelheaderContainer.setAttribute('class', 'panelBodyHeader');

            panelBodyEle.appendChild(panelheaderContainer);

            let individualTestContainer = document.createElement('div');
            individualTestContainer.setAttribute('class', 'individual-test');

            let ulEle = document.createElement('div');

            obj.runs.forEach(function(run) {
                var res = makeListElem(ulEle, run, obj.date);
                if (res) {
                    panelBodyEle.appendChild(res);
                }
            });

            // panelBodyEle.appendChild(ulEle);

            defaultPanelEle.appendChild(bodyPanelContainer);
            bodyPanelContainer.appendChild(panelBodyEle);

            dates.push(obj.date);

            rootEle.appendChild(defaultPanelEle);

        });

//        let doc = loadDoc("logs/smoketestDates2.xml");
//        displayXMLResult(doc, "dates2.xsl", "dates");
    }

    function findNode(node, searchName) {
        for(let index in node.children) {
            if(node.children[index].nodeName === searchName) {
                return node.children[index];
            }
        }
    }

    function doCountResults (node) {
        let msgs = [];
        for (let i = 0; i < node.children.length; i++) {
            let c = node.children[i];
            if (c.localName === 'error') {
                let msg = c.getAttribute('msg');
                if (msg !== '-') {
                    msgs.push(msg)
                }
            }
        }
        return {total: 1, errors: msgs.length > 0 ? 1 : 0, msg:msgs};
    }

    function click(e) {
        let date = $(this).attr('href');
        e.preventDefault();
        $('#tests').empty();
        utils.loadNewResults(utils.getResult(date));
    }

    return {
        getResult: getResult,
        loadNewResults:loadNewResults,
        loadAndDisplayPage: loadAndDisplayPage,
        getIpAddresses: getIpAddresses,
        getTestRunInfo: getTestRunInfo,
        loadDoc: loadDoc
    };
})();