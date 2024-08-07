<div align="center">

<picture>
    <source media="(prefers-color-scheme: dark)" srcset="/docs/logo_reboot_dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="/docs/logo_reboot_light.svg">
    <img alt="reboot saas logo" src="/public/logo_reboot_light.svg" width="50%" height="50%">
</picture>

Reboot SAAS: The first SAAS project coded at Enterprise Level Quality

[![Tests](https://github.com/andreivisan/open-saas-app/actions/workflows/test.yml/badge.svg)](https://github.com/andreivisan/open-saas-app/actions/workflows/test.yml)

<h3>

[Homepage](https://github.com/andreivisan/reboot-saas) | [Documentation](/docs) | [Premium](http://rebootsaas.org)

</h3>

</div>

---

This may not be the most popular SaaS boilerplate in terms of technologies used, but it is the fastest and most professionally built. The principles based on which this projects is built are principles brought from more than 20 years of developing Enterprise Software.

- <b>Robust Software</b> - by using proper unit and integration testing (which most SaaS boilerplate products don't do) we insure that whatever product you deliver using our SaaS boilerplate is stable and well tested and will allow you to have a safety net for when you add new features.

- <b>Maintainable Software</b> - by using SOLID principles we insure that our code is easy to read and understand which in turn will allow you do add features, develop and ship your product to customers faster.

- <b>Extendable Software</b> - by using a no-nonsense approach, coupled with modular architecture and the correct implementation of Design Patterns, extensibility is at the core of our product. The idea is to provide you with a product which you can easily extend with your own features before and after delivering it into production.

## Technologies used

### HTMX

No-nonsense framework, easy and respects HATEOAS and REST.

### TailwindCSS

To create beautiful UI.

### DaisyUI

To create a beautiful product with amazing components

### FastAPI

Python backend

### Jinja2 Templates

To work with HTMX

We will offer the possibility to use different backend technologies like GO and Rust. If you want others like Spring Boot or NextJS please open a ticket or feel free to contribute.

## Implementation

### Components

There are 2 types of components inside the project:

1. Client Components: example dasboard sliding sidebar. Since there is no data needed from the server this is just an html file imported as jinja template in the dashboard main page.

2. Server Components: example dashboard home page -> data card, graph and data table. Since these components use data from the back-end I created
a components folder that holds routes to components and serves these components with the required data.
