<template>
  <div>
    <h3>Dictionary</h3>
    <dl>
      <template v-for="entry in dictionary">
        <dt :key="'dt' + entry.id">
          <code>{{ entry.word }}</code>
        </dt>
        <dd :key="'dd' + entry.id">
          {{ entry.meaning }}
        </dd>
      </template>
    </dl>
    <input type="text" v-model="word">
    <input type="text" v-model="meaning" @keyup.enter="addEntry" maxlength="255">
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import {DictionaryEntry} from '../types';

@Component
export default class Dictionary extends Vue {
  @Prop(Array) public dictionary!: DictionaryEntry[];
  private word = '';
  private meaning = '';

  private addEntry() {
    if (this.word === '' || this.meaning === '') {
      return;
    }
    this.$emit('addentry', {
      word: this.word,
      meaning: this.meaning,
    });
    this.word = '';
    this.meaning = '';
  }
}
</script>