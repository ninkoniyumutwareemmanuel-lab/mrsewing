/* Non-secret routing only. Public intake validation stays on the main-branch Worker. */
(()=>{'use strict';const config=/* public-api-config */{};window.MrPublicAPI={url(value){const u=new URL(value,location.href);if(u.origin===location.origin&&config.paths.includes(u.pathname)&&config.productionOrigins.includes(location.origin))return config.backendOrigin+u.pathname;return value;}};})();
