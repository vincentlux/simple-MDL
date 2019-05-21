<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell">
      <label>File
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
        <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data(){
      return {
        file: ''
      }
    },

    methods: {
      submitFile(){
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
              }
            }
          ).then(function(response){
        console.log(response)
      })
      .catch(function(){
        console.log('FAILURE!!');
      });
    },
      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }
    }
  }
</script>

