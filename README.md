# Multnomah Libertarians — Website

Jekyll site with Sveltia CMS for non-technical content editing.  
Live at: https://www.multnomahlibertarians.com  
Preview: https://lporegon.github.io/lpmultco

---

## Content editing (for non-technical editors)

Go to `https://lporegon.github.io/lpmultco/admin` (or `https://www.multnomahlibertarians.com/admin` once live) and log in with a GitHub personal access token.

### First-time login setup

You need a GitHub account with write access to the LPOregon/lpmultco repo. Then:

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token (classic)**
2. Set **Expiration** to "No expiration"
3. Set **Resource owner** to **LPOregon**
4. Under **Select scopes**, check **repo** (the top-level checkbox — this includes read/write access to contents)
5. Click **Generate token** and copy it
6. Go to `/admin`, click **Sign in with token**, paste the token

You don't need to save the token. If you lose it or it stops working, generate a new one — takes 30 seconds.

### What you can edit in the CMS

- **News & Announcements** — create, edit, and delete posts. Rich text editor. Click Save, it publishes within 1–2 minutes.
- **Officers** — update names and roles
- **Meetup details** — time, location, welcome note
- **Resources** — add, remove, or edit the links section

### Monthly maintenance — updating the RSVP button

Each month when a new event is created in Luma:

1. Go to `luma.com`, open the new event, click **Manage → More tab → Embed Registration Button**
2. Copy the `evt-XXXXXXXXXXXXXXXXX` ID from the code snippet
3. Open the CMS → **Site Settings → Meetup Details**
4. Update **Luma Event ID** with the new `evt-XXXXXXXXXXXXXXXXX` value
5. Update **Next Event Date** with the display date, e.g. `May 3, 2026`
6. Click Save — site updates within 1–2 minutes

### Editing static content directly

For things not covered by the CMS — hero text, pillars, page structure — edit `index.html` directly in GitHub:

1. Go to https://github.com/LPOregon/lpmultco
2. Click `index.html`
3. Click the pencil (edit) icon
4. Make your changes
5. Click **Commit changes** → **Commit directly to main**

The site rebuilds in about 60 seconds. The same approach works for any file in the repo.

---

## Going live on the custom domain

When ready to switch from the github.io preview to `multnomahlibertarians.com`:

1. **Set DNS records** at your domain registrar:

| Type  | Name | Value              |
|-------|------|--------------------|
| A     | @    | 185.199.108.153    |
| A     | @    | 185.199.109.153    |
| A     | @    | 185.199.110.153    |
| A     | @    | 185.199.111.153    |
| CNAME | www  | lporegon.github.io |

2. **Update `_config.yml`**: change `baseurl: "/lpmultco"` to `baseurl: ""`
3. Go to repo Settings → Pages → add `multnomahlibertarians.com` as custom domain → check **Enforce HTTPS**
4. Commit and push — site will be live once DNS propagates (usually under an hour)

---

## GitHub Pages setup

If Pages ever needs to be re-enabled:

1. Repo Settings → Pages
2. Source: Deploy from branch → `main` → `/ (root)` → Save

The site builds automatically on every push to `main`.

---

## Local development

### Prerequisites
- Ruby 3.x (`brew install ruby`)
- Bundler (`gem install bundler`)

### Run locally
```bash
cd lpmultco
bundle install
bundle exec jekyll serve --baseurl ""
```
Site runs at http://localhost:4000.

---

## If something goes wrong and the original maintainer is unavailable

Everything lives in GitHub. No other accounts or services are required.

1. **The repo** is owned by the LPOregon org — any org owner has full access
2. **The domain** registrar is controlled by the org — log in and repoint DNS if needed
3. **The CMS** — each editor generates their own GitHub PAT. If login stops working, generate a new one as described above. No shared credentials, no third-party service to fix.
4. **GitHub Pages** — if the site stops building, go to repo Settings → Pages for build status and error details
5. **To edit without the CMS** — edit files directly in GitHub as described above. No local tools required.

### If the repo needs to move to a fork

1. Fork the repo into the org (or a new org)
2. Enable GitHub Pages on the fork (Settings → Pages)
3. **3.** The custom domain `multnomahlibertarians.com` is claimed in the original repo's Pages settings. The original maintainer must remove it before you can claim it on the fork. If the original maintainer is unreachable, GitHub has a deceased user process — it is slow but it exists. If GitHub itself becomes untenable, the site is portable to GitLab Pages or Codeberg Pages with minor changes — see the site's maintainer for details, or search "Jekyll GitLab Pages" or "Jekyll Codeberg Pages" for current instructions.
4. Once released, add `multnomahlibertarians.com` in the fork's Pages settings and update DNS

---

## Adding editors

Editors need a GitHub account and write access to the repo:

1. Go to https://github.com/orgs/LPOregon/people → **Invite member**
2. Once they accept, go to repo → Settings → Collaborators and teams → add them with **Write** access
3. They can then generate a PAT and log into `/admin` as described above

---

## File structure

```
lpmultco/
├── _config.yml          # Build settings and site URLs
├── _data/
│   └── site.yml         # Officers, meetup info, resources (edited via CMS)
├── _includes/
│   ├── nav.html         # Navigation bar
│   └── footer.html      # Footer
├── _layouts/
│   ├── default.html     # Main page wrapper
│   └── post.html        # Blog post wrapper
├── _posts/              # News posts (edited via CMS)
├── admin/
│   ├── index.html       # Sveltia CMS entry point
│   └── config.yml       # CMS configuration
├── assets/
│   ├── css/main.css     # All styles
│   └── images/          # Logo and uploaded images
├── index.html           # Homepage
├── news.html            # News archive
└── CNAME                # Custom domain
```
