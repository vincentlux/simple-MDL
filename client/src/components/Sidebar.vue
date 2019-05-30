<template>
    <div>
    <b-dropdown style= "position: absolute; left: 20px;" id="dropdown-1" variant="outline" class="m-md-3" no-caret>
        <template slot="button-content">
        <b-img v-bind="mainProps" src="../../static/img/icons/1.png"></b-img>
        <!-- <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div> -->
        </template>
        <b-dropdown-item @click="mdlGrammar">Help</b-dropdown-item>
        <b-dropdown-item @click="showModal">Upload</b-dropdown-item>
        <!-- <b-dropdown-item>Delete</b-dropdown-item> -->

    </b-dropdown>

    <!-- <b-modal ref="upload-modal" hide-footer title="Using Component Methods">
      <div class="d-block text-center">
        <h3>Hello From My Modal!</h3>
      </div>
      <b-button class="mt-3" variant="outline-danger" block @click="hideModal">Close Me</b-button>
      <b-button class="mt-2" variant="outline-warning" block @click="toggleModal">Toggle Me</b-button>
    </b-modal> -->

    <b-modal ref="addBookModal"
            id="book-modal"
            title="Upload a new file"
            hide-footer>
        <Upload @fileNamePass="fileNamePass1"></Upload>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Archive</th>
              <th></th>
              <!-- <th></th>
              <th></th> -->
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>
                <!-- <div class="btn-group" role="group"> -->
                  <button type="button" class="btn btn-primary btn-sm" @click="applyFile(book)">Apply</button>
                  <button type="button" class="btn btn-danger btn-sm" v-show="ifDemo(book)" @click="deleteFile(book)">Delete</button>
                <!-- </div> -->
              </td>
            </tr>
          </tbody>
        </table>
        <!-- <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-title-group"
                        label="Title:"
                        label-for="form-title-input">
            <b-form-input id="form-title-input"
                            type="text"
                            v-model="addBookForm.title"
                            required
                            placeholder="Enter title">
            </b-form-input>
            </b-form-group>
            <b-form-group id="form-author-group"
                        label="Author:"
                        label-for="form-author-input">
                <b-form-input id="form-author-input"
                            type="text"
                            v-model="addBookForm.author"
                            required
                            placeholder="Enter author">
                </b-form-input>
            </b-form-group> -->
            <!-- <b-form-group id="form-read-group">
            <b-form-checkbox-group v-model="addBookForm.read" id="form-checks">
                <b-form-checkbox value="true">Read?</b-form-checkbox>
            </b-form-checkbox-group>
            </b-form-group> -->
            <!-- <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button> -->
        <!-- </b-form> -->
    </b-modal>
    </div>

</template>

<script>
  import axios from 'axios';
  import Upload from './Upload';
  export default {
      components: {
      Upload
    },
    data() {
        return {
        mainProps: {width: 25, height: 25, class: 'm1' },
        books: [],
        addBookForm: {
            title: '',
            // author: '',
            read: [],
        },
      }
    },
    methods: {
        fileNamePass1(fname){
            // getbooks here to update the archive list
            this.getBooks();
            this.$emit('fileNamePass2', fname);

        },
        ifDemo(book){
            if(book.title == 'Enron Dataset'){
                return false;
            }
            else{
                return true;
            }
        },
        applyFile(book){
            console.log(book.title);
            const path = `https://mdl.unc.edu/api/file_list/${book.title}`;
            axios.put(path)
                .then((res) => {
                // console.log(res);
                this.getBooks();
                this.$emit('fileNamePass2', res.data.title);
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
                this.getBooks();
                
                });

            // this.$router.push({path: '/'});
            this.$refs['addBookModal'].hide();
        },

        deleteFile(book){
            const path = `https://mdl.unc.edu/api/delete_file/${book.title}`;
            axios.put(path)
                .then((res) => {
                // console.log(res);
                this.getBooks();
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
                this.getBooks();
                });


            // IF does not want to show that file already deleted: 

            // this.$emit('fileNamePass2', 'Enron Dataset');
            // const query = {'query':'reset'}
            // const path = 'https://mdl.unc.edu/api/reset_solr';
            // axios.post(path, query)
            //   .then((res)=>{
            //     console.log(res);
            //     })
            //   .catch((error) => {
            //     console.error(error);
            //     });
        },
        mdlGrammar(){
        var url = "https://simple.unc.edu/documentation/";
        window.open(url, '_blank', 'x=y');
        },
        showModal(){ 
            // modal should be added
            // console.log('showModal')
            // this.$refs['upload-modal'].show()
            this.$refs['addBookModal'].show()
        },
        hideModal() {
            this.$refs['upload-modal'].hide()
        },
        toggleModal() {
            // We pass the ID of the button that we want to return focus to
            // when the modal has hidden
            this.$refs['upload-modal'].toggle('#toggle-btn')
        },
        getBooks() {
        // const path = 'http://localhost:5001/books';
        const path = 'https://mdl.unc.edu/api/file_list';
        axios.get(path)
            .then((res) => {
            this.books = res.data.books;
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
        },
        
    },
    created() {
        this.getBooks();
    },
  }
</script>

<style>
.bar {
  width: 35px;
  height: 5px;
  background-color: black;
  margin: 6px 0;
}
</style>

