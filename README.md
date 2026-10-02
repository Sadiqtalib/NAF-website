# NAF Properties Limited — website redesign

A static website (HTML, CSS and JavaScript) for Nigerian Air Force Properties Limited.
No build step is needed to host it: upload the files as they are.

## Pages

- `index.html`: home, with the scrolling estate tour
- `about.html`, `leadership.html`, `mission.html`, `team.html`: About section
- `communities.html`, `portfolio.html`, `services.html`, `adverts.html`, `contact.html`
- `property-*.html`: one page per estate

## Hosting on Vercel

1. Push this folder to a GitHub repository.
2. In Vercel, choose **Add New → Project**, import the repository, set **Framework Preset** to **Other**, leave the build command empty, and deploy.

`vercel.json` turns on clean URLs, so `/about` works as well as `/about.html`.

## Editing content

All text, estates, people and services live in `_build/content.py`. After editing, regenerate the pages:

```bash
python3 _build/build.py
```

Styles are in `assets/css/styles.css`; interactions are in `assets/js/main.js`.

## Before launch

- Forms show a confirmation but do not send anything yet. Connect them to the existing `/message` endpoint (fields: `name`, `email`, `phone`, `report`, `category`, `page`, plus the CSRF `_token`) or a form service.
- Replace the Facebook and YouTube links in `_build/content.py` with the company's real pages.
- Confirm the expanded leadership titles (DOF, DOW, DLS, CSLA) with the client.
