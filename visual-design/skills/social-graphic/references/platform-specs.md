# Platform Specs

Dimensions, safe zones, text guidelines, and format recommendations for each supported platform.

## Twitter / X

| Format | Dimensions | Aspect Ratio | Safe Zone |
|--------|-----------|--------------|-----------|
| Post image | 1200 x 675 px | 16:9 | Center 960 x 540 px |
| Header / banner | 1500 x 500 px | 3:1 | Center 1300 x 400 px (profile photo overlaps bottom-left) |
| Card image (link preview) | 800 x 418 px | ~1.91:1 | Full frame |

- Max file size: 5 MB (images), 15 MB (GIFs)
- Feed images are cropped to 16:9. Vertical images get center-cropped.
- Header displays differently on mobile vs desktop. Avoid important content near edges.

## LinkedIn

| Format | Dimensions | Aspect Ratio | Safe Zone |
|--------|-----------|--------------|-----------|
| Post image | 1200 x 627 px | 1.91:1 | Center 960 x 500 px |
| Cover / banner | 1584 x 396 px | 4:1 | Center 1200 x 300 px (profile photo overlaps bottom-left) |
| Article cover | 1200 x 644 px | ~1.86:1 | Full frame |

- Max file size: 10 MB
- Square (1080 x 1080) and vertical (1080 x 1350) also display well in the feed.
- Cover banner gets heavy cropping on mobile. Test at both viewports.

## Instagram

| Format | Dimensions | Aspect Ratio | Safe Zone |
|--------|-----------|--------------|-----------|
| Square post | 1080 x 1080 px | 1:1 | Center 864 x 864 px |
| Portrait post | 1080 x 1350 px | 4:5 | Center 864 x 1080 px |
| Landscape post | 1080 x 566 px | 1.91:1 | Full frame |
| Story / Reel cover | 1080 x 1920 px | 9:16 | Center 1080 x 1420 px |
| Carousel | 1080 x 1080 or 1080 x 1350 px | 1:1 or 4:5 | Same as post format |

- Stories: Avoid text in top 14% or bottom 14% (UI overlays for username and reply bar).
- Portrait takes up more feed real estate than square. Good for maximizing visibility.
- Carousel slides must all share the same aspect ratio. First slide drives engagement.

## Substack

| Format | Dimensions | Aspect Ratio | Safe Zone |
|--------|-----------|--------------|-----------|
| Newsletter header | 1100 x 220 px | 5:1 | Center 900 x 180 px |
| Inline / feature image | 1456 px wide (height flexible) | 2:1 to 4:3 | Full frame |
| Post social preview (OG) | 1200 x 630 px | 1.91:1 | Center 960 x 504 px |

- Newsletter header: Keep simple -- brand name, tagline, or issue identifier.
- Inline images: Keep file size under 1 MB for fast email loading.

## YouTube

| Format | Dimensions | Aspect Ratio | Safe Zone |
|--------|-----------|--------------|-----------|
| Thumbnail | 1280 x 720 px | 16:9 | Center 1024 x 576 px (duration overlay covers bottom-right) |
| Channel banner | 2560 x 1440 px | 16:9 | Center 1546 x 423 px (visible on all devices) |

- Thumbnail max file size: 2 MB. For detailed thumbnail design, use `visual-design:thumbnail` skill.
- Channel banner: Full image on TVs, center ~2560 x 423 on desktop, center ~1546 x 423 on mobile. Design for smallest safe zone first.

## Blog / Website

| Format | Dimensions | Aspect Ratio | Safe Zone |
|--------|-----------|--------------|-----------|
| Feature image (hero) | 1200 x 630 px | 1.91:1 | Full frame |
| OG image (Open Graph) | 1200 x 630 px | 1.91:1 | Center 960 x 504 px |
| Email header | 600 x 200 px (1200 x 400 retina) | 3:1 | Full frame |

- Feature image doubles as default OG image if no specific OG image is set.
- OG image: Include brand identity, page title, and a compelling visual for social sharing.
- Email header: Keep file size under 200 KB. Many email clients block images by default.

---

## General Guidelines

### Safe Zones
- **Default rule:** Keep text and key visual elements within 80% of the frame (10% margin on each side)
- **Platform UI overlays:** Account for profile photos, timestamps, like buttons, and duration stamps
- **When in doubt:** Place critical content in the center third of the image

### Text Minimum Sizes
- **Headlines:** Minimum 24 px at the final output resolution (visible on mobile)
- **Body text on images:** Minimum 16 px at final output resolution
- **Fine print:** Avoid placing small text on images entirely -- unreadable on mobile
- **Rule of thumb:** If you have to squint to read it at 50% zoom, it is too small

### File Format Recommendations
- **PNG:** Graphics with text, logos, sharp edges, or transparency
- **JPEG:** Photographs and complex gradients (quality 85-92%)
- **WebP:** Web delivery -- smaller file sizes with equivalent quality
- **GIF:** Simple animations only. Use MP4/WebM for complex animations

### Accessibility
- **Contrast ratio:** Maintain at least 4.5:1 between text and background (WCAG AA)
- **Color independence:** Do not convey information through color alone
- **Alt text:** Always provide descriptive alt text for social media posts
- **Font choice:** Use clean, sans-serif fonts for screen readability
