# Wedding Invitation

A single-page wedding invitation: a sealed envelope opens into an unfolding letter with the
couple's names, a welcome message, and the date/time/venue. Built with React + Vite and animated
with [Framer Motion](https://www.framer.com/motion/).

## Running locally

```bash
npm install
npm run dev
```

Then open the printed `localhost` URL in your browser.

## Editing the content

Everything guests see lives in [`src/components/LetterContent.jsx`](src/components/LetterContent.jsx):

- **Names, date, time, venue** — edit the text directly in the JSX.
- **Welcome message** — the paragraph in the `welcomeMessage` block.
- **Maps link** — the `href` on the "view location on maps" link.

Colors and fonts are defined once as CSS variables in
[`src/styles/tokens.css`](src/styles/tokens.css).

## Project structure

```
src/
  components/
    Envelope/        Stage 1 — the sealed envelope
    Letter/           Stage 2 — the unfolding letter shell
    LetterContent.jsx The letter's actual text
    Petals.jsx        Falling petal effect after the letter opens
  assets/images/      Decorative images (deduplicated — each image is stored once,
                      reused via CSS transforms for mirroring)
  styles/             Design tokens + global CSS reset
```

## Deploying (Vercel via GitHub)

1. Push this project to a GitHub repository.
2. In [Vercel](https://vercel.com), click **New Project** and import that repository.
3. Vercel auto-detects the Vite framework preset — no configuration needed. Click **Deploy**.
4. Any future push to the main branch redeploys automatically.
