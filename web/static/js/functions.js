function copyToClipboard(id){
  var copyText = document.getElementById(id);

  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  navigator.clipboard.writeText(copyText.value);

}

function disableButton(id){
  document.getElementById(id).disabled = true
}

function enableButton(id){
  document.getElementById(id).disabled = false
}

function renderError(errorMsg){
 $("<div class=\"alert alert-danger\"> " +
     "<h4 class=\"alert-heading\">Ha ocurrido un error</h4>" +
     "<p>"+ errorMsg + "</p>"+
     "<hr>"+
     "<p class=\"mb-0\">Sí introduciste tu correo es posible que encuentres el resultado ahí en unos minutos.</p>"
     +"</div>").appendTo("#resultados")
}