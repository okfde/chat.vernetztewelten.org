<template>
  <div class="media" :class="{'bg-dark': itsMe}">
    <div class="mr-1 p-1 emoji-flag" :title="user.countryName">
      {{ emojiFlag }}
    </div>
    <div class="media-body p-1">
      {{ user.username }}
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import {Session} from '../types';

import {FLAGS} from '../data/emojiflags';

@Component
export default class UserItem extends Vue {
  @Prop(Object) public user: Session;
  @Prop(Object) public session: Session;

  get emojiFlag() {
    return FLAGS[this.user.country] || '?';
  }
  get itsMe() {
    return this.user.username === this.session.username;
  }
}
</script>

<style lang="scss" scoped>
  .emoji-flag {
    cursor: help;
  }
</style>
