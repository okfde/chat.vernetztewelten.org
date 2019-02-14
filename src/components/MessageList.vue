<template>
  <div class="message-container">
    <div class="message-list" ref="messages">
      <MessageItem v-for="message in messageList" :key="message.id"
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
      <div class="input-group-append ">
        <emoji-select
          class="relative-picker border border-light p-1 pl-2 pr-2 bg-light"
          :isMobile="isMobile"
          :fixed="false"
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
import { Component, Vue, Prop, Watch } from 'vue-property-decorator';

import MessageItem from './MessageItem.vue';

import EmojiSelect from './EmojiSelect.vue';

import {Message, Session} from '../types';

const TIME_THRESHOLD = 1000 * 60 * 5;

@Component({
  components: {
    MessageItem,
    EmojiSelect,
  },
})
export default class MessageList extends Vue {
  @Prop(Array) public messages!: Message[];
  @Prop(Object) public session!: Session;
  @Prop(Boolean) public isMobile!: boolean;
  private message = '';

  public mounted() {
    this.triggerScoll();
  }

  get messageList() {
    let lastTime: number|null = null;
    let lastDate: string|null = null;
    let lastUsername: string|null = null;
    return this.messages.map((mes) => {
      const date = new Date(mes.timestamp);
      const mesTimestamp = date.getTime();
      const mesDate = date.toISOString().slice(0, 10);
      mes.showTime = false;
      if (!lastTime) {
        mes.showTime = true;
      } else {
        const diff = mesTimestamp - lastTime;
        if (diff > TIME_THRESHOLD) {
          mes.showTime = true;
        }
      }

      mes.showDate = false;
      if (!lastDate || lastDate !== mesDate) {
        mes.showDate = true;
      }

      mes.showUser = false;
      if (!lastUsername || lastUsername !== mes.username) {
        mes.showUser = true;
      }

      lastTime = mesTimestamp;
      lastDate = mesDate;
      lastUsername = mes.username;
      return mes;
    });
  }

  @Watch('messages')
  private onMessagesChanged(val: Message[], oldVal: Message[]) {
    this.triggerScoll();
  }

  private submitMessage() {
    if (this.message === '') {
      return;
    }
    this.$emit('sendmessage', this.message);
    this.message = '';
    this.triggerScoll();
  }

  private triggerScoll() {
    window.setTimeout(() => {
      this.showLatestMessage();
    }, 250);
  }

  private showLatestMessage() {
    const el = this.$refs.messages;
    if (el instanceof Element) {
      const last = el.querySelector('.message:last-child');
      if (last !== null) {
        last.scrollIntoView({behavior: 'smooth', block: 'end'});
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.message-list {
  max-height: 65vh;
  overflow: scroll;
}
@media (min-width: 576px) {
  .message-container {
    max-height: 100vh;
  }
  .message-list {
    max-height: calc(100vh - 70px);
  }
}
</style>
