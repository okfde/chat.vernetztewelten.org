<template>
  <div class="media" :key="entry.id">
    <div class="mr-2 p-1">
      {{ entry.word }}
    </div>
    <div class="media-body pt-1">
      {{ entry.meaning}}
      <span class="float-right">{{ emojiFlag }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import {DictionaryEntry} from '../types';

import {FLAGS} from '../data/emojiflags';

@Component
export default class DictionaryItem extends Vue {
  @Prop(Object) public entry: DictionaryEntry;

  get emojiFlag() {
    return FLAGS[this.entry.country] || '?';
  }
}
</script>