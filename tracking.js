/* Analytics + chat for photobooth.soundsdjevents.com. Added 11 Oct 2026.
   Modelled on weddings.soundsdjevents.com/tracking.js, minus the wedding
   lead value and the wedding thank-you conversion.

   GA4        G-7EG50CWDVF   (same property as soundsdjevents.com + weddings.)
   Google Ads AW-972541419   (base tag only, no conversion fires here)
   Clarity    yd28luey3g
   Meta Pixel 860582841130253
   Chat       ProfitFlo widget 6a23a991e53da97e71ee22c1 ("Master DJ AI")

   Events sent:
     check_date_click   any click on a Check My Date / Check the Prices CTA
     phone_click        any click-to-call
   The inquiry form is a ProfitFlo iframe, so a real submission can't be seen
   from this page. Corporate conversions belong on the form's own success
   step in ProfitFlo, not on a button click here.
*/

window.dataLayer = window.dataLayer || [];
function gtag(){ dataLayer.push(arguments); }
gtag('js', new Date());

var SDJ_LINKER = { 'domains': ['photobooth.soundsdjevents.com', 'soundsdjevents.com', 'weddings.soundsdjevents.com', 'corporate.soundsdjevents.com'] };
gtag('config', 'G-7EG50CWDVF', { 'linker': SDJ_LINKER });
gtag('config', 'AW-972541419', { 'linker': SDJ_LINKER });

(function(){
  var t = document.createElement('script'); t.async = true;
  t.src = 'https://www.googletagmanager.com/gtag/js?id=G-7EG50CWDVF';
  document.head.appendChild(t);
})();

/* Clarity, the Meta pixel and the chat load on the visitor's first scroll,
   tap, click or key, or 8 s after load, so they don't compete with the hero. */
function sdjLoadLater(fn){
  var done = false, evs = ['scroll','pointerdown','keydown','touchstart'];
  function go(){ if (done) return; done = true;
    evs.forEach(function(e){ removeEventListener(e, go, true); }); fn(); }
  evs.forEach(function(e){ addEventListener(e, go, { capture: true, passive: true, once: true }); });
  if (document.readyState === 'complete') setTimeout(go, 8000);
  else addEventListener('load', function(){ setTimeout(go, 8000); });
}
function sdjAddScript(src){
  var t = document.createElement('script'); t.async = true; t.src = src;
  var y = document.getElementsByTagName('script')[0]; y.parentNode.insertBefore(t, y);
}

/* Microsoft Clarity */
window.clarity = window.clarity || function(){ (window.clarity.q = window.clarity.q || []).push(arguments); };
sdjLoadLater(function(){ sdjAddScript('https://www.clarity.ms/tag/yd28luey3g'); });

/* Meta Pixel */
!function(f){if(f.fbq)return;var n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];}(window);
fbq('init','860582841130253');
fbq('track','PageView');
sdjLoadLater(function(){ sdjAddScript('https://connect.facebook.net/en_US/fbevents.js'); });

/* ProfitFlo chat widget — same agent as soundsdjevents.com. */
sdjLoadLater(function(){
  var s = document.createElement('script');
  s.src = 'https://widgets.leadconnectorhq.com/loader.js';
  s.setAttribute('data-resources-url', 'https://widgets.leadconnectorhq.com/chat-widget/loader.js');
  s.setAttribute('data-widget-id', '6a23a991e53da97e71ee22c1');
  s.setAttribute('data-source', 'WEBSITE');
  document.body.appendChild(s);
});

document.addEventListener('click', function(e){
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a) return;
  var href = a.getAttribute('href') || '';
  var label = ((a.innerText || a.textContent || '').trim().replace(/\s+/g, ' ')).slice(0, 80);

  if (href === '#check' || href === '#pricing') {
    gtag('event', 'check_date_click', { 'page_name': 'photobooth', 'link_text': label, 'link_url': href });
    if (window.fbq) fbq('trackCustom', 'CheckDateClick', { page_name: 'photobooth' });
  } else if (href.indexOf('tel:') === 0) {
    gtag('event', 'phone_click', { 'page_name': 'photobooth', 'link_text': label, 'phone_number': href.replace('tel:', '') });
    if (window.fbq) fbq('trackCustom', 'PhoneClick', { page_name: 'photobooth' });
  }
}, true);
