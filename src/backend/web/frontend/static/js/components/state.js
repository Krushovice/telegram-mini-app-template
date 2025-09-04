export const CATALOG = [
  {id:1, title:"Эспрессо",     cat:"Кофе",    price:120, desc:"30 мл, крепкий", emoji:"☕️"},
  {id:2, title:"Американо",    cat:"Кофе",    price:140, desc:"250 мл",        emoji:"☕️"},
  {id:3, title:"Капучино",     cat:"Кофе",    price:190, desc:"250 мл",        emoji:"🥛"},
  {id:4, title:"Латте",        cat:"Кофе",    price:200, desc:"300 мл",        emoji:"🥛"},
  {id:5, title:"Матча латте",  cat:"Напитки", price:220, desc:"300 мл",        emoji:"🍵"},
  {id:6, title:"Чай бергамот", cat:"Напитки", price:160, desc:"400 мл",        emoji:"🍵"},
  {id:7, title:"Круассан",     cat:"Выпечка", price:150, desc:"Сливочный",     emoji:"🥐"},
  {id:8, title:"Чизкейк",      cat:"Десерты", price:260, desc:"Нью-Йорк",      emoji:"🍰"},
];

export const CATS = ["Все", ...Array.from(new Set(CATALOG.map(x=>x.cat)))];

export const state = {
  category: "Все",
  cart: new Map(), // id -> {item, qty}
};

export const money = v => `${v} ₽`;
export const cartCount = () => Array.from(state.cart.values()).reduce((n, {qty})=>n+qty, 0);
export const cartSum   = () => Array.from(state.cart.values()).reduce((s, {item,qty})=>s+item.price*qty, 0);
