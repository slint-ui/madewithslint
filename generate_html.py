import json

def is_valid(app_data):
    """Check if the required fields in app_data are non-empty and valid."""
    required_fields = ['class_style', 'image_src', 'image_alt', 'app_title', 'app_company', 'app_description']
    
    # Check that all required fields are present and non-empty
    for field in required_fields:
        if field not in app_data or not app_data[field].strip():
            print(f"Skipping invalid entry due to missing or empty field: {field}")
            return False
    return True

def generate_html(app_data):
    """Generate HTML for an application entry."""
    image_src = app_data['image_src']
    image_alt = app_data['image_alt']
    app_title = app_data['app_title']
    app_company = app_data['app_company']
    app_description = app_data['app_description']
    class_style = app_data['class_style']
    
    # Optional fields
    app_quote = app_data.get('app_quote', '').strip()
    git_link = app_data.get('git_link', '')
    preview_link = app_data.get('preview_link', '')
    doc_link = app_data.get('doc_link', '')
    license_text = app_data.get('license_text', '')
    license_type = app_data.get('license_type', '')
    license_icon = "fa-lock"
    story_link = app_data.get('story_link', '')

    if license_type == "open-source":
        license_icon = "fa-lock-open"
    elif license_type == "dual":
        license_icon = "fa-unlock"

    html_template = f"""
                    <!-- {app_title} -->
                    <div class="application-item {class_style}">
                        <div class="application-header">
                            <img src="{image_src}" alt="{image_alt}" loading="lazy">
                        </div>
                        <div class="application-body">
                            <h3 class="application-title">{app_title}</h3>
                            <h4 class="application-company">{app_company}</h4>"""

    # Only include quote if it's not empty
    if app_quote:
        html_template += f"""
                            <p class="application-quote">"{app_quote}"</p>"""
    
    # App Description
    html_template += f"""
                            <p class="application-description">
                                {app_description}
                            </p>"""
    
    # CTA (Call-to-Action) buttons - include links only if they are provided
    html_template += """
                            <div class="application-cta">"""
    
    if git_link:
        html_template += f"""
                                <a href="{git_link}" target="_blank"><i class="fab fa-git-alt"></i></a>"""
    
    if preview_link:
        html_template += f"""
                                <a href="{preview_link}" target="_blank"><i class="fas fa-play-circle"></i></a>"""
    
    if doc_link:
        html_template += f"""
                                <a href="{doc_link}" target="_blank"><i class="fas fa-globe"></i></a>"""
    
    if license_text:
        html_template += f"""
                                <a href="#" class="tooltip"><i class="fas {license_icon}"></i><span class="tooltip-text">{license_text}</span></a>"""
    
    if story_link:
        html_template += f"""
                                <a href="{story_link}" target="_blank"><i class="fas fa-comment"></i></a>"""
    
    # Closing tags
    html_template += """
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

def generate_html_for_all_apps(data):
    html_output = f"""
            <section class="applications">
                <div class="col-wrap">"""
    for app in data:
        if is_valid(app):  # Only generate HTML for valid entries
            html_output += generate_html(app)
        else:
            print("Skipping entry due to invalid data.")
    html_output += """
                </div><!-- .col-wrap -->
            </section><!-- .applications -->\n"""
    return html_output

def replace_placeholder_in_html(html_file_path, placeholder, new_content):
    # Read the HTML file
    with open(html_file_path, 'r') as file:
        file_content = file.read()

    # Replace the placeholder with the new content
    updated_content = file_content.replace(placeholder, new_content)

    # Write the updated content back to the HTML file
    with open('index.html', 'w') as file:
        file.write(updated_content)

# Load data from the JSON file
json_file_path = 'showcases.json'
data = load_data_from_json(json_file_path)

# Generate HTML for all the valid applications in the JSON array
html_code = generate_html_for_all_apps(data)

# Print or save the generated HTML
print(html_code)

# Create index.html
html_file_path = 'template.html'  
placeholder = '<?applications?>'
replace_placeholder_in_html(html_file_path, placeholder, html_code)
