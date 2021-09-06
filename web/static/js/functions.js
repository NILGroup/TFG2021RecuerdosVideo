function copyToClipboard(id){
  var copyText = document.getElementById(id);

  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  navigator.clipboard.writeText(copyText.value);

}