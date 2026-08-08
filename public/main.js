
document.addEventListener('DOMContentLoaded',function(){
  var b=document.querySelector('.burger'),l=document.querySelector('.nav-links');
  if(b){b.addEventListener('click',function(){l.classList.toggle('open');});}
  // reflect chosen audience in hidden field label if present
  document.querySelectorAll('input[name="inquiry_type"]').forEach(function(r){
    r.addEventListener('change',function(){});
  });
});
