# Multnomah Libertarians — Website

Jekyll site with Decap CMS for non-technical content editing.  
Live at: https://www.multnomahlibertarians.com

---

## Local development

### Prerequisites
- Ruby 3.x (`brew install ruby`)
- Bundler (`gem install bundler`)

### Run locally
```bash
cd lpmc
bundle install
bundle exec jekyll serve
```
Site runs at http://localhost:4000. Changes to files rebuild automatically.

---

## Deploying to GitHub Pages

1. Push repo to GitHub (already done if you're reading this)
2. Go to **Settings → Pages → Source**: Deploy from branch → `main` → `/` (root)
3. The site builds automatically on every push to `main`
4. Custom domain is already set via the `CNAME` file

### DNS records (set at your domain registrar)
Point `multnomahlibertarians.com` to GitHub Pages with these records:

| Type  | Name | Value          |
|-------|------|----------------|
| A     | @    | 185.199.108.153 |
| A     | @    | 185.199.109.153 |
| A     | @    | 185.199.110.153 |
| A     | @    | 185.199.111.153 |
| CNAME | www  | satat​anicmechanic.github.io |

After transferring to the org, update the CNAME record value to `their-org.github.io`.

---

## Setting up Decap CMS (content editing at /admin)

Editors log in at `https://www.multnomahlibertarians.com/admin` using their GitHub account.

### One-time setup: GitHub OAuth app

1. Go to **GitHub → (org or your account) → Settings → Developer settings → OAuth Apps → New OAuth App**
2. Fill in:
   - **Application name**: Multnomah Libertarians CMS
   - **Homepage URL**: `https://www.multnomahlibertarians.com`
   - **Authorization callback URL**: `https://www.multnomahlibertarians.com/admin/`
3. Click **Register application**
4. Copy the **Client ID**
5. Generate a **Client Secret** and copy it
6. Open `admin/config.yml` and add under `backend`:
   ```yaml
   backend:
     name: github
     repo: SatanicMechanic/lpmc
     branch: main
     base_url: https://api.github.com
     auth_endpoint: login/oauth/authorize
     app_id: YOUR_CLIENT_ID
   ```
   Note: the GitHub backend uses implicit OAuth — the Client Secret is not needed in the config.

### Inviting editors
Editors need a GitHub account and must be added as a collaborator on the repo (or be a member of the org with write access).

---

## Content editing (for non-technical editors)

Go to `https://www.multnomahlibertarians.com/admin` and log in with GitHub.

### What you can edit in the CMS:
- **News & Announcements** — create, edit, and delete posts. Rich text editor. Click Save, it publishes automatically within 1–2 minutes.
- **Officers** — update names and roles
- **Meetup details** — time, location, welcome note
- **Resources** — add, remove, or edit the links section

### Editing static content directly (for advanced edits)

For things not covered by the CMS — like the hero text, pillars section, or page structure — edit `index.html` directly in GitHub:

1. Go to the repo on GitHub
2. Click `index.html`
3. Click the pencil (edit) icon
4. Make your changes
5. Click **Commit changes** → **Commit directly to main**

The site rebuilds in about 60 seconds. The same approach works for any file in the repo.

---

## Transferring to the org (when ready)

1. **Transfer the repo**: repo Settings → Danger Zone → Transfer → enter org name
2. **Update `admin/config.yml`**: change `repo: SatanicMechanic/lpmc` to `repo: their-org/lpmc`
3. **Update the OAuth app**: GitHub → OAuth App settings → update the callback URL if needed, or create a new OAuth app under the org
4. **Update DNS CNAME** record from `satat​anicmechanic.github.io` to `their-org.github.io`
5. Make all intended org members **Owners** in the org settings

---

## If something goes wrong and the original maintainer is unavailable

Everything you need is in GitHub. No other accounts or services are required.

1. **The repo** is owned by the org — you already have full access as an org owner
2. **The domain** registrar account is controlled by the org — log in and repoint DNS if needed
3. **The CMS** authenticates via GitHub — if the OAuth app breaks, go to GitHub org Settings → Developer settings → OAuth Apps and create a new one, then update `admin/config.yml`
4. **GitHub Pages** — if the site stops building, go to repo Settings → Pages and check the build status. Error details are shown there
5. **To edit anything on the site** without the CMS: edit files directly in GitHub as described above — no local tools required

If you need to move the site to a fork (e.g. the original repo becomes inaccessible):
1. Fork the repo to the org
2. Enable GitHub Pages on the fork (Settings → Pages)
3. The original maintainer (or GitHub's deceased user process) must remove the custom domain from their repo's Pages settings before you can claim it on the fork
4. Once released, add `multnomahlibertarians.com` in the fork's Pages settings and update DNS

---

## File structure

```
lpmc/
├── _config.yml          # Site settings, URLs, social links
├── _data/
│   └── site.yml         # Officers, meetup info, resources (edited via CMS)
├── _includes/
│   ├── nav.html          # Navigation bar
│   └── footer.html       # Footer
├── _layouts/
│   ├── default.html      # Main page wrapper
│   └── post.html         # Blog post wrapper
├── _posts/               # News posts (edited via CMS)
├── admin/
│   ├── index.html        # Decap CMS entry point
│   └── config.yml        # CMS configuration
├── assets/
│   ├── css/main.css      # All styles
│   └── images/           # Logo and uploaded images
├── index.html            # Homepage
├── news.html             # News archive
└── CNAME                 # Custom domain
```
