var datas = {},tablas=[];

// Aplicar datatable
$(document).ready(function() {
    // CONTAR
    var h, htmls = document.getElementsByTagName('table'), len=htmls.length;

	while(len--){
        h = htmls[len];
        h.style = 'font-size:13px';
        h.classList.remove("table","table-striped","table-bordered","dt-responsive","nowrap");
        h.classList.add("display","compact","nowrap");
        tablas.push($(htmls[len]).DataTable( {
            responsive:true,
            paging: false,
            ordering: false,
            info: false,
            "oLanguage": {
              "sSearch": "Filtrar"
            },
            "columnDefs": [
                {
                    "targets": [ 0 ],
                    "visible": false,
                    "searchable": false
                }
            ]
        }));
    }

	acomodarTitulosTablas();

    divOpcionesAGE.onchange=tildarUnaUnicaOpcion;
    htmls = document.getElementsByClassName('ocultar'), len=htmls.length;
    while(len--)
      datas[(Object.keys(htmls[len].dataset)[0])]=true;


    window.scrollTo(0, 0);
    main.style.display = "";
    aplicarFiltro();
    setTimeout(()=>{
      divloader.remove();
    },200);

});

function acomodarTitulosTablas(){
	var ths = document.querySelectorAll('thead > tr > th'), len = ths.length;
	while(len--){
		let h = ths[len];
		if(/^[_\d]+$/.test(h.innerText)){
			//ths[len].innerText += ' ';
			ths[len].style=(len%2==0?'color:orange':'');
		}
	}
}

// ocultar
function ocultarHTML(){
    var htmls = document.getElementsByClassName('mostrar'), len=htmls.length;
    while(len--){
      htmls[len].id='';
      htmls[len].classList.add('ocultar');
      htmls[len].classList.remove('mostrar');
    }
}

function mostrarCategorias(filtro){
  var estado=filtro[0].id, ESTADO=estado[0]=='d'?'des':'neg', ane=filtro[1].id,
      ANE = ane=='pag'?'PAGARE':ane.toUpperCase().replace('_',' ');

  var monto = document.querySelector(`[data-monto="monto_${ane}_${ESTADO}"]`),
      valor = document.querySelector(`[data-valor="cheques_${ane}_${ESTADO}"]`),
      tablaizq = document.querySelector(`[data-tablaIzq="${estado} ${ANE}"]`),
      tablaDer = document.querySelector(`[data-tablaDer="${ANE}"]`);


  try {
    monto.classList.add('mostrar');
    monto.classList.remove('ocultar');
    valor.classList.add('mostrar');
    valor.classList.remove('ocultar');

    tablaizq.classList.add('mostrar');
    tablaizq.classList.remove('ocultar');
    tablaDer.classList.add('mostrar');
    tablaDer.classList.remove('ocultar');

    graficar(procesarDatosTabla(tablaDer),estado=='desierta');

  } catch (e) {
    graficar([]);
  }

}

function procesarDatosTabla(table){
  var tabla={}, htable = table.querySelectorAll('tbody>tr'),len=htable.length;
  while(len--){
    let fila = htable[len].children
    tabla[len] = {};
    for (let i = 0; i < fila.length; i++) {
      let celda = fila[i].innerText;
      if(celda=='-'){
        tabla[len][i]=0;
      }else if(/^[\d,.]+$/.test(celda)){
        tabla[len][i] = (celda.replace(/\./g,'').replace(/,\d+$/,''))*1;
      }else {
        tabla[len][i] = celda;
      }
    }
  }
  return tabla;
}

// mostrar
function mostrarHTML(data,filtro){

  var estado=filtro[0].id, ESTADO=estado[0]='d'?'des':'neg', ane=filtro[1].id;

  //monto_cpd_des
  console.log(data,filtro,`[data-monto="monto_${ane}_${ESTADO}"]`);

  //var h = document.querySelector(`[data-${data}="${estado} ${avalado}"]`)

  /*  var estado=filtro[0].id, avalado=filtro[1].id,
        h = document.querySelector(`[data-${data}="${estado} ${avalado}"]`) ||
            document.querySelector(`[data-${data}="${estado}"]`) ||
            document.querySelector(`[data-${data}="${avalado}"]`);
    if(h){
      h.classList.add('mostrar');
      h.classList.remove('ocultar');
    }
    tablas[0].responsive.rebuild();
    tablas[0].responsive.recalc();
    tablas[1].responsive.rebuild();
    tablas[1].responsive.recalc();*/
}

// Filtro para las opciones
function aplicarFiltro(){
  var checks = document.querySelectorAll('input[type="radio"]:checked');
  ocultarHTML();
  mostrarCategorias(checks);
  /*for(let v in datas)
    mostrarHTML(v,checks);*/
}

function tildarUnaUnicaOpcion(e){
  console.log(55555);
  var htmls = divOpcionesAGE.querySelectorAll('input'), len=htmls.length;
  while(len--){
    htmls[len].checked=false;
  }
  e.target.checked=true;
}
