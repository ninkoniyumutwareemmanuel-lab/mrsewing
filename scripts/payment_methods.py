"""Owner-approved payment labels and original generic symbols; no gateway."""
def payment_methods():
 paths=[('Mobile Money','<rect x="7" y="2" width="14" height="24" rx="3"/><path d="M11 6h6M12 22h4M10 12h8M10 16h5"/>'),('Bank Transfer','<path d="M2 10 14 3l12 7H2ZM4 24h20M7 12v9m7-9v9m7-9v9M2 27h24"/>'),('Cryptocurrency','<circle cx="14" cy="14" r="11"/><circle cx="14" cy="8" r="2"/><circle cx="9" cy="17" r="2"/><circle cx="19" cy="17" r="2"/><path d="m13 10-3 5m5-5 3 5m-7 2h6"/>')]
 return '<ul class="payment-methods" aria-label="Accepted payment methods">'+''.join('<li><svg width="28" height="28" viewBox="0 0 28 30" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false">'+path+'</svg><span>'+label+'</span></li>' for label,path in paths)+'</ul>'
