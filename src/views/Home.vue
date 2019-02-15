<template>
  <div class="home">
    <div class="row main-row justify-content-center">
      <div class="col-md-4">
        <h2 class="mb-5 mt-5">
          Vernetzte Welten – Chat
        </h2>
        <Login :session="session" :room="room" :countries="countries"/>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Login from '@/components/Login.vue'; // @ is an alias to /src

@Component({
  components: {
    Login,
  },
  props: {
    session: {
      type: Object,
      default: null,
    },
    room: {
      type: Object,
      default: null,
    },
    countries: {
      type: Array,
    },
  },
})
export default class Home extends Vue {}
</script>

<style lang="scss" scoped>

.main-row {
  height: 100vh;
  overflow: scroll;
}

</style>

