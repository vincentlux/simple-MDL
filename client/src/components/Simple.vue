<template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" >

      <b-form-group id="exampleInputGroup2"
                    label="SIMPLE query:"
                    label-for="exampleInput2">
        <b-form-input id="exampleInput2"
                      type="text"
                      v-model="form.name"
                      required
                      placeholder="Type here and press Enter">
        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>

    
    <b-card class="text-center" v-show="isResult">
   Fetched  {{ this.num }} result(s) by {{ this.time }} ms.
    </b-card>

  <div class="searchResult" v-show="isResult" transition="expand">
    <a v-for="elem in resObj" :key="elem">

      
    <b-card nobody>
        <h3 class="card-text">{{ elem.subject[0] }}</h3>
        <p class="card-text">
            From: {{ elem.from[0] }}
        </p>
        <p class="card-text">
            From_name: {{ elem.from_name[0] }}
        </p>
        <p class="card-text">
            To: {{ elem.to[0] }}
        </p>
        <p class="card-text">
            To_name: {{ elem.to_name[0] }}
        </p>
        <p class="card-text">
            Date: {{ elem.date }}
        </p>
        <p class="card-text">
            Content: {{ elem.content }}
        </p>
    </b-card>
  <div>
</div>



    </a>
  </div>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  data () {
    return {
      form: {
        name: '',
      },
      time:'',
      num:'',
      resObj:null,
      isResult:false
     // show: true
    }
  },
  methods: {

    fetchResult(query){
      console.log(JSON.stringify(query));
      const path = 'http://localhost:5000/simple';
      // Axios
      axios.post(path, query)
        .then((res)=>{
            console.log(res);
            this.time = res.data.QTime;
            this.num = Object.keys(res.data.docs).length;
            this.resObj = res.data.docs;
            console.log(this.num);
            this.isResult = true;
            // this.title = res.

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });

    },
    onSubmit (evt) {
      evt.preventDefault();
    //   alert(JSON.stringify(this.form));
      
      const query = {query:this.form.name};
      this.fetchResult(query);
    },
    onReset (evt) {
      evt.preventDefault();
      /* Reset our form values */
      this.form.name = '';
      this.isResult = false;
    }
  },

}
</script>

<!-- b-form-1.vue -->