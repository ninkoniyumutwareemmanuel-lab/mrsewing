import {handle} from '../../scripts/edge/customer-requests.mjs';
export const onRequest = ({request,env}) => handle(request,env);
