# Gujri Yaden – publish karne ki guide

## Files

| File | Kahan upload karein |
|---|---|
| `Gujri_Yaden_Kindle.epub` | Amazon KDP → Kindle eBook → Manuscript |
| `kindle-cover.jpg` | Amazon KDP → Kindle eBook → Cover |
| `pothi/Gujri_Yaden_Interior_A5.pdf` | Pothi.com → Paperback → Interior (84 pages, A5) |
| `pothi/Gujri_Yaden_Cover.pdf` (ya `.jpg`) | Pothi.com → Paperback → Cover |
| `listing.md` | Title, description, keywords – dono jagah copy-paste |

## 1. Kindle eBook (Amazon KDP)
1. kdp.amazon.com par apne Amazon account se login karein.
2. Account → Tax information (W-8BEN, PAN se) aur bank details bharein.
3. "+ Create" → **Kindle eBook**.
4. Language: **Hindi**. Title, author, description, keywords `listing.md` se copy karein.
5. Manuscript: `Gujri_Yaden_Kindle.epub` upload karein. Cover: `kindle-cover.jpg` ("Upload a cover you already have").
6. AI-generated content: cover ki tasveerein AI se bani hain to **Yes → Images**.
7. "Launch Previewer" mein kuch pages dekh lein.
8. Pricing: 70% royalty, amazon.in par ₹99. **Publish** dabayein. 24–72 ghante mein live.

## 2. Paperback (Pothi.com)
1. pothi.com par account banayein → "Publish" → Print book.
2. Book size: **A5 (5.83 × 8.27 in / 148 × 210 mm)**, Paperback, Black & White interior, Matte/Glossy cover.
3. Interior PDF aur cover PDF upload karein.
4. ISBN: Pothi se ISBN lein (ya isbn.gov.in se free). ISBN milne ke baad uska barcode back cover ke **safed box** mein lagana hai (ye box isi ke liye khaali chhoda gaya hai) – Pothi team ya hum ise add kar denge.
5. Price set karein (₹199–₹299 theek rahega; Pothi printing cost aur royalty dikhata hai).
6. Distribution mein **Amazon.in aur Flipkart** select karein.

### Cover ke technical details
- Spine Pothi ke formula se: 84 pages × 0.001968" = 0.167"
- Bleed: har taraf 0.2"; total size 12.227" × 8.667" @ 300 DPI
- Agar Pothi page count ya spine alag bataye to dobara banane ke liye:
  `python3 tools/make_cover.py kindle-cover.jpg <back.jpg> <pages> pothi/Gujri_Yaden_Cover.pdf`
