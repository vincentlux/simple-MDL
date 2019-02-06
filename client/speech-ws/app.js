const io = require('socket.io')(5000);
const ss = require('socket.io-stream');
console.log('Server is starting....DONE');
io.on('connection', function (socket) {
    // const record = require('node-record-lpcm16');
    const Speech = require('@google-cloud/speech');

// Instantiates a client
   const speech = new Speech.SpeechClient({
        keyFilename: './simple-MDL-d4dbab56cb6c.json' // file json key
   });
    const encoding = 'LINEAR16';
    const sampleRateHertz = 16000;

    var request = {
        config: {
            encoding: encoding,
            sampleRateHertz: sampleRateHertz,
            languageCode: 'en-US'
        },
        interimResults: true // If you want interim results, set this to true
    };

    socket.on('LANGUAGE_SPEECH', function (language) {
        console.log('set language');
        request.config.languageCode = language;
        console.log("set!")
        console.log(language);
    })

// Create a recognize stream
    const recognizeStream = speech.streamingRecognize(request)
        .on('error', function(error){
            console.log('ERROR:',error);
        })
        .on('data', function(data){
            console.log('GoogleData:',data.results[0]);
            socket.emit('SPEECH_RESULTS',(data.results[0] && data.results[0].alternatives[0])
                ? `${data.results[0].alternatives[0].transcript}\n`
                : `q`)
        });


    console.log('SERVER CONNECT');
    ss(socket).on('START_SPEECH', function (stream) {
        console.log("1");
        stream.pipe(recognizeStream);
        console.log("2");
    });

    socket.on('STOP_SPEECH', function () {
        console.log('Disconnected!');
    })
});

