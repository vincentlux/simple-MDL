<template>
  <div class="header">
    <h1 class="cover-heading ">Simple Search (test)</h1>
      <b-form @submit="onSubmit">
        <b-form-group id="Inp1"
                    label-sr-only
                    label-for="Inp1">
        <b-form-input id="Inp2"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Type here and press Enter">
        </b-form-input>
      </b-form-group>
      <b-button class = "button" type="submit" variant="warning">Submit</b-button>
      
      <!-- <b-button class = "button" variant="primary" v-show="btn && !btnReset" v-on:click="startRecording">Start Recording</b-button>
      <b-button class = "button" variant="danger" v-show="btnStop" v-on:click="stopRecording">Stop</b-button> -->
      <b-button class = "button" variant="danger" v-show="btnReset" v-on:click="redirectError">Reset</b-button>
    </b-form>


    <b-card class="text" v-show="isResult&noError">
      Fetched  {{ this.num }} email(s) by {{ this.time }} s.
    </b-card>
    <b-card class="text-center" v-show="!noError">
      {{ this.errMsg }} Please refer to  <a href="https://github.com/vincentlux/Cymantix/wiki">Project Wiki Page</a>
    </b-card>
  

  <b-pagination v-show="isResult&noError" :total-rows="0 || parseInt(this.num)" v-model="currentPage" :per-page="10">
  </b-pagination>
  <div class="searchResult" v-show="isResult&noError" transition="expand">
        <a v-for="elem in filter(resObj)" :key="elem.message_id">

    <b-card no-body>
        <h3 class="card-text">{{ elem.subject[0] }}</h3>
        <p class="card-text">
            Date: {{ elem.date.replace("Z", " ").replace("T", " ") }}
        </p>
        <p class="card-text">
            From: {{ elem.from[0] }}
            From_name: {{ elem.from_name[0].replace(/ *\<[^>]*\> */g, "") }}
        </p>
        <p class="card-text" v-if="elem.to != null">
            To: {{ elem.to[0] }}
            To_name: {{ elem.to_name[0].replace(/<(?!\/?p\b)[^>]+>/ig, "") }}
        </p>
        <p class="card-text" v-if="elem.to == null && elem.to_name != null">
            To: {{ elem.to }}
            To_name: {{ elem.to_name[0].replace(/<(?!\/?p\b)[^>]+>/ig, "") }}
        </p>
        <p class="card-text" v-if="elem.to == null && elem.to_name == null">
            To: {{ elem.to }}
            To_name: {{ elem.to_name }}
        </p>

        <p class="card-text">
            {{ elem.content[0] }}
        </p>
    </b-card>
    </a>
  </div>
  <b-pagination v-show="isResult&noError" align="center" :total-rows="0 || parseInt(this.num)" v-model="currentPage" :per-page="10">
  </b-pagination>
    

  </div>

</template>

<script>

  import axios from 'axios';
  import qs from 'qs';
  // var audioContext = new(window.AudioContext || window.webkitAudioContext)();
  // var socket = io.connect('http://localhost:5000');
  // var ssStream = ss.createStream();
  // var scriptNode;
  
  export default {
    // inject: ['reload'],
    data() {
      return {
        btn: true,
        btnStop: false,
        btnReset: false,
        result: false,
        resultError: false,
        selected: 'en-US',
        items: [
          {
            text: 'English (United States)',
            value: 'en-US'
          }
        ],
        form: {
        name: '',
        },
        time:'',
        num:'',
        // resObj:null,
        resObj: null,
        isResult:false,
        noError:true,
        errMsg: '',
        // show: true
        currentPage:1,
      }
    },
    methods: {

      fetchResult(query){
      // console.log(JSON.stringify(query));
      //const path = 'http://167.99.3.111:5001/simple';
      const path = 'http://3.86.172.253:5001/simple';
      // Axios
      axios.post(path, query)
        .then((res)=>{
            // console.log(res);
            this.time = res.data.QTime / 1000;
            // console.log(this.time);
            this.num = Object.keys(res.data.docs).length;
            // console.log(this.num);
            this.resObj = res.data.docs;
            // console.log(this.resObj);
            // console.log(this.num);
            this.isResult = true;
            this.noError = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          // console.error(error);
          // console.log(error.response.data.message)
          this.errMsg =  error.response.data.message
          // console.log("Error handling here");
          this.noError = false;
        });

    },

      onSubmit (evt) {
        evt.preventDefault();
      //   alert(JSON.stringify(this.form));
        
        const query = {query:this.form.name};
        // console.log(query);
        this.fetchResult(query);
      },

      filter (_resObj) {
        if (this.isResult&this.noError){
          // return _resObj
          return Object.values(_resObj).slice((this.currentPage-1)*10, (this.currentPage-1)*10+10);
          
        }
      },


      successCallback(stream) {
        const vm = this;
        console.log('successCallback:...IN');
        console.log('successCallback:...IN');
        // add user gesture
        console.log(audioContext.resume());
        var input = audioContext.createMediaStreamSource(stream);
        //console.log(input)
        var bufferSize = 2048;
        scriptNode = audioContext.createScriptProcessor(bufferSize, 1, 1);
        scriptNode.onaudioprocess = scriptNodeProcess;
        input.connect(scriptNode);
  
        // console.log('ScriptNode BufferSize:', scriptNode.bufferSize);
        function scriptNodeProcess(audioProcessingEvent) {
        var inputBuffer = audioProcessingEvent.inputBuffer;
        var outputBuffer = audioProcessingEvent.outputBuffer;
        var inputData = inputBuffer.getChannelData(0);
        var outputData = outputBuffer.getChannelData(0);

  
        // Loop through the 4096 samples
        for (var sample = 0; sample < inputBuffer.length; sample++) {
          outputData[sample] = inputData[sample];
        }
        ssStream.write(new ss.Buffer(vm.downsampleBuffer(inputData, 44100, 16000)));
      }
      },
      downsampleBuffer(buffer, sampleRate, outSampleRate) {
        if (outSampleRate == sampleRate) {
          return buffer;
        }
        if (outSampleRate > sampleRate) {
          throw "downsampling rate show be smaller than original sample rate";
        }
        var sampleRateRatio = sampleRate / outSampleRate;
        var newLength = Math.round(buffer.length / sampleRateRatio);
        var result = new Int16Array(newLength);
        var offsetResult = 0;
        var offsetBuffer = 0;
        while (offsetResult < result.length) {
          var nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
          var accum = 0,
            count = 0;
          for (var i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
            accum += buffer[i];
            count++;
          }
  
          result[offsetResult] = Math.min(1, accum / count) * 0x7FFF;
          offsetResult++;
          offsetBuffer = nextOffsetBuffer;
        }
        return result.buffer;
      },
      startRecording() {

        console.log("recording!!");
        // as
        // const languageSelected = this.selected;
        // socket.emit('LANGUAGE_SPEECH', languageSelected);
        this.result = true;
        this.btn = false;
        this.btnStop = true;
        this.btnReset = false;
        scriptNode.connect(audioContext.destination);
        console.log(audioContext.destination);
        console.log("START_SPEECH"); 
        ss(socket).emit('START_SPEECH', ssStream);
        setInterval(function() {
          this.stopRecording();
        }.bind(this), 55000);
      },
      stopRecording() {
        console.log("Stop recording!");
        //console.log("sh")
        this.btnStop = false;
        this.btn = true;
        this.btnReset = true;
        console.log(audioContext.destination);
        scriptNode.disconnect(audioContext.destination);
        ssStream.end();
        socket.emit('STOP_SPEECH', {});
      },
      errorCallback(error) {
        // console.log('errorCallback:', error);
      },
      redirectError(){
        this.noError = true;
        window.location.href = "http://localhost:8080/";
      },
      // reloadPage(){
      //   this.reload();
      // },
    },

    // created() {
    //   const that = this;
    //   // console.log(audioContext) 
    //   // console.log("created")
    //   // console.log(that.result, that.btn, that.btnStop);
    //   socket.on('SPEECH_RESULTS', function(text) {
    //     // console.log(text)
    //     if('q' == text){

    //       that.resultError = true;
    //       console.log("error")
    //     }else{
    //       // console.log(text)
        
    //       // that.textResult = text;
    //       that.form.name = text;
    //       // console.log("text:")
    //       // console.log("2")
    //       // // console.log(text)
    //     }
    //   })
    //     if (navigator.mediaDevices.getUserMedia) {
    //       // console.log('getUserMedia supported...');
    //       navigator.webkitGetUserMedia({ audio: true }, function(stream) {
    //         // console.log("stream?");
    //         // // console.log(stream);
    //         that.successCallback(stream)
    //       }, function(error) {
    //         // console.log("error2")
    //         that.errorCallback(error)
    //       });
    //     } else {
    //       // console.log('getUserMedia not supported on your browser!');
    //     }
    //   },


    }
</script>


<style>
  .slide-enter {
    opacity: 0;
  }
  
  .slide-enter-active {
    animation: slide-in 1s ease-out forwards;
    transition: opacity .5s;
  }
  
  .slide-move {
    transition: transform 1s;
  }
  
  @keyframes slide-in {
    from {
      transform: translateY(20px);
    }
    to {
      transform: translateY(0);
    }
  }
</style>
