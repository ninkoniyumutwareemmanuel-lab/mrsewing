import {pages} from '../_lib/shop-preview-pages.js';
import {handlePreview} from '../_lib/shop-preview-handler.js';
export const onRequest=context=>handlePreview(context,pages);
