import json
import argparse
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
    app_quote_author = app_data.get('app_quote_author', '')
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

    app_id = convert_to_html_id(app_title)
    html_template = f"""
                    <!-- {app_title} -->
                    <div id="{app_id}" class="application-item {class_style}">
                        <div class="application-content">
                            <div class="application-header">"""
    if story_link:
        html_template += f"""
                                <a href="{story_link}" target="_blank">"""
    html_template += f"""
                                    <img src="{image_src}" alt="{image_alt}" loading="lazy">"""
    if story_link:
        html_template += f"""
                                </a>"""
        
    html_template += f"""
                            </div>
                            <div class="application-body">
                                <h3 class="application-title">{app_title}</h3>
                                <h4 class="application-company">{app_company}</h4>"""

    # Only include quote if it's not empty
    if app_quote:
        html_template += f"""
                                <div class="application-quote">
                                    <p class="quote-text">"{app_quote}"</p>
                                    <p class="quote-author">{app_quote_author}</p>
                                </div>"""
    
    # App Description
    html_template += f"""
                                <p class="application-description">
                                {app_description}
                            </p>"""
    
    # CTA (Call-to-Action) buttons - include links only if they are provided
    html_template += """
                                <div class="application-cta">"""
    
    
    if preview_link:
        html_template += f"""
                                    <a href="{preview_link}" target="_blank" class="tooltip"><i class="fas fa-play-circle"></i><span class="tooltip-text">Open Live Preview</span></a>"""
    
    if story_link:
        html_template += f"""
                                    <a href="{story_link}" target="_blank" class="tooltip"><i class="fas fa-comment"></i><span class="tooltip-text">Read Customer Journey</span></a>"""
    if doc_link:
        html_template += f"""
                                    <a href="{doc_link}" target="_blank" class="tooltip"><i class="fas fa-globe"></i><span class="tooltip-text">Open Product Page</span></a>"""
    
    if license_text:
        html_template += f"""
                                    <a id="#{app_id}-license" href="#{app_id}-license" class="tooltip"><i class="fas {license_icon}"></i><span class="tooltip-text">{license_text}</span></a>"""

    if git_link:
        html_template += f"""
                                    <a href="{git_link}" target="_blank" class="tooltip"><i class="fab fa-git-alt"></i><span class="tooltip-text">Open Git Repo</span></a>"""    
    # Closing tags
    html_template += """        </div>
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
