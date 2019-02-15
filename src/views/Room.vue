<template>
  <div class="room">
    <div class="row main-row">

      <div class="col-sm-5 col-md-4 order-sm-12 align-self-start side-column">
        <div class="card border-warning bg-transparent mt-3 mb-3" id="userlist">
          <div class="card-header bg-transparent border-dark">
            <h3 class="float-left mt-2">
              <span v-if="roomName">
                <strong>{{ roomName }}</strong>
              </span>
            </h3>
            <div v-show="isMobile" class="float-right">
              <button title="Nachrichten" @click="showCard = 'messages'" class="emoji btn btn-outline-light mr-2"
                :class="{'btn-warning': showMessages}">
                <span>📝</span>
              </button>
              <button title="Emoji-Wörterbuch" @click="showCard = 'dictionary'" class="emoji btn btn-outline-light mr-2"
                :class="{'btn-warning': showDictionary}">
                <span>📙</span>
              </button>
              <button title="Teilnehmer" @click="showCard = 'userlist'" class="emoji btn btn-outline-light"
                :class="{'btn-warning': showUserlist}">
                <span>👤</span>
              </button>
            </div>
          </div>
        </div>
        <user-list v-show="showUserlist"
          :users="users"
          :session="session"
          :countries="countryMap"
        ></user-list>
        <dictionary v-show="showDictionary"
          :dictionary="dictionary"
          :countries="countryMap"
          @addentry="addDictionaryEntry"
        ></dictionary>
      </div>

      <div v-show="showMessages" class="col-sm-7 col-md-8 order-sm-1 align-self-end">
        <message-list :messages="messages"
          :session="session"
          :has-more="hasMoreMessages"
          @sendmessage="sendMessage"
          @moremessages="getMoreMessages"
        ></message-list>
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
  moremessages: Message[] | undefined;
  name: string | undefined;
  userlist: Session[] | undefined;
  user: UserChanged | undefined;
  session: Session | undefined;
  dictionary: DictionaryEntry[] | undefined;
}

interface WebSocketMessage {
  type: string;
  message?: string;
  entry?: EntrySubmission;
  before?: string;
}

const byTimestamp = (a: Message, b: Message) => {
  if (a.timestamp > b.timestamp) { return 1; }
  if (a.timestamp < b.timestamp) { return -1; }
  return 0;
};

const BOOTSTRAP_SM_WIDTH = 576;

@Component({
  components: {
    UserList,
    MessageList,
    Dictionary,
  },
})
export default class Room extends Vue {
  @Prop(String) public roomUid!: string;
  @Prop(Array) public countries: string[][];
  private socket: WebSocket | null = null;
  private messages: Message[] = [];
  private users: Session[] = [];
  private dictionary: DictionaryEntry[] = [];
  private roomName: string|null = null;
  private session: Session|null = null;
  private heartBeatInterval: number|undefined = undefined;
  private retryInterval: number|undefined = undefined;
  private isMobile: boolean = true;
  private showCard: string = 'messages';
  private hasMoreMessages: boolean|null = null;

  get showUserlist() {
    return !this.isMobile || this.showCard === 'userlist';
  }
  get showMessages() {
    return !this.isMobile || this.showCard === 'messages';
  }
  get showDictionary() {
    return !this.isMobile || this.showCard === 'dictionary';
  }

  get countryMap() {
    const countryMap: {[key: string]: string} = {};
    this.countries.forEach((cl) => {
      countryMap[cl[0]] = cl[1];
    });
    return countryMap;
  }

  public mounted() {
    this.checkWidth();
    window.addEventListener('resize', () => {this.checkWidth(); });
    this.connectSocket();
  }
  public checkWidth() {
    this.isMobile = window.innerWidth <= BOOTSTRAP_SM_WIDTH;
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
      if (data.moremessages !== undefined) {
        if (data.moremessages.length === 0) {
          this.hasMoreMessages = false;
        } else {
          this.hasMoreMessages = true;
          this.messages = this.mergeMessages(data.moremessages);
        }
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
  public useSocket(message: WebSocketMessage) {
    if (this.socket === null) {
      this.connectSocket();
    }
    if (this.socket !== null) {
      this.socket.send(JSON.stringify(message));
    }
  }
  public sendMessage(message: string) {
    this.useSocket({
      type: 'message',
      message,
    });
  }
  public getMoreMessages() {
    this.useSocket({
      type: 'list_messages',
      before: this.messages[0].timestamp,
    });
  }
  public addDictionaryEntry(entry: EntrySubmission) {
    this.useSocket({
      type: 'dictionary_entry',
      entry,
    });
  }
}
</script>

<style lang="scss" scoped>

.main-row {
  height: 100vh;
  overflow: scroll;
}


@media (min-width: 576px) {
  .side-column {
    height: 100vh;
    overflow: scroll;
  }
}

</style>
