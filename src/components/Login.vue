<template>
  <div class="login">
    <h3>Login</h3>
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <form action="/enter" method="post" @submit="enterRoom">
    <p>
      <label for="id_room">Room:</label>
      <input v-model="roomName" type="text" name="room" required="" id="id_room">
    </p>
    <p>
      <label for="id_username">Username:</label>
      <input v-model="username" type="text" name="username" maxlength="255" required="" id="id_username">
    </p>
    <p>
      <label for="id_country">Country:</label>
      <select v-model="country" name="country" required="" id="id_country">
        <option v-for="countryLabel in countries" :key="countryLabel[0]" :value="countryLabel[0]">
          {{ countryLabel[1] }}
        </option>
      </select>
    </p>
    <button type="submit">Eintreten</button>
  </form>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import router from '../router';

@Component
export default class Login extends Vue {
  @Prop({type: Object, default: null}) private session: object | null | undefined;
  @Prop({type: Object, default: null}) private room: object | null | undefined;
  @Prop(Array) private countries!: Array<Array<string>>;
  username = ''
  roomName = ''
  country = ''
  error = ''

  mounted() {
    if(this.room !== null) {
      this.roomName = this.room.name;
    }
    if(this.session !== null) {
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
  enterRoom(e: Event) {
    e.preventDefault();
    this.error = ''
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
      })
    }).then((response) => response.json())
    .then((data) => {
      if (data.error) {
        console.error(data.message);
        this.error = data.message;
      }
      router.replace(data.room);
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

</style>
