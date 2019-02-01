<template>
  <div class="header">
    <h1 class="cover-heading ">SimpLe search</h1>
    <b-form @submit="onSubmit" @reset="onReset" >
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
      <b-button class = "button" type="reset" variant="warning">Reset</b-button>
    </b-form>

    
    <b-card class="text" v-show="isResult&noError">
   Fetched  {{ this.num }} result(s) by {{ this.time }} s.
    </b-card>

    <b-card class="text-center" v-show="!noError">
   Error! Please refer to  <a href="https://github.com/vincentlux/Cymantix/wiki">Project Wiki Page</a>
    </b-card>

  <div class="searchResult" v-show="isResult&noError" transition="expand">
    <a v-for="elem in resObj" :key="elem.message_id">

      
    <b-card nobody>
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
      // resObj:null,
      resObj: null,
      isResult:false,
      noError:true
     // show: true
    }
  },
  methods: {

    fetchResult(query){
      // console.log(JSON.stringify(query));
      const path = 'http://167.99.3.111:5001/simple';
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
            // this.title = res.

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          console.log("Error handling here")
          this.noError = false;
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
      this.noError = true;
    }
  },

}
</script>

<!-- b-form-1.vue -->