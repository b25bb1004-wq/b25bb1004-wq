# Setup — hades-3008 GitHub Profile

## 1. Create the profile repository

Create a **public** repository named exactly:

`hades-3008`

Do not initialize it with another README if you plan to push this folder.

## 2. Copy these files into the repo

Everything in this folder belongs in the root of that repository.

## 3. Push

```bash
git init
git branch -M main
git add .
git commit -m "build animated GitHub profile"
git remote add origin https://github.com/hades-3008/hades-3008.git
git push -u origin main
```

## 4. Enable the workflow

Go to **Actions** → **Update profile art** → **Run workflow**.

The first run fetches your public contribution calendar and replaces the placeholder heatmap.

The workflow then refreshes the heatmap daily.

## 5. When you build your portfolio

Edit only the `Portfolio coming soon.` line in `README.md` and replace it with your portfolio URL.

## Regenerating the portrait locally

Install the requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
```

Then:

```bash
python scripts/prep_photo.py assets/source-photo.jpg
python scripts/make_ascii_svg.py
python scripts/make_info_card.py
```

The supplied photo already has a clean light background, so background removal is not required.
