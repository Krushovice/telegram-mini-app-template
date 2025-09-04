import {state, money, cartCount, cartSum} from "./state.js";

export function exposeCartAPI(tg){
  const sheet = document.getElementById('sheet');
  const sheetBody = document.getElementById('sheetBody');
  const sheetCount = document.getElementById('sheetCount');
  const sumEl = document.getElementById('sum');
  const totalEl = document.getElementById('total');
  const badgeEl = document.getElementById('cartBadge');

  function open(){ sheet.classList.add('open'); tg.BackButton.show(); render(); }
  function close(){ sheet.classList.remove('open'); tg.BackButton.hide(); }
  tg.BackButton.onClick(close);

  function render(){
    sheetCount.textContent = `${cartCount()} поз.`;
    sheetBody.innerHTML = "";
    for (const {item, qty} of state.cart.values()){
      const row = document.createElement('div'); row.className="item";
      const left = document.createElement('div');
      const name = document.createElement('div'); name.className='name'; name.textContent = item.title;
      const meta = document.createElement('div'); meta.className='muted'; meta.textContent = money(item.price);
      left.append(name, meta);
      const right = document.createElement('div'); right.className='qty';
      const minus = document.createElement('button'); minus.textContent='–'; minus.onclick=()=>removeOne(item.id);
      const num = document.createElement('div'); num.textContent = qty;
      const plus = document.createElement('button'); plus.textContent='+'; plus.onclick=()=>addOne(item.id);
      right.append(minus, num, plus);
      row.append(left, right);
      sheetBody.appendChild(row);
    }
    const s = cartSum();
    sumEl.textContent = money(s);
    totalEl.textContent = money(s);
    updateBadge();
  }

  function updateBadge(){
    badgeEl.textContent = cartCount();
    if (cartCount()>0) {
      tg.MainButton.setText(`Оформить • ${money(cartSum())}`);
      tg.MainButton.show();
    } else {
      tg.MainButton.hide();
    }
  }

  function add(item){
    const cur = state.cart.get(item.id) || {item, qty:0};
    cur.qty += 1; state.cart.set(item.id, cur);
    updateBadge(); open(); render(); tg.HapticFeedback.impactOccurred('light');
  }
  function addOne(id){ const cur = state.cart.get(id); if(!cur) return; cur.qty+=1; state.cart.set(id, cur); render(); updateBadge(); }
  function removeOne(id){
    const cur = state.cart.get(id); if(!cur) return;
    cur.qty -= 1; if (cur.qty<=0) state.cart.delete(id); else state.cart.set(id, cur);
    render(); updateBadge();
  }

  // Глобально — чтобы base.html мог вызвать closeSheet()
  window.Coffee = { closeSheet: close };

  // бейдж откроет корзину
  badgeEl.addEventListener('click', ()=>{ if(cartCount()>0){ open(); render(); }});

  // MainButton оформляет черновик (пока шлём в бота, позже — /api/checkout)
  tg.MainButton.onClick(()=>{
    const payload = {
      type: "checkout_draft",
      items: Array.from(state.cart.values()).map(({item, qty})=>({id:item.id, title:item.title, price:item.price, qty})),
      sum: cartSum(),
      at: new Date().toISOString()
    };
    tg.sendData(JSON.stringify(payload));
    tg.close();
  });

  return { add };
}
