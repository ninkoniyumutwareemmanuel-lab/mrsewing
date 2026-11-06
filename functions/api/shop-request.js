import { products, providerKey } from "../_lib/shop-runtime.js";
import { handle } from "../_lib/shop-handler.js";
export const onRequest = ({ request }) =>
  handle(request, products, providerKey);
