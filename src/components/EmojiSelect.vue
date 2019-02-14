<template>
  <div>
    <div @click="showPicker = !showPicker" class="emoji-picker emoji">
      <svg v-if="!defaultemoji" height="20" viewBox="0 0 24 24" width="20" xmlns="http://www.w3.org/2000/svg">
        <path d="M0 0h24v24H0z" fill="none"/>
        <path d="M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z"/>
      </svg>
      <span v-else>{{ defaultemoji }}</span>
    </div>
    <picker
      v-show="showPicker"
      title=""
      :perLine="perLine"
      :native="true"
      :show-search="false" 
      :show-preview="true"
      :show-skin-tones="true"
      @select="insert"
      :i18n="i18n"
      :style="style" 
    ></picker>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import { Picker } from 'emoji-mart-vue';

interface Emoji {
  colons: string;
  emoticons: string[];
  id: string;
  name: string;
  native: string;
  skin: number|null;
  unified: string;
}

@Component({
  components: {
    Picker,
  },
  directives: {
    focus: {
      inserted(el) {
        el.focus();
      },
    },
  },
})
export default class EmojiSelect extends Vue {
  @Prop({type: String, default: ''}) public defaultemoji!: string|null;
  @Prop(Boolean) public isMobile!: boolean;
  @Prop(Boolean) public fixed: boolean;

  private showPicker = false;
  private i18n = {
    search: 'Suchen',
    notfound: 'Kein Emoji gefunden',
    categories: {
      search: 'Suchergebnisse',
      recent: 'Oft verwendet',
      people: 'Gesichter & Menschen',
      nature: 'Tiere & Natur',
      foods: 'Essen & Trinken',
      activity: 'Freizeit',
      places: 'Reisen & Orte',
      objects: 'Objekte',
      symbols: 'Symbole',
      flags: 'Flaggen',
      custom: 'Eigene',
    },
  };
  get perLine() {
    if (this.isMobile) {
      return 7;
    }
    return 9;
  }
  get style() {
    if (this.fixed) {
      return {
        position: 'fixed',
        bottom: '40px',
        left: '15px',
        zIndex: '1000',
      };
    }
    return {
      position: 'absolute',
      bottom: '40px',
      left: '0px',
      zIndex: '1000',
    };
  }

  private insert(emoji: Emoji) {
    this.showPicker = false;
    this.$emit('emoji', emoji.native);
  }
}
</script>

<style lang="scss">
.emoji-mart-preview-emoji, .emoji-mart-preview-data {
  display: none;
}
.emoji-mart-emoji > span {
  cursor: pointer;
}
.emoji-picker {
  cursor: pointer;
  text-align: center;
}
</style>
