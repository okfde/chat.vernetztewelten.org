<template>
  <div class="login">
    <h3>Betrete einen Raum</h3>
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <form action="/enter" method="post" @submit="enterRoom">
      <div class="form-group">
        <label for="id_room">Name des Raums:</label>
        <input v-model="roomName" type="text" name="room" required=""  maxlength="255" id="id_room" class="form-control">
      </div>
      <div class="form-group">
        <label for="id_username">Dein Nutzername:</label>
        <input v-model="username" type="text" name="username" maxlength="255" required="" id="id_username" class="form-control">
      </div>
      <div class="form-group">
        <label for="id_country">Dein Land:</label>
        <select v-model="country" name="country" required="" id="id_country" class="form-control">
          <option v-for="countryLabel in countries" :key="countryLabel[0]" :value="countryLabel[0]">
            {{ countryLabel[1] }}
          </option>
        </select>
      </div>
      <p class="text-right">
        <button class="btn btn-primary" type="submit">Eintreten</button>
      </p>
    </form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import router from '../router';

import {Room, Session} from '../types';

@Component
export default class Login extends Vue {
  @Prop({type: Object, default: null}) private session: Session | null;
  @Prop({type: Object, default: null}) private room: Room | null;
  @Prop(Array) private countries!: string[][];
  private username = '';
  private roomName = '';
  private country = '';
  private error = '';

  public mounted() {
    if (this.room !== null) {
      this.roomName = this.room.name;
    }
    if (this.session !== null) {
      this.username = this.session.username;
      this.country = this.session.country;
    }
  }

  get csrfToken(): string {
    const el = document.querySelector('input[name=csrfmiddlewaretoken]') as HTMLInputElement;
    if (el !== null) {
      return el.value;
    }
    return '';
  }

  private enterRoom(e: Event) {
    e.preventDefault();
    this.error = '';
    window.fetch('/enter/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': this.csrfToken,
      },
      body: JSON.stringify({
        username: this.username,
        room: this.roomName,
        country: this.country,
      }),
    }).then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error(data.message);
        this.error = data.message;
      }
      router.replace(data.room);
    });
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
