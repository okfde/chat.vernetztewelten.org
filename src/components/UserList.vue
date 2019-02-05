<template>
  <div>
    <h3>Users</h3>
    <ul>
      <li v-for="user in users">
        {{ user.username }}
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import router from '../router';

import {Session} from '../types';

@Component
export default class UserList extends Vue {
  @Prop(Array) public users!: Session[];
}
</script>