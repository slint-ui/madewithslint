# About

![#MadeWithSlint](./docs/assets/img/madewithslint-logo-light.svg#gh-light-mode-only)![#MadeWithSlint](./docs/assets/img/madewithslint-logo-dark.svg#gh-dark-mode-only)

This is the repository that showcases applications #MadeWithSlint

## Add a new entry

Each entry is composed of the following fields:

### Mandatory

- Application Title
- Application Company: Name of company or Individual
- Application Description
- Application Image
- Application Image Alt text
- Class Style: Size of the card

### Optional

- Application Quote
- Git Link
- Preview Link
- Doc Link
- Success Story Link
- License Text
- License Type

Create a PR to add the above info in the following JSON structure in showcases.json

```json
{
      "app_title": "Application Name",
      "app_company": "Application Author",
      "app_description": "Application Description",
      "app_quote": "Quote from Author",
      "image_src": "URL to Application screenshot",
      "image_alt": "Alt text for image",
      "class_style": "Size of card (col-3-row-3, col-3-row-2, col-2-row-2, col-2-row-1, col-1-row-1)",
      "git_link": "URL to Git repo",
      "preview_link": "URL to WASM binary",
      "doc_link": "URL to Product page",
      "license_text": "Type of license (Proprietary, MIT, BSD, etc.)",
      "license_type": "Type of license (closed, open-source, dual)",
      "story_link": "URL to success story"
    }
```

See example below for Cargo UI

```json
{
        "app_title": "Cargo UI",
        "app_company": "SixtyFPS GmbH",
        "app_description": "A GUI frontend for Cargo",
        "app_quote": "",
        "image_src": "https://madewithslint.com/assets/img/madewithslint-cargoui.png",
        "image_alt": "Screenshot of Cargo UI",
        "class_style": "col-3-row-1",
        "git_link": "https://github.com/slint-ui/cargo-ui/",
        "preview_link": "",
        "doc_link": "",
        "license_text": "MIT, Apache 2.0",
        "license_type": "open-source",
        "story_link": ""
      }
```

## Test Locally

Run the command

```shell
python3 generate_html.py
```

and then run http.server

```shell
python3 -m http.server
```
