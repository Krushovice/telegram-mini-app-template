export function initTheme(tg){
  function apply(){
    document.documentElement.style.setProperty('--bg', tg.backgroundColor || '#ffffff');
    document.documentElement.style.setProperty('--text', tg.colorScheme === 'dark' ? '#efefef' : '#111111');
    document.documentElement.style.setProperty('--muted', tg.colorScheme === 'dark' ? '#9ca3af' : '#6b7280');
    document.documentElement.style.setProperty('--card', tg.colorScheme === 'dark' ? '#1f2937' : '#f5f5f7');
    document.documentElement.style.setProperty('--sep', tg.colorScheme === 'dark' ? '#374151' : '#e5e7eb');
  }
  apply(); tg.onEvent('themeChanged', apply);
}
