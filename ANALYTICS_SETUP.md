# Google Analytics Setup for killasnus.store

## Quick Setup Steps

### 1. Get Your Google Analytics ID
1. Go to https://analytics.google.com
2. Sign in with your Google account
3. Click "Admin" → "Property Settings"
4. Copy your **Measurement ID** (starts with G-)

### 2. Add GA4 Tracking to Your Pages

Replace `G-XXXXXXXXXX` with your actual Measurement ID in your HTML pages, in the `<head>` section:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 3. Insert into Key Pages
Add the GA script to these templates (they cover all variations):
- `/en/index.htm` (homepage)
- `/en/category/*/index.htm` (categories)
- `/tuote/*/index.htm` (product pages)
- `/checkout/index.htm` (checkout)

### 4. Verify Installation
After 24-48 hours:
1. Go to Google Analytics Dashboard
2. Check "Realtime" → "Overview"
3. Should show active users

## Manual Method (If You Prefer)
Edit each main page's `<head>` section and paste the GA tracking code above.

## Track Events (Optional)
Add event tracking for conversions:
```javascript
gtag('event', 'purchase', {
  'value': 99.99,
  'currency': 'EUR'
});
```
