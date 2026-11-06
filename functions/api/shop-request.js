import {publicIntake} from '../_lib/public-api-cors.js';
import { products, providerKey } from "../_lib/shop-runtime.js";
import { handle } from "../_lib/shop-handler.js";
export const onRequest = context =>
  publicIntake(context,request=>handle(request, products, providerKey));
