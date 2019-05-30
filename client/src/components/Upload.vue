<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
        <!-- <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/> -->
        <b-form-file
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose an email archive ..."
          drop-placeholder="Drop file here..."
        ></b-form-file>
        <!-- <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div> -->

        <!-- <button v-on:click="submitFile()">Submit</button> -->
        <h4 style=" margin-bottom: 1.5rem"> </h4>
        <b-progress :value="uploadPercentage" :max=101 v-show="file" show-progress animated></b-progress>
        <h4 style=" margin-bottom: 1.5rem"> </h4>
        <b-button class = "button" variant="danger" v-show="file" v-on:click="submitFile">
        <!-- <b-spinner small type="grow" v-show="!firstLoad&!uploaded"></b-spinner> -->
          Upload</b-button>
        <!-- <h4 style=" margin-bottom: 1.5rem" v-show="!file"> or</h4>
        <b-button class = "button" variant="danger" v-show="!file" v-on:click="demo">Try with demo email archive</b-button> -->
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data(){
      return {
        file: '',
        firstLoad: true,
        uploaded: false,
        noUploadError: true,
        uploadErrMsg: '',
        uploadPercentage: 0,
      }
    },

    methods: {
      submitFile(){
        this.firstLoad = false;
        // initialize form data
        let formData = new FormData();
        // Add the form data we need to submit
        formData.append('file', this.file);
        // make the request to the POST /single-file URL
        axios.post( 'https://mdl.unc.edu/api/upload_file',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              },
              onUploadProgress: function( progressEvent ) {
                this.uploadPercentage = parseInt( Math.round( ( progressEvent.loaded * 100 ) / progressEvent.total ) );
              }.bind(this)
            }
        ).then((res)=>{
          this.UploadErrMsg = res.data;
          console.log(this.UploadErrMsg);
          this.uploaded = true;
          console.log(this.uploaded);
          this.thisPage();
        })
        .catch((error) => {
          console.error(error);
        });
      },  
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      },
      demo(){
        // reset corename to demo
        console.log('reset here');
        const query = {'query':'reset'}
        
        const path = 'https://mdl.unc.edu/api/reset_solr';
        axios.post(path, query)
          .then((res)=>{
            console.log(res);
            })
          .catch((error) => {
            console.error(error);
            });
        this.$router.push({path: '/test'});
      },
      thisPage(){
        // this.$router.push({path: '/'});
        window.location.href = "http://localhost:8080/";
      },
      nextPage(){
        this.$router.push({path: '/test'});
        // window.location.href = "http://localhost:8080/test";
      },
    }
  }
</script>

