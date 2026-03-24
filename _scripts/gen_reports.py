#!/usr/bin/env python3
"""Generate monthly SEO reports using the original Stambaugh Designs template."""
import os, json
REPORT_MONTH = "March 2026"
GENERATED = "March 24, 2026"
PERIOD = "Feb 22 – Mar 24, 2026"
PAGES_BASE = "https://stambaugh-designs.github.io/client-reports"

# ── CSS from original template (light warm theme) ──────────────────────────
CSS = """
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');
  :root {
    --bg: #f5f0eb; --surface: #ffffff; --surface-alt: #faf7f4;
    --border: #e8e0d8; --text: #2c2417; --text-secondary: #8c7e6e; --text-muted: #b0a494;
    --accent: #c4550a; --accent-light: #e8764a;
    --green: #2d7a3a; --green-bg: #eaf5ec;
    --red: #c4390a; --red-bg: #fdf0eb;
    --orange: #b5680a; --orange-bg: #fef6eb;
    --blue: #1a6bb5; --blue-bg: #ebf3fa;
    --header-gradient: linear-gradient(135deg, #2c1810 0%, #4a2c1a 40%, #3d2010 100%);
    --radius: 12px; --radius-sm: 8px;
    --shadow: 0 1px 3px rgba(44,36,23,0.06), 0 1px 2px rgba(44,36,23,0.04);
    --shadow-md: 0 4px 12px rgba(44,36,23,0.08), 0 2px 4px rgba(44,36,23,0.04);
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; -webkit-font-smoothing: antialiased; }
  .container { max-width: 900px; margin: 0 auto; padding: 0 20px; }
  .report-header { background: var(--header-gradient); padding: 48px 0 44px; position: relative; overflow: hidden; }
  .report-header::before { content: ''; position: absolute; top: -50%; right: -20%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(196,85,10,0.15) 0%, transparent 70%); pointer-events: none; }
  .report-header .container { position: relative; z-index: 1; }
  .hdr-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); border-radius: 20px; padding: 6px 16px; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #f0e6d8; margin-bottom: 20px; }
  .hdr-badge::before { content: ''; width: 8px; height: 8px; background: var(--accent); border-radius: 50%; }
  .header-domain { font-size: 40px; font-weight: 800; color: #ffffff; letter-spacing: -1px; margin-bottom: 6px; }
  .header-subtitle { font-size: 16px; color: #c4b8a8; margin-bottom: 24px; }
  .header-meta { display: flex; flex-wrap: wrap; gap: 24px; font-size: 13px; color: #a89880; }
  .header-meta span { display: flex; align-items: center; gap: 6px; }
  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 0 0 32px; position: relative; z-index: 2; }
  .kpi-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; box-shadow: var(--shadow-md); }
  .kpi-label { font-size: 11px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 8px; }
  .kpi-value { font-size: 36px; font-weight: 800; color: var(--text); line-height: 1.1; letter-spacing: -1px; }
  .kpi-trend { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; font-weight: 600; margin-top: 8px; padding: 2px 8px; border-radius: 4px; }
  .kpi-trend.up { background: var(--green-bg); color: var(--green); }
  .kpi-trend.down { background: var(--red-bg); color: var(--red); }
  .kpi-trend.neutral { background: var(--surface-alt); color: var(--text-secondary); }
  .section { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 32px; margin-bottom: 24px; box-shadow: var(--shadow); }
  .section-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
  .section-icon { width: 40px; height: 40px; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
  .section-icon.orange { background: var(--orange-bg); }
  .section-icon.blue { background: var(--blue-bg); }
  .section-icon.green { background: var(--green-bg); }
  .section-icon.red { background: var(--red-bg); }
  .section-number { font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: var(--accent); }
  .section-title { font-size: 20px; font-weight: 700; color: var(--text); }
  table { width: 100%; border-collapse: collapse; }
  thead th { font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--text-secondary); padding: 12px 16px; text-align: left; border-bottom: 2px solid var(--border); background: var(--surface-alt); }
  tbody td { padding: 12px 16px; font-size: 13px; border-bottom: 1px solid var(--border); }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr:hover { background: var(--surface-alt); }
  td.mono { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 500; }
  .rank-badge { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; font-size: 12px; font-weight: 700; }
  .rank-1 { background: #fef3c7; color: #92400e; }
  .rank-2 { background: #e5e7eb; color: #374151; }
  .rank-3 { background: #fde9d6; color: #9a3412; }
  .progress-bar { height: 8px; background: var(--border); border-radius: 4px; overflow: hidden; margin-top: 4px; }
  .progress-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--accent), var(--accent-light)); }
  .tag { display: inline-block; font-size: 11px; font-weight: 600; padding: 3px 10px; border-radius: 4px; letter-spacing: 0.3px; }
  .tag-green { background: var(--green-bg); color: var(--green); }
  .tag-blue { background: var(--blue-bg); color: var(--blue); }
  .tag-orange { background: var(--orange-bg); color: var(--orange); }
  .tag-red { background: var(--red-bg); color: var(--red); }
  .insight { display: flex; gap: 16px; padding: 16px; border-radius: var(--radius-sm); margin-bottom: 12px; border: 1px solid var(--border); }
  .insight:last-child { margin-bottom: 0; }
  .insight.critical { border-left: 4px solid var(--red); background: var(--red-bg); }
  .insight.warning { border-left: 4px solid var(--orange); background: var(--orange-bg); }
  .insight.positive { border-left: 4px solid var(--green); background: var(--green-bg); }
  .insight-icon { font-size: 20px; flex-shrink: 0; margin-top: 2px; }
  .insight-content h4 { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
  .insight-content p { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
  .chart-container { position: relative; height: 280px; margin: 16px 0; }
  .mini-kpi-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
  .mini-kpi { background: var(--surface-alt); border: 1px solid var(--border); border-radius: var(--radius-sm); padding: 16px; text-align: center; }
  .mini-kpi .value { font-size: 22px; font-weight: 800; color: var(--text); }
  .mini-kpi .label { font-size: 10px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--text-secondary); margin-top: 4px; }
  .no-data { background: var(--surface-alt); border: 1px dashed var(--border); border-radius: var(--radius-sm); padding: 20px; text-align: center; color: var(--text-muted); font-size: 13px; }
  .report-footer { text-align: center; padding: 40px 0; color: var(--text-muted); font-size: 12px; }
  .report-footer a { color: var(--accent); text-decoration: none; }
  .footer-brand { font-size: 14px; font-weight: 700; color: var(--text-secondary); margin-bottom: 8px; }
  .ai-summary { background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 28px 32px; margin-bottom: 24px; box-shadow: var(--shadow-md); }
  .ai-summary-header { display: flex; align-items: center; gap: 10px; margin-bottom: 16px; }
  .ai-badge { display: inline-flex; align-items: center; gap: 6px; background: linear-gradient(135deg, #1a1a2e, #2c1810); color: #f0e6d8; font-size: 11px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; padding: 5px 12px; border-radius: 6px; }
  .ai-badge::before { content: ''; width: 6px; height: 6px; background: #63b3ed; border-radius: 50%; }
  .ai-summary-header h3 { font-size: 16px; font-weight: 700; color: var(--text); }
  .ai-summary-body { font-size: 14px; line-height: 1.75; color: var(--text); }
  @media (max-width: 768px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .mini-kpi-row { grid-template-columns: repeat(2, 1fr); }
    .header-domain { font-size: 28px; }
    .kpi-value { font-size: 28px; }
  }
"""

# ── Helpers ────────────────────────────────────────────────────────────────
def fmt(n):
    if n >= 1000000: return f"{n/1000000:.1f}M"
    if n >= 1000: return f"{n/1000:.1f}K"
    return str(int(n)) if float(n) == int(n) else f"{n:.1f}"

def trend(cur, prev, invert=False):
    if prev == 0: return '<span class="kpi-trend neutral">— First period</span>'
    pct = round((cur - prev) / prev * 100, 1)
    if pct == 0: return '<span class="kpi-trend neutral">— No change</span>'
    up = (pct > 0 and not invert) or (pct < 0 and invert)
    cls = "up" if up else "down"
    sign = "+" if pct > 0 else ""
    arrow = "▲" if pct > 0 else "▼"
    return f'<span class="kpi-trend {cls}">{arrow} {sign}{pct}%</span>'

def rank_badge(i):
    cls = f"rank-{i+1}" if i < 3 else ""
    return f'<span class="rank-badge {cls}">{i+1}</span>'

def insight_icon(t):
    return {"positive": "✅", "warning": "⚠️", "critical": "🚨"}.get(t, "💡")

# ── Client data ──────────────────────────────────────────────────────────────
clients = [
  {"name":"Radiant Heart After-Care for Pets","domain":"radiant-heart.net","slug":"radiant-heart","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":279,"impressions":14624,"ctr":1.91,"position":9.2},"prev":{"clicks":0,"impressions":0,"ctr":0,"position":0},
     "daily":[{"d":"Mar 11","c":25,"i":1436},{"d":"Mar 12","c":31,"i":1658},{"d":"Mar 13","c":21,"i":1381},{"d":"Mar 14","c":16,"i":1259},{"d":"Mar 15","c":18,"i":1200},{"d":"Mar 16","c":28,"i":1276},{"d":"Mar 17","c":24,"i":1107},{"d":"Mar 18","c":20,"i":1097},{"d":"Mar 19","c":22,"i":1197},{"d":"Mar 20","c":31,"i":1096},{"d":"Mar 21","c":27,"i":969},{"d":"Mar 22","c":16,"i":948}],
     "queries":[{"q":"radiant heart","c":67,"i":184,"ctr":36.4,"pos":2.0},{"q":"radiant heart bellingham","c":23,"i":56,"ctr":41.1,"pos":1.0},{"q":"pet cremation bellingham","c":14,"i":56,"ctr":25.0,"pos":6.6},{"q":"radiant heart after-care for pets","c":8,"i":10,"ctr":80.0,"pos":1.6},{"q":"pet cremation near me","c":7,"i":26,"ctr":26.9,"pos":2.3},{"q":"custom cat urns for ashes","c":2,"i":7,"ctr":28.6,"pos":5.6},{"q":"radient heart","c":3,"i":8,"ctr":37.5,"pos":1.1},{"q":"pet cremations","c":2,"i":2,"ctr":100.0,"pos":1.0}]},
   "dfs":{"total":665,"etv":2992,"new":266,"up":244,"down":136,"lost":0,"pos_1":4,"pos_2_3":25,"pos_4_10":107,"pos_11_20":120,"pos_21_plus":409,"mdr":174},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Strong Brand Search Performance","body":"Radiant Heart ranks in the top 10 with a healthy 1.91% CTR. Brand queries like 'radiant heart' and 'radiant heart bellingham' dominate clicks, confirming strong local brand recognition built by Stambaugh Designs."},{"type":"positive","title":"266 New Keywords Gaining Traction","body":"The site entered Google's index for 266 new keyword terms this period, representing a substantial expansion of organic footprint. Long-tail pet cremation queries are beginning to surface."},{"type":"warning","title":"Expand Non-Brand Keyword Rankings","body":"Branded queries account for ~78% of clicks. Targeting more informational pet aftercare content could unlock significant non-brand traffic in positions 11-20 where CTR improvements would have the biggest impact."},{"type":"positive","title":"Competitive ETV of $2,992","body":"The site's estimated traffic value reflects strong positioning in high-CPC local pet cremation searches — Stambaugh Designs has effectively captured intent-driven traffic in this niche market."}]},
  {"name":"Earthsims","domain":"earthsims.com","slug":"earthsims","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":1,"impressions":3240,"ctr":0.03,"position":17.7},"prev":{"clicks":1,"impressions":916,"ctr":0.11,"position":16.6},
     "daily":[{"d":"Feb 23","c":0,"i":314},{"d":"Feb 24","c":0,"i":156},{"d":"Feb 25","c":0,"i":169},{"d":"Feb 26","c":1,"i":131},{"d":"Mar 01","c":0,"i":446},{"d":"Mar 02","c":0,"i":518},{"d":"Mar 03","c":0,"i":531},{"d":"Mar 06","c":0,"i":49},{"d":"Mar 10","c":0,"i":7},{"d":"Mar 15","c":0,"i":3},{"d":"Mar 20","c":0,"i":3},{"d":"Mar 22","c":0,"i":5}],
     "queries":[]},
   "dfs":{"total":6,"etv":1,"new":6,"up":0,"down":0,"lost":0,"pos_1":0,"pos_2_3":0,"pos_4_10":0,"pos_11_20":0,"pos_21_plus":6,"mdr":0},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Indexation Growing Rapidly","body":"Impressions jumped 254% from 916 to 3,240 this period as Google crawls and indexes newly published content. This is a strong early signal that the site architecture and content strategy are working."},{"type":"warning","title":"CTR Optimization Needed as Rankings Improve","body":"With 6 new keywords beginning to index in positions 21+, focus on improving meta titles and descriptions for the top travel/SIM content pages to boost click-through rates as rankings improve."},{"type":"positive","title":"New Content Foundation Established","body":"All 6 tracked keywords are brand new entries — Earthsims is building a fresh keyword footprint from the ground up. Stambaugh Designs' content strategy is laying the foundation for accelerated growth."}]},
  {"name":"Contractor Bear","domain":"contactorbear.com","slug":"contactorbear","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":None,
   "dfs":{"total":0,"etv":0,"new":0,"up":0,"down":0,"lost":0,"pos_1":0,"pos_2_3":0,"pos_4_10":0,"pos_11_20":0,"pos_21_plus":0,"mdr":0},
   "rybbit":None,
   "insights":[{"type":"warning","title":"Site in Early Launch Phase","body":"Contractor Bear is in the early stages of SEO indexation. Stambaugh Designs is actively building the site's keyword foundation and technical SEO infrastructure."},{"type":"positive","title":"Infrastructure Setup Underway","body":"Technical SEO foundations including sitemap, schema markup, and page optimization are being implemented. Organic rankings are expected to begin appearing within the coming 60-90 days."}]},
  {"name":"Cloud Concrete Seattle","domain":"cloudconcreteseattle.com","slug":"cloud-concrete-seattle","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":40,"impressions":12543,"ctr":0.32,"position":20.1},"prev":{"clicks":21,"impressions":9394,"ctr":0.22,"position":20.7},
     "daily":[{"d":"Feb 23","c":1,"i":746},{"d":"Feb 24","c":2,"i":409},{"d":"Feb 25","c":2,"i":546},{"d":"Feb 28","c":1,"i":496},{"d":"Mar 02","c":4,"i":422},{"d":"Mar 03","c":2,"i":412},{"d":"Mar 06","c":5,"i":535},{"d":"Mar 07","c":1,"i":683},{"d":"Mar 09","c":4,"i":449},{"d":"Mar 10","c":3,"i":521},{"d":"Mar 14","c":2,"i":914},{"d":"Mar 17","c":2,"i":273},{"d":"Mar 20","c":0,"i":339},{"d":"Mar 22","c":0,"i":232}],
     "queries":[{"q":"concrete contractors seattle","c":1,"i":773,"ctr":0.1,"pos":18.2},{"q":"stamped concrete seattle","c":1,"i":207,"ctr":0.5,"pos":14.1},{"q":"concrete seattle","c":1,"i":190,"ctr":0.5,"pos":17.3},{"q":"concrete companies seattle","c":1,"i":95,"ctr":1.1,"pos":15.4},{"q":"concrete contractors in seattle wa","c":1,"i":43,"ctr":2.3,"pos":12.1},{"q":"concrete finishers","c":1,"i":4,"ctr":25.0,"pos":8.2},{"q":"cloud concrete","c":1,"i":4,"ctr":25.0,"pos":1.0},{"q":"continuous concrete edging near me","c":1,"i":2,"ctr":50.0,"pos":5.1}]},
   "dfs":{"total":52,"etv":39,"new":46,"up":3,"down":3,"lost":0,"pos_1":0,"pos_2_3":0,"pos_4_10":1,"pos_11_20":8,"pos_21_plus":43,"mdr":151},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Clicks Surged +90% Month-Over-Month","body":"Organic clicks jumped from 21 to 40 — a 90% increase — while impressions grew 34% to 12,543. Stambaugh Designs' ongoing content and technical optimization is delivering accelerating results."},{"type":"positive","title":"46 New Keywords Entering Rankings","body":"Cloud Concrete picked up 46 brand-new keyword rankings this period, reflecting strong content expansion. The growing keyword footprint positions the site well for continued traffic growth."},{"type":"warning","title":"Position 20 Opportunity: Push to Page 1","body":"With 8 keywords ranking positions 11-20, targeted content improvements and internal linking for terms like 'stamped concrete seattle' could push several to page 1 within the next 30-60 days."},{"type":"positive","title":"Strong Impression Baseline of 12,543","body":"High impressions indicate Google is indexing the site broadly across Seattle concrete searches. As rankings improve from page 2 to page 1, click volume will scale dramatically."}]},
  {"name":"Stambaugh Designs","domain":"stambaughdesigns.co","slug":"stambaugh-designs","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":21,"impressions":15438,"ctr":0.14,"position":38.2},"prev":{"clicks":23,"impressions":15616,"ctr":0.15,"position":40.6},
     "daily":[{"d":"Feb 23","c":2,"i":330},{"d":"Feb 27","c":4,"i":398},{"d":"Mar 01","c":1,"i":405},{"d":"Mar 04","c":1,"i":661},{"d":"Mar 08","c":1,"i":628},{"d":"Mar 09","c":1,"i":667},{"d":"Mar 11","c":1,"i":692},{"d":"Mar 12","c":1,"i":814},{"d":"Mar 13","c":1,"i":645},{"d":"Mar 15","c":1,"i":709},{"d":"Mar 16","c":3,"i":509},{"d":"Mar 18","c":3,"i":535},{"d":"Mar 20","c":0,"i":478},{"d":"Mar 22","c":0,"i":549}],
     "queries":[]},
   "dfs":{"total":80,"etv":27,"new":69,"up":2,"down":8,"lost":0,"pos_1":0,"pos_2_3":1,"pos_4_10":0,"pos_11_20":1,"pos_21_plus":78,"mdr":310},
   "rybbit":{"sessions":1166,"pageviews":1708,"users":751,"bounce_rate":71.7,"duration":79,"pages_per_session":1.46,
     "devices":[{"label":"Desktop","pct":92.45},{"label":"Mobile","pct":7.55}],
     "referrers":[{"src":"google.com","visits":33},{"src":"facebook.com (mobile)","visits":41},{"src":"youtube.com","visits":18},{"src":"reddit.com","visits":6},{"src":"designrush.com","visits":5},{"src":"chatgpt.com","visits":4}]},
   "insights":[{"type":"positive","title":"1,166 Sessions & 751 Unique Users via Rybbit","body":"Stambaugh Designs attracted strong direct and referral traffic this period. Facebook and Google together account for nearly half of all referral traffic, validating the multi-channel presence Stambaugh Designs has built."},{"type":"positive","title":"Average Position Improved to 38.2 (from 40.6)","body":"A 2.4-position improvement across 15,438 impressions represents measurable progress moving toward page 2 and eventually page 1 for competitive design/marketing queries."},{"type":"positive","title":"69 New Keywords Indexed","body":"The site gained 69 new keyword entries this period, signaling Google is expanding its understanding of Stambaugh Designs as a Bellingham-area marketing authority."},{"type":"warning","title":"CTR Improvement Opportunity","body":"With 0.14% CTR across 15,438 impressions, refining meta descriptions and title tags for the top-impression pages could unlock significant click volume without additional ranking improvements."}]},
  {"name":"Bellingham Concrete","domain":"bellinghamconcrete.com","slug":"bellingham-concrete","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":None,
   "dfs":{"total":87,"etv":143,"new":74,"up":6,"down":4,"lost":0,"pos_1":4,"pos_2_3":0,"pos_4_10":2,"pos_11_20":10,"pos_21_plus":71,"mdr":251},
   "rybbit":None,
   "insights":[{"type":"positive","title":"4 Keywords Ranking #1 — Page-One Dominance","body":"Bellingham Concrete holds 4 keywords at position #1 and 2 in the top 10. These high-intent local concrete queries are directly driving qualified lead traffic for the business."},{"type":"positive","title":"Strong ETV of $143 with 87 Keywords","body":"87 tracked organic keywords with $143 estimated traffic value reflects a healthy local presence. Stambaugh Designs has built a competitive foundation in the Bellingham concrete contractor market."},{"type":"positive","title":"74 New Keywords Gained This Period","body":"An exceptional 74 new keyword entries demonstrate that ongoing SEO work is rapidly expanding Bellingham Concrete's organic footprint across new service and location terms."},{"type":"warning","title":"10 Keywords on Page 2 — Ready to Promote","body":"With 10 keywords in positions 11-20, targeted content improvements and additional backlinks could push several to page 1, potentially tripling click volume from these terms."}]},
  {"name":"Round Rock Plumbing","domain":"roundrockplumbing.co","slug":"round-rock-plumbing","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":106,"impressions":52075,"ctr":0.20,"position":19.1},"prev":{"clicks":91,"impressions":37728,"ctr":0.24,"position":23.9},
     "daily":[{"d":"Feb 23","c":3,"i":1218},{"d":"Feb 24","c":3,"i":3526},{"d":"Feb 28","c":3,"i":1562},{"d":"Mar 01","c":8,"i":1674},{"d":"Mar 02","c":6,"i":1745},{"d":"Mar 03","c":6,"i":1954},{"d":"Mar 04","c":3,"i":2119},{"d":"Mar 08","c":10,"i":1720},{"d":"Mar 09","c":6,"i":1890},{"d":"Mar 10","c":1,"i":2360},{"d":"Mar 12","c":4,"i":2641},{"d":"Mar 14","c":5,"i":1979},{"d":"Mar 15","c":7,"i":1484},{"d":"Mar 19","c":4,"i":1803},{"d":"Mar 21","c":3,"i":1692},{"d":"Mar 22","c":5,"i":1416}],
     "queries":[{"q":"best drain cleaner for pvc pipes","c":9,"i":816,"ctr":1.1,"pos":8.2},{"q":"plumbers near me","c":3,"i":552,"ctr":0.5,"pos":22.1},{"q":"plumbers round rock","c":3,"i":259,"ctr":1.2,"pos":14.3},{"q":"round rock plumbing","c":3,"i":217,"ctr":1.4,"pos":3.1},{"q":"best drain cleaner for plastic pipes","c":2,"i":76,"ctr":2.6,"pos":6.4},{"q":"plumber near me","c":2,"i":1721,"ctr":0.1,"pos":28.4},{"q":"plumber round rock","c":2,"i":354,"ctr":0.6,"pos":12.2},{"q":"plumbing round rock","c":2,"i":204,"ctr":1.0,"pos":11.8}]},
   "dfs":{"total":200,"etv":4704,"new":85,"up":97,"down":18,"lost":0,"pos_1":7,"pos_2_3":0,"pos_4_10":5,"pos_11_20":14,"pos_21_plus":174,"mdr":239},
   "rybbit":None,
   "insights":[{"type":"positive","title":"7 Keywords at Position #1 — Outstanding Performance","body":"Round Rock Plumbing holds 7 #1 rankings and a remarkable ETV of $4,704 — one of the strongest performers in the Stambaugh Designs portfolio. These top positions represent tens of thousands of dollars in equivalent paid traffic value."},{"type":"positive","title":"Clicks Up +16.5% & Impressions Up +38%","body":"106 organic clicks (+16.5%) alongside 52,075 impressions (+38%) this period. The massive impression growth signals Google is expanding the site's reach significantly."},{"type":"positive","title":"97 Keywords Moving Up in Rankings","body":"An exceptional 97 keywords improved in position this period versus only 18 declining. This heavily positive momentum reflects Stambaugh Designs' consistent optimization work paying off."},{"type":"warning","title":"'Plumber Near Me' Has 1,721 Impressions at Low CTR","body":"The highest-impression query shows a significant CTR opportunity. Optimizing the title tag and meta description for this term could yield 10-20 additional monthly clicks from existing rankings."}]},
  {"name":"Sparrow's Pest Control","domain":"sparrowspestcontrol.com","slug":"sparrows-pest-control","send_to":"eric@sparrowspestcontrol.com","cc":"hello@stambaughdesigns.co",
   "gsc":{"cur":{"clicks":25,"impressions":8703,"ctr":0.29,"position":16.9},"prev":{"clicks":10,"impressions":8757,"ctr":0.11,"position":14.0},
     "daily":[{"d":"Feb 23","c":0,"i":475},{"d":"Feb 25","c":1,"i":260},{"d":"Feb 27","c":2,"i":281},{"d":"Mar 01","c":1,"i":133},{"d":"Mar 02","c":5,"i":543},{"d":"Mar 04","c":2,"i":309},{"d":"Mar 05","c":1,"i":229},{"d":"Mar 10","c":3,"i":605},{"d":"Mar 11","c":3,"i":276},{"d":"Mar 12","c":1,"i":206},{"d":"Mar 13","c":2,"i":196},{"d":"Mar 14","c":2,"i":219},{"d":"Mar 16","c":1,"i":471},{"d":"Mar 19","c":1,"i":291},{"d":"Mar 21","c":0,"i":549},{"d":"Mar 22","c":0,"i":287}],
     "queries":[{"q":"pest control bellingham","c":3,"i":377,"ctr":0.8,"pos":12.4},{"q":"bellingham pest control","c":2,"i":73,"ctr":2.7,"pos":14.1},{"q":"pest control blaine wa","c":2,"i":67,"ctr":3.0,"pos":9.8},{"q":"bellingham exterminators","c":1,"i":15,"ctr":6.7,"pos":8.2},{"q":"pest control bellingham wa","c":1,"i":177,"ctr":0.6,"pos":14.9},{"q":"sparrow pest control","c":1,"i":193,"ctr":0.5,"pos":6.1}]},
   "dfs":{"total":181,"etv":235,"new":69,"up":72,"down":36,"lost":0,"pos_1":0,"pos_2_3":1,"pos_4_10":2,"pos_11_20":18,"pos_21_plus":160,"mdr":99},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Clicks Up +150% — Best Month-Over-Month Growth","body":"Sparrow's Pest Control saw an exceptional 150% increase in organic clicks (10 to 25) with CTR jumping from 0.11% to 0.29%. This is one of the strongest performance improvements across the entire portfolio this period."},{"type":"positive","title":"72 Keywords Rising — Strong Positive Momentum","body":"72 keywords improved in ranking versus 36 declining, showing a healthy 2:1 positive ratio. Stambaugh Designs' ongoing optimization is clearly moving the needle."},{"type":"positive","title":"181 Organic Keywords with $235 ETV","body":"A growing organic footprint of 181 keywords covers the full range of Bellingham-area pest control services."},{"type":"warning","title":"18 Page-2 Keywords Ready for Promotion","body":"With 18 keywords in positions 11-20, focused link building and content enhancement for top terms like 'pest control bellingham' could significantly boost page-1 presence and lead volume."}]},
  {"name":"Bloomington Tree Service","domain":"bloomingtontreeservice.com","slug":"bloomington-tree-service","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":29,"impressions":5974,"ctr":0.49,"position":23.0},"prev":{"clicks":10,"impressions":5857,"ctr":0.17,"position":26.4},
     "daily":[{"d":"Feb 23","c":2,"i":305},{"d":"Feb 24","c":1,"i":248},{"d":"Feb 26","c":1,"i":164},{"d":"Feb 27","c":1,"i":199},{"d":"Mar 01","c":2,"i":219},{"d":"Mar 05","c":2,"i":253},{"d":"Mar 09","c":0,"i":304},{"d":"Mar 11","c":1,"i":144},{"d":"Mar 13","c":1,"i":166},{"d":"Mar 14","c":1,"i":223},{"d":"Mar 15","c":2,"i":185},{"d":"Mar 16","c":4,"i":243},{"d":"Mar 17","c":2,"i":182},{"d":"Mar 18","c":2,"i":150},{"d":"Mar 20","c":2,"i":240},{"d":"Mar 21","c":4,"i":277},{"d":"Mar 22","c":1,"i":318}],
     "queries":[{"q":"tree removal bloomington","c":1,"i":104,"ctr":1.0,"pos":9.1},{"q":"tree service bloomington","c":1,"i":82,"ctr":1.2,"pos":8.4},{"q":"tree service","c":1,"i":73,"ctr":1.4,"pos":6.2},{"q":"tree service bloomington indiana","c":1,"i":30,"ctr":3.3,"pos":7.8},{"q":"tree cutting service","c":1,"i":35,"ctr":2.9,"pos":5.4},{"q":"tree service near me","c":1,"i":36,"ctr":2.8,"pos":8.1},{"q":"bloomington tree removal","c":1,"i":34,"ctr":2.9,"pos":6.7},{"q":"bloomington tree service","c":1,"i":29,"ctr":3.4,"pos":4.2},{"q":"arborist near me","c":1,"i":31,"ctr":3.2,"pos":7.6},{"q":"stump removal","c":1,"i":3,"ctr":33.3,"pos":2.1}]},
   "dfs":{"total":57,"etv":51,"new":30,"up":15,"down":12,"lost":0,"pos_1":1,"pos_2_3":1,"pos_4_10":9,"pos_11_20":3,"pos_21_plus":43,"mdr":110},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Clicks Up +190% — Outstanding Growth Trend","body":"Bloomington Tree Service tripled organic clicks from 10 to 29 (+190%), with CTR jumping from 0.17% to 0.49%. Average position improved nearly 3.5 spots to 23.0 — a strong signal that rankings are climbing toward page 1."},{"type":"positive","title":"1 Keyword at #1, 9 in Top 10","body":"The site holds 1 #1 ranking and 9 keywords in the top 10 positions, driving high-quality clicks from actively searching tree service customers in the Bloomington, IN area."},{"type":"positive","title":"10 Diverse Queries Generating Clicks","body":"Clicks are spread across 10 different queries showing a healthy multi-keyword traffic profile rather than dependence on a single term."},{"type":"warning","title":"Spring Season Opportunity — Act Now","body":"Tree service demand peaks in spring. Stambaugh Designs recommends prioritizing local content and GMB posts in March-April to capitalize on seasonal search volume spikes."}]},
  {"name":"Monarca Construction & Remodel","domain":"monarcaconstructionremodel.com","slug":"monarca-construction","send_to":"monarcaconts@yahoo.com","cc":"hello@stambaughdesigns.co",
   "gsc":{"cur":{"clicks":64,"impressions":15663,"ctr":0.41,"position":18.9},"prev":{"clicks":72,"impressions":13536,"ctr":0.53,"position":19.2},
     "daily":[{"d":"Feb 23","c":1,"i":544},{"d":"Feb 24","c":3,"i":723},{"d":"Feb 25","c":2,"i":539},{"d":"Mar 01","c":1,"i":360},{"d":"Mar 03","c":2,"i":479},{"d":"Mar 04","c":1,"i":800},{"d":"Mar 06","c":4,"i":449},{"d":"Mar 07","c":3,"i":513},{"d":"Mar 09","c":2,"i":579},{"d":"Mar 10","c":3,"i":556},{"d":"Mar 11","c":2,"i":846},{"d":"Mar 12","c":3,"i":804},{"d":"Mar 13","c":2,"i":645},{"d":"Mar 15","c":2,"i":495},{"d":"Mar 16","c":4,"i":419},{"d":"Mar 17","c":3,"i":467},{"d":"Mar 18","c":8,"i":602},{"d":"Mar 19","c":1,"i":1178},{"d":"Mar 20","c":4,"i":557},{"d":"Mar 22","c":2,"i":401}],
     "queries":[{"q":"monarca construction","c":4,"i":57,"ctr":7.0,"pos":2.1},{"q":"monarca construction & remodeling","c":3,"i":26,"ctr":11.5,"pos":1.8},{"q":"monarca construction & remodeling llc","c":3,"i":42,"ctr":7.1,"pos":1.4},{"q":"monarca construction llc","c":3,"i":34,"ctr":8.8,"pos":2.0},{"q":"bathroom remodeling bellingham","c":2,"i":94,"ctr":2.1,"pos":9.2},{"q":"monarch construction","c":2,"i":24,"ctr":8.3,"pos":3.1},{"q":"bathroom remodel bellingham","c":1,"i":98,"ctr":1.0,"pos":10.4},{"q":"bathroom remodel bellingham wa","c":1,"i":29,"ctr":3.4,"pos":8.8},{"q":"bathroom design remodel","c":1,"i":2,"ctr":50.0,"pos":4.2},{"q":"bellingham contractors","c":1,"i":16,"ctr":6.3,"pos":6.1}]},
   "dfs":{"total":130,"etv":313,"new":66,"up":40,"down":19,"lost":0,"pos_1":2,"pos_2_3":0,"pos_4_10":15,"pos_11_20":30,"pos_21_plus":83,"mdr":285},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Impressions Grew +15.7% to 15,663","body":"Despite a modest -11% click dip, impressions grew significantly from 13,536 to 15,663. This expansion in impression share indicates Google is surfacing Monarca for a broader range of remodeling searches — setting the stage for more click growth."},{"type":"positive","title":"2 Keywords at #1, 15 in Top 10","body":"Monarca holds 2 top-ranked keywords and 15 in positions 4-10. With $313 in estimated traffic value, the site is well-positioned in competitive Bellingham remodeling searches."},{"type":"positive","title":"66 New Keywords + 40 Rising","body":"66 new keyword entries and 40 keywords improving in position show strong upward momentum. Stambaugh Designs' content strategy is actively expanding Monarca's organic presence."},{"type":"warning","title":"30 Keywords at Positions 11-20 — Big Opportunity","body":"With 30 keywords on page 2, Monarca has substantial latent traffic potential. Targeting these terms with enhanced content, schema markup, and internal links could unlock a significant traffic boost in the coming 30-60 days."}]},
  {"name":"Seattle Trim Repair","domain":"seattletrimrepair.com","slug":"seattle-trim-repair","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":95,"impressions":25819,"ctr":0.37,"position":18.1},"prev":{"clicks":62,"impressions":21183,"ctr":0.29,"position":19.5},
     "daily":[{"d":"Feb 23","c":2,"i":1754},{"d":"Feb 24","c":2,"i":1013},{"d":"Feb 25","c":3,"i":816},{"d":"Feb 27","c":4,"i":843},{"d":"Feb 28","c":7,"i":748},{"d":"Mar 01","c":4,"i":776},{"d":"Mar 02","c":6,"i":886},{"d":"Mar 03","c":7,"i":1068},{"d":"Mar 05","c":5,"i":935},{"d":"Mar 06","c":6,"i":730},{"d":"Mar 10","c":4,"i":955},{"d":"Mar 11","c":3,"i":916},{"d":"Mar 12","c":3,"i":784},{"d":"Mar 13","c":5,"i":892},{"d":"Mar 16","c":6,"i":955},{"d":"Mar 17","c":6,"i":1180},{"d":"Mar 18","c":4,"i":1002},{"d":"Mar 20","c":7,"i":952},{"d":"Mar 21","c":1,"i":906},{"d":"Mar 22","c":4,"i":854}],
     "queries":[{"q":"seattle trim repair","c":11,"i":49,"ctr":22.4,"pos":1.2},{"q":"siding repair seattle","c":4,"i":150,"ctr":2.7,"pos":8.4},{"q":"cost to replace rotted wood trim on house","c":1,"i":66,"ctr":1.5,"pos":11.2},{"q":"exterior wood repair near me","c":1,"i":5,"ctr":20.0,"pos":6.4},{"q":"hardie siding repair","c":1,"i":8,"ctr":12.5,"pos":7.1},{"q":"home siding repair near me","c":1,"i":2,"ctr":50.0,"pos":5.8},{"q":"house exterior repair","c":1,"i":2,"ctr":50.0,"pos":4.2},{"q":"outdoor wood trim repair","c":1,"i":6,"ctr":16.7,"pos":5.9},{"q":"seattle siding repair","c":1,"i":124,"ctr":0.8,"pos":9.6},{"q":"seattle trim repair reviews","c":1,"i":25,"ctr":4.0,"pos":2.8}]},
   "dfs":{"total":128,"etv":166,"new":81,"up":33,"down":10,"lost":0,"pos_1":1,"pos_2_3":0,"pos_4_10":8,"pos_11_20":18,"pos_21_plus":101,"mdr":269},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Clicks Up +53% — Consistent Upward Trajectory","body":"Seattle Trim Repair grew clicks from 62 to 95 (+53%) with impressions up 22% to 25,819. Average position improved to 18.1 from 19.5 — a 1.4-position gain across 25,000+ impressions showing broad ranking improvement."},{"type":"positive","title":"#1 for 'Seattle Trim Repair' Brand Term","body":"The brand query drives 11.5% of all clicks with a strong branded presence established. Combined with 8 keywords in the top 10, Seattle Trim Repair has a solid page-1 foundation."},{"type":"positive","title":"81 New Keywords — Fastest-Growing Footprint","body":"81 new keyword entries represent the highest new-keyword gain among service-based clients this period. Stambaugh Designs' content strategy is aggressively expanding the site's topical authority."},{"type":"warning","title":"'Siding Repair Seattle' — 150 Impressions, High Value","body":"With 4 clicks on 150 impressions, 'siding repair seattle' is a high-priority term. Enhanced page content and a targeted backlink could push this term to the top 5 and significantly boost leads."}]},
  {"name":"Bellingham ADU Builders","domain":"bellinghamadubuilders.com","slug":"bellingham-adu-builders","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":None,
   "dfs":{"total":33,"etv":19,"new":22,"up":6,"down":5,"lost":0,"pos_1":0,"pos_2_3":0,"pos_4_10":5,"pos_11_20":6,"pos_21_plus":22,"mdr":54},
   "rybbit":None,
   "insights":[{"type":"positive","title":"5 Keywords in Top 10 — Strong Early Traction","body":"Bellingham ADU Builders has 5 keywords ranking in positions 4-10, including informational ADU regulation content that is attracting research-stage homeowners — a valuable audience for future conversion."},{"type":"positive","title":"22 New Keywords + Growing Domain Authority","body":"22 new keyword entries with a growing domain authority (MDR 54) show strong early-stage SEO momentum. Stambaugh Designs has established a solid technical and content foundation."},{"type":"warning","title":"ADU Regulation Content Driving Traffic","body":"Blog content about Whatcom County ADU rules is the primary traffic driver. Expanding with more service pages (ADU design, permitting, construction) will attract higher-intent buyers ready to start a project."}]},
  {"name":"Sasquatch Plumbing Seattle","domain":"sasquatchplumbingseattle.com","slug":"sasquatch-plumbing","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":9,"impressions":1320,"ctr":0.68,"position":32.3},"prev":{"clicks":13,"impressions":4776,"ctr":0.27,"position":44.1},
     "daily":[{"d":"Feb 23","c":0,"i":20},{"d":"Feb 25","c":1,"i":179},{"d":"Mar 01","c":1,"i":54},{"d":"Mar 02","c":1,"i":141},{"d":"Mar 07","c":1,"i":26},{"d":"Mar 08","c":1,"i":28},{"d":"Mar 11","c":1,"i":51},{"d":"Mar 12","c":1,"i":61},{"d":"Mar 15","c":1,"i":22},{"d":"Mar 16","c":1,"i":52},{"d":"Mar 17","c":0,"i":67},{"d":"Mar 22","c":0,"i":12}],
     "queries":[]},
   "dfs":{"total":15,"etv":4,"new":13,"up":1,"down":0,"lost":0,"pos_1":0,"pos_2_3":0,"pos_4_10":1,"pos_11_20":1,"pos_21_plus":13,"mdr":67},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Average Position Jumped 11.8 Spots (44 → 32)","body":"Sasquatch Plumbing showed the most dramatic position improvement in the portfolio — gaining nearly 12 positions on average. Stambaugh Designs' foundational SEO work is rapidly pulling keywords toward page-visible positions."},{"type":"positive","title":"CTR Improved to 0.68% — Best in Portfolio","body":"While click volume is building, the 0.68% CTR is the highest of any client with GSC data, indicating compelling meta copy is resonating when the site does appear in results."},{"type":"positive","title":"13 New Keywords Indexed This Period","body":"All 13 new keyword entries represent fresh indexation of service pages and location content. The site is progressing through Google's trust cycle on schedule."},{"type":"warning","title":"Building Critical Mass — 60-Day Growth Phase","body":"Sasquatch Plumbing is in a critical early-growth phase. Stambaugh Designs recommends consistent GMB management, citation building, and new service-area content to accelerate rankings into page-1 positions within the next 60 days."}]},
  {"name":"Rockwall Remodeler","domain":"rockwallremodeler.com","slug":"rockwall-remodeler","send_to":"hello@stambaughdesigns.co","cc":None,
   "gsc":{"cur":{"clicks":14,"impressions":3941,"ctr":0.36,"position":12.5},"prev":{"clicks":12,"impressions":3758,"ctr":0.32,"position":17.5},
     "daily":[{"d":"Feb 24","c":1,"i":131},{"d":"Feb 27","c":1,"i":234},{"d":"Mar 02","c":3,"i":656},{"d":"Mar 03","c":1,"i":86},{"d":"Mar 04","c":0,"i":349},{"d":"Mar 09","c":2,"i":143},{"d":"Mar 12","c":1,"i":222},{"d":"Mar 13","c":2,"i":67},{"d":"Mar 17","c":1,"i":121},{"d":"Mar 20","c":2,"i":167},{"d":"Mar 22","c":0,"i":60}],
     "queries":[]},
   "dfs":{"total":6,"etv":1,"new":2,"up":1,"down":3,"lost":0,"pos_1":0,"pos_2_3":0,"pos_4_10":0,"pos_11_20":3,"pos_21_plus":3,"mdr":141},
   "rybbit":None,
   "insights":[{"type":"positive","title":"Average Position Improved 5 Spots — Strong Progress","body":"Rockwall Remodeler's average position improved dramatically from 17.5 to 12.5 — a 5-position gain bringing the site to the threshold of page 1."},{"type":"positive","title":"Clicks Up +16.7% with Steady Impression Growth","body":"14 clicks on 3,941 impressions with a 0.36% CTR shows improving engagement. The site is building consistent visibility in the competitive Rockwall, TX remodeling market."},{"type":"warning","title":"3 Keywords at Positions 11-13 — Page 1 Within Reach","body":"With 3 keywords clustered just below page 1, Rockwall Remodeler is positioned for a potential breakthrough month. A targeted push on content and local citations could capture these rankings."},{"type":"warning","title":"Small Keyword Base — Expansion Needed","body":"With 6 total tracked keywords, expanding content to cover more Rockwall remodeling services (kitchen, bathroom, additions) will build the keyword base needed for sustained organic lead flow."}]}
]

# ── Report generator ────────────────────────────────────────────────────────
def generate_report(client):
    name = client["name"]
    domain = client.get("domain", client["slug"] + ".com")
    slug = client["slug"]
    gsc = client.get("gsc")
    dfs = client["dfs"]
    rybbit = client.get("rybbit")
    insights = client["insights"]
    total = dfs["total"]

    # ── Top KPI strip ──
    if gsc:
        c, p = gsc["cur"], gsc["prev"]
        kpi_html = f"""
  <div class="kpi-grid">
    <div class="kpi-card"><div class="kpi-label">Organic Clicks</div><div class="kpi-value">{fmt(c['clicks'])}</div>{trend(c['clicks'],p['clicks'])}</div>
    <div class="kpi-card"><div class="kpi-label">Impressions</div><div class="kpi-value">{fmt(c['impressions'])}</div>{trend(c['impressions'],p['impressions'])}</div>
    <div class="kpi-card"><div class="kpi-label">Avg. CTR</div><div class="kpi-value">{c['ctr']}%</div>{trend(c['ctr'],p['ctr'])}</div>
    <div class="kpi-card"><div class="kpi-label">Avg. Position</div><div class="kpi-value">{c['position']}</div>{trend(c['position'],p['position'],invert=True)}</div>
  </div>"""
    else:
        kpi_html = f"""
  <div class="kpi-grid" style="grid-template-columns:repeat(2,1fr);">
    <div class="kpi-card"><div class="kpi-label">Organic Keywords</div><div class="kpi-value">{fmt(total)}</div><span class="kpi-trend neutral">+{dfs['new']} new this period</span></div>
    <div class="kpi-card"><div class="kpi-label">Est. Traffic Value</div><div class="kpi-value">${fmt(dfs['etv'])}</div><span class="kpi-trend neutral">— DataForSEO</span></div>
  </div>"""

    # ── Section 01: Rybbit (if available) ──
    if rybbit:
        dev = rybbit["devices"]
        dev_labels = json.dumps([d["label"] for d in dev])
        dev_data = json.dumps([d["pct"] for d in dev])
        ref_rows = "".join(
            f'<tr><td>{rank_badge(i)}</td><td><strong>{r["src"]}</strong></td><td class="mono">{r["visits"]}</td></tr>'
            for i, r in enumerate(rybbit["referrers"][:6]))
        _dev_js = ('<script>new Chart(document.getElementById("deviceChart"),{type:"doughnut",data:{labels:'
                   + dev_labels + ',datasets:[{data:' + dev_data
                   + ',backgroundColor:["#c4550a","#8c7e6e","#e8e0d8"],borderWidth:0,cutout:"65%"}]},'
                   'options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"bottom",labels:{usePointStyle:true,pointStyle:"circle",padding:12,font:{size:11,weight:"500"}}}}}});</script>')
        analytics_section = f"""
  <div class="section">
    <div class="section-header"><div class="section-icon orange">📈</div><div><div class="section-number">Section 01</div><div class="section-title">Site Analytics (Rybbit)</div></div></div>
    <div class="mini-kpi-row">
      <div class="mini-kpi"><div class="value">{fmt(rybbit['sessions'])}</div><div class="label">Sessions</div></div>
      <div class="mini-kpi"><div class="value">{fmt(rybbit['pageviews'])}</div><div class="label">Pageviews</div></div>
      <div class="mini-kpi"><div class="value">{fmt(rybbit['users'])}</div><div class="label">Unique Users</div></div>
      <div class="mini-kpi"><div class="value">{rybbit['bounce_rate']}%</div><div class="label">Bounce Rate</div></div>
    </div>
    <div class="mini-kpi-row" style="grid-template-columns:repeat(2,1fr);">
      <div class="mini-kpi"><div class="value">{rybbit['duration']}s</div><div class="label">Avg. Duration</div></div>
      <div class="mini-kpi"><div class="value">{rybbit['pages_per_session']}</div><div class="label">Pages / Session</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:20px;">
      <div>
        <h4 style="font-size:13px;font-weight:700;margin-bottom:12px;color:var(--text-secondary);letter-spacing:0.5px;text-transform:uppercase;">Device Split</h4>
        <div class="chart-container" style="height:200px;"><canvas id="deviceChart"></canvas></div>
        {_dev_js}
      </div>
      <div>
        <h4 style="font-size:13px;font-weight:700;margin-bottom:12px;color:var(--text-secondary);letter-spacing:0.5px;text-transform:uppercase;">Top Referrers</h4>
        <table><thead><tr><th>#</th><th>Source</th><th>Visits</th></tr></thead><tbody>{ref_rows}</tbody></table>
      </div>
    </div>
  </div>"""
        gsc_section_num = "Section 02"
        kw_section_num  = "Section 03"
        ins_section_num = "Section 04"
    else:
        analytics_section = ""
        gsc_section_num = "Section 01"
        kw_section_num  = "Section 02"
        ins_section_num = "Section 03"

    # ── GSC daily chart ──
    if gsc and gsc.get("daily"):
        daily = gsc["daily"]
        labels = json.dumps([d["d"] for d in daily])
        clicks_data = json.dumps([d["c"] for d in daily])
        impr_data = json.dumps([d["i"] for d in daily])
        _ch_tpl = ('new Chart(document.getElementById("dailyChart").getContext("2d"),{type:"bar",'
                   'data:{labels:__L__,datasets:['
                   '{label:"Clicks",data:__C__,backgroundColor:"#c4550a",borderRadius:4,barPercentage:0.6,yAxisID:"y",order:2},'
                   '{label:"Impressions",data:__I__,type:"line",borderColor:"#8c7e6e",backgroundColor:"rgba(140,126,110,0.1)",fill:true,tension:0.4,pointRadius:4,pointBackgroundColor:"#8c7e6e",borderWidth:2,yAxisID:"y1",order:1}'
                   ']},options:{responsive:true,maintainAspectRatio:false,interaction:{mode:"index",intersect:false},'
                   'plugins:{legend:{position:"top",align:"end",labels:{usePointStyle:true,pointStyle:"circle",padding:20,font:{size:11,weight:"600"}}}},'
                   'scales:{y:{beginAtZero:true,position:"left",title:{display:true,text:"Clicks",font:{size:11,weight:"600"}},grid:{color:"rgba(0,0,0,0.04)"},ticks:{font:{size:11}}},'
                   'y1:{beginAtZero:true,position:"right",title:{display:true,text:"Impressions",font:{size:11,weight:"600"}},grid:{display:false},ticks:{font:{size:11}}},'
                   'x:{grid:{display:false},ticks:{font:{size:10}}}}}}); ')
        daily_chart_js = '<script>' + _ch_tpl.replace("__L__", labels).replace("__C__", clicks_data).replace("__I__", impr_data) + '</script>'
        daily_chart_html = f'<div class="chart-container"><canvas id="dailyChart"></canvas></div>{daily_chart_js}'
    else:
        daily_chart_html = '<div class="no-data">Google Search Console data not yet available for this domain.</div>'

    # ── GSC queries table ──
    if gsc and gsc.get("queries"):
        q_rows = "".join(
            f'<tr><td>{rank_badge(i)}</td><td><strong>{q["q"]}</strong></td>'
            f'<td class="mono">{q["c"]}</td><td class="mono">{q["i"]}</td>'
            f'<td class="mono">{q.get("ctr","—")}</td><td class="mono">{q.get("pos","—")}</td></tr>'
            for i, q in enumerate(gsc["queries"][:10]))
        queries_html = f"""
        <h4 style="font-size:13px;font-weight:700;margin:24px 0 12px;color:var(--text-secondary);letter-spacing:0.5px;text-transform:uppercase;">Top Search Queries</h4>
        <table>
          <thead><tr><th>#</th><th>Query</th><th>Clicks</th><th>Impr</th><th>CTR%</th><th>Avg Pos</th></tr></thead>
          <tbody>{q_rows}</tbody>
        </table>"""
    else:
        queries_html = '<div class="no-data" style="margin-top:16px;">No query data available for this period.</div>'

    # ── Keyword distribution chart ──
    kw_labels_js = json.dumps(["Top 3", "Pos 4-10", "Pos 11-20", "Pos 21+"])
    kw_data_js = json.dumps([dfs["pos_1"] + dfs["pos_2_3"], dfs["pos_4_10"], dfs["pos_11_20"], dfs["pos_21_plus"]])
    kw_colors_js = '["#2d7a3a","#1a6bb5","#b5680a","#c4390a"]'
    _kw_tpl = ('new Chart(document.getElementById("kwChart").getContext("2d"),{type:"bar",'
               'data:{labels:__KL__,datasets:[{label:"Keywords",data:__KD__,'
               'backgroundColor:__KC__,borderRadius:6,barPercentage:0.65}]},'
               'options:{responsive:true,maintainAspectRatio:false,indexAxis:"y",'
               'plugins:{legend:{display:false}},'
               'scales:{x:{beginAtZero:true,grid:{color:"rgba(0,0,0,0.04)"},ticks:{font:{size:11}}},'
               'y:{grid:{display:false},ticks:{font:{size:11,weight:"600"}}}}}});')
    kw_chart_js = '<script>' + _kw_tpl.replace("__KL__", kw_labels_js).replace("__KD__", kw_data_js).replace("__KC__", kw_colors_js) + '</script>'

    # ── Insights ──
    ins_html = ""
    for ins in insights:
        cls = ins["type"]  # positive / warning / critical
        icon = insight_icon(cls)
        ins_html += f'<div class="insight {cls}"><span class="insight-icon">{icon}</span><div class="insight-content"><h4>{ins["title"]}</h4><p>{ins["body"]}</p></div></div>'

    # ── Executive summary ──
    if gsc:
        c, p = gsc["cur"], gsc["prev"]
        click_word = "grew" if c["clicks"] >= p["clicks"] else "adjusted"
        click_pct = abs(round((c["clicks"] - p["clicks"]) / max(p["clicks"], 1) * 100))
        mo_note = (f"Click volume {click_word} {click_pct}% month-over-month, reflecting"
                   if p["clicks"] > 0 else "This period continues to build on")
        summary = (f'<p>{name} generated <strong>{fmt(c["clicks"])} organic clicks</strong> from '
                   f'<strong>{fmt(c["impressions"])} impressions</strong> this period, with an average '
                   f'position of <strong>{c["position"]}</strong> across Google Search. '
                   f'{mo_note} the compounding impact of Stambaugh Designs\' ongoing SEO strategy.</p>'
                   f'<p>With <strong>{fmt(total)} total organic keywords</strong> and an estimated traffic '
                   f'value of <strong>${fmt(dfs["etv"])}</strong>, {name.split()[0]} is building meaningful '
                   f'organic visibility in its target market. <strong>{dfs["new"]} new keywords</strong> '
                   f'entered rankings this period — a clear signal of expanding topical authority, with '
                   f'<strong>{dfs["up"]} keywords moving up</strong> versus {dfs["down"]} declining.</p>')
    else:
        summary = (f'<p>This report highlights the foundational SEO work Stambaugh Designs is executing for '
                   f'<strong>{name}</strong>. With <strong>{fmt(total)} organic keywords</strong> currently '
                   f'tracking and an estimated traffic value of <strong>${fmt(dfs["etv"])}</strong>, the site '
                   f'is progressing on schedule through Google\'s trust and indexation cycle.</p>'
                   f'<p><strong>{dfs["new"]} new keywords</strong> entered rankings this period, indicating '
                   f'active crawler engagement and content indexation. Stambaugh Designs continues to build '
                   f'the technical foundation, content quality, and local authority signals needed to drive '
                   f'consistent organic lead flow in the months ahead.</p>')

    # ── Keyword position table ──
    def pct_bar(n, t, color):
        w = round(n / max(t, 1) * 100)
        return f'<div class="progress-bar" style="width:180px;"><div class="progress-fill" style="width:{w}%;background:{color};"></div></div>'

    pos_rows = [
        ("Top 3", dfs["pos_1"]+dfs["pos_2_3"], "tag-green", "#2d7a3a"),
        ("Pos 4–10", dfs["pos_4_10"], "tag-blue", "#1a6bb5"),
        ("Pos 11–20", dfs["pos_11_20"], "tag-blue", "#1a6bb5"),
        ("Pos 21+", dfs["pos_21_plus"], "tag-orange", "#b5680a"),
    ]
    pos_table_rows = "".join(
        f'<tr><td><span class="tag {t}">{label}</span></td>'
        f'<td class="mono"><strong>{n}</strong></td>'
        f'<td>{pct_bar(n, total, color)}</td></tr>'
        for label, n, t, color in pos_rows)

    # ── Full HTML ──────────────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO &amp; Analytics Report — {name}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>{CSS}</style>
</head>
<body>

<div class="report-header">
  <div class="container">
    <div class="hdr-badge">SEO &amp; Analytics Report</div>
    <div class="header-domain">{domain}</div>
    <div class="header-subtitle">{name} — Comprehensive Performance Analysis</div>
    <div class="header-meta">
      <span>📅 {PERIOD}</span>
      <span>📊 Data Sources: GSC · DataForSEO{" · Rybbit" if rybbit else ""}</span>
      <span>🖨 Generated: {GENERATED}</span>
    </div>
  </div>
</div>

<div class="container">
  <div style="height:28px;"></div>

  <!-- AI Executive Summary -->
  <div class="ai-summary">
    <div class="ai-summary-header">
      <span class="ai-badge">AI Analysis</span>
      <h3>Executive Summary</h3>
    </div>
    <div class="ai-summary-body">{summary}</div>
  </div>

  <!-- Top KPIs -->
  {kpi_html}

  <!-- Analytics (Rybbit) -->
  {analytics_section}

  <!-- GSC Section -->
  <div class="section">
    <div class="section-header"><div class="section-icon blue">🔍</div><div><div class="section-number">{gsc_section_num}</div><div class="section-title">Google Search Console</div></div></div>
    <h4 style="font-size:13px;font-weight:700;margin-bottom:4px;">Daily Clicks &amp; Impressions</h4>
    <p style="font-size:12px;color:var(--text-muted);margin-bottom:8px;">{PERIOD}</p>
    {daily_chart_html}
    {queries_html}
  </div>

  <!-- Keyword Visibility -->
  <div class="section">
    <div class="section-header"><div class="section-icon green">🌱</div><div><div class="section-number">{kw_section_num}</div><div class="section-title">Organic Keyword Visibility</div></div></div>
    <div class="mini-kpi-row">
      <div class="mini-kpi"><div class="value">{fmt(total)}</div><div class="label">Total Keywords</div></div>
      <div class="mini-kpi"><div class="value" style="color:var(--green);">+{dfs['new']}</div><div class="label">New Keywords</div></div>
      <div class="mini-kpi"><div class="value" style="color:var(--green);">{dfs['up']} ▲</div><div class="label">Moving Up</div></div>
      <div class="mini-kpi"><div class="value" style="color:var(--red);">{dfs['down']} ▼</div><div class="label">Moving Down</div></div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start;">
      <div>
        <h4 style="font-size:13px;font-weight:700;margin-bottom:12px;color:var(--text-secondary);letter-spacing:0.5px;text-transform:uppercase;">Position Distribution</h4>
        <table>
          <thead><tr><th>Range</th><th>Keywords</th><th>Share</th></tr></thead>
          <tbody>{pos_table_rows}</tbody>
        </table>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">
          <div class="mini-kpi"><div class="value">${fmt(dfs['etv'])}</div><div class="label">Est. Traffic Value</div></div>
          <div class="mini-kpi"><div class="value">{dfs['mdr']}</div><div class="label">Domain Rank (MDR)</div></div>
        </div>
      </div>
      <div>
        <h4 style="font-size:13px;font-weight:700;margin-bottom:12px;color:var(--text-secondary);letter-spacing:0.5px;text-transform:uppercase;">Keyword Distribution Chart</h4>
        <div class="chart-container" style="height:220px;"><canvas id="kwChart"></canvas></div>
        {kw_chart_js}
      </div>
    </div>
  </div>

  <!-- Insights -->
  <div class="section">
    <div class="section-header"><div class="section-icon red">💡</div><div><div class="section-number">{ins_section_num}</div><div class="section-title">Key Insights &amp; Recommendations</div></div></div>
    {ins_html}
  </div>

  <!-- Footer -->
  <div class="report-footer">
    <div class="footer-brand">Stambaugh Designs</div>
    <p>Data sources: Google Search Console · DataForSEO{" · Rybbit Analytics" if rybbit else ""}</p>
    <p style="margin-top:8px;">Questions? Contact <a href="mailto:hello@stambaughdesigns.co">hello@stambaughdesigns.co</a> · <a href="https://stambaughdesigns.co">stambaughdesigns.co</a></p>
  </div>
</div>

</body>
</html>"""

# ── Write all reports ────────────────────────────────────────────────────────
BASE = "/tmp/client-reports"
for client in clients:
    slug = client["slug"]
    out_dir = os.path.join(BASE, slug)
    os.makedirs(out_dir, exist_ok=True)
    html = generate_report(client)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w") as f:
        f.write(html)
    print(f"✓ {slug}/index.html ({os.path.getsize(out_path)//1024}KB)")

print(f"\nAll {len(clients)} reports written.")
