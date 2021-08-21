Dropzone.options.dropper = {
    paramName: 'file',
    maxFiles: 1,
    autoProcessQueue: false,
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

        dzClosure = this; // Makes sure that 'this' is understood inside the functions below.
        // for Dropzone to process the queue (instead of default form behavior):
        document.getElementById("submit-all").addEventListener("click", function(e) {

            //<div class="alert alert-primary">El proceso puede tardar varios minutos. Por favor, espere hasta que aparezcan los resultados.</div>

            var newDiv = document.createElement("div");
            var newContent = document.createTextNode("El proceso puede tardar varios minutos. Por favor, espere hasta que aparezcan los resultados.");
            newDiv.classList.add("alert", "alert-primary", "mt-3");
            newDiv.appendChild(newContent);
            document.getElementById("dropper").appendChild(newDiv);

            // Make sure that the form isn't actually being sent.
            e.preventDefault();
            e.stopPropagation();
            dzClosure.processQueue();
        });


        this.on("sending", function(data, xhr, formData) {
            formData.append("modoTrancript", jQuery("input[name='modoTrancript']:checked").val());
        });


        this.on("success", function(file){

            var response = JSON.parse(file.xhr.response)
            document.getElementById("resultados").style.visibility = 'visible';
            document.getElementById("submit-all").style.visibility = 'hidden';
            let error = "";

            console.log(document.cookie)
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

            document.cookie = "ckSummary=; max-age=0";
            document.cookie = "ckTranscript=; max-age=0";

        })

    }
}