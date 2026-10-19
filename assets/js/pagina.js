/* RAF Serventia Docs — preferências locais. Nenhuma conexão com o PJe. */
'use strict';
const favButton=document.getElementById('fav');
let favorites=new Set();
try{const a=JSON.parse(localStorage.getItem('raf-serventia-favoritos')||'[]');if(Array.isArray(a))favorites=new Set(a)}catch{}
function updateFav(){
 if(!favButton)return;
 const active=favorites.has(favButton.dataset.code);
 favButton.textContent=active?'★ Favoritado':'☆ Favoritar';
 favButton.classList.toggle('is-fav',active);
 favButton.setAttribute('aria-pressed',String(active));
}
if(favButton){
 favButton.addEventListener('click',()=>{
  const code=favButton.dataset.code;
  favorites.has(code)?favorites.delete(code):favorites.add(code);
  try{localStorage.setItem('raf-serventia-favoritos',JSON.stringify([...favorites]))}catch{}
  updateFav();
 });
 updateFav();
}
function applyTheme(value){
 document.documentElement.classList.toggle('dark',value==='dark');
 try{localStorage.setItem('raf-serventia-theme',value)}catch{}
}
try{if(localStorage.getItem('raf-serventia-theme')==='dark')document.documentElement.classList.add('dark')}catch{}
const themeButton=document.getElementById('theme');
if(themeButton)themeButton.addEventListener('click',()=>applyTheme(document.documentElement.classList.contains('dark')?'light':'dark'));
