<template>
  <div>
    <div class="message">
      <MessageItem v-for="message in messages" :key="message.id"
        :message="message"
        :session="session"
      ></MessageItem>
    </div>

    <div class="input-group mb-3 mt-3">
      <input v-model="message" type="text" class="form-control"
        placeholder="Deine Nachricht"
        aria-label="Deine Nachricht"
        aria-describedby="send-button"
        @keyup.enter="submitMessage"
      >
      <div class="input-group-append">
        <emoji-select
          class="relative-picker border border-light p-1 bg-light"
          @emoji="message += $event">
        </emoji-select>
      </div>
      <div class="input-group-append">
        <button
          class="btn btn-outline-light" type="button" id="send-button"
          @click="submitMessage"
        >
          Absenden
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import MessageItem from './MessageItem.vue';

import EmojiSelect from './EmojiSelect.vue';

import {Message, Session} from '../types';

@Component({
  components: {
    MessageItem,
    EmojiSelect,
  },
})
export default class Userlist extends Vue {
  @Prop(Array) public messages!: Message[];
  @Prop(Object) public session!: Session;
  private message = '';

  private submitMessage() {
    this.$emit('sendmessage', this.message);
    this.message = '';
  }
}
</script>