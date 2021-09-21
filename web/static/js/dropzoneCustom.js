Dropzone.options.dropper = {
    paramName: 'file',
    acceptedFiles: '.mp4, .mov, .avi',
    autoProcessQueue: false,
    chunking: true,
    forceChunking: true,
    url: '/subirFichero',
    parallelChunkUploads: true,
    timeout: 0,
    maxFilesize: 4000, // megabytes
    chunkSize: 200000000, // bytes
    dictDefaultMessage: "Arrastra el archivo o haz click",
    dictInvalidFileType: "Solo puedes subir vídeos en formato mp4, mov o avi",
    init: function() {

        this.on('dragover', function(event){
            document.getElementById('dropper').style.background= '#e6f5ff'
        })

         this.on('dragleave', function(event){
            document.getElementById('dropper').style.background= 'white'
        })

         this.on('drop', function(event){
            document.getElementById('dropper').style.background= 'white'
        })

        this.on('error', function(file, errorMessage, xhr){
            $(".dz-error-message").remove()
            if (xhr && xhr.status === 504) {
                renderError("Las limitaciones técnicas del servidor provocaron un error por esperar demasiado una respuesta.")
            }
            else {
                renderError(errorMessage)
            }
        })

        this.on('addedfile', function(file) {
            uploadingFiles = this.getUploadingFiles()
            if (this.files.length > 1 && uploadingFiles.length == 0) {
                this.removeFile(this.files[0]);
                $(":submit").prop("disabled", false);
            }else if (uploadingFiles.length > 0){
                this.removeFile(file)
            }
        });

        dzClosure = this; // Makes sure that 'this' is understood inside the functions below.
        // for Dropzone to process the queue (instead of default form behavior):
        document.getElementById("submit-all").addEventListener("click", function(e) {

            // Make sure that the form isn't actually being sent.
            e.preventDefault();
            e.stopPropagation();
            dzClosure.processQueue();
        });


        this.on("sending", function(data, xhr, formData) {
            $(":submit").prop("disabled", true);
            //$("input").prop("disabled", true);
            $("#resultados").empty()

            formData.append("modoTrancript", jQuery("input[name='modoTrancript']:checked").val());
            formData.append("divideBySpeaker", jQuery("input[name='divideBySpeaker']:checked").val());
            formData.append("divideBySegments", jQuery("input[name='divideBySegments']:checked").val());
            formData.append("sizeSegments", jQuery("input[name='sizeSegments']").val());
            formData.append("email", jQuery("input[name='email']").val());
        });

        this.on("uploadprogress", function(file, progress, bytesSent){
            if(progress === 100 && !$('#load-container').length){
                 $("<div id='load-container'>" + "<div class=\"loader\"></div>" +
                     "<div class=\"alert alert-primary\">El proceso puede tardar varios minutos. Por favor, espere hasta que aparezcan los resultados.</div>\n"
                 +"</div>")
                     .appendTo("#resultados")
            }
        })

        this.on("success", function(file){
            $('<div class="info-action-bar"><h5>Resumen</h5> <button class="btn btn-info" onclick="copyToClipboard(\'summary\')">⧉ Copiar</button> </div>\n' +
                '                <div class="form-group py-2">\n' +
                '                    <textarea class="form-control" id="summary" readonly>\n' +
                '                    </textarea>\n' +
                '                </div>\n' +
                '                <div class="info-action-bar"><h5>Transcripción</h5><button class="btn btn-info" onclick="copyToClipboard(\'transcript\')">⧉ Copiar</button> </div>\n' +
                '                <div class="form-group py-1">\n' +
                '                    <textarea class="form-control" id="transcript" readonly></textarea>\n' +
                '                </div>\n' +
                '                <div id="error" class="alert alert-danger" role="alert" style="visibility: hidden;"></div>').appendTo("#resultados")

            var response = JSON.parse(file.xhr.response)
            document.getElementById("resultados").style.visibility = 'visible';

            let error = "";

            //Se obtienen los resultados que han sido almacenados en cookies
            var ckTranscript = document.cookie.replace(/(?:(?:^|.*;\s*)ckTranscript\s*\=\s*([^;]*).*$)|^.*$/, "$1");
            var ckSummary = document.cookie.replace(/(?:(?:^|.*;\s*)ckSummary\s*\=\s*([^;]*).*$)|^.*$/, "$1");

            if(typeof response["summary"] !== 'undefined'){
                document.getElementById("summary").innerHTML = response["summary"];
            }else if (ckSummary !== 'undefined'){
                document.getElementById("summary").innerHTML = ckSummary;
            }else{
                error = "Hubo un problema al generar el resumen.";
            }

            if(typeof response["transcript"] !== 'undefined') {
                document.getElementById("transcript").innerHTML = response["transcript"].replaceAll(". ", ". \n");
            }else if (ckTranscript !== 'undefined'){
                document.getElementById("transcript").innerHTML = ckTranscript.replaceAll(". ", ". \n");
            }else {
                error += "<br>Hubo un problema al generar la transcripcion.";
            }

            if (error !== ""){
                ele = document.getElementById("error");
                ele.style.visibility = 'visible';
                ele.innerHTML = "ERROR INESPERADO. Pruebe a intentarlo de nuevo. <br>" + error;
               
            }

            //Se eliminan las cookies utilizadas para los resultados
            document.cookie = "ckSummary=; max-age=0";
            document.cookie = "ckTranscript=; max-age=0";

        })

        this.on("complete", function(file){
            $("#load-container").remove()
        })

    }
}