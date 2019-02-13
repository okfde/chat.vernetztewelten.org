<template>
  <div class="card border-dark bg-transparent mb-3" id="userlist">
    <div class="card-header bg-transparent border-dark text-muted">
      {{ userCount }} Teilnehmer
    </div>
    <div class="card-body text-light border-dark">
      <template v-for="user in users">
        <user-item :user="user" :session="session" :key="user.username"/>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import router from '../router';

import UserItem from './UserItem.vue';

import {Session} from '../types';

@Component({
  components: {
    UserItem,
  },
})
export default class UserList extends Vue {
  @Prop(Array) public users!: Session[];
  @Prop(Object) public session!: Session;

  get userCount() {
    return this.users.length;
  }
}
</script>

<style lang="scss" scoped>
#userlist {
  max-height: 50%;
  overflow: scroll;
}
</style>
