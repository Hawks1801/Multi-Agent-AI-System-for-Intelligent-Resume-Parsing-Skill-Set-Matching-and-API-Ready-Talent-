from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.core.config import settings
from app.api.v1.api import api_router

app = FastAPI(
    title="MultiagentAI",
    description="Advanced Multi-Agent system for resume parsing, skill normalization, and semantic matching.",
    version="1.0.4",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=None, 
    redoc_url=None
)

# Custom Swagger UI that perfectly mirrors the Dashboard
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - API Protocol Docs",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        custom_js="""
        // Inject Dashboard Header
        window.addEventListener('load', function() {
            const header = document.createElement('header');
            header.className = 'fixed top-0 w-full glass-header z-50';
            header.innerHTML = `
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div class="flex items-center justify-between h-20">
                        <div class="flex items-center gap-2 cursor-pointer" onclick="window.location.href='http://localhost:3001'">
                            <div class="w-10 h-10 bg-teal-500 rounded-xl flex items-center justify-center">
                                <i class="fas fa-microchip text-slate-900 text-xl"></i>
                            </div>
                            <span class="font-extrabold text-2xl tracking-tight text-white uppercase">Multiagent<span class="text-teal-400">AI</span></span>
                        </div>
                        <nav class="hidden md:flex items-center gap-10">
                            <span class="mono text-[10px] text-teal-500 font-bold tracking-[0.3em] uppercase">SYSTEM_DOCS_ACTIVE</span>
                        </nav>
                        <div class="flex items-center gap-4">
                            <button onclick="window.location.href='http://localhost:3001'" class="bg-slate-900 text-white px-6 py-2.5 rounded-full font-bold text-sm hover:bg-slate-800 transition-all border border-slate-800">
                                Open Dashboard
                            </button>
                        </div>
                    </div>
                </div>
            `;
            document.body.prepend(header);
            
            // Add Font Awesome
            const fa = document.createElement('link');
            fa.rel = 'stylesheet';
            fa.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
            document.head.appendChild(fa);
            
            // Add Space Grotesk Font
            const font = document.createElement('link');
            font.rel = 'stylesheet';
            font.href = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap';
            document.head.appendChild(font);
        });
        """,
        custom_css="""
        @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
        
        :root {
            --bg-deep: #0a0c10;
            --bg-panel: #12151c;
            --accent-teal: #2dd4bf;
            --accent-orange: #fb923c;
            --border-dim: #1e293b;
            --text-main: #94a3b8;
        }

        body { 
            background-color: var(--bg-deep) !important;
            font-family: 'Space Grotesk', sans-serif !important;
            margin: 0;
            padding-top: 80px;
            background-image: radial-gradient(var(--border-dim) 1px, transparent 1px) !important;
            background-size: 40px 40px !important;
        }

        .glass-header {
            background: rgba(10, 12, 16, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-dim);
            position: fixed; top: 0; left: 0; width: 100%; z-index: 1000;
        }

        .swagger-ui {
            filter: invert(0) !important;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px;
        }

        .swagger-ui .topbar { display: none !important; }
        
        .swagger-ui .info {
            background: var(--bg-panel);
            border: 1px solid var(--border-dim);
            padding: 40px;
            margin-bottom: 40px;
            position: relative;
        }

        .swagger-ui .info::before {
            content: ''; position: absolute; top: -1px; left: -1px; width: 10px; height: 10px;
            border-top: 2px solid var(--accent-teal); border-left: 2px solid var(--accent-teal);
        }

        .swagger-ui .info .title { 
            color: #ffffff !important; 
            font-size: 3rem !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: -0.05em;
        }

        .swagger-ui .info p, .swagger-ui .info li, .swagger-ui .info table { 
            color: var(--text-main) !important; 
            font-weight: 500;
        }

        .swagger-ui .scheme-container { 
            background-color: transparent !important; 
            box-shadow: none !important;
            padding: 0 !important;
            margin-bottom: 40px !important;
        }

        .swagger-ui .opblock-tag-section {
            background: var(--bg-panel);
            border: 1px solid var(--border-dim);
            margin-bottom: 20px;
        }

        .swagger-ui .opblock-tag {
            color: #ffffff !important;
            font-family: 'JetBrains Mono', monospace !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            padding: 20px !important;
        }

        .swagger-ui .opblock.opblock-get { 
            background: rgba(45, 212, 191, 0.03) !important; 
            border-color: var(--accent-teal) !important; 
        }
        
        .swagger-ui .opblock.opblock-get .opblock-summary-method { 
            background: var(--accent-teal) !important; 
            color: var(--bg-deep) !important; 
            font-weight: 900;
        }

        .swagger-ui .opblock.opblock-post { 
            background: rgba(96, 165, 250, 0.03) !important; 
            border-color: #60a5fa !important; 
        }
        
        .swagger-ui .opblock.opblock-post .opblock-summary-method { 
            background: #60a5fa !important; 
            color: var(--bg-deep) !important;
            font-weight: 900;
        }

        .swagger-ui .opblock .opblock-summary-path { 
            color: #ffffff !important; 
            font-family: 'JetBrains Mono', monospace !important;
            font-weight: 700 !important;
        }

        .swagger-ui .btn.execute { 
            background-color: var(--accent-teal) !important; 
            color: var(--bg-deep) !important; 
            border: none !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
        }

        .swagger-ui section.models { 
            border: 1px solid var(--border-dim) !important; 
            background: var(--bg-panel) !important; 
        }
        
        .swagger-ui section.models h4 { 
            color: #ffffff !important; 
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        .mono { font-family: 'JetBrains Mono', monospace !important; }
        """
    )

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Welcome to the Multi-Agent Resume Intelligence API", "status": "operational"}

@app.get("/health", tags=["Health"])
def health_check():
    """Returns the health status of the API and underlying agents."""
    return {
        "status": "healthy",
        "version": "1.0.4",
        "agents": ["Parser", "Normalizer", "Matcher", "Interviewer"]
    }
