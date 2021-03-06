<template>
  <div class="card border-warning bg-transparent mb-3">
    <div class="card-header bg-warning border-warning text-dark">
      <h5 class="float-left mt-2">Emoji-Wörterbuch</h5>
      <button class="emoji download-button btn float-right" title="Download" @click="exportCSV">
        <span>⬇️</span>
      </button>
    </div>
    <div class="card-body bg-transparent">
      <emoji-select
        v-show="showPicker"
        class="border border-light bg-light"
        @emoji="word = $event ; showPicker = false"
        :defaultemoji="word">
      </emoji-select>
      <div v-show="!showPicker" class="form-inline mb-3">
        <div class="form-row w-100">
          <div class="col-auto col-md-auto col-sm-12 mt-2">
            <div @click="showPicker = !showPicker" class="bg-light p-2 emoji-picker-container">
              <emoji-select-field
                :defaultemoji="word"
              ></emoji-select-field>
            </div>
          </div>
          <div class="col col-sm-12 col-md mt-2">
            <div class="input-group mb-3 w-100">
              <input type="text" v-model="meaning" @keyup.enter="addEntry"
                class="form-control" maxlength="255"
                placeholder="Bedeutung"/>
              <div class="input-group-append">
                <button class="btn btn-outline-light" type="button" @click="addEntry">
                  <span class="d-none d-lg-inline">Eintragen</span>
                  <span class="d-inline d-lg-none">+</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-show="!showPicker" class="entries">
        <dictionary-item v-for="entry in enhancedDictionary"
          :entry="entry" :key="entry.id"
        ></dictionary-item>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import EmojiSelect from './EmojiSelect.vue';
import EmojiSelectField from './EmojiSelectField.vue';
import DictionaryItem from './DictionaryItem.vue';

import {FLAGS} from '../data/emojiflags';
import {DictionaryEntry} from '../types';

const processRow = (row: string[]) => {
  let finalVal = '';
  for (let j = 0; j < row.length; j++) {
    const innerValue = row[j] === null ? '' : row[j].toString();
    let result = innerValue.replace(/"/g, '""');
    if (result.search(/("|,|\n)/g) >= 0) {
      result = '"' + result + '"';
    }
    if (j > 0) {
      finalVal += ',';
    }
    finalVal += result;
  }
  return finalVal;
};


@Component({
  components: {
    DictionaryItem,
    EmojiSelect,
    EmojiSelectField,
  },
})
export default class Dictionary extends Vue {
  @Prop(Array) public dictionary!: DictionaryEntry[];
  @Prop(Object) public countries: {[key: string]: string};

  private word = '';
  private meaning = '';
  private showPicker = false;

  get enhancedDictionary() {
    return this.dictionary.map((entry) => {
      entry.countryName = this.countries[entry.country] || '';
      return entry;
    });
  }

  private addEntry() {
    if (this.word === '') {
      return;
    }
    if (this.meaning === '') {
      return;
    }
    this.$emit('addentry', {
      word: this.word,
      meaning: this.meaning,
    });
    this.word = '';
    this.meaning = '';
  }

  private exportCSV() {
    const filename = 'woerterbuch.csv';
    const csvContent = ['wort,bedeutung,land'];
    for (const entry of this.dictionary) {
      csvContent.push(processRow([entry.word, entry.meaning, entry.country]));
    }

    const blob = new Blob([csvContent.join('\n')], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
      navigator.msSaveBlob(blob, filename);
    } else {
      const link = document.createElement('a');
      if (link.download !== undefined) { // feature detection
        // Browsers that support HTML5 download attribute
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }
    }
  }
}

</script>

<style lang="scss" scoped>

.download-button {
  cursor: pointer;
}

</style>
