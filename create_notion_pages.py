import json
import os
import urllib.request
import urllib.error

TOKEN = os.environ["NOTION_TOKEN"]
PARENT_ID = os.environ.get("NOTION_PARENT_PAGE_ID", "311b3490-e35a-80bb-afcf-fb14f5a27feb")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def api(method, path, data=None):
    url = f"https://api.notion.com/v1{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"Error {e.code}: {e.read().decode()}")
        return None

def text(content, bold=False, color="default"):
    t = {"type": "text", "text": {"content": content}}
    if bold or color != "default":
        t["annotations"] = {"bold": bold, "color": color}
    return t

def h1(content):
    return {"object": "block", "type": "heading_1", "heading_1": {"rich_text": [text(content)]}}

def h2(content):
    return {"object": "block", "type": "heading_2", "heading_2": {"rich_text": [text(content)]}}

def h3(content):
    return {"object": "block", "type": "heading_3", "heading_3": {"rich_text": [text(content)]}}

def para(content, bold=False):
    if isinstance(content, str):
        content = [text(content, bold=bold)]
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": content}}

def bullet(content):
    if isinstance(content, str):
        content = [text(content)]
    return {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {"rich_text": content}}

def numbered(content):
    return {"object": "block", "type": "numbered_list_item", "numbered_list_item": {"rich_text": [text(content)]}}

def callout(content, emoji="💡"):
    if isinstance(content, str):
        content = [text(content)]
    return {"object": "block", "type": "callout", "callout": {"rich_text": content, "icon": {"type": "emoji", "emoji": emoji}}}

def quote(content):
    return {"object": "block", "type": "quote", "quote": {"rich_text": [text(content)]}}

def divider():
    return {"object": "block", "type": "divider", "divider": {}}

def toggle(title, children=None):
    b = {"object": "block", "type": "toggle", "toggle": {"rich_text": [text(title)], "children": children or []}}
    return b

def table(rows):
    # rows is list of lists of strings
    width = len(rows[0])
    cells = []
    for row in rows:
        cells.append([[text(cell)] for cell in row])
    return {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": width,
            "has_column_header": True,
            "has_row_header": False,
            "children": [
                {"object": "block", "type": "table_row", "table_row": {"cells": row}}
                for row in cells
            ]
        }
    }

def create_page(parent_id, title, emoji, blocks):
    # Notion API limits 100 blocks per request
    data = {
        "parent": {"page_id": parent_id},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": {"title": {"title": [{"text": {"content": title}}]}},
        "children": blocks[:100]
    }
    result = api("POST", "/pages", data)
    if result and len(blocks) > 100:
        page_id = result["id"]
        for i in range(100, len(blocks), 100):
            api("PATCH", f"/blocks/{page_id}/children", {"children": blocks[i:i+100]})
    return result


# ── PAGE DEFINITIONS ──────────────────────────────────────────────────────────

pages = {}

# 1. START HERE
pages["start_here"] = ("Start Here", "🏠", [
    h1("Early Career Job Search Guide"),
    callout("No hustle content. No paid courses. Just a practical system — what to do, in what order, with templates you can use today.", "💡"),
    divider(),
    h2("Who this is for"),
    bullet("Fresh graduates in tech — SWE, data engineering, data science, data analytics"),
    bullet("Fresh graduates in business and finance — analysts, consulting, corporate finance"),
    bullet("Candidates on F-1 OPT or student visa navigating job search with visa constraints"),
    divider(),
    h2("Where are you right now?"),
    para("Pick your situation and go straight to what you need."),
    callout("🟢  I haven't started yet\n\nStart here, in this order:\n1. Fix your resume first — nothing else matters if your resume isn't solid\n2. Set up your LinkedIn profile\n3. Build your target company list (20–30 companies)\n4. Start applying directly + start outreach in parallel", "🟢"),
    callout("🟡  I'm applying but not hearing back\n\nYour problem is likely one of three things:\n• Resume isn't passing ATS → go to Resume\n• Applying through Easy Apply → go to Job Search Strategy\n• Applying to the wrong places → go to Job Boards\n\nThe fix is almost never 'apply to more jobs.' It's apply differently.", "🟡"),
    callout("🟠  I'm getting interviews but not converting\n\nYou've cleared the resume and application stage — that's more than most people. Now it's about prep:\n• Behavioral interviews → Interview Prep → Behavioral section\n• Technical screen → Interview Prep → your track\n• You freeze up or go blank → do mock interviews, not more reading", "🟠"),
    callout("🔵  I have an offer — now what?\n\nDon't accept on the spot. Go to Offer & Negotiation + Benefits.", "💙"),
    divider(),
    h2("All sections"),
    table([
        ["Section", "What's inside"],
        ["🗂 Resume", "US format, ATS basics, writing bullets, templates"],
        ["📋 Job Boards", "Where to find jobs by track — tech, finance, OPT"],
        ["🎯 Job Search Strategy", "Why Easy Apply doesn't work, what to do instead"],
        ["🤝 Networking", "Alumni outreach, cold messaging, outreach templates"],
        ["🎤 Interview Prep", "Behavioral, technical, case — by track"],
        ["💰 Offer & Negotiation", "How to evaluate and negotiate an offer"],
        ["🏥 Benefits", "Health, dental, 401k, RSUs, ESPP explained"],
        ["🛂 Visa / OPT Track", "OPT timeline, finding sponsors, H1B basics"],
        ["👥 People to Follow", "Curated by track — signal, not noise"],
    ]),
    divider(),
    h2("The honest timeline"),
    quote("Actively searching, doing everything right: 8–12 weeks to an offer\nPassively applying, Easy Apply only: 5–6 months, maybe longer\nOPT candidates: Start before graduation — your clock starts at graduation day\n\nIf you're 3 weeks in and discouraged — that's normal.\nIf you're 3 months in with no traction — something in your system needs to change, not just your effort level."),
    divider(),
    para("Built for friends and contacts. No affiliation with any job board, coaching service, or recruiter."),
])

# 2. RESUME
pages["resume"] = ("Resume", "🗂", [
    h1("Resume"),
    callout("Your resume has two jobs: get past the ATS filter, then get a human excited enough to call you. Most people write resumes for humans and wonder why they never hear back.", "💡"),
    divider(),
    h2("Format — non-negotiable"),
    callout("If your resume has columns, tables, icons, or was made in Canva — redo it. It's probably invisible to ATS.", "⚠️"),
    bullet("One page. No exceptions unless you have 10+ years of experience."),
    bullet("No photo, no date of birth, no address (city + state is fine)"),
    bullet("Standard fonts only — Calibri, Arial, Garamond"),
    bullet("No tables, no columns, no text boxes — ATS can't read them"),
    bullet("No graphics, icons, or skill bars ('Python: 80%')"),
    bullet("Save as PDF unless the posting specifically asks for Word"),
    divider(),
    h2("Structure"),
    quote("Your Name\nCity, State | Phone | Email | LinkedIn URL | GitHub (tech only)\n\nSummary (optional, 2–3 lines max)\nOnly include if you have something specific to say. Skip if it'll be generic filler.\n\nExperience\nCompany Name | Job Title | Month Year – Month Year\n- Bullet\n- Bullet\n\nEducation\nUniversity | Degree, Major | Graduation Year\nGPA (include if 3.5+, leave out if below 3.3)\n\nSkills\nList specific tools and languages only — relevant to the role"),
    divider(),
    h2("How to write bullets that actually work"),
    para("The formula: Action verb + what you did + result/scale"),
    para("If you don't have a number, estimate. 'Reduced time by ~50%' is fine. 'Improved efficiency' is not."),
    table([
        ["❌ Bad", "✅ Good"],
        ["Responsible for analyzing sales data and creating reports", "Built automated weekly sales dashboard in Tableau, reducing manual reporting time by 4 hours/week"],
        ["Worked on improving the onboarding process", "Redesigned onboarding flow, reducing time-to-productivity for new hires by 2 weeks"],
        ["Helped the finance team with monthly close", "Automated monthly close reconciliation in Python, cutting process from 3 days to 4 hours"],
    ]),
    h3("Strong action verbs"),
    toggle("Tech / Data", [
        para("Built, Developed, Designed, Automated, Deployed, Optimized, Implemented, Architected, Migrated"),
    ]),
    toggle("Finance / Business", [
        para("Analyzed, Forecasted, Modeled, Optimized, Evaluated, Structured, Presented, Streamlined"),
    ]),
    toggle("Leadership", [
        para("Led, Managed, Coordinated, Mentored, Launched, Drove, Spearheaded"),
    ]),
    callout("Avoid: Helped, Assisted, Worked on, Was responsible for, Participated in", "⚠️"),
    divider(),
    h2("Keywords — how ATS actually works"),
    para("ATS scans your resume for keywords from the job description. If the job says 'financial modeling' and your resume says 'built models,' it might not match."),
    para("Do this for every job you apply to:"),
    numbered("Read the job description"),
    numbered("Note the exact phrases they use (tools, skills, methods)"),
    numbered("Make sure those exact phrases appear in your resume — naturally, not stuffed"),
    para("Example: Job says 'experience with dbt and Snowflake' — your resume should say dbt and Snowflake, not 'data transformation tools.'"),
    divider(),
    h2("Tech vs. Business/Finance resume"),
    toggle("Tech (SWE, Data Engineering, Data Science)", [
        bullet("GitHub link is expected"),
        bullet("Projects section matters a lot if you have limited experience"),
        bullet("Stack matters — list specific languages and tools, not just 'programming'"),
        bullet("Quantify model performance, system scale, data volume"),
    ]),
    toggle("Business / Finance / Data Analytics", [
        bullet("Excel and PowerPoint are assumed — only list if advanced (pivot tables, VBA, macros)"),
        bullet("Certifications matter more here (CFA Level 1, Google Data Analytics, etc.)"),
        bullet("Include relevant coursework if recent grad with limited experience"),
        bullet("Consulting track: GPA and school name carry more weight than in tech"),
    ]),
    divider(),
    h2("Templates"),
    table([
        ["Template", "Best for"],
        ["Jake's Resume (Overleaf/LaTeX)", "Tech — clean, ATS-safe, most common"],
        ["Google Docs resume templates", "Business/Finance — simpler to edit"],
        ["Harvard OCS templates", "Consulting/Finance track"],
    ]),
    divider(),
    h2("Before you submit — checklist"),
    toggle("✅ Run through this before every application", [
        para("☐ One page"),
        para("☐ No columns, tables, or text boxes"),
        para("☐ Every bullet has an action verb + result"),
        para("☐ Keywords from the job description are in my resume"),
        para("☐ No typos (run through Grammarly)"),
        para("☐ Saved as PDF"),
        para("☐ LinkedIn URL is updated and matches resume"),
    ]),
])

# 3. JOB BOARDS
pages["job_boards"] = ("Job Boards", "📋", [
    h1("Where to Find Jobs"),
    callout("Pick 2–3 platforms maximum and work them well. More boards = more noise. Fewer boards, better applications, more outreach = better results.", "💡"),
    divider(),
    h2("Understand the channels first"),
    table([
        ["Channel", "Effectiveness", "Notes"],
        ["Referrals", "Highest", "Someone vouches for you internally"],
        ["Direct apply", "High", "Company career page, targeted"],
        ["Campus recruiting", "High", "Structured programs for new grads"],
        ["Job boards", "Lowest", "Highest volume, lowest conversion"],
    ]),
    divider(),
    h2("New grad / early career first"),
    table([
        ["Platform", "Best for", "Notes"],
        ["Handshake", "All tracks", "University-connected, companies actively recruiting new grads"],
        ["RippleMatch", "All tracks", "AI-matched early career roles, less noise than LinkedIn"],
        ["WayUp", "All tracks", "Entry-level and internships specifically"],
        ["Simplify.jobs", "Tech + Business", "Aggregates early career roles, auto-fills applications"],
        ["Parker Dewey", "All tracks", "Micro-internships that often lead to full-time"],
    ]),
    divider(),
    h2("By track"),
    toggle("💻 Tech (SWE, Data Engineering, Data Science)", [
        table([
            ["Platform", "Best for", "Notes"],
            ["Wellfound (AngelList)", "Startups", "Transparent salary + equity upfront"],
            ["Levels.fyi", "Big tech", "Compensation data + job listings"],
            ["Y Combinator job board", "YC startups", "work.ycombinator.com — curated, high signal"],
            ["Dice", "Tech broadly", "Large volume of tech roles"],
            ["Kaggle Jobs", "Data science", "Niche but good quality"],
            ["Built In", "Tech-adjacent", "Data, ops, analytics, growth roles"],
        ]),
    ]),
    toggle("📊 Business / Finance / Data Analytics", [
        table([
            ["Platform", "Best for", "Notes"],
            ["eFinancialCareers", "Finance, banking", "IB, asset management, corporate finance, risk"],
            ["Wall Street Oasis", "IB, PE, consulting", "Community-vetted, strong for finance early career"],
            ["Mergers & Inquisitions", "IB, corporate finance", "Best free guides + job board"],
            ["Vault", "Consulting", "Firm rankings, culture reviews, recruiting timelines"],
            ["LinkedIn (targeted)", "All business roles", "Apply directly — not Easy Apply"],
            ["Glassdoor", "All tracks", "Job listings + salary + interview reviews"],
        ]),
    ]),
    toggle("🛂 OPT / Visa candidates", [
        table([
            ["Platform", "Best for", "Notes"],
            ["myvisajobs.com", "OPT/H1B", "Filters roles by H1B sponsoring employers"],
            ["H1Bdata.info", "Research", "USCIS public data — see actual filing history"],
            ["Immigrationhelp.org", "OPT/visa", "Visa-specific job board"],
            ["LinkedIn (sponsor filter)", "All tracks", "Search 'visa sponsorship' in filters"],
        ]),
        callout("Before applying anywhere on OPT — check the company on H1Bdata.info first. A company saying 'we consider sponsorship' means nothing. Actual filing history does.", "⚠️"),
    ]),
    divider(),
    h2("Direct company applications — don't skip this"),
    para("Build a list of 20–30 companies you want to work at. Bookmark their careers page. Check weekly."),
    toggle("Tech — structured new grad programs (apply August–October)", [
        bullet("Google, Meta, Amazon, Microsoft, Apple — all have dedicated new grad hiring cycles"),
        bullet("Apply directly on their career pages, not through job boards"),
        bullet("Set alerts so you don't miss the window"),
    ]),
    toggle("Finance / Consulting — structured new grad programs", [
        bullet("Goldman Sachs, JPMorgan, Morgan Stanley — summer analyst applications open August"),
        bullet("McKinsey, BCG, Bain — recruiting starts September–October for following year"),
        bullet("Big 4 (Deloitte, PwC, EY, KPMG) — campus recruiting calendar on their websites"),
    ]),
    callout("If you're a May grad starting your search in March — you've already missed most structured programs. Focus on direct applications + networking for immediate roles.", "⚠️"),
    divider(),
    h2("Recommended setup by track"),
    table([
        ["Track", "Board 1", "Board 2", "Also"],
        ["Any new grad", "Handshake", "Track-specific board", "Company career pages"],
        ["Tech", "Handshake", "Wellfound + Levels.fyi", "Company career pages"],
        ["Finance", "Handshake", "eFinancialCareers + WSO", "Company career pages"],
        ["Data Analytics", "Handshake", "Simplify.jobs + Built In", "Company career pages"],
        ["OPT candidates", "All of the above", "myvisajobs.com", "H1Bdata.info for vetting"],
    ]),
])

# 4. JOB SEARCH STRATEGY
pages["job_search_strategy"] = ("Job Search Strategy", "🎯", [
    h1("Why Easy Apply Doesn't Work (And What to Do Instead)"),
    callout("Easy Apply is optimized for your convenience, not your chances. It's designed to make applying feel productive. It isn't.", "⚠️"),
    divider(),
    h2("What's actually happening when you click Easy Apply"),
    para("When a company posts on LinkedIn, they get 200–500 Easy Apply submissions in the first 48 hours. A recruiter is not reading 400 resumes. They're scanning 20, maybe 30. The rest get archived."),
    quote("Apply to 50 jobs → hear back from 2 → conclude the market is tough\nApply to 50 more → same result → repeat until demoralized\n\nThe problem isn't the market. It's the channel."),
    callout("Job boards are where candidates go. Referrals are where jobs get filled. Studies consistently show 70–80% of jobs are filled through networking.", "💡"),
    divider(),
    h2("What to do instead"),
    para("Use all three approaches in parallel."),
    divider(),
    h3("1. Targeted direct applications"),
    para("Apply directly on the company's career page — not through LinkedIn or Indeed."),
    para("Why this works:"),
    bullet("Signals genuine interest in that specific company"),
    bullet("Often goes into a different pipeline than third-party aggregators"),
    bullet("Forces you to be selective, which means better-matched applications"),
    para("How to do it:"),
    numbered("Build a list of 20–30 target companies you actually want to work at"),
    numbered("Bookmark their careers pages"),
    numbered("Apply directly, tailoring your resume to each role"),
    numbered("Track every application — company, role, date, status, next step"),
    callout("Aim for 10–15 quality applications per week, not 50 generic ones.", "💡"),
    divider(),
    h3("2. Referrals — highest conversion, most effort"),
    para("A referred candidate is 3–4x more likely to get an interview than a cold applicant."),
    numbered("Find a role you want to apply to"),
    numbered("Search LinkedIn for people at that company — filter by university, city, mutual connections"),
    numbered("Send a short, specific message — not 'can you refer me'"),
    numbered("Have a conversation first — ask about their experience, the team, the role"),
    numbered("If it goes well, they'll offer or you can ask directly"),
    toggle("✅ Message that works", [
        quote("\"Hi [Name], I noticed you work at [Company] on the [Team] team. I'm a recent grad in [field] and I'm really interested in the [Role] — I came across your profile because we both went to [University]. Would you have 15 minutes to chat about your experience there? No pressure at all.\""),
    ]),
    toggle("❌ Message that doesn't work", [
        quote("\"Hi, I am interested in the [Role] position at your company. Can you refer me?\""),
        para("People refer candidates they've talked to, not strangers who ask cold."),
    ]),
    divider(),
    h3("3. Warm outreach to hiring managers"),
    para("For smaller companies and startups, reach the hiring manager directly — not HR."),
    para("How to find them: LinkedIn search '[Company] + [Engineering Manager / Data Manager / Finance Lead]'"),
    toggle("✅ Message template", [
        quote("\"Hi [Name], I came across the [Role] posting at [Company] and it lines up closely with my background in [X]. I'd love to learn more about the team and what you're looking for — would you be open to a quick 15-minute call?\""),
    ]),
    divider(),
    h2("Your weekly system"),
    quote("Monday\n→ Research 5 target companies\n→ Find 1–2 people at each to reach out to\n\nTuesday–Thursday\n→ Send 5–10 personalized LinkedIn messages\n→ Apply directly on 5–10 company career pages (tailored resume)\n\nFriday\n→ Follow up on applications from 2 weeks ago\n→ Update tracking spreadsheet\n→ Respond to any recruiter messages"),
    divider(),
    h2("The mindset shift"),
    callout("Stop thinking of job searching as submitting applications. Start thinking of it as having conversations. Applications are a byproduct of conversations.", "💡"),
])

# 5. NETWORKING
pages["networking"] = ("Networking", "🤝", [
    h1("Networking"),
    callout("Networking for job search is simple: talk to people who are doing what you want to do, and learn from them. You're not asking for favors. Most people are happy to help because someone helped them.", "💡"),
    divider(),
    h2("The three sources of people to talk to"),
    table([
        ["Source", "Difficulty", "Response rate"],
        ["Alumni from your university", "Easiest", "Highest"],
        ["People you've worked with before", "Easy", "High"],
        ["Cold outreach to strangers", "Harder", "Lower — but scales"],
    ]),
    para("Start with alumni and former colleagues. Don't start with cold outreach."),
    divider(),
    h2("Alumni network — step by step"),
    para("How to find them on LinkedIn:"),
    numbered("Go to your university's LinkedIn page"),
    numbered("Click 'Alumni'"),
    numbered("Filter by: Where they work, What they do, When they graduated"),
    numbered("Look for people 2–5 years ahead of you"),
    toggle("✅ Alumni outreach message", [
        quote("\"Hi [Name], I'm a recent [University] grad in [field] and came across your profile. I'm exploring roles in [area] and noticed you've been at [Company] for a couple of years — I'd love to hear how you got there and what the work is actually like. Would you have 20 minutes for a quick call sometime this week or next?\""),
    ]),
    callout("Expect 20–30% response rate. If 10 people don't respond, 2–3 will. That's 2–3 conversations you wouldn't have had.", "💡"),
    divider(),
    h2("The informational interview"),
    para("A 20–30 minute call where you ask someone about their experience. Not a job interview — a conversation."),
    toggle("What to ask", [
        para("Opening:"),
        bullet("'How did you end up at [Company] / in [field]?'"),
        bullet("'What does a typical week look like for you?'"),
        para("The real stuff:"),
        bullet("'What do you wish you'd known when you were job searching?'"),
        bullet("'What do companies in this space actually look for in new grads?'"),
        bullet("'Is there anyone else you'd recommend I talk to?'"),
        para("The close:"),
        bullet("'Is there anything I could send you — resume, portfolio — where you could give me feedback?'"),
    ]),
    callout("Always ask the 'anyone else' question. Five conversations can turn into fifteen through introductions.", "💡"),
    toggle("✅ Thank you message (send within 24 hours)", [
        quote("\"Thanks so much for your time today — the advice on [specific thing] was really helpful. I'll keep you posted on how the search goes.\""),
    ]),
    divider(),
    h2("Cold outreach on LinkedIn"),
    para("Hooks that get responses:"),
    bullet("You read something they wrote (post, article)"),
    bullet("You're applying to their company and want to learn more first"),
    bullet("You share a specific background (same city, same major, similar path)"),
    toggle("✅ Cold outreach template", [
        quote("\"Hi [Name], I've been following your posts on [topic] and found your take on [specific thing] really useful. I'm a recent grad exploring roles in [area] and your path from [X to Y] caught my attention. Would you be open to a 20-minute call? Happy to work around your schedule.\""),
    ]),
    toggle("❌ What kills cold outreach", [
        bullet("Generic openers: 'I am very passionate about your company'"),
        bullet("Attaching your resume in the first message"),
        bullet("Asking for a referral before having a conversation"),
        bullet("Copy-pasting the same message to everyone — people can tell"),
    ]),
    divider(),
    h2("All outreach templates"),
    toggle("Alumni outreach", [quote("\"Hi [Name], I'm a recent [University] grad in [field] and came across your profile. I'm exploring roles in [area] and noticed you've been at [Company] for a couple of years — I'd love to hear how you got there and what the work is actually like. Would you have 20 minutes for a quick call sometime this week or next?\"")]),
    toggle("Cold outreach — general", [quote("\"Hi [Name], I've been following your posts on [topic] and found your take on [specific thing] really useful. I'm a recent grad exploring roles in [area] and your path from [X to Y] caught my attention. Would you be open to a 20-minute call? Happy to work around your schedule.\"")]),
    toggle("Outreach before applying", [quote("\"Hi [Name], I came across the [Role] posting at [Company] and it lines up closely with my background in [X]. Before applying I wanted to get a sense of the team from someone inside. Would you have 15–20 minutes to chat? No pressure at all.\"")]),
    toggle("Referral ask (after a conversation)", [quote("\"Thanks again for the chat last week — it was really helpful. I'm planning to apply for the [Role] at [Company]. Would you be comfortable putting in a referral, or is there someone you'd suggest I reach out to?\"")]),
    toggle("Hiring manager outreach", [quote("\"Hi [Name], I came across the [Role] posting at [Company] and it lines up closely with my background in [X]. I'd love to learn more about what you're looking for — would you be open to a quick 15-minute call?\"")]),
    toggle("Follow-up if no response (once, after 1 week)", [quote("\"Hi [Name], just following up on my message from last week — happy to work around your schedule if timing was the issue. Either way, appreciate your time.\"")]),
])

# 6. INTERVIEW PREP
pages["interview_prep"] = ("Interview Prep", "🎤", [
    h1("Interview Prep"),
    callout("Knowing the structure removes the anxiety of not knowing what's coming. Most companies run the same 4–5 step process.", "💡"),
    divider(),
    h2("How hiring interviews actually work"),
    table([
        ["Round", "What it is", "What they're checking"],
        ["Recruiter screen", "15–20 min phone call", "Fit, basics, salary expectations"],
        ["Hiring manager screen", "30 min", "Your background and genuine interest"],
        ["Technical / case round", "45–60 min", "Role-specific skills (see tracks below)"],
        ["Final round / onsite", "3–5 back-to-back interviews", "Deep fit + technical"],
        ["Offer", "—", "—"],
    ]),
    divider(),
    h2("The recruiter screen"),
    para("They're checking three things:"),
    bullet("Can you talk about yourself clearly?"),
    bullet("Do your background and expectations match the role?"),
    bullet("Are you a reasonable human being?"),
    toggle("'Tell me about yourself' — 90-second answer", [
        para("Structure: Present → Past → Future"),
        quote("\"I'm a recent Data Analytics grad from [University] where I focused on SQL and Python for business problems. During my internship at [Company] I built dashboards the sales team used daily. I'm now looking for an analyst role where I can work on real business problems with data — which is why this role caught my attention.\""),
    ]),
    toggle("'What are your salary expectations?'", [
        para("Never give a number first if you can avoid it."),
        quote("\"I'm still learning about the full scope of the role. What's the budgeted range for this position?\""),
        para("If they push: give a range based on Levels.fyi (tech) or Glassdoor/WSO (finance). Anchor slightly high."),
    ]),
    divider(),
    h2("Behavioral interviews — every role, every company"),
    h3("The STAR method"),
    table([
        ["Letter", "What it means", "Tips"],
        ["S — Situation", "Set the context briefly", "1–2 sentences max"],
        ["T — Task", "What were you responsible for", "Be specific about your role"],
        ["A — Action", "What YOU specifically did", "Not 'we' — what did you do"],
        ["R — Result", "What happened", "Quantify if possible"],
    ]),
    h3("Common questions"),
    table([
        ["Question", "What they want to see"],
        ["Tell me about a time you faced a challenge", "Resilience, problem-solving"],
        ["Tell me about a time you worked with a difficult person", "Maturity, communication"],
        ["Tell me about a project you're proud of", "Ownership, impact"],
        ["Tell me about a time you failed", "Self-awareness, learning"],
        ["Tell me about a time you led something", "Initiative, leadership"],
    ]),
    callout("Prepare 5–6 strong stories from your experience. Internships, class projects, part-time jobs, student orgs all count. One strong story beats ten weak ones.", "💡"),
    divider(),
    h2("Technical prep — by track"),
    toggle("💻 Tech (SWE, Data Engineering, Data Science)", [
        para("LeetCode-style coding problems, 1–2 per round, 45 minutes, talking through your thinking."),
        table([
            ["Priority", "Topics"],
            ["Must know", "Arrays, strings, hashmaps, two pointers, sliding window"],
            ["Should know", "Trees, graphs, BFS/DFS, recursion"],
            ["Good to have", "Dynamic programming, heaps, tries"],
        ]),
        para("Resources:"),
        table([
            ["Resource", "What it's for"],
            ["Neetcode.io", "Structured roadmap, video explanations — best starting point"],
            ["LeetCode", "Do Neetcode 150, not random problems"],
            ["interviewing.io", "Mock interviews with real engineers"],
        ]),
    ]),
    toggle("📊 Data Analytics", [
        para("Expect SQL + take-home case + behavioral."),
        para("SQL — know cold: JOINs, GROUP BY, HAVING, window functions, CTEs, CASE WHEN, date functions"),
        para("Practice: DataLemur, StrataScratch (real questions from Meta, Amazon, Google)"),
        para("Statistics to know: A/B testing, p-value in plain English, statistical vs practical significance, correlation vs causation"),
        para("Take-home case structure:"),
        numbered("What question are you answering?"),
        numbered("What did you find? (key insight first, not methodology first)"),
        numbered("What does it mean for the business?"),
        numbered("What would you recommend?"),
        numbered("What are the limitations?"),
    ]),
    toggle("💰 Finance & Consulting", [
        para("Finance — technical questions to know cold:"),
        table([
            ["Question", "Key points"],
            ["Walk me through a DCF", "Future free cash flows → discount at WACC → terminal value"],
            ["Three financial statements", "Net income flows to retained earnings + starts cash flow statement"],
            ["Depreciation increases $10", "Net income -$7, cash from ops +$3, PP&E -$10, balanced"],
            ["What is EBITDA?", "Earnings before interest, taxes, depreciation, amortization"],
            ["Enterprise vs equity value", "EV = equity + debt - cash"],
        ]),
        para("Resources: Mergers & Inquisitions (free), Wall Street Prep, Breaking Into Wall Street"),
        para("Consulting — case interviews:"),
        numbered("Clarify — ask 1–2 questions before structuring"),
        numbered("Structure — lay out your framework out loud"),
        numbered("Analyze — work through each area, prioritize what matters most"),
        numbered("Synthesize — 'My recommendation is...'"),
        para("Practice: Case in Point (book), IGotAnOffer, firm-published cases (McKinsey, BCG, Bain)"),
        callout("Non-negotiable: practice cases out loud with a partner. Solo reading is not enough.", "⚠️"),
    ]),
    divider(),
    h2("Questions to ask the interviewer"),
    toggle("Good questions to ask", [
        bullet("'What does success look like in this role in the first 90 days?'"),
        bullet("'What's the biggest challenge the team is working through right now?'"),
        bullet("'What do you like most about working here?'"),
        bullet("'What are the growth paths from this role?'"),
    ]),
    callout("Always prepare 2–3 questions. 'I don't have any questions' is a red flag.", "⚠️"),
    divider(),
    h2("After the interview"),
    callout("Same day: Send a thank you email. Two sentences.\n\n\"Thanks for taking the time today — I really enjoyed learning about [specific thing]. It's made me even more excited about the role.\"\n\nOne follow-up if you don't hear back. Not three.", "💡"),
])

# 7. OFFER & NEGOTIATION
pages["offer_negotiation"] = ("Offer & Negotiation", "💰", [
    h1("Offer & Negotiation"),
    callout("The most common mistake: accepting on the spot. Companies expect negotiation. Recruiters are not offended by it. The offer is not withdrawn because you asked.", "⚠️"),
    divider(),
    h2("When you get the call"),
    para("You do not need to respond immediately. Ever."),
    quote("\"Thank you so much — I'm really excited about this. Can I have a few days to review everything carefully?\""),
    para("Standard ask is 3–5 business days. If they pressure you for same-day, that's a signal about the company culture."),
    divider(),
    h2("Research market rate first"),
    para("Never negotiate without data. Feelings don't move offers. Numbers do."),
    table([
        ["Source", "Best for"],
        ["Levels.fyi", "Tech roles — most accurate, self-reported"],
        ["Glassdoor", "Broad — directionally useful"],
        ["Wall Street Oasis", "Finance and consulting compensation"],
        ["LinkedIn Salary", "General roles, business tracks"],
        ["Blind", "Tech — anonymous, candid real numbers"],
        ["Payscale", "Entry-level benchmarking"],
    ]),
    divider(),
    h2("What's actually negotiable"),
    table([
        ["What", "Negotiable?"],
        ["Base salary", "Always"],
        ["Signing bonus", "Always (often easier to move than base)"],
        ["Start date", "Always"],
        ["Annual bonus target", "Sometimes"],
        ["Equity / RSUs", "Sometimes (especially at startups)"],
        ["Remote/hybrid", "Sometimes"],
        ["Title", "More than people think"],
        ["Benefits structure, insurance, 401k match", "Rarely at big companies"],
    ]),
    callout("At big companies, base salary has bands — they can move within the band. Signing bonus is often where they have the most flexibility.", "💡"),
    divider(),
    h2("How to counter"),
    toggle("For base salary", [
        quote("\"I'm really excited about this role and [Company]. Based on my research on Levels.fyi and conversations with people in similar roles, I was expecting something closer to [X]. Is there flexibility to get there?\""),
        para("Then stop talking. Let them fill the silence."),
    ]),
    toggle("If base won't move — ask about signing bonus", [
        quote("\"I understand if the base is fixed within the band. Would there be flexibility on a signing bonus to bridge the gap?\""),
    ]),
    toggle("If you have a competing offer", [
        quote("\"I want to be transparent — I have another offer at [X]. [Company] is my first choice, but I want to make sure I'm making the right decision. Is there any room to get closer to that number?\""),
        callout("A competing offer is the strongest leverage you have. Use it if it's real. Never fabricate one.", "⚠️"),
    ]),
    divider(),
    h2("Evaluating the full offer"),
    toggle("Compensation", [
        bullet("Base salary"),
        bullet("Signing bonus (one-time)"),
        bullet("Annual bonus — target % and how often it actually pays out"),
        bullet("Equity / RSUs — total grant, vesting schedule, cliff"),
    ]),
    toggle("Benefits", [
        bullet("Health insurance — premium and quality"),
        bullet("401k match and vesting schedule"),
        bullet("PTO — unlimited PTO is often less than a fixed number in practice"),
        bullet("Other: parental leave, FSA/HSA, wellness stipend"),
    ]),
    toggle("Career", [
        bullet("Learning and development budget"),
        bullet("Promotion timeline — how long do people typically stay at this level?"),
        bullet("Who you'll be working for directly"),
        bullet("Team size and growth trajectory"),
    ]),
    toggle("Logistics", [
        bullet("Remote / hybrid / in-office"),
        bullet("Start date"),
        bullet("Relocation assistance if needed"),
    ]),
    callout("A $5k higher salary at a company with poor mentorship and no growth path may be worth less than a $5k lower offer where you'll learn faster and get promoted sooner.", "💡"),
    divider(),
    h2("For OPT candidates"),
    callout("Before accepting any offer:\n• Confirm company is enrolled in E-Verify (required for STEM OPT extension)\n• Confirm company has sponsored H1B before and will for your role\n• Understand your start date relative to the H1B filing timeline\n\nGet these answers before you sign. Not after.", "⚠️"),
    divider(),
    h2("After you accept"),
    bullet("Get the offer letter in writing before giving notice anywhere"),
    bullet("Confirm start date in writing"),
    bullet("Do not post on LinkedIn until you've signed — offers are occasionally rescinded"),
])

# 8. BENEFITS
pages["benefits"] = ("Benefits", "🏥", [
    h1("Benefits — What They Are and What Actually Matters"),
    callout("Benefits can add $10,000–$30,000+ of real value to a compensation package. Most new grads look at base salary and ignore everything else. That's a mistake.", "💡"),
    divider(),
    h2("Health Insurance (Medical)"),
    para("In the US, health insurance is employer-sponsored. Your employer pays part of the premium — you pay the rest from each paycheck."),
    h3("Key terms"),
    table([
        ["Term", "What it means"],
        ["Premium", "What you pay per paycheck for coverage"],
        ["Deductible", "What you pay out-of-pocket before insurance kicks in (e.g. $1,500/year)"],
        ["Copay", "Fixed fee per visit (e.g. $20 per doctor visit)"],
        ["Coinsurance", "Your share after the deductible (e.g. 80/20 = insurance pays 80%, you pay 20%)"],
        ["Out-of-pocket maximum", "The most you'll pay in a year — after this, insurance covers 100%"],
        ["In-network", "Doctors with agreements with your insurer — always cheaper"],
    ]),
    h3("Plan types"),
    table([
        ["Plan", "What it means", "Good for"],
        ["PPO", "See any doctor, no referral, higher premium", "Flexibility, ongoing care"],
        ["HMO", "In-network only, referral needed for specialists, lower premium", "Healthy, want lower cost"],
        ["HDHP", "High deductible, low premium — pairs with HSA", "Healthy, young, want to save pre-tax"],
    ]),
    callout("For most healthy new grads: HDHP + HSA is usually the best financial choice.", "💡"),
    toggle("HSA (Health Savings Account) — what makes it powerful", [
        bullet("Contribute pre-tax dollars"),
        bullet("Money grows tax-free"),
        bullet("Withdraw tax-free for medical expenses"),
        bullet("Rolls over every year — it's yours forever, even if you leave"),
        bullet("Triple tax advantage: the best savings vehicle available to you"),
        para("Think of it as a second retirement account."),
    ]),
    toggle("FSA (Flexible Spending Account)", [
        bullet("Pre-tax dollars for medical expenses"),
        bullet("Use it or lose it each year — unlike HSA"),
        bullet("Good for predictable expenses (glasses, prescriptions, planned procedures)"),
    ]),
    divider(),
    h2("Dental"),
    para("Usually $10–20/month employee premium. Separate from medical."),
    table([
        ["Care type", "Typical coverage"],
        ["Preventive (cleanings, X-rays)", "100% covered"],
        ["Basic (fillings, extractions)", "70–80% covered"],
        ["Major (crowns, root canals)", "50% covered"],
        ["Orthodontics (braces, Invisalign)", "Separate lifetime max (~$1,500–$2,000)"],
    ]),
    divider(),
    h2("Vision"),
    para("Usually $5–10/month. Covers annual eye exam + allowance for glasses or contacts ($150–$300/year). If you wear glasses or contacts, this pays for itself immediately."),
    divider(),
    h2("Life Insurance"),
    para("Employer typically provides 1–2x your annual salary free. Additional coverage available through payroll deductions."),
    callout("If you're single with no dependents, the free employer coverage is enough. Life insurance matters more when others depend on your income.", "💡"),
    divider(),
    h2("401k — Retirement"),
    callout("The employer match is free money. Always contribute at least enough to get the full match.\n\nExample: $80,000 salary, employer matches 100% up to 4%\n→ You contribute $3,200 → employer adds $3,200 free\n→ That's an instant 100% return on your contribution", "💡"),
    toggle("Vesting schedule — the catch", [
        para("The employer match often vests over time. You only 'own' it after staying a certain amount of time."),
        table([
            ["Type", "What it means"],
            ["Cliff vesting", "100% vested after X years — get nothing if you leave before"],
            ["Graded vesting", "% per year — keep what's vested if you leave early"],
            ["Immediate", "You own the match right away — best case"],
        ]),
    ]),
    toggle("Traditional vs Roth 401k", [
        table([
            ["Type", "How it works", "Good for"],
            ["Traditional", "Pre-tax now, pay taxes at withdrawal", "Lower tax bracket in retirement"],
            ["Roth", "Post-tax now, tax-free at withdrawal", "New grads — you're likely in a lower bracket now than later"],
        ]),
    ]),
    divider(),
    h2("Equity"),
    toggle("RSUs (Restricted Stock Units) — most common at public companies", [
        para("Company grants you shares that vest over time. When they vest, you own them and can sell."),
        para("Typical schedule: 4-year vest, 1-year cliff — nothing vests until month 12, then 25% at end of year 1, remaining 75% over years 2–4."),
        para("Tax: RSUs are taxed as ordinary income when they vest. Company withholds shares automatically."),
        callout("Key question: Is this a public company (can sell immediately) or private (illiquid until IPO/acquisition)?", "💡"),
    ]),
    toggle("Stock Options — more common at startups", [
        para("Right to buy company shares at a fixed strike price. Value only if the company grows above that price."),
        table([
            ["Type", "Tax treatment"],
            ["ISO (Incentive Stock Options)", "Better tax treatment, for employees"],
            ["NSO (Non-qualified Stock Options)", "Less favorable tax treatment"],
        ]),
        callout("For new grads at startups: treat options as a lottery ticket, not a salary component. They can be life-changing or worthless.", "⚠️"),
    ]),
    toggle("ESPP (Employee Stock Purchase Plan) — public companies only", [
        para("Buy company stock at a discount (usually 10–15%) through payroll deductions."),
        callout("ESPP is almost always worth participating in — even a straight 15% discount is a guaranteed return if you sell immediately. Many plans also have a lookback provision that can significantly increase the effective discount.", "💡"),
    ]),
    divider(),
    h2("Other benefits worth evaluating"),
    table([
        ["Benefit", "What to know"],
        ["PTO", "Fixed PTO is often better than unlimited in practice — ask what people actually take"],
        ["Commuter benefits", "Pre-tax transit/parking — saves 20–30% on commute costs"],
        ["Remote work stipend", "One-time home office setup ($500–$2,000) + monthly internet stipend"],
        ["L&D budget", "$1,000–$5,000/year for courses, conferences, certifications"],
        ["Wellness / gym stipend", "$50–$100/month toward gym or fitness apps"],
        ["Parental leave", "Federal minimum is 12 weeks unpaid — companies vary from 0 to 4+ months paid"],
    ]),
    divider(),
    h2("Questions to ask before accepting"),
    toggle("Health insurance", [
        para("☐ What's the monthly premium for individual coverage?"),
        para("☐ What plan types are available (PPO, HMO, HDHP)?"),
        para("☐ Does the company contribute to the HSA?"),
    ]),
    toggle("401k", [
        para("☐ What's the employer match and up to what % of salary?"),
        para("☐ What's the vesting schedule on the match?"),
        para("☐ Is Roth 401k available?"),
    ]),
    toggle("Equity", [
        para("☐ What's the total RSU / option grant?"),
        para("☐ What's the vesting schedule and cliff?"),
        para("☐ For options: what's the strike price and current 409A valuation?"),
        para("☐ Is ESPP available? What's the discount and lookback?"),
    ]),
])

# 9. VISA / OPT
pages["visa_opt"] = ("Visa / OPT Track", "🛂", [
    h1("Visa / OPT Track"),
    callout("Read this before you start applying. If you're on F-1 OPT, your job search has hard constraints that don't apply to other candidates. Ignoring them doesn't make them go away.", "⚠️"),
    divider(),
    h2("The OPT timeline — what you can't miss"),
    table([
        ["When", "What to do"],
        ["60 days before graduation", "Apply for OPT through your DSO. USCIS processing takes 3–5 months — apply early."],
        ["Graduation", "OPT start date can be up to 60 days after graduation. Choose your start date strategically."],
        ["OPT active", "12 months to work. 90-day unemployment limit — days without a job count against you."],
        ["Before OPT expires", "Employer files H1B (April lottery, starts October). STEM extension buys more time if not selected."],
    ]),
    callout("The most common mistake: waiting until graduation to start the job search. By then you may have already burned 60 days of your unemployment clock. Start before you graduate.", "⚠️"),
    divider(),
    h2("STEM OPT extension"),
    para("If your degree is in a STEM field, you're eligible for a 24-month extension — giving you 36 months total."),
    para("Requirements:"),
    bullet("Degree must be on the STEM designated degree program list (check uscis.gov)"),
    bullet("Employer must be enrolled in E-Verify"),
    bullet("Must apply before your initial OPT expires"),
    callout("STEM OPT gives you two more H1B lottery cycles. That dramatically improves your odds over time. Confirm whether your degree qualifies — your DSO can tell you.", "💡"),
    divider(),
    h2("The 90-day unemployment rule"),
    para("During OPT you can only be unemployed for 90 days total (150 days with STEM extension). Days accumulate whether you're tracking them or not."),
    toggle("What counts as employment", [
        bullet("✅ Full-time job"),
        bullet("✅ Part-time job (must be related to your degree)"),
        bullet("✅ Contract / freelance work (if structured correctly — talk to your DSO)"),
        bullet("❌ Volunteer work"),
        bullet("❌ Unpaid internships"),
        bullet("❌ Job searching"),
    ]),
    callout("Track your days. Your DSO tracks them too. If you're approaching 60 days unemployed, escalate your urgency.", "⚠️"),
    divider(),
    h2("Finding companies that actually sponsor"),
    callout("'We consider all candidates' often means 'we don't sponsor.' The only thing that matters is whether a company has actually filed H1B petitions before — and you can look this up.", "💡"),
    para("How to vet a company:"),
    numbered("Go to H1Bdata.info"),
    numbered("Search the company name"),
    numbered("Look at: petitions filed (last 3 years), approval rate, job titles sponsored, salary ranges"),
    table([
        ["Signal", "What it means"],
        ["100+ petitions, 90%+ approval rate", "Established sponsor, real process"],
        ["10–50 petitions, good approval rate", "Sponsors selectively — ask about process early"],
        ["1–5 petitions total", "Case-by-case — high risk"],
        ["Zero petitions", "Almost certainly won't sponsor despite what they say"],
    ]),
    toggle("General patterns (not guarantees — always verify)", [
        bullet("✅ Typically sponsor: Large tech (FAANG, Microsoft), Big 4 consulting, major banks, large healthcare/pharma"),
        bullet("⚠️ Varies: Startups, mid-size tech, consulting boutiques"),
        bullet("❌ Rarely/never: Government contractors, small businesses, most retail/hospitality"),
    ]),
    divider(),
    h2("When to bring up visa status"),
    para("Bring it up before the final round — not at the offer stage. Raising it after 4 rounds of interviews wastes everyone's time."),
    para("Best time: the recruiter screen, or right after you pass it."),
    quote("\"I want to be transparent — I'm currently on F-1 OPT and will need H1B sponsorship down the line. I wanted to make sure that's something [Company] is able to support before we go further.\""),
    divider(),
    h2("The H1B lottery"),
    table([
        ["Date", "What happens"],
        ["April 1", "Registration window opens"],
        ["Mid-April", "Lottery results announced"],
        ["April–June", "Selected employers file full petitions"],
        ["October 1", "H1B status begins (new fiscal year)"],
    ]),
    bullet("65,000 regular cap"),
    bullet("20,000 additional for US master's degree holders — two lottery entries if you have a US master's"),
    callout("Lottery odds have been roughly 30–40% in recent years. Even doing everything right, there's a real chance of not being selected the first time. Have a backup plan before April results come out.", "⚠️"),
    divider(),
    h2("OPT job search checklist"),
    toggle("☐ Before graduation", [
        para("☐ OPT application submitted to DSO (60+ days before graduation)"),
        para("☐ Confirmed whether your degree is STEM-designated"),
        para("☐ Job search actively started"),
    ]),
    toggle("☐ Once OPT begins", [
        para("☐ Tracking unemployment days"),
        para("☐ Every company checked on H1Bdata.info before applying"),
        para("☐ Visa status raised in recruiter screen, not at offer stage"),
    ]),
    toggle("☐ At offer stage", [
        para("☐ Confirmed company is E-Verify enrolled"),
        para("☐ Sponsorship commitment discussed with HR"),
        para("☐ Understand start date relative to H1B filing timeline"),
    ]),
    toggle("☐ H1B cycle", [
        para("☐ Employer registers by April 1"),
        para("☐ Know lottery result before making other plans"),
        para("☐ Have a backup plan if not selected"),
    ]),
    divider(),
    h2("Resources"),
    table([
        ["Resource", "What it's for"],
        ["H1Bdata.info", "Search H1B filing history by company"],
        ["myvisajobs.com", "Job board filtered by H1B sponsoring employers"],
        ["USCIS.gov", "Primary source — always current"],
        ["Murthy Law Firm (murthy.com)", "Best free guides on F-1, OPT, H1B mechanics"],
        ["trackitt.com", "H1B processing times, community-reported"],
    ]),
    h3("Communities"),
    table([
        ["Community", "Where"],
        ["r/f1visa", "Reddit — F-1 and OPT questions"],
        ["r/OPTjobs", "Reddit — job search on OPT specifically"],
        ["r/h1b", "Reddit — lottery, RFE experiences"],
        ["Immihelp forums", "immihelp.com"],
    ]),
])

# 10. PEOPLE TO FOLLOW
pages["people_to_follow"] = ("People to Follow", "👥", [
    h1("People to Follow"),
    callout("Follow 5–10 people max, not 50. More follows = more noise. Pick one person per category that resonates with how you think and go deep. The goal is a system, not a feed.", "💡"),
    divider(),
    h2("Job Search & Career (general)"),
    table([
        ["Person", "Platform", "Why follow"],
        ["Laszlo Bock", "LinkedIn", "Former SVP People Ops at Google. Seen millions of resumes from the other side. Posts on what companies actually look for."],
        ["Austin Belcak", "LinkedIn", "Practical tactics — networking scripts, resume strategy, cold outreach. More actionable than most."],
        ["Jenny Foss", "LinkedIn", "Resume and career strategy for early career and career changers. Clear, no-nonsense."],
    ]),
    divider(),
    h2("Tech Track"),
    table([
        ["Person", "Platform", "Why follow"],
        ["Rahul Pandey", "YouTube + LinkedIn", "Ex-Facebook/Pinterest, co-founder of Taro. Honest about how big tech hiring actually works."],
        ["Neetcode", "YouTube", "Best free LeetCode prep resource. Structured roadmap, clear explanations."],
        ["Gergely Orosz", "Substack (The Pragmatic Engineer)", "Most credible voice on tech industry careers, compensation, and hiring trends."],
        ["Kevin Naughton Jr.", "YouTube", "SWE job search, resume, and interview prep specifically for new grads."],
    ]),
    divider(),
    h2("Data / Analytics Track"),
    table([
        ["Person", "Platform", "Why follow"],
        ["Ken Jee", "YouTube + LinkedIn", "Data science career, portfolio projects, breaking into the field as a new grad."],
        ["Luke Barousse", "YouTube", "Data analyst careers, SQL, Python, job search for analytics specifically."],
        ["Alex Freberg (Alex The Analyst)", "YouTube", "SQL, Python, Tableau — skills and career path for data analysts."],
        ["Seattle Data Guy", "YouTube", "Data engineering career path, tools, and what interviews actually look like."],
    ]),
    divider(),
    h2("Finance / Business Track"),
    table([
        ["Person", "Platform", "Why follow"],
        ["Patrick Curtis", "LinkedIn + Wall Street Oasis", "Founded WSO, former IB analyst. Most practical voice on breaking into finance as a new grad."],
        ["10x EBITDA", "YouTube + LinkedIn", "IB and PE interview prep. Best free resource for finance technical questions."],
        ["Mergers & Inquisitions", "Website + newsletter", "Most comprehensive free resource for finance recruiting. Bookmark it."],
        ["Marc Cenedella", "LinkedIn", "Founder of Ladders. Job search strategy from the employer's perspective."],
    ]),
    divider(),
    h2("Visa / OPT Specific"),
    table([
        ["Person", "Platform", "Why follow"],
        ["Stacy Monahan Tucker", "LinkedIn", "Immigration attorney. Plain-English H1B and OPT content. Addresses real scenarios."],
        ["Sophie Alcorn", "LinkedIn + newsletter (Dear Sophie)", "Weekly Q&A on visa scenarios. Good for edge cases."],
    ]),
    divider(),
    h2("Subreddits worth bookmarking"),
    table([
        ["Track", "Subreddit", "Best for"],
        ["Tech", "r/cscareerquestions", "Job search, resume feedback, interview experiences"],
        ["Tech", "r/datascience", "Data science career"],
        ["Tech", "r/dataengineering", "Data engineering career"],
        ["Finance", "r/FinancialCareers", "Finance job search broadly"],
        ["Finance", "r/ibanking", "IB specifically"],
        ["Finance", "r/consulting", "Consulting recruiting and career"],
        ["Visa/OPT", "r/f1visa", "F-1 and OPT questions"],
        ["Visa/OPT", "r/OPTjobs", "Job search on OPT specifically"],
        ["Visa/OPT", "r/h1b", "H1B lottery and processing"],
    ]),
    divider(),
    h2("Newsletters worth subscribing to"),
    table([
        ["Newsletter", "Track", "Why"],
        ["The Pragmatic Engineer", "Tech", "Best coverage of tech hiring and compensation"],
        ["Levels.fyi newsletter", "Tech", "Salary data, hiring trends, layoff tracker"],
        ["WSO Daily", "Finance", "Finance news + recruiting updates"],
        ["Mergers & Inquisitions", "Finance/IB", "Recruiting timelines, interview guides"],
        ["Dear Sophie", "Visa/OPT", "Weekly immigration Q&A in plain English"],
    ]),
])

# ── CREATE ALL PAGES ──────────────────────────────────────────────────────────

print("Creating pages in Notion...\n")
for key, (title, emoji, blocks) in pages.items():
    print(f"  Creating: {emoji} {title}...", end=" ")
    result = create_page(PARENT_ID, title, emoji, blocks)
    if result:
        print(f"✓ Done")
    else:
        print(f"✗ Failed")

print("\nAll done!")
