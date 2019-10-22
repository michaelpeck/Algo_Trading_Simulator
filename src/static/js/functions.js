window.onload = function () {
    function chartData(date_time, type, price){

        var i;
        var dataset = new Array();
        for (i=0; i< date_time.length; i++){
            dataset.push({ x: Date.parse(date_time[i]), y: price[i])})
        }

    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "light2",
        title:{
            text: "Simple Line Chart"
        },
        axisY:{
            includeZero: false
        },
        data: [{
            type: "line",
            xValueType: "dateTime",
            dataPoints: dataset;
        }]
    });
    chart.render();
    }
}