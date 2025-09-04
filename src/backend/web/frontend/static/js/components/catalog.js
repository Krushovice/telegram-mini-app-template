import {CATALOG, CATS, state, money} from "./state.js";

export function mountCategories(el, onChange){
  el.innerHTML = "";
  CATS.forEach(c=>{
    const b = document.createElement('button');
    b.className = 'chip' + (state.category===c ? ' active' : '');
    b.textContent = c;
    b.onclick = ()=>{ state.category = c; onChange(); };
    el.appendChild(b);
  });
}

export function mountGrid(el, onAdd){
  const items = state.category==="Все" ? CATALOG : CATALOG.filter(x=>x.cat===state.category);
  el.innerHTML = "";
  items.forEach(x=>{
    const card = document.createElement('div'); card.className="card";
    const img = document.createElement('div'); img.className="img"; img.textContent = x.emoji;
    const body = document.createElement('div'); body.className="body";
    const t = document.createElement('div'); t.className="title"; t.textContent = x.title;
    const m = document.createElement('div'); m.className="meta"; m.textContent = x.desc;
    const row = document.createElement('div'); row.className="row";
    const price = document.createElement('div'); price.className="price"; price.textContent = money(x.price);
    const btn = document.createElement('button'); btn.className="btn"; btn.textContent="В корзину";
    btn.onclick = ()=> onAdd(x);
    row.append(price, btn);
    body.append(t, m, row);
    card.append(img, body);
    el.appendChild(card);
  });
}
