
# 🌐 Domain Configuration Guide for tsembwog

## Namecheap DNS Setup

1. Go to your domain dashboard
2. Set `Nameservers` to `Namecheap BasicDNS`
3. Add the following A record for backend (Render):
   - Type: A
   - Host: @
   - Value: [Render backend IP or CNAME]
4. Add CNAME for Netlify frontend:
   - Type: CNAME
   - Host: www
   - Value: your-site.netlify.app

## Cloudflare DNS Setup

1. Add your domain to Cloudflare
2. Point your registrar to Cloudflare nameservers
3. Add A/CNAME records:
   - A record `@` → Render backend IP
   - CNAME `www` → your-site.netlify.app
4. Enable proxying (orange cloud) for security
