<template>
  <div class="header">
    <h1 class="cover-heading ">Simple Search (test)</h1>
    <b-button variant="link" v-on:click="mdlGrammar">MDL Grammar</b-button>
      <b-form @submit="onSubmit">
        <b-form-group id="Inp1"
                    label-sr-only
                    label-for="Inp1">
        <b-form-input id="Inp2"
                      type="text"
                      v-model="form.speechInp"
                      required
                      placeholder="Type here and press Enter">
        </b-form-input>
      </b-form-group>
      <!-- <b-button class = "button" type="submit" variant="warning">Submit</b-button> -->
      <b-button class = "button" type="submit" variant="warning">
	      <b-spinner small type="grow" v-show="!firstLoad&!isResult&noError"></b-spinner>
	      Submit</b-button>

      <b-button v-b-modal.modal-speech class = "button" variant="primary" v-show="btn && !btnReset" v-on:click="startRecording">Start Recording</b-button>
      <b-button class = "button" variant="danger" v-show="btnStop" v-on:click="stopRecording">Stop</b-button>
      <b-button class = "button" variant="danger" v-show="btnReset" v-on:click="redirectError">Reset</b-button>
    </b-form>


    <b-card class="text" v-show="isResult&noError">
      Fetched  {{ this.num }} email(s) by {{ this.time }} s.
    </b-card>
    <b-card class="text-center" v-show="!noError">
      <b-button variant="warning link" v-on:click="mdlGrammar">{{ this.errMsg }}</b-button>
    </b-card>
  

  <b-pagination v-show="isResult&noError&this.num!=0" :total-rows="0 || parseInt(this.num)" v-model="currentPage" :per-page="5">
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
  <b-pagination v-show="isResult&noError&this.num!=0" :total-rows="0 || parseInt(this.num)" v-model="currentPage" :per-page="5">
  </b-pagination>
  
  <!-- Modal Component -->
  <b-modal
    id="modal-speech"
    ref="modal"
    size="sm"
    title="Please start speaking"
    centered
    no-close-on-backdrop
    no-close-on-esc
    hide-header-close
    ok-title="stop"
    cancel-title="reset"
    @ok="handleOk"
    @cancel="handleCancel"
    @shown="clearSpeechInp"
    
  >
    <form @submit.stop.prevent="handleSubmit">
      <!-- <b-form-input v-model="speechInp" placeholder="speech test"></b-form-input> -->
      <b-form-input v-model="form.name" placeholder="e.g. on soccer"></b-form-input>
    </form>
  </b-modal>

  </div>

</template>

<script>

  import axios from 'axios';
  import qs from 'qs';
  var audioContext = new(window.AudioContext || window.webkitAudioContext)();
  //var socket = io.connect('http://3.86.172.253', {path: '/ws/'});
  var socket = io.connect('wss://mdl.unc.edu', {path: '/ws/'});
  //var socket = io.connect('http://3.86.172.253/ws', {secure: true});
  //var socket = io.connect('http://167.99.3.111:5002', {secure: true});
  var ssStream = ss.createStream();
  var scriptNode;
  
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
        speechInp: '',
        },
        time:'',
        num:'',
        // resObj:null,
        resObj: null,
        isResult:false,
        noError:true,
        errMsg: '',
        firstLoad: true,
        currentPage:1,
      }
    },
    watch: { // to reset param after an error happens
      'form': {
        handler: function(v) {
          if (this.errMsg!= ''){
            this.firstLoad = true;
            this.noError = true;
          }
        },
        deep: true
      },
    },
    methods: {
      fetchResult(query){
      // console.log(JSON.stringify(query));
      //const path = 'http://167.99.3.111:5001/simple';
      //const path = 'http://3.86.172.253:5001/simple';
      const path = 'http://3.86.172.253/api/simple';
      // Axios
      axios.post(path, query)
        .then((res)=>{
            this.time = res.data.QTime / 1000;
            this.num = Object.keys(res.data.docs).length;
            this.resObj = res.data.docs;
            this.isResult = true;
            this.noError = true;
        })
        .catch((error) => {
          this.errMsg =  error.response.data.message;
          this.noError = false;
        });
    },

    clearSpeechInp() {
        this.form.name = ''
    },
    handleOk(bvModalEvt) {
      // Prevent modal from closing
      bvModalEvt.preventDefault()
      if (!this.form.name) { // should modify this part for a validity check
        alert('speech input does not match with mdl grammar')
      } else {
        this.handleSubmit()
      }
    },
    handleCancel(bvModalEvt) {
      // reset?
      this.redirectError()
    },
    handleSubmit() { // stop recording here
      console.log(this.form.name)
      // return result to the main text box
      this.form.speechInp = this.form.name 
      this.clearSpeechInp()
      this.$nextTick(() => {
        // Wrapped in $nextTick to ensure DOM is rendered before closing
        this.$refs.modal.hide()
      })
      this.stopRecording()
    },

    onSubmit (evt) {
      evt.preventDefault();
      
      const query = {query:this.form.speechInp};
      this.firstLoad = false;
      this.isResult = false;
      this.fetchResult(query);
    },

    filter (_resObj) {
      if (this.isResult&this.noError){
        return Object.values(_resObj).slice((this.currentPage-1)*5, (this.currentPage-1)*5+5);
        
      }
    },
    successCallback(stream) {
      const vm = this;
      console.log('successCallback:...IN');
      console.log('successCallback:...IN');
      // add user gesture
      console.log(audioContext.resume());
      var input = audioContext.createMediaStreamSource(stream);
      var bufferSize = 2048;
      scriptNode = audioContext.createScriptProcessor(bufferSize, 1, 1);
      scriptNode.onaudioprocess = scriptNodeProcess;
      input.connect(scriptNode);

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
      console.log(this.form.speechInp)
      console.log("Stop recording!");
      this.btnStop = false;
      this.btn = true;
      this.btnReset = true;
      console.log(audioContext.destination);
      scriptNode.disconnect(audioContext.destination);
      ssStream.end();
      socket.emit('STOP_SPEECH', {});
      console.log(this.form.speechInp)
      // send to flask here for speech to result (regex) way
      const query = {'query':this.form.speechInp}
      console.log(query)
      //const path = 'http://3.86.172.253:5001/speech_regex';
      const path = 'http://3.86.172.253/api/speech_regex';
      axios.post(path, query)
        .then((res)=>{
          console.log(res);
          this.form.speechInp = res.data.res_query;
          })
        .catch((error) => {
          console.error(error);
          });
    },
    errorCallback(error) {
      // console.log('errorCallback:', error);
    },
    redirectError(){
      this.noError = true;
      // refresh page
      this.$router.go(0);
    },
    mdlGrammar(){
      var url = "https://simple.unc.edu/documentation/";
      window.open(url, '_blank', 'x=y');
      },
    },

    created() {
       const that = this;
       socket.on('SPEECH_RESULTS', function(text) {
         if('q' == text){
           that.resultError = true;
           console.log("error")
         }else{
           that.form.name = text;
         }
       })
         if (navigator.mediaDevices.getUserMedia) {
           navigator.webkitGetUserMedia({ audio: true }, function(stream) {
             that.successCallback(stream)
           }, function(error) {
             that.errorCallback(error)
           });
         } else {
           // console.log('getUserMedia not supported on your browser!');
         }
       },
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
