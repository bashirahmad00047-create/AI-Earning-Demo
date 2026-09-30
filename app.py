"""
AI Business Solutions - Flask Web Application
A modern, mobile-responsive freelance portfolio website demonstrating
Websites, AI Automation, Chatbots, and Digital Solutions for small businesses.
"""

import os
import json
import re
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ai-business-solutions-demo-key-2026')

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

# ---------------------------------------------------------
# PORTFOLIO DATA
# ---------------------------------------------------------
PORTFOLIO_PROJECTS = {
    "restaurant-website": {
        "id": "restaurant-website",
        "title": "Bella Cucina Bistro",
        "category": "Business Website Development",
        "tagline": "Modern High-Converting Restaurant Portal with Online Reservations",
        "description": "A high-performance, mobile-first website created for an upscale artisanal restaurant. Includes an interactive visual menu with dietary filtering, seamless table reservation request system, and local SEO optimization resulting in a 65% increase in online reservations.",
        "client": "Bella Cucina Group",
        "metrics": [
            {"label": "Mobile Speed Score", "value": "99/100"},
            {"label": "Online Bookings", "value": "+65%"},
            {"label": "Bounce Rate Reduction", "value": "42%"}
        ],
        "tags": ["HTML5/CSS3", "JavaScript", "Flask", "Responsive UI", "Local SEO"],
        "features": [
            "Interactive digital menu with category filtering (Appetizers, Mains, Desserts, Vegan)",
            "Automated table booking request system with instant email confirmation",
            "Google Maps & business hours integration with active status indicator",
            "Optimized for 100% smooth browsing on smartphones and tablets"
        ],
        "badge": "Live Demo Case Study",
        "color": "from-amber-500 to-rose-500"
    },
    "automation-dashboard": {
        "id": "automation-dashboard",
        "title": "Apex Flow Operations",
        "category": "Python Automation",
        "tagline": "Automated Multi-Source Invoice & Sales Operations Dashboard",
        "description": "An end-to-end Python automation pipeline connecting Stripe, Excel, and Gmail. Automatically extracts invoice data, reconciles discrepancies, generates weekly PDF executive reports, and sends real-time Slack notifications—saving over 18 hours of manual labor per week.",
        "client": "Apex Logistics & Retail",
        "metrics": [
            {"label": "Hours Saved Weekly", "value": "18.5 hrs"},
            {"label": "Reporting Accuracy", "value": "100%"},
            {"label": "ROI Realization", "value": "< 3 Weeks"}
        ],
        "tags": ["Python", "Pandas", "Automation", "Flask", "ReportLab", "API Integration"],
        "features": [
            "Automated PDF & CSV invoice parsing with smart field mapping",
            "Real-time sync to central operational dashboard with live charts",
            "Automated weekly email summary to stakeholders with attached PDF report",
            "Zero manual data entry errors across 1,200+ monthly transactions"
        ],
        "badge": "Efficiency Champion",
        "color": "from-cyan-500 to-blue-600"
    },
    "docuquery-ai": {
        "id": "docuquery-ai",
        "title": "DocuQuery AI Assistant",
        "category": "PDF & Document Q&A",
        "tagline": "Intelligent Semantic Search & Policy Assistant for Business Documents",
        "description": "A lightweight, secure document intelligence tool enabling small business staff to upload dense PDF contracts, HR policies, and compliance manuals and get instant, cited answers in plain English without sharing confidential data with public models.",
        "client": "Summit Legal & Advisory",
        "metrics": [
            {"label": "Search Time Saved", "value": "85%"},
            {"label": "Document Ingestion", "value": "< 5 Sec"},
            {"label": "Staff Adoption Rate", "value": "94%"}
        ],
        "tags": ["Python", "NLP / Vector Search", "Flask", "Document AI", "Knowledge Base"],
        "features": [
            "Instant query response with direct citation of source page and paragraph",
            "Pre-indexed knowledge base for policies, FAQs, and product spec sheets",
            "100% private data isolation suitable for sensitive client documentation",
            "Clean web interface accessible from desktop and mobile browsers"
        ],
        "badge": "AI Powered",
        "color": "from-purple-500 to-indigo-600"
    }
}

# ---------------------------------------------------------
# SERVICES DATA
# ---------------------------------------------------------
SERVICES_DATA = [
    {
        "id": "website-dev",
        "title": "Business Website Development",
        "icon": "globe",
        "short_desc": "Ultra-fast, mobile-responsive custom websites engineered to convert visitors into paying clients.",
        "benefits": [
            "Mobile-first responsive layout (looks stunning on all phones & tablets)",
            "Clean modern design tailored to your industry",
            "SEO structure & lightning-fast page loading speeds",
            "Integrated contact forms, WhatsApp links, and call buttons"
        ],
        "tech": "HTML5 • Modern CSS3 • JavaScript • Flask / Python",
        "deliverable": "Turnkey website ready in 3 to 7 days"
    },
    {
        "id": "python-automation",
        "title": "Python Automation",
        "icon": "cpu",
        "short_desc": "Eliminate repetitive tasks, web scraping, and spreadsheet headaches with custom Python scripts.",
        "benefits": [
            "Automated data extraction from websites, portals, and PDFs",
            "Excel / CSV cleaning, transformation, and automated reporting",
            "Email & Slack auto-notifications triggered by business events",
            "Scheduled background jobs that run 24/7 without intervention"
        ],
        "tech": "Python • Pandas • Requests • Beautiful Soup • Cron / Task Scheduler",
        "deliverable": "Working automated script + documentation & walkthrough"
    },
    {
        "id": "ai-chatbot",
        "title": "AI Chatbot Integration",
        "icon": "message-square",
        "short_desc": "Deploy intelligent 24/7 conversational agents that qualify leads, answer FAQs, and book calls.",
        "benefits": [
            "Instant 24/7 response to customer inquiries without wait times",
            "Trained on your business FAQs, services, and pricing policies",
            "Lead capture forms directly inside the conversational flow",
            "Works without expensive subscriptions or complex setups"
        ],
        "tech": "NLP • Flask API • JavaScript Web Widget • Local / API Models",
        "deliverable": "Custom embedded chatbot ready for your site"
    },
    {
        "id": "doc-qa",
        "title": "PDF & Document Q&A Systems",
        "icon": "file-text",
        "short_desc": "Empower your team to query hundreds of PDF contracts, manuals, and documents in seconds.",
        "benefits": [
            "Search through complex policies, SOPs, and product specifications instantly",
            "Provides accurate answers with exact page and section citations",
            "Preserves business privacy with secure local or private storage",
            "Eliminates hours spent manually flipping through dense documentation"
        ],
        "tech": "Python • PyPDF / PDFPlumber • Vector Embeddings • Semantic Search",
        "deliverable": "Private web dashboard for your team"
    },
    {
        "id": "ai-content",
        "title": "AI Content Solutions",
        "icon": "sparkles",
        "short_desc": "Scale your brand with customized AI workflows for SEO articles, social posts, and product copy.",
        "benefits": [
            "Automated generation of high-quality, SEO-optimized blog posts",
            "Social media copy and newsletter sequences customized to your brand voice",
            "Batch product description generation for e-commerce stores",
            "Built-in human editing guidelines and anti-hallucination checks"
        ],
        "tech": "Prompt Engineering • Python Content Pipelines • Markdown / CMS Sync",
        "deliverable": "Automated content generation pipeline & prompt templates"
    }
]

# ---------------------------------------------------------
# LOCAL AI ASSISTANT KNOWLEDGE BASE
# ---------------------------------------------------------
FAQ_KNOWLEDGE_BASE = [
    {
        "keywords": ["service", "services", "offer", "what do you do", "help me with", "solutions"],
        "reply": "At **AI Business Solutions**, we specialize in five core digital services for small and growing businesses:\n\n1. **Business Website Development** – Mobile-responsive, high-converting websites.\n2. **Python Automation** – Custom scripts to eliminate manual data entry & repetitive work.\n3. **AI Chatbot Integration** – 24/7 smart customer service & lead capture bots.\n4. **PDF/Document Q&A Systems** – Instant semantic search over contracts and SOPs.\n5. **AI Content Solutions** – Automated marketing, social, and SEO content pipelines.\n\nWhich of these would you like to explore for your business?",
        "suggestions": ["Tell me about Website Development", "How does Python Automation work?", "Show me chatbot pricing", "Contact the team"],
        "action": {"text": "View Our Services", "target": "#services"}
    },
    {
        "keywords": ["website", "web design", "web development", "landing page", "redesign", "mobile"],
        "reply": "Our **Business Website Development** service delivers clean, modern, and mobile-responsive websites built to convert visitors into clients.\n\n• **Turnaround:** Usually 3 to 7 days.\n• **Tech Stack:** Modern HTML5, CSS3, JavaScript, Python/Flask.\n• **Included:** Fast loading, responsive layout for all screen sizes, SEO basics, contact forms, and easy local setup.\n\nWould you like a quote for your business website?",
        "suggestions": ["See Restaurant Website Demo", "How much does it cost?", "Request a Quote"],
        "action": {"text": "Get a Free Website Quote", "target": "#contact"}
    },
    {
        "keywords": ["python", "automation", "automate", "script", "scraping", "excel", "csv", "repetitive", "workflow"],
        "reply": "Our **Python Automation** service automates time-consuming business tasks so you can focus on growth!\n\n**Common Automations We Build:**\n• Automated invoice & receipt data extraction\n• Web scraping for market prices, competitors, and leads\n• Excel / CSV cleaning, calculations, and auto-generated PDF reports\n• Automatic email and Slack alerts on critical events\n\nMost clients save **10 to 20 hours every single week**.",
        "suggestions": ["See Automation Dashboard Demo", "Can you scrape data from websites?", "Request an Automation Audit"],
        "action": {"text": "Explore Automation Demos", "target": "#portfolio"}
    },
    {
        "keywords": ["chatbot", "chat bot", "ai assistant", "customer service", "agent", "support"],
        "reply": "We build and integrate **AI Chatbots** that work around the clock for your business!\n\n• **Instant 24/7 Answers:** Solves customer queries without keeping visitors waiting.\n• **Lead Generation:** Gathers visitor contact info and project requirements.\n• **Flexible Deployment:** Can run on external APIs or lightweight local FAQ models with zero monthly API cost.\n• **Seamless Embed:** Easily integrates into any existing website.\n\nYou are testing a live demonstration right now in this very window!",
        "suggestions": ["How do I install this on my site?", "Does it require an expensive API?", "Talk to a Developer"],
        "action": {"text": "Contact Us for Chatbot Setup", "target": "#contact"}
    },
    {
        "keywords": ["pdf", "document", "q&a", "docuquery", "search", "manual", "contract", "policy"],
        "reply": "Our **PDF/Document Q&A Systems** let you interact with your company documents like a search engine:\n\n• Upload contracts, employee handbooks, or product manuals.\n• Ask questions in plain English and receive direct answers with exact page numbers.\n• Keeps your confidential business files private and secure.\n\nIt saves hours of flipping through multi-page PDF files.",
        "suggestions": ["See DocuQuery Demo", "Can it handle 100+ page files?", "Request a Consultation"],
        "action": {"text": "View DocuQuery Case Study", "target": "#portfolio"}
    },
    {
        "keywords": ["content", "seo", "blog", "writing", "marketing", "social media"],
        "reply": "With our **AI Content Solutions**, we create customized workflows to generate high-quality, on-brand content:\n\n• Automated SEO blog outlines and full articles.\n• Social media caption bundles for LinkedIn, Twitter, and Instagram.\n• E-commerce product descriptions tailored to boost conversions.\n• Human-in-the-loop review guides to ensure accuracy and tone.",
        "suggestions": ["How fast can content be created?", "What services do you offer?", "Get in touch"],
        "action": {"text": "Contact for Content Strategy", "target": "#contact"}
    },
    {
        "keywords": ["price", "cost", "pricing", "rate", "how much", "quote", "budget", "affordable", "fiverr", "upwork"],
        "reply": "We believe in **transparent, affordable pricing** tailored for small businesses and startups:\n\n• **Starter Business Website:** From $150 – $350 (Complete mobile-ready site)\n• **Custom Python Automation:** From $99 – $250 per workflow\n• **AI Chatbot Setup:** From $120 – $300 (Turnkey integration)\n• **Document Q&A Portal:** From $200 – $450\n\nWe provide a **100% free initial consultation** and a fixed-price quote with no surprises.",
        "suggestions": ["Request a Free Quote", "What is the turnaround time?", "See Portfolio Projects"],
        "action": {"text": "Request a Free Quote", "target": "#contact"}
    },
    {
        "keywords": ["turnaround", "how long", "timeline", "time", "duration", "fast"],
        "reply": "We pride ourselves on rapid execution without cutting corners:\n\n• **Simple Business Websites & Landing Pages:** 3 to 5 business days.\n• **Python Automation Scripts:** 2 to 4 business days.\n• **AI Chatbots & Integrations:** 3 to 6 business days.\n\nNeed an urgent rush project? We can often accommodate 48-hour delivery upon request!",
        "suggestions": ["Start a Project Today", "What services do you offer?", "How do we get started?"],
        "action": {"text": "Start Your Project", "target": "#contact"}
    },
    {
        "keywords": ["about", "who are you", "who is", "company", "team", "mission", "small business"],
        "reply": "**AI Business Solutions** is a modern digital agency dedicated to helping small businesses leverage the power of web development, Python automation, and artificial intelligence.\n\nOur mission is to make high-end enterprise technology accessible and affordable for local shops, service providers, and growing entrepreneurs—helping you save time, boost sales, and outpace competitors.",
        "suggestions": ["View Portfolio", "What services do you offer?", "Contact Us"],
        "action": {"text": "Read About Us", "target": "#about"}
    },
    {
        "keywords": ["contact", "hire", "email", "reach", "call", "schedule", "quote", "freelance", "upwork", "fiverr", "message"],
        "reply": "You can easily reach us via the contact form on this page or send an inquiry directly!\n\n• **Response Time:** We reply to all inquiries within 2 to 4 hours.\n• **Deliverables:** Free project scope, architecture suggestion, and fixed-price quote.\n\nFill out the form below and let's bring your project to life!",
        "suggestions": ["Fill out the contact form", "What services do you offer?", "See our demo projects"],
        "action": {"text": "Go to Contact Form", "target": "#contact"}
    },
    {
        "keywords": ["hello", "hi", "hey", "good morning", "good evening", "greetings", "test"],
        "reply": "Hello! 👋 Welcome to **AI Business Solutions**. I am your interactive AI Assistant demo.\n\nI can answer questions about our **Website Development**, **Python Automation**, **AI Chatbots**, **Document Q&A**, and **Pricing**.\n\nHow can I help your business today?",
        "suggestions": ["What services do you offer?", "How much does a website cost?", "How can Python save me time?", "See Demo Projects"],
        "action": {"text": "Explore Services", "target": "#services"}
    }
]

def find_ai_response(user_message: str):
    """
    Intelligent local rule & keyword matching engine that returns natural,
    contextual answers and suggested follow-ups without requiring any external paid API.
    """
    cleaned = re.sub(r'[^\w\s]', '', user_message.lower()).strip()
    words = set(cleaned.split())

    if not cleaned:
        return {
            "reply": "Please feel free to ask any question regarding our digital and AI services, pricing, or portfolio!",
            "suggestions": ["What services do you offer?", "How much does a website cost?", "Contact the team"],
            "action": None
        }

    # Score each FAQ item based on keyword matches and phrase presence
    best_match = None
    highest_score = 0

    for faq in FAQ_KNOWLEDGE_BASE:
        score = 0
        for kw in faq["keywords"]:
            if " " in kw:
                if kw in cleaned:
                    score += 4
            else:
                if kw in words:
                    score += 2
                elif kw in cleaned:
                    score += 1
        
        if score > highest_score:
            highest_score = score
            best_match = faq

    if best_match and highest_score > 0:
        return {
            "reply": best_match["reply"],
            "suggestions": best_match.get("suggestions", []),
            "action": best_match.get("action")
        }

    # Fallback response guiding the visitor toward our core capabilities
    return {
        "reply": f"Thanks for asking about that! While I am currently operating on a lightweight local demo knowledge base, our team builds custom AI solutions, automated workflows, and high-performance websites tailored to your exact needs.\n\nWould you like to send us a quick message with your specific requirements, or check out our services?",
        "suggestions": [
            "What services do you offer?",
            "How much does a website cost?",
            "How can Python automation help me?",
            "Request a free consultation"
        ],
        "action": {"text": "Send Us a Message", "target": "#contact"}
    }

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------
@app.route('/')
def home():
    return render_template(
        'index.html',
        services=SERVICES_DATA,
        portfolio=PORTFOLIO_PROJECTS,
        year=datetime.now().year
    )

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        data = request.get_json(force=True, silent=True) or {}
        message = data.get('message', '').strip()
        response_data = find_ai_response(message)
        return jsonify({
            "status": "success",
            "reply": response_data["reply"],
            "suggestions": response_data["suggestions"],
            "action": response_data["action"]
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "reply": "I'm having a momentary hiccup. Please feel free to use the contact form below to get in touch with our human team!",
            "suggestions": ["What services do you offer?", "Go to Contact Form"],
            "action": {"text": "Contact Us", "target": "#contact"}
        }), 500

@app.route('/api/contact', methods=['POST'])
def api_contact():
    try:
        data = request.get_json(force=True, silent=True) or request.form.to_dict()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        service = data.get('service', 'General Inquiry').strip()
        message = data.get('message', '').strip()

        if not name or not phone or not email or not message:
            return jsonify({
                "status": "error",
                "message": "Please fill in all required fields (Name, Phone / WhatsApp, Email, and Message)."
            }), 400

        # Simple email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({
                "status": "error",
                "message": "Please provide a valid email address."
            }), 400

        new_entry = {
            "id": int(datetime.now().timestamp() * 1000),
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "phone": phone,
            "email": email,
            "service": service,
            "message": message,
            "status": "received"
        }

        # Save to local messages file
        messages = []
        if os.path.exists(MESSAGES_FILE):
            try:
                with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
            except Exception:
                messages = []
        
        messages.append(new_entry)
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2)

        return jsonify({
            "status": "success",
            "message": f"Thank you, {name}! Your message has been received. Our team will review your inquiry and get back to you within 2 to 4 hours."
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "An error occurred while saving your message. Please try again or reach out directly."
        }), 500

@app.route('/api/portfolio/<project_id>')
def api_portfolio_detail(project_id):
    project = PORTFOLIO_PROJECTS.get(project_id)
    if not project:
        return jsonify({"status": "error", "message": "Project not found"}), 404
    return jsonify({"status": "success", "project": project})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[*] AI Business Solutions server running on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
