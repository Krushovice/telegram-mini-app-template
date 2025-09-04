import { initTheme } from "./components/theme.js";
import { mountCategories, mountGrid } from "./components/catalog.js";
import { exposeCartAPI } from "./components/cartSheet.js";
import { state } from "./components/state.js";

const tg = window.Telegram.WebApp;
tg.ready(); tg.expand();
initTheme(tg);

const categoriesEl = document.getElementById('categories');
const gridEl = document.getElementById('grid');

const cart = exposeCartAPI(tg);

function rerender(){
  mountCategories(categoriesEl, rerender);
  mountGrid(gridEl, cart.add);
}

rerender();
