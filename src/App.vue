<template>
  <div id="app" class="container-fluid blackspot">
    <div class="row">
      <div class="col-12">
        <router-view
          :session="session"
          :room="room"
          :countries="countries"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
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
export default class App extends Vue {
}
</script>

<style lang="scss">
@import "styles/base.scss";

</style>
