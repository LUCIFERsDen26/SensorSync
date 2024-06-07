const headers = {
  'Content-Type': 'application/json'
};

let chartQI; // Move the chart object out of the function so that it can be destroyed and re-created

function updateGraphQIndex() {
  const state = document.getElementById("state-select").value;

  fetch(`/api/StateData/${state}`, {
      method: 'GET',
      headers: headers
    })
    .then(response => response.json())
    .then(data => {
      const x = data.data.map(d => d.month_name);
      const y = data.data.map(d => d.Qindex);

      const chart_data = {
        labels: x,
        datasets: [{
          label: `QIndex of ${state}`,
          backgroundColor: 'rgb(255, 99, 132)',
          borderColor: 'rgb(255, 99, 132)',
          data: y,
        }]
      };

      const config = {
        type: 'line',
        data: chart_data,
        options: {}
      };

      const linechartElement = document.getElementById('linechart');
      if (chartQI) chartQI.destroy(); // Destroy the old chart object before creating a new one
      chartQI = new Chart(linechartElement, config);
    })
    .catch(error => console.error(error));
}

fetch('/api/StateCount', {
    method: 'GET',
    headers: headers
  })
  .then(response => response.json())
  .then(data => {
    const x = data.data.map(d => d.state_name);
    const y = data.data.map(d => d.count);

    const chart_data = {
      labels: x,
      datasets: [{
        label: 'State Count',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: y,
      }]
    };

    const config = {
      type: 'bar',
      data: chart_data,
      options: {},
    };

    const stateCount = new Chart(document.getElementById('barchart'), config);
    console.log(config);
  })
  .catch(error => console.error(error));


const graphData = {
  x: [],
  y: []
};

const graphchart = document.getElementById('Graphline');
const graphconfig = {
  type: 'line',
  data: {
    labels: graphData.x,
    datasets: [{
      label: 'Sensor Value',  
      data: graphData.y,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    scales: {
      y: {
        suggestedMin: -10,
        suggestedMax: 10
      }
    }
  }
};

let chartRTC = new Chart(graphchart, graphconfig);

function updateGraphRTC() {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      const data = JSON.parse(this.responseText);
      const newDataX = data.data.map(d => d.x_value);
      const newDataY = data.data.map(d => d.y_value);

      // Clear the first 7 values
      graphData.x.splice(0, 7);
      graphData.y.splice(0, 7);

      // Move the remaining values to the left
      for (let i = 0; i < 8; i++) {
        graphData.x[i] = graphData.x[i + 7];
        graphData.y[i] = graphData.y[i + 7];
      }

      // append new data to end of array
      graphData.x.push(...newDataX);
      graphData.y.push(...newDataY);

      // update chart with new data
      chartRTC.data.labels = graphData.x;
      chartRTC.data.datasets[0].data = graphData.y;
      chartRTC.update();
    }
  };
  xhttp.open("GET", "/api/graph", true);
  xhttp.send();
}

// update graph every 5 seconds




const waveData = {
  x: [],
  y: []
};

const wavechart = document.getElementById('Waveline');
const waveconfig = {
  type: 'line',
  data: {
    labels: waveData.x,
    datasets: [{
      label: 'Waveform',  
      data: waveData.y,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  },
  options: {
    scales: {
      y: {
        suggestedMin: -10,
        suggestedMax: 10
      }
    }
  }
};

let wavechartRTC = new Chart(wavechart, waveconfig);

function updateWaveRTC() {
  const xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      const data = JSON.parse(this.responseText);
      const newDataX = data.data.map(d => d.x_value);
      const newDataY = data.data.map(d => d.y_value);

      // Clear the first 7 values
      waveData.x.splice(0, 7);
      waveData.y.splice(0, 7);

      // Move the remaining values to the left
      for (let i = 0; i < 8; i++) {
        waveData.x[i] = waveData.x[i + 7];
        waveData.y[i] = waveData.y[i + 7];
      }

      // append new data to end of array
      waveData.x.push(...newDataX);
      waveData.y.push(...newDataY);

      // update chart with new data
      wavechartRTC.data.labels = waveData.x;
      wavechartRTC.data.datasets[0].data = waveData.y;
      wavechartRTC.update();
    }
  };
  xhttp.open("GET", "/api/wave", true);
  xhttp.send();
}

function atonce(){
    updateGraphRTC();
    updateWaveRTC();
}

setInterval(atonce, 3000);

function onloadfun(){
    updateGraphQIndex();
    
}

