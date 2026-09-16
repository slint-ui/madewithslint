import json
import argparse
import os
import re

def is_valid(app_data):
    """Check if the required fields in app_data are non-empty and valid."""
    required_fields = ['class_style', 'image_src', 'image_alt', 'app_title', 'app_company', 'app_description']
    
    # Check that all required fields are present and non-empty
    for field in required_fields:
        if field not in app_data or not app_data[field].strip():
            print(f"Skipping invalid entry due to missing or empty field: {field}")
            return False
    return True

def convert_to_html_id(text):
    # Replace spaces and underscores with hyphens
    text = text.replace(" ", "-").replace("_", "-")
    
    # Remove any characters that are not alphanumeric or hyphens
    text = re.sub(r'[^a-zA-Z0-9-]', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    return text

# Inline SVG icons (24px grid, stroked), so the cards don't need an icon font.
# width/height are set on the element so they render at a sane size even on a
# page without the card CSS.
ICONS = {
    "story": '<path d="M2 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H2z"/><path d="M22 4h-7a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h8z"/>',
    "live": '<path d="M7 4l13 8-13 8z"/>',
    "source": '<path d="M8 7l-5 5 5 5"/><path d="M16 7l5 5-5 5"/>',
    "website": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
}
# Filter labels, in display order. An entry's "category" must be one of these
# keys; the filter lists only the categories that have entries.
CATEGORIES = {
    "embedded": "Embedded",
    "audio": "Audio & music",
    "games": "Games",
    "tools": "Developer tools",
    "productivity": "Productivity",
    "components": "Components",
}

# Card images: the 800px WebP thumbnails make_thumbs.py writes, served from
# madewithslint.com so they resolve on both sites. thumbs.json gives each one's
# size; an entry without a thumbnail uses its image_src as before.
THUMB_BASE = "https://madewithslint.com/assets/img/thumbs/"
THUMB_MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'img', 'thumbs', 'thumbs.json')

# Cards in the first row load straight away; the rest wait until scrolled near.
EAGER_CARDS = 4

ARROW = '<svg class="app-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def icon(name):
    return (f'<svg class="app-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


def load_thumbs():
    try:
        with open(THUMB_MANIFEST, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def image_tag(app_data, app_id, thumbs, eager):
    """The card image: the thumbnail when there is one for this image_src.

    If the thumbnail fails to load (not deployed yet, say) the image falls back
    to image_src. The onload/onerror handlers let the gallery show a placeholder until the
    image has loaded; see LOADER_JS.
    """
    image_src = app_data['image_src']
    image_alt = app_data['image_alt']
    thumb = thumbs.get(app_id)
    loading = 'eager' if eager else 'lazy'
    if thumb and thumb.get('source') == image_src:
        src = THUMB_BASE + app_id + '.webp'
        size = f' width="{thumb["width"]}" height="{thumb["height"]}"'
        fallback = f' data-fallback="{image_src}"'
    else:
        src, size, fallback = image_src, '', ''
    return (f'<img src="{src}" alt="{image_alt}"{size} loading="{loading}" decoding="async"{fallback} '
            f'onload="mwsImg(this)" onerror="mwsImg(this, true)">')


def generate_html(app_data, thumbs=None, eager=False):
    """Generate HTML for an application entry.

    Every card has the same shape: screenshot, product name, author or company,
    a short description, then one row of actions. The first available link is
    the main text link, in this priority order:

        customer story > live demo > source > website

    and any others follow as icon links. Each icon link keeps its label in a
    <span class="app-act-label"> -- the page can hide it visually and it still
    names the link for screen readers.
    """
    app_title = app_data['app_title']
    app_company = app_data['app_company']
    app_description = app_data['app_description']
    class_style = app_data['class_style']

    # Optional fields
    category = app_data.get('category', '').strip()
    git_link = app_data.get('git_link', '')
    preview_link = app_data.get('preview_link', '')
    doc_link = app_data.get('doc_link', '')
    story_link = app_data.get('story_link', '')

    app_id = convert_to_html_id(app_title)

    # (href, label, icon), in priority order.
    actions = []
    if story_link:
        actions.append((story_link, "Read customer story", "story"))
    if preview_link:
        actions.append((preview_link, "Try it live", "live"))
    if git_link:
        actions.append((git_link, "View source", "source"))
    if doc_link:
        actions.append((doc_link, "Visit website", "website"))

    primary = actions[0] if actions else None
    secondary = actions[1:]

    # The screenshot doubles as a click target for the main link.
    img_tag = image_tag(app_data, app_id, thumbs or {}, eager)
    header_media = (f'<a href="{primary[0]}" target="_blank" rel="noopener">{img_tag}</a>'
                    if primary else img_tag)

    actions_html = ''
    if primary:
        primary_html = (f'<a class="application-primary" href="{primary[0]}" target="_blank" rel="noopener">'
                        f'{primary[1]} {ARROW}</a>')
        secondary_html = ''
        if secondary:
            links = ''.join(
                f'<a href="{href}" target="_blank" rel="noopener" class="app-act" title="{label}">'
                f'{icon(name)}<span class="app-act-label">{label}</span></a>'
                for (href, label, name) in secondary
            )
            secondary_html = f'<div class="application-cta">{links}</div>'
        actions_html = f'<div class="application-actions">{primary_html}{secondary_html}</div>'

    category_attr = f' data-category="{category}"' if category else ''

    html_template = f"""
                    <!-- {app_title} -->
                    <div id="{app_id}" class="application-item {class_style}"{category_attr}>
                        <div class="application-content">
                            <div class="application-header">
                                {header_media}
                            </div>
                            <div class="application-body">
                                <h3 class="application-title">{app_title}</h3>
                                <h4 class="application-company">{app_company}</h4>
                                <p class="application-description">{app_description}</p>
                                {actions_html}
                            </div>
                        </div>
                    </div><!-- .application-item -->\n"""

    return html_template

def load_data_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        # You can log more details or handle the error as needed
    except Exception as e:
        print(f"An error occurred: {e}")

# Marks an image's box loaded, so the placeholder shimmer stops and the image
# fades in. On an error it first retries data-fallback (the original image),
# and marks the box loaded when there is nothing left to try. Defined before
# the cards, so it exists when their onload/onerror fire.
LOADER_JS = (
    "function mwsImg(img,failed){"
    "if(failed&&img.dataset.fallback){var f=img.dataset.fallback;delete img.dataset.fallback;"
    "img.removeAttribute('width');img.removeAttribute('height');img.src=f;return;}"
    "var box=img.closest('.application-header');if(box)box.classList.add('is-loaded');}"
)


def filter_html(categories):
    """Radios + labels for the category filter, and the CSS that connects them.

    Radios sit before .col-wrap as siblings, so `:checked ~ .col-wrap` can hide
    the cards of other categories without script.
    """
    if len(categories) < 2:
        return '', ''
    keys = ['all'] + categories
    radios = ''.join(
        f'<input type="radio" class="mws-radio" name="mws-cat" id="mws-cat-{k}"{" checked" if k == "all" else ""}>'
        for k in keys)
    labels = ''.join(
        f'<label for="mws-cat-{k}">{"All" if k == "all" else CATEGORIES[k]}</label>' for k in keys)
    on = ',\n'.join(f'#mws-cat-{k}:checked ~ .mws-filter label[for="mws-cat-{k}"]' for k in keys)
    focus = ',\n'.join(f'#mws-cat-{k}:focus-visible ~ .mws-filter label[for="mws-cat-{k}"]' for k in keys)
    hide = ',\n'.join(
        f'#mws-cat-{k}:checked ~ .col-wrap .application-item:not([data-category="{k}"])' for k in categories)
    css = (f'{on} {{ background: var(--mws-accent); color: #fff; }}\n'
           f'{focus} {{ outline: 2px solid var(--mws-focus); outline-offset: 2px; }}\n'
           f'@media (forced-colors: active) {{ {on} {{ forced-color-adjust: none; background: Highlight; color: HighlightText; }} }}\n'
           f'{hide} {{ display: none; }}\n')
    return (radios + f'<div class="mws-filter" role="group" aria-label="Filter by category">{labels}</div>'), css


def generate_html_for_all_apps(data):
    valid = []
    for app in data:
        if is_valid(app):  # Only generate HTML for valid entries
            valid.append(app)
        else:
            print("Skipping entry due to invalid data.")

    for app in valid:
        category = app.get('category', '').strip()
        if not category:
            print(f"No category for {app['app_title']}; it will only show under All")
        elif category not in CATEGORIES:
            print(f"Unknown category '{category}' for {app['app_title']}; expected one of {', '.join(CATEGORIES)}")

    present = [k for k in CATEGORIES if any(app.get('category', '').strip() == k for app in valid)]
    filter_markup, filter_css = filter_html(present)

    gallery_css = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'css', 'gallery.css'),
                       encoding='utf-8').read()

    html_output = f"""
            <section class="applications mws-gallery">
                <style>
{gallery_css}
{filter_css}
                </style>
                <script>{LOADER_JS}</script>
                {filter_markup}
                <div class="col-wrap">"""
    thumbs = load_thumbs()
    for i, app in enumerate(valid):
        html_output += generate_html(app, thumbs, eager=i < EAGER_CARDS)
    html_output += """
                </div><!-- .col-wrap -->
            </section><!-- .applications -->\n"""
    return html_output


def replace_placeholder_in_html(template_file_path, html_file_path, placeholder, new_content):
    # Read the HTML file
    with open(template_file_path, 'r') as file:
        file_content = file.read()

    # Replace the placeholder with the new content
    updated_content = file_content.replace(placeholder, new_content)

    # Write the updated content back to the HTML file
    with open(html_file_path, 'w') as file:
        file.write(updated_content)

def main(json_file_path, template_file_path, html_file_path):
    placeholder = '<?applications?>'

    # Load data from JSON
    data = load_data_from_json(json_file_path)

    # Generate HTML for all the valid applications in the JSON array
    html_code = generate_html_for_all_apps(data)

    # Replace the placeholder in the HTML file
    replace_placeholder_in_html(template_file_path, html_file_path, placeholder, html_code)

if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Generate madewithslint showcase page.")
    parser.add_argument('--json', default='showcases.json', help='Path to the JSON file with application data')
    parser.add_argument('--template', default='template.html', help='The tenplate HTML file that should be used')
    parser.add_argument('--output', default='index.html', help='The HTML file that should be created')
    
    # Parse command line arguments
    args = parser.parse_args()

    # Call the main function with the provided file paths
    main(args.json, args.template, args.output)
