function openPanels(id1,id2) {
  	var x = document.getElementById(id1);
  	var y = document.getElementById(id2);
		x.style.display = "none";
		y.style.display = "block";
		window.myLineChart = [1,2,3,4,5,6];

}
function expandMenu(id1, id2, id3, id4, id5) {
    var x = document.getElementById(id1);
  	var y = document.getElementById(id2);
  	var z = document.getElementById(id3);
  	var a = document.getElementById(id4);
  	var b = document.getElementById(id5);
  	    x.style.display = "none";
		y.style.display = "flex";
		z.classList.toggle("box-expanded");
		a.classList.toggle("expand-btn-show");
		b.classList.toggle("expand-btn-show");
}
function togglePanels(id1, id2) {
    var x = document.getElementById(id1);
  	var y = document.getElementById(id2);
  	    x.style.display = "none";
		y.style.display = "block";
}

function displayEntry(id1, id2, entryid) {
    var x = document.getElementById(id1);
  	var y = document.getElementById(id2);
  	    x.style.display = "none";
		y.style.display = "block";
		console.log(entryid);
		createGraph(entryid, id1);
		createTables(entryid, id1);
}

function showEntries(id1, id2) {
    var x = document.getElementById(id1);
  	var y = document.getElementById(id2);
  	    x.style.display = "none";
		y.style.display = "block";
}

function toggle(id1, id2) {
    var x = document.getElementById(id1);
  	var y = document.getElementById(id2);
  	    x.style.display = "none";
		y.style.display = "block";
}

function createTables(entryid, id1) {
    var buy = JSON.parse(document.getElementById(entryid).dataset.buy);
    var sell = JSON.parse(document.getElementById(entryid).dataset.sell);
    var money = JSON.parse(document.getElementById(entryid).dataset.money);
    var ticker = JSON.parse(document.getElementById(entryid).dataset.ticker);
    var period = JSON.parse(document.getElementById(entryid).dataset.period);
    var interval = JSON.parse(document.getElementById(entryid).dataset.interval);
    var avlength = JSON.parse(document.getElementById(entryid).dataset.avlength);
    var finalmoney = JSON.parse(document.getElementById(entryid).dataset.finalmoney);
    var finalowned = JSON.parse(document.getElementById(entryid).dataset.finalowned);
    var finalliquid = JSON.parse(document.getElementById(entryid).dataset.finalliquid);
    var tt = JSON.parse(document.getElementById(entryid).dataset.tt);
    var prefix = id1.slice(id1.length - 2);
    document.getElementById(prefix+"money").innerHTML = money;
    document.getElementById(prefix+"ticker").innerHTML = ticker;
    document.getElementById(prefix+"period").innerHTML = period;
    if (avlength == null) {
        document.getElementById(prefix+"label").innerHTML = 'Interval';
        document.getElementById(prefix+"avint").innerHTML = interval;
    } else if (avlength != null){
        document.getElementById(prefix+"label").innerHTML = 'Average';
        document.getElementById(prefix+"avint").innerHTML = (avlength + ' days');
    }
    document.getElementById(prefix+"buy").innerHTML = buy;
    document.getElementById(prefix+"sell").innerHTML = sell;
    document.getElementById(prefix+"ebalance").innerHTML = finalmoney;
    document.getElementById(prefix+"eshares").innerHTML = finalowned;
    document.getElementById(prefix+"lebalance").innerHTML = finalliquid;
    document.getElementById(prefix+"trades").innerHTML = money;
    document.getElementById(prefix+"buys").innerHTML = money;
    document.getElementById(prefix+"sells").innerHTML = money;
}

function createGraph(entryid, id1) {
    var buy = JSON.parse(document.getElementById(entryid).dataset.buy);
    var sell = JSON.parse(document.getElementById(entryid).dataset.sell);
    var td = JSON.parse(document.getElementById(entryid).dataset.td);
    var tt = JSON.parse(document.getElementById(entryid).dataset.tt);
    var tradetype = JSON.parse(document.getElementById(entryid).dataset.ty);
    var tradeprice = JSON.parse(document.getElementById(entryid).dataset.tp);
    var wmax = JSON.parse(document.getElementById(entryid).dataset.wmax);
    var wmay = JSON.parse(document.getElementById(entryid).dataset.wmay);
    var axis_dt = [];
    var i;
    var dt = '';
    var hold;
    for (i = 0; i < td.length; i++) {
        var date = td[i];
        var time = tt[i];
        hold = dt.concat(date.slice(6,10),'-', date.slice(3,5),'-',date.slice(0,2),'T',time,':00');
        axis_dt.push(hold);
        dt='';
    }
    var high = Math.max.apply(Math, tradeprice);
    var low = Math.min.apply(Math, tradeprice);
    var range = (high - low);
    var min = (low - (range/2));
    var max = (high + (range/2));
    var datetime = axis_dt;
    var pointBackgroundColors = [];
    var dataset = new Array();
    for (i=0; i< datetime.length; i++){
        var dict = { x: datetime[i], y: tradeprice[i]}
        dataset.push(dict)
    }
    var ma_dataset = new Array();
    for (i=0; i< wmax.length; i++){
        var dict = { x: wmax[i], y: wmay[i]}
        ma_dataset.push(dict)
    }
    var prefix = id1.slice(id1.length - 2);
    var arrpos = (parseInt(id1.slice(id1.length - 1)) - 1);
    var arr = [1,2,3,4,5,6];
    if (! arr.includes(window.myLineChart[arrpos])){
        window.myLineChart[arrpos].destroy();
    }
    var ctx = document.getElementById(prefix+'Chart');
    window.myLineChart[arrpos] = new Chart(ctx, {
        type: 'line',
        data:     {
            datasets: [
                {
                    data: dataset,
                    pointBackgroundColor: pointBackgroundColors,
                    fill: false,
                    lineTension: 0,
                    borderColor: "#2d6886"
                },
                {
                data: ma_dataset,
                pointRadius: 0,
                fill: false,
                lineTension: 0,
                borderColor: "#4095BF",
                label: "Moving Average"
            },
            ]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    },
                    gridLines: {
                        display:false
                    }
                    }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Price [$]'
                    },
                    display: true,
                    ticks: {
                        min: min,
                        max: max
                    }
                }]
            },
            legend: {
                display: false,
            }
        }
    });
    for (i = 0; i < myLineChart[arrpos].data.datasets[0].data.length; i++) {
        if (tradetype[i] == 's') {
            pointBackgroundColors.push("#90EE90");
        } else {
            pointBackgroundColors.push("red");
        }
    }
    myLineChart[arrpos].update();

}