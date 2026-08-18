
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),l=document.querySelector('.nav-links');
  if(b){b.addEventListener('click',function(){l.classList.toggle('open');});}
  // reflect chosen audience in hidden field label if present
  document.querySelectorAll('input[name="inquiry_type"]').forEach(function(r){
    r.addEventListener('change',function(){});
  });
  // Video facade: swap the poster for a real player only when asked. Nothing from
  // youtube.com is requested until this fires, so the page stays light.
  document.addEventListener('click',function(e){
    var b=e.target.closest?e.target.closest('.vid-btn'):null;
    if(!b) return;
    var id=b.getAttribute('data-yt'); if(!id) return;
    var f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';
    f.title=b.getAttribute('aria-label')||'Video';
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    f.referrerPolicy='strict-origin-when-cross-origin';
    f.setAttribute('allowfullscreen','');
    b.parentNode.replaceChild(f,b);
  });
});
