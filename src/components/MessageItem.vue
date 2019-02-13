<template>
  <div>
    <strong>{{ message.username }}</strong>:
    <code>
      {{ message.message }}
    </code>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import {Message, Session} from '../types';

@Component
export default class Userlist extends Vue {
  @Prop(Object) public message!: Message;
  @Prop(Object) public session!: Session;

  get isMe() {
    return this.message.username === this.session.username;
  }
}
</script>