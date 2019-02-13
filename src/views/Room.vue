<template>
  <div class="room">
    <!-- <h1>
      Chat room
      <span v-if="roomName">
      „{{ roomName }}“
      </span>
    </h1> -->

    <div class="row">
      <div class="col-sm-8">
        <message-list :messages="messages"
          :session="session"
          @sendmessage="sendMessage"
        ></message-list>
      </div>
      <div class="col-sm-4">
        <div class="card border-warning bg-transparent mb-3" id="userlist">
          <div class="card-header bg-transparent border-dark">
            Raum:
            <span v-if="roomName">
            <strong>{{ roomName }}</strong>
            </span>
          </div>
        </div>
        <user-list :users="users" :session="session"></user-list>
        <dictionary :dictionary="dictionary"
          @addentry="addDictionaryEntry"
        ></dictionary>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import UserList from '../components/UserList.vue';
import MessageList from '../components/MessageList.vue';
import Dictionary from '../components/Dictionary.vue';

import {
  Message, Session, DictionaryEntry, UserChanged,
  EntrySubmission,
} from '../types';

interface WebSocketUpdate {
  messages: Message[] | undefined;
  name: string | undefined;
  userlist: Session[] | undefined;
  user: UserChanged | undefined;
  session: Session | undefined;
  dictionary: DictionaryEntry[] | undefined;
}

const byTimestamp = (a: Message, b: Message) => {
  if (a.timestamp > b.timestamp) { return 1; }
  if (a.timestamp < b.timestamp) { return -1; }
  return 0;
};

@Component({
  components: {
    UserList,
    MessageList,
    Dictionary,
  },
})
export default class Room extends Vue {
  @Prop(String) public roomUid!: string;
  private socket: WebSocket | null = null;
  private messages: Message[] = [];
  private users: Session[] = [];
  private dictionary: DictionaryEntry[] = [];
  private roomName: string|null = null;
  private session: Session|null = null;
  private heartBeatInterval: number|undefined = undefined;
  private retryInterval: number|undefined = undefined;

  public mounted() {
    this.connectSocket();
  }
  public connectSocket() {
    this.socket = this.createSocket();
    if (this.retryInterval) {
      window.clearInterval(this.retryInterval);
      this.retryInterval = undefined;
    }
    this.socket.onopen = (e) => {
      this.heartBeatInterval = setInterval(() => {
        if (this.socket && this.socket.readyState === 1) {
          this.socket.send(JSON.stringify({type: 'heartbeat'}));
        } else {
          window.clearInterval(this.heartBeatInterval);
          this.heartBeatInterval = undefined;
        }
      }, 30000);
    };

    this.socket.onmessage = (e) => {
      const data = JSON.parse(e.data) as WebSocketUpdate;

      if (data.messages) {
        this.messages = this.mergeMessages(data.messages);
      }
      if (data.userlist) {
        this.users = data.userlist;
      }
      if (data.session) {
        this.session = data.session;
      }
      if (data.dictionary) {
        this.dictionary = data.dictionary;
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
      this.heartBeatInterval = undefined;
      if (this.retryInterval === undefined) {
        this.retryInterval = window.setInterval(this.connectSocket, 3000);
      }
    };
  }
  public mergeMessages(newMessages: Message[]) {
    const messageMap: {[key: number]: boolean} = {};
    this.messages.forEach((m) => messageMap[m.id] = true);
    const reallyNewMessages = newMessages.filter((m) => messageMap[m.id] === undefined);
    const unsortedMessages = [
      ...this.messages,
      ...reallyNewMessages,
    ];
    return unsortedMessages.sort(byTimestamp);
  }
  public createSocket() {
    let prot = 'ws';
    if (document.location.protocol === 'https:') {
      prot = 'wss';
    }
    return new WebSocket(
      `${prot}://${window.location.host}/ws/chat/${this.roomUid}/`);
  }
  public sendMessage(message: string) {
    if (this.socket === null) {
      this.connectSocket();
    }
    if (this.socket !== null) {
      this.socket.send(
        JSON.stringify({
          type: 'message',
          message,
        }));
    }
  }
  public addDictionaryEntry(entry: EntrySubmission) {
    if (this.socket === null) {
      this.connectSocket();
    }
    if (this.socket !== null) {
      this.socket.send(
        JSON.stringify({
          type: 'dictionary_entry',
          entry,
        }));
    }
  }
}
</script>
