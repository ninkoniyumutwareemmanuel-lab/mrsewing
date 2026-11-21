/* Preserve consent-era section links by opening the still-effective HTML Terms. */
(()=>{'use strict';
const current='/terms-and-conditions/current/';
if(location.pathname==='/terms-and-conditions/'&&location.hash){
  const hash=location.hash.slice(1);
  if(/^[a-zA-Z0-9_-]{1,100}$/.test(hash)){
    location.replace(current+location.search+location.hash);
  }
}
})();
