"""Reusable customer-facing service facts, from the owner-approved handoff only."""
from html import escape
from customer_information import expand,information
from site_seo import ROOT

def styles():return (ROOT/'_templates/service-information.css').read_text()
def section(title,text,ident=None):
 content=expand(text)
 if content.startswith('<div class="tw"'):
  end=content.index('</div>')+6;content=content[:end]+'<p>'+content[end:].strip()+'</p>'
 else:content='<p>'+content+'</p>'
 return '<section class="offer-section"'+(' id="'+ident+'"' if ident else '')+'><h2>'+escape(title)+'</h2>'+content+'</section>'
def price_link():return '<a class="home-text-link" href="/faq/prices-packages-payments/">Suit prices, packages &amp; payments</a>'
def tailoring():
 return section('Standard suit prices','{{suit_price_table}} {{higherCollections}} {{extras}}','suit-prices')+section('Suit contents and package','{{contents}} {{package}}')+section('Suit-order accessories and packaging','{{accessoryTerms}} {{packagingTerms}}')+section('Plan your order','{{timing}} {{suitPayment}} {{balance}}')+'<nav class="offer-links" aria-label="Related service pricing"><a href="/services/express-tailoring/">Express tailoring</a><a href="/services/mobile-fitting/">Mobile fittings</a>'+price_link()+'</nav>'
def express():return section('Express pricing','{{expressPricing}} {{expressExamples}}')+section('Express and mobile together','{{combinedPricing}} {{mobileScope}}')
def mobile():return section('Kigali mobile suit orders','{{mobilePricing}} {{mobileExample}}')+section('Express and mobile together','{{combinedPricing}}')+section('Confirm the scope first','{{mobileScope}}')
def alterations():return section('Starting alteration prices','{{alteration_table}} These are starting prices, not a fixed price for every job. A jacket, trousers and shirt alteration is not a three-piece suit with a waistcoat.')+section('Assessment, payment and timing','{{alterationTiming}} {{standalonePayment}} {{balance}}')+section('Express alterations','{{alterationExpress}}')+section('Optional services and transport','{{alterationExtras}} {{packagingTerms}}')
def paid_care():return section('Paid suit-cleaning packages','{{care_price_table}} {{careIncluded}}','paid-suit-cleaning')+section('Standard and express timing','{{careTiming}} {{careExpress}}')+section('Collection, return and other garments','{{careArrangements}}')+section('Included suit care and packaging','{{package}} Follow-up care is separate from the initial cleaning in the standard suit package. Confirm any applicable arrangement with the team. {{packagingTerms}}')
def payment():return section('Payment methods','{{paymentMethods}} {{paymentComingSoon}}')
