<template>
  <div>
    <h3>Messages</h3>
    <ul>
      <li v-for="message in messages">
        {{ message.username }}:
        <code>
          {{ message.message }}
        </code>
      </li>
    </ul>
    <input type="text" v-model="message" @keyup.enter="submitMessage">
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import router from '../router';

import Message from '../types';

@Component
export default class Userlist extends Vue {
  @Prop(Array) messages!: Array<Message>;
  message = '';

  submitMessage () {
    this.$emit('sendmessage', this.message)
    this.message = '';
  }
}
</script>