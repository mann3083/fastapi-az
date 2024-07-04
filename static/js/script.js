let mediaRecorder;
let audioChunks = [];

document.getElementById('start').addEventListener('click', async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks);
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = document.getElementById('audioPlayback');
        audio.src = audioUrl;
        audio.play();

        const formData = new FormData();
        formData.append('file', audioBlob, 'audio.webm');

        const response = await fetch('/upload-audio', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        console.log(result);

        audioChunks = [];
    };

    mediaRecorder.start();
    document.getElementById('start').disabled = true;
    //document.getElementById('stop').disabled = false;

    // Automatically stop recording after 10 seconds or when silence is detected
    setTimeout(stopRecording, 10000);

    let audioContext = new AudioContext();
    let source = audioContext.createMediaStreamSource(stream);
    let processor = audioContext.createScriptProcessor(2048, 1, 1);
    let silenceTimeout;

    processor.onaudioprocess = (event) => {
        const input = event.inputBuffer.getChannelData(0);
        const isSilent = input.every(sample => Math.abs(sample) < 0.01);
        if (isSilent) {
            if (!silenceTimeout) {
                silenceTimeout = setTimeout(stopRecording, 3000); // Stop after 3 seconds of silence
            }
        } else {
            clearTimeout(silenceTimeout);
            silenceTimeout = null;
        }
    };

    source.connect(processor);
    processor.connect(audioContext.destination);
});


/* document.getElementById('stop').addEventListener('click', () => {
    stopRecording();
}); */

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        document.getElementById('start').disabled = false;
        //document.getElementById('stop').disabled = true;
    }
}
