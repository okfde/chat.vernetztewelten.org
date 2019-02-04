import Vue from 'vue';
import App from './App.vue';
import router from './router';
import './registerServiceWorker';

Vue.config.productionTip = false;

interface IPropsObject {
  [key: string]: string|boolean|null;
}

function snakeToCamel(s: string) {
  return s.replace(/(-\w)/g, (m) => m[1].toUpperCase());
}

function getPropsFromElement(el: Element) {
  const attrs = el.attributes;
  const props: IPropsObject = {};

  for (const attr of attrs) {
    if (attr.name[0] === 'v' && attr.name[1] === '-') {
      continue;
    }
    if (attr.name === 'id' || attr.name === 'class') {
      continue;
    }
    let val = attr.value;
    let nonStringVal: boolean|null = false;
    let name = attr.name;
    if (attr.name[0] === ':') {
      name = attr.name.substring(1);
      if (attr.value[0] === '{' || attr.value[0] === '[') {
        val = JSON.parse(attr.value);
      }
      if (attr.value === 'true') {
        nonStringVal = true;
      }
      if (attr.value === 'null') {
        nonStringVal = null;
      }
    }
    const attrName = snakeToCamel(name);
    if (nonStringVal !== false) {
      props[attrName] = nonStringVal;
    } else {
      props[attrName] = val;
    }
  }
  return props;
}

const appId = '#app';
const app = document.querySelector(appId);

if (app !== null) {
  new Vue({
    router,
    render: (h) => h(App, {
      props: getPropsFromElement(app),
    }),
  }).$mount(appId);
}
