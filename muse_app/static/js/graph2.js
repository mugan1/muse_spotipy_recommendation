$.getJSON("/data.json", data => {
    var playlist = []
    for (var key in data['playlist']) {
        playlist.push(data['playlist'][key])
    }
    var recommend = []
    for (var key in data['recommend']) {
        recommend.push(data['recommend'][key])
    }

    var lineCanvas = document.getElementById("lineChart");

    var lineData = {
        labels: ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "valence"],
        datasets: [{
            label: "Your List",
            fill: true,
            backgroundColor: "rgba(200,0,0,0.2)",
            data: playlist,
        }, {
            label: "Recommended",
            fill: true,
            backgroundColor: "rgba(0,0,200,0.2)",
            data: recommend,
        }]
    };

    var lineChart = new Chart(lineCanvas, {
        type: 'line',
        title: {
            display: true,
            text: 'Compare Line Chart'
        },
        data: lineData,
        options: {
            responsive: true,
        }
    });


});