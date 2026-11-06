import {providerKey} from '../_lib/shop-runtime.js';
import {handleSelected} from '../_lib/selected-design-handler.js';
export const onRequest=({request})=>handleSelected(request,providerKey);
