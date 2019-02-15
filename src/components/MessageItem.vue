<template>
  <div class="message">
    <template v-if="message.showTime || message.showDate">
      <p class="text-center text-muted mb-1">
        <small v-if="message.showDate">{{ dateLabel }}</small>
        <span v-if="message.showDate && message.showTime"> - </span>
        <small v-if="message.showTime">{{ time }}</small>
      </p>
    </template>
    
    <p class="message-paragraph" :title="messageTitle">
      <strong class="text-muted" :class="{'hide-username': hideUsername}">{{ message.username }}:</strong>
      {{ message.message }}
    </p>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import {Message, Session} from '../types';

const pad = (s: string) => {
    if (s.length < 2) {
      s = '0' + s;
    }
    return s;
};

@Component
export default class Userlist extends Vue {
  @Prop(Object) public message!: Message;
  @Prop(Object) public session!: Session;

  get isMe() {
    return this.message.username === this.session.username;
  }
  get messageTitle() {
    return `${this.dateLabel} - ${this.time}`;
  }
  get date() {
    return new Date(this.message.timestamp);
  }
  get time() {
    const hours = pad('' + this.date.getHours());
    const mins = pad('' + this.date.getMinutes());
    return `${hours}:${mins}`;
  }
  get dateLabel() {
    return `${pad('' + this.date.getDate())}.${pad('' + this.date.getMonth())}.${this.date.getFullYear()}`;
  }
  get hideUsername() {
    return !this.message.showUser && !(this.message.showDate || this.message.showTime);
  }
}
</script>

<style lang="scss" scoped>
  .message-paragraph {
    margin-bottom: 0.25rem;
  }
  .hide-username {
    color: #222 !important;
  }
</style>
