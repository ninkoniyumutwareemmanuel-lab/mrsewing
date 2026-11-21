"""Small optional R57 homepage additions. Existing homepage sections stay intact."""
from html import escape
from homepage_redesign import video_preview

def portrait_showcase():
    """Reuse approved visual fallback; videos stay held until full publication gates."""
    return video_preview()

def featured_photo():
    """One approved tailoring photograph, without brochure-length text."""
    return ('''<section class="home-r57-feature" aria-labelledby="home-r57-feature-title">
      <div class="home-shell home-r57-feature-layout">
        <figure><img src="/hero-alterations.webp" alt="Tailor adjusting a jacket on a mannequin" width="1000" height="571" loading="lazy" decoding="async"></figure>
        <div><p class="home-eyebrow">The craft behind the fit</p><h2 id="home-r57-feature-title">Tailored to your ideas.</h2>
        <a class="home-button home-button-gold" href="/services/custom-tailoring/">Explore Tailoring &amp; Clothing Services <span aria-hidden="true">→</span></a></div>
      </div></section>''')
