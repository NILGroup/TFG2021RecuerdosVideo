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
        var response = JSON.parse(file.xhr.response)
        if(typeof response["summary"] !== 'undefined' || typeof response["transcript"] !== 'undefined'){
          document.getElementById("summary").innerHTML = response["summary"]
          document.getElementById("transcript").innerHTML = response["transcript"]
        }else{
            //Poner algún tipo de mensaje de error bonito en la página con CSS y eso
            //A veces se devuelve strings vacias en la respuesta, en ese caso decir qeu se vuelva a intentar y que hubo un error inesperado.
        }

      })
    }
}