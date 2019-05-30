<template>
    <div>
    <b-dropdown style= "position: absolute; left: 20px;" id="dropdown-1" variant="outline" class="m-md-3" no-caret>
        <template slot="button-content">
        <b-img v-bind="mainProps" src="../../static/img/icons/1.png"></b-img>
        <!-- <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div> -->
        </template>
        <b-dropdown-item>Help</b-dropdown-item>
        <b-dropdown-item @click="showModal">Upload</b-dropdown-item>
        <b-dropdown-item>Delete</b-dropdown-item>

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
        <Upload></Upload>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Archive</th>

            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index">
              <td>{{ book.title }}</td>
              <td>
                <!-- <div class="btn-group" role="group"> -->
                  <button type="button" class="btn btn-primary btn-sm">Apply</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
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
        showModal(){ 
            // modal should be added
            console.log('showModal')
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
        const path = 'http://localhost:5001/books';
        axios.get(path)
            .then((res) => {
            this.books = res.data.books;
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
        },
        addBook(payload) {
        const path = 'http://localhost:5001/books';
        axios.post(path, payload)
            .then(() => {
            this.getBooks();
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.log(error);
            this.getBooks();
            });
        },
        initForm() {
        this.addBookForm.title = '';
        // this.addBookForm.author = '';
        this.addBookForm.read = [];
        },
        onSubmit(evt) {
        evt.preventDefault();
        this.$refs.addBookModal.hide();
        let read = false;
        if (this.addBookForm.read[0]) read = true;
        const payload = {
            title: this.addBookForm.title,
            // author: this.addBookForm.author,
            read, // property shorthand
        };
        this.addBook(payload);
        this.initForm();
        },
        onReset(evt) {
        evt.preventDefault();
        this.$refs.addBookModal.hide();
        this.initForm();
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

