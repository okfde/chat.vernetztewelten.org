<template>
  <div>
    <picker
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
  private width = 1024;

  public mounted() {
    this.calculateWidth();
    window.addEventListener('orientationchange', this.calculateWidth);
    window.addEventListener('resize', this.calculateWidth);
  }
  public calculateWidth() {
    this.width = window.innerWidth;
  }

  get perLine() {
    if (this.width > 1200) {
      return 9;
    } else if (this.width > 992) {
      return 7;
    } else if (this.width > 576) {
      return 6;
    } else if (this.width < 400) {
      return 6;
    }
    return 9;
  }
  get style() {
    return {
      margin: 'auto',
    };
  }

  private insert(emoji: Emoji) {
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
.emoji-mart-preview {
  height: 36px !important;
}
</style>
