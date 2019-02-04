<template>
  <div class="about">
    <h1>
      Chat room
      <span v-if="roomName">
      „{{ roomName }}“
      </span>
    </h1>
    <span v-if="session">
      Username: {{ session.username}} ({{ session.country }})
    </span>

    <user-list :users="users"></user-list>
    <message-list :messages="messages"
      @sendmessage="sendMessage"
    ></message-list>

  </div>
</template>


<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import UserList from '../components/UserList.vue';
import MessageList from '../components/MessageList.vue';

import {Message, User, DictionaryEntry} from '../types';

const byTimestamp = (a, b) => {
  if (a.timestamp > b.timestamp) { return 1; }
  if (a.timestamp < b.timestamp) { return -1; }
  return 0;
};

@Component({
  components: {
    UserList,
    MessageList,
  },
  props: {
    roomUid: {
      type: String,
    }
  },
})
export default class Room extends Vue {
  socket: WebSocket | null = null;
  messages: Message[] = [];
  users: User[] = [];
  dictionary: DictionaryEntry[] = [];
  roomName: string|null = null;
  session: object|null = null;
  private heartBeatInterval: number|null = null;
  private retryInterval: number|null = null;

  mounted() {
    this.connectSocket();
  }
  connectSocket() {
    this.socket = this.createSocket();
    if (this.retryInterval) {
      window.clearInterval(this.retryInterval);
      this.retryInterval = null;
    }
    this.socket.onopen = (e) => {
      this.heartBeatInterval = setInterval(() => {
        if (this.socket.readyState === 1) {
          this.socket.send(JSON.stringify({type: 'heartbeat'}));
        } else {
          window.clearInterval(this.heartBeatInterval);
          this.heartBeatInterval = null;
        }
      }, 30000);
    };

    this.socket.onmessage = (e) => {
      const data = JSON.parse(e.data);

      if (data.messages) {
        this.messages = this.mergeMessages(data.messages);
      }
      if (data.userlist) {
        this.users = data.userlist;
      }
      if (data.you) {
        this.session = data.you;
      }
      if (data.user) {
        console.log(`${data.user.username} ${data.user.action}`);
      }
      if (data.name) {
        this.roomName = data.name;
      }
    };

    this.socket.onclose = (e) => {
      console.error('Chat socket closed unexpectedly');
      window.clearInterval(this.heartBeatInterval);
      this.heartBeatInterval = null;
      if (this.retryInterval === null) {
        this.retryInterval = window.setInterval(this.connectSocket, 3000);
      }
    };
  }
  public mergeMessages(newMessages) {
    const messageMap = {};
    this.messages.forEach((m) => messageMap[m.id] = true);
    const reallyNewMessages = newMessages.filter((m) => messageMap[m.id] === undefined);
    const unsortedMessages = [
      ...this.messages,
      ...reallyNewMessages,
    ];
    return unsortedMessages.sort(byTimestamp);
  }
  public createSocket () {
    return new WebSocket(
      `ws://${window.location.host}/ws/chat/${this.roomUid}/`);
  }
  public sendMessage(message) {
    if (this.socket === null) {
      this.connectSocket();
    }
    if (this.socket !== null) {
      this.socket.send(
        JSON.stringify({
          type: 'message',
          message: message,
        }));
    }
  }
}
</script>
