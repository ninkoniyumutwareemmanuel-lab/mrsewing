import {publicIntake} from '../_lib/public-api-cors.js';
import {providerKey} from '../_lib/shop-runtime.js';
import {handleSelected} from '../_lib/selected-design-handler.js';
export const onRequest=context=>publicIntake(context,request=>handleSelected(request,providerKey));
