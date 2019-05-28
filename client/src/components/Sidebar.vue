<template>
    <div>
    <b-dropdown  style= "position: absolute; left: 20px;" id="dropdown-1" variant="outline" class="m-md-3" no-caret>
        <template slot="button-content">
        <b-img v-bind="mainProps" src="../../static/img/icons/1.png"></b-img>
        <!-- <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div> -->
        </template>
        <b-dropdown-item>Help</b-dropdown-item>
        <b-dropdown-item v-on:click="test1">Upload</b-dropdown-item>
        <b-dropdown-item>Delete</b-dropdown-item>

    </b-dropdown>
    </div>

</template>

<script>
  export default {
    data() {
        return {
        mainProps: {width: 25, height: 25, class: 'm1' }
      }
    },
    methods: {
        test1(){ 
            // modal should be added
            console.log('test1')
        },
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

