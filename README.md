# About

![#MadeWithSlint](./docs/assets/img/madewithslint-logo-light.svg#gh-light-mode-only)![#MadeWithSlint](./docs/assets/img/madewithslint-logo-dark.svg#gh-dark-mode-only)

This is the repository that contains data for the madewithslint.com website.

## Add a new entry

Each entry is composed of the following fields:

- Application Name
- Application Creator: Name of company or Individual
- Application Screenshot
- Application Description
- Application License
- Application Repo

Create a PR to add the above info in the following HTML structure in index.html (Please append to the end of the list)

See example below for Cargo UI

- Application Name: Cargo UI
- Application Creator: SixtyFPS GmbH
- Application Screenshot: /assets/img/madewithslint-cargoui.png
- Application Description: A GUI frontend for Cargo.
- Application License: MIT / Apache 2.0
- Application Repo: https://github.com/slint-ui/cargo-ui/

```html
<div id="cargo-ui" class="application-item">
    <div class="application-overview">
        <div class="application-overview-name">
            <h3 class="application-name">Cargo UI</h3>
            <h3 class="application-company"><small>SixtyFPS GmbH</small></h3>
        </div>
        <div class="application-overview-img">
            <img data-src="/assets/img/madewithslint-cargoui.png" alt="Screenshot of Cargo UI">
        </div>
        <div>
            <p>A GUI frontend for Cargo.<br><br> License: MIT / Apache 2.0</p>
        </div>
        <div class="application-cta">
            <!-- Use this is for running a wasm binary
            <p><a href="" class="btn">Run in Browser</a></p> 
            --> 
            <p><a class="btn" href="https://github.com/slint-ui/cargo-ui/">Project Repo</a></p>                    
        </div>
    </div>
</div><!-- .application-item -->
```
