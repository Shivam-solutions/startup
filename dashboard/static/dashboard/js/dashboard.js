document.getElementById('sidebarToggle')?.addEventListener('click', function(e){
  const sidebar = document.getElementById('sidebar');
  if(!sidebar) return;
  if(sidebar.style.display === 'none' || getComputedStyle(sidebar).display === 'none'){
    sidebar.style.display = 'block';
  } else {
    sidebar.style.display = 'none';
  }
});
