/* Only URLs present in the build-generated, publication-gated catalogue are accepted. */
(()=>{'use strict';
const read=id=>JSON.parse(document.getElementById(id)?.textContent||'{}');
function resolve(state){const designs=read('requestDesignMedia'),projects=read('portfolioRequestData');const d=Object.hasOwn(designs,state.design||'')?designs[state.design]:null;if(!d)return null;const project=state.project?(Object.hasOwn(projects,state.project)?projects[state.project]:null):null;if(state.project&&(!project||project.designRef!==state.design))return null;const images=project?.images||d.images||[];const url=state.photo||images[0]?.url;const image=images.find(i=>i.url===url);if(!image)return null;return{...d,...image,name:project?.name||d.name,photoURL:image.url,route:project?.route||d.route,project:project?state.project:null};}
window.MrSelectedDesign={resolve};
})();
