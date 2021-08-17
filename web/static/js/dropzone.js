Dropzone.options.dropper = {
    paramName: 'file',
    maxFiles: 1,
    chunking: true,
    forceChunking: true,
    url: '/subirFichero',
    parallelChunkUploads: true,
    timeout: 1200000,
    maxFilesize: 4000, // megabytes
    chunkSize: 200000000, // bytes
    dictDefaultMessage: "Arrastra el archivo o haz click",
    init: function() {
      this.on('addedfile', function(file) {
        if (this.files.length > 1) {
          this.removeFile(this.files[0]);
        }
      });

      this.on('success', function(file){

        var response = JSON.parse(file.xhr.response);
        document.getElementById("resultados").style.visibility = 'visible';
        let error = "";

        if(typeof response["summary"] !== 'undefined')
            document.getElementById("summary").innerHTML = response["summary"];
        else
            error = "Hubo un problema al generar el resumen.";

        if(typeof response["transcript"] !== 'undefined')
            document.getElementById("transcript").innerHTML = response["transcript"];
        else
            error += "<br>Hubo un problema al generar la transcripcion.";

        if (error !== ""){
            ele = document.getElementById("error");
            ele.style.visibility = 'visible';
            ele.innerHTML = "ERROR INESPERADO. Pruebe a intentarlo de nuevo. <br>" + error;
        }

      })
    }
}