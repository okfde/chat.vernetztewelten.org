<template>
  <div class="card border-warning bg-transparent mb-3">
    <div class="card-header bg-warning border-warning text-dark">
      <strong>Emoji-Wörterbuch</strong>
    </div>
    <div class="card-body bg-transparent">
      <div class="form-inline mb-3">
        <label class="sr-only" for="inlineFormInputGroupUsername2">Username</label>
        
        <div class="form-row">
          <div class="col-3">
            <div class="bg-light p-2 emoji-picker">
              <emoji-select
                class="simple-picker"
                @emoji="word = $event"
                :defaultemoji="word">
              </emoji-select>
            </div>
          </div>
          <div class="col-9">
            <input type="text" v-model="meaning" @keyup.enter="addEntry"
              class="form-control" maxlength="255"
              placeholder="Neue Bedeutung"/>
          </div>
        </div>
      </div>

      <template v-for="entry in dictionary">
        <div class="media" :key="entry.id">
          <div class="mr-2 p-1">
            {{ entry.word }}
          </div>
          <div class="media-body pt-1">
            {{ entry.meaning}}
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import EmojiSelect from './EmojiSelect.vue';

import {DictionaryEntry} from '../types';

@Component({
  components: {
    EmojiSelect,
  },
})
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

<style lang="scss" scoped>
.emoji-picker {
  position: relative;
}
</style>
