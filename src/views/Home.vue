<template>
  <div class="home">
    <Login :session="session" :room="room" :countries="countries"/>
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
