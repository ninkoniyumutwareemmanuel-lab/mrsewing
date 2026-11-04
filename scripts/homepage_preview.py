"""Homepage-only visual-review output; source destinations remain available for later phases."""
import json
import re


def disconnect(source):
    # Skip navigation is an accessibility control, not a destination-page link.
    def anchor(match):
        tag = match[0]
        if 'class="skip-link"' in tag:
            return tag
        tag = re.sub(r'\s(?:href|target|rel|tabindex|aria-disabled|role)="[^"]*"', '', tag)
        return tag[:-1] + ' role="link" aria-disabled="true" data-preview-link>'
    source = re.sub(r'<a\b[^>]*>', anchor, source)

    # Keep the form's appearance but remove submission credentials and all live actions.
    source = re.sub(r'<input\b(?=[^>]*type="hidden")[^>]*>', '', source)
    source = re.sub(r'(<form\b[^>]*)(>)', lambda m: re.sub(r'\s(?:action|method)="[^"]*"', '', m[1]) + ' data-preview-form aria-describedby="homepage-preview-note">', source)
    source = re.sub(r'<(?:input|select|textarea)\b[^>]*>', lambda m: m[0][:-1] + ' disabled>', source)
    source = re.sub(r'<button\b(?=[^>]*type="submit")[^>]*>', lambda m: m[0].replace('type="submit"', 'type="button" disabled'), source)
    source = re.sub(r'<div id="quoteSuccess".*?</div>', '', source, flags=re.S)
    source = source.replace('Your request is sent through Web3Forms for forwarding to Mr Sewing by email. Do not send payment PINs or sensitive documents.', 'Quotation form preview. Requests cannot be sent while we finish the homepage design.')
    source = source.replace('WhatsApp links open a message for you to review and send yourself.', 'Contact links are disconnected during this homepage design review.')
    source = source.replace('The form requires JavaScript for confirmed submission. Please', 'Homepage design preview. Contact actions are disconnected. You can review the layout below. Previously available contact options:')

    # The legacy order popup is not part of the visual-only homepage review.
    source = re.sub(r'  <!-- Order popup:.*?(?=\n\n</body>)', '', source, flags=re.S)
    source = re.sub(r'<noscript>\s*<p style=.*?</noscript>', '', source, flags=re.S)
    note = '<div class="homepage-preview-note" id="homepage-preview-note" role="note">Homepage design preview · Links and enquiries are not connected yet.</div>'
    source = source.replace('<main id="main-content">', '<main id="main-content">\n' + note, 1)

    # Do not advertise disconnected navigation as working structured-data destinations.
    def schema(match):
        data = json.loads(match[2])
        if isinstance(data, dict) and '@graph' in data:
            data['@graph'] = [node for node in data['@graph'] if node.get('@type') != 'SiteNavigationElement']
        return match[1] + json.dumps(data, ensure_ascii=False, indent=2) + match[3]
    return re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', schema, source, flags=re.S)
