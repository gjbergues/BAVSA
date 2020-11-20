
function getRandomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function ordenar(items,pos){
  items.sort(function (a, b) {
    if (a[pos] < b[pos]) {
      return 1;
    }
    if (a[pos] > b[pos]) {
      return -1;
    }
    // a must be equal to b
    return 0;
  });
}

  var items = [
    { name: 'Edward', value: 21 },
    { name: 'Sharpe', value: 37 },
    { name: 'And', value: 45 },
    { name: 'The', value: -12 },
    { name: 'Magnetic', value: 13 },
    { name: 'Zeros', value: 37 }
  ];

ordenar(items,'value')

function graficar(tabla,desierta){

  var arr = [], arrLabels=[], arrDatos=[], arrColors=[];

  desierta = desierta?1:2;

  for(let fila in tabla){
    fila = tabla[fila];
    if(fila[0] && fila[desierta]*1){
      arr.push({
        dato:fila[desierta]*1,
        label:fila[0],
        color:getRandomColor()
      })
    }
  }

  ordenar(arr,'dato');

  for(let o of arr){
    arrLabels.push(o.label);
    arrDatos.push(o.dato);
    arrColors.push(o.color);
  }

  var canvas = document.createElement('canvas'),
      grafico = document.getElementById("graficos");

  canvas.width="800";
  canvas.height="400";

  grafico.innerHTML = '';
  grafico.append(canvas);

  if(arrDatos.length)
    new Chart(canvas, {
        type: 'horizontalBar',
        data: {
          labels: arrLabels,
          datasets: [{
            label: "SGR",
            backgroundColor: arrColors,
            data: arrDatos
          }]
        },
        options: {
          responsive: true,
          legend: {
             position: 'left',
           },
          title: {
            display: true,
            text: ''
          }
        }
    });
}
