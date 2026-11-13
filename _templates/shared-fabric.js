/* Shared enquiry preferences; palette labels are requests, never inventory claims. */
window.MrFabricPreferences=function(source){
 const labels={now:'I Want to Choose a Fabric',advice:'Help Me Choose a Fabric',own:'I Have My Own Fabric'};
 function clean(value){
  if(!value||typeof value!=='object'||!Object.hasOwn(labels,value.choice))return null;
  const out={choice:value.choice,fabricRef:'',colour:'',colourDescription:''};
  if(out.choice==='now'){
   out.fabricRef=Object.hasOwn(source.fabrics,value.fabricRef||'')?value.fabricRef:'';
   out.colour=Object.hasOwn(source.colours||{},value.colour||'')?value.colour:'';
   if(out.colour==='other'&&typeof value.colourDescription==='string'&&value.colourDescription.length<=80&&/^[\p{L}\p{N} .,'’()/+#-]*$/u.test(value.colourDescription))out.colourDescription=value.colourDescription.trim();
  }
  return out;
 }
 function valid(value){const p=clean(value);return !!p&&(p.choice!=='now'||!!p.fabricRef&&!!p.colour&&(p.colour!=='other'||!!p.colourDescription));}
 function details(value){const p=clean(value);return p?{...p,label:labels[p.choice],fabricName:source.fabrics[p.fabricRef]?.name||'',colourName:source.colours?.[p.colour]?.name||''}:null;}
 function pack(value){const p=clean(value);return p?JSON.stringify([p.choice,p.fabricRef,p.colour,p.colourDescription]):'';}
 function unpack(value){try{if(typeof value!=='string'||value.length>600)return null;const a=JSON.parse(value);return Array.isArray(a)&&a.length===4?clean({choice:a[0],fabricRef:a[1],colour:a[2],colourDescription:a[3]}):null;}catch{return null;}}
 return{clean,valid,details,pack,unpack};
};
