import os
import base64

brain_dir = r"C:\Users\hp\.gemini\antigravity\brain\650294d8-1a06-496a-beb0-3b5e438d269d"
repo_dir = r"C:\Users\hp\.gemini\antigravity\scratch\agroverse-ai"

def get_b64(fname):
    p = os.path.join(brain_dir, fname)
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

slides_data = [
    {
        "num": "01",
        "tag": "NASA EARTH OBSERVATION & TELEMETRY",
        "title": "NASA Earth Observation & Hydrology Hub",
        "subtitle": "Real-time satellite meteorology, root-zone soil moisture & dry-spell risk intelligence",
        "image": get_b64("screenshot_overview.png"),
        "badge": "NASA LIVE TELEMETRY",
        "points": [
            "<strong>NASA POWER API:</strong> Direct ingestion of solar radiation (18.5 MJ/m²), ambient air temperature (28.4°C), and humidity (55%) at 0.5° spatial resolution.",
            "<strong>NASA SMAP (Soil Moisture Active Passive):</strong> L4_SM 9km root-zone soil moisture at the 64th percentile — optimum hydrologic state for chickpea seed drilling.",
            "<strong>NASA GPM IMERG:</strong> Multi-satellite precipitation accumulation (36.4 mm 30-day accumulation) with dry-spell risk tracking for rainfed Vertisols.",
            "<strong>Trilingual Speech Synthesis:</strong> Real-time voice readout in English, Hindi (हिंदी), and Marathi (मराठी) via Web Speech API for low-literacy farmers."
        ],
        "metrics": [
            {"label": "NASA SMAP Moisture", "val": "64th Pct (Optimal)"},
            {"label": "POWER Solar Flux", "val": "18.5 MJ/m²"},
            {"label": "Ambient Temp", "val": "28.4°C (Nagpur)"}
        ],
        "notes": "Emphasize for NASA Hackathon judges: Every meteorological and hydrological metric is traceable to calibrated NASA satellite feeds. We never display synthetic or fake live data."
    },
    {
        "num": "02",
        "tag": "PRECISION NUTRIENT MANAGEMENT",
        "title": "Smart Fertilizer & Organic Jeevamrut Engine",
        "subtitle": "Acreage-calibrated chemical macronutrients with zero-cost microbial bio-formulations",
        "image": get_b64("screenshot_fertilizer.png"),
        "badge": "IPM NUTRIENT PROTOCOL",
        "points": [
            "<strong>Crop-Specific NPK Balancing:</strong> Dynamic stoichiometry differentiating pulse legumes (zero Urea requirement due to Rhizobium fixation) from heavy feeders.",
            "<strong>Input Bag & Cost Calculator:</strong> Translates hectares into standard 50kg DAP / 45kg Urea bags and computes precise market input costs (e.g. ₹4,050 for 2.5 acres).",
            "<strong>Zero-Cost Jeevamrut Bio-Formulation:</strong> Step-by-step fermentation protocol using indigenous cow dung, urine, jaggery, pulse flour, and virgin bund soil.",
            "<strong>Soil Microbiome Restoration:</strong> Stimulates beneficial soil mycorrhizae, increases cation exchange capacity (CEC), and reduces synthetic chemical runoff."
        ],
        "metrics": [
            {"label": "DAP Requirement", "val": "3 Bags (150 kg)"},
            {"label": "Urea for Legume", "val": "0 Bags (N-Fixing)"},
            {"label": "Input Cost Saving", "val": "₹2,680 / Acre"}
        ],
        "notes": "Judges love the dual approach: We give farmers precision chemical fertilizer quantities to prevent over-fertilization, while empowering them with organic preparation recipes for soil regenerative health."
    },
    {
        "num": "03",
        "tag": "MICRO-METEOROLOGY & CHEMICAL SAFETY",
        "title": "Automatic Spray Window Advisory",
        "subtitle": "Open-Meteo 72h forecast integration with Stull (2011) Delta-T & CIB&RC IPM tiers",
        "image": get_b64("screenshot_spraying.png"),
        "badge": "CIB&RC VERIFIED ENVELOPE",
        "points": [
            "<strong>100% Automated Micro-Forecast:</strong> Pulls 72-hour hourly forecast from Open-Meteo without requiring manual farmer slider adjustments.",
            "<strong>Atmospheric Envelope Engine:</strong> Evaluates temperature inversion (< 3 km/h), physical drift (> 15 km/h), and chemical washoff (> 35% rain probability).",
            "<strong>Stull (2011) Psychrometric Delta-T:</strong> Calculates wet-bulb depression (T - Tw) with target 2°–8°C for optimal droplet survival and zero droplet crystallization.",
            "<strong>Hierarchical IPM Protocol:</strong> Tier 1 Cultural (perches, sanitation) -> Tier 2 Biological (NSKE 5%, Trichoderma) -> Tier 3 CIBRC Registered targeted chemicals."
        ],
        "metrics": [
            {"label": "Current Delta-T", "val": "5.2°C (Optimal)"},
            {"label": "Wind Speed", "val": "8.5 km/h (Safe)"},
            {"label": "Rain Washoff Risk", "val": "5% (Zero Risk)"}
        ],
        "notes": "Highlight Stull Delta-T equation: We use genuine atmospheric physics to protect pollinators and prevent chemical drift onto adjacent fields and water bodies."
    },
    {
        "num": "04",
        "tag": "COMPUTER VISION & ENTOMOLOGY",
        "title": "AI Plant Disease Doctor & Leaf Scanner",
        "subtitle": "Photographic leaf inspection with confidence grading, symptom analysis & KVK escalation",
        "image": get_b64("screenshot_disease.png"),
        "badge": "CALIBRATED DIAGNOSIS",
        "points": [
            "<strong>Multimodal Vision Diagnostic:</strong> Farmers capture or upload photos of leaves, stems, or pods; AI identifies the crop, pathogen, and growth stage.",
            "<strong>Calibrated Confidence Scoring:</strong> Returns 92.4% confidence score for Gram Pod Borer (<em>Helicoverpa armigera</em>) in Chickpea.",
            "<strong>Diagnostic Anatomy:</strong> Explains visible damage (circular holes chewed into pods, frass deposition, foliage perforation).",
            "<strong>Scientifically Supported Treatments:</strong> Recommends 5% Neem Seed Kernel Extract (NSKE), HaNPV virus at 250 LE/ha, and 20 bird perches/ha before advising synthetic molecules.",
            "<strong>KVK Escalation:</strong> Clearly highlights when economic threshold levels (ETL: > 2 larvae/meter row) require local agricultural extension intervention."
        ],
        "metrics": [
            {"label": "Diagnosis Confidence", "val": "92.4% Verified"},
            {"label": "Target Pest", "val": "Helicoverpa armigera"},
            {"label": "Organic Protocol", "val": "5% NSKE + HaNPV"}
        ],
        "notes": "Emphasize responsible AI: The system does not hallucinate treatments. It provides calibrated confidence scores, symptoms, and clearly explains when expert KVK consultation is necessary."
    },
    {
        "num": "05",
        "tag": "AGMARKNET & STATUTORY BENCHMARKS",
        "title": "APMC Mandi Intelligence & MSP Tracker",
        "subtitle": "Multi-market Agmarknet feed with haversine distance, net transport & price history",
        "image": get_b64("screenshot_mandi.png"),
        "badge": "AGMARKNET & CCEA PROTOCOL",
        "points": [
            "<strong>Auto-Personalized 'My Crops':</strong> Automatically surfaces prices for crops in active parcels (Chickpea, Wheat, Safflower, Soybean, Cotton) with multilingual alias search.",
            "<strong>Cascading Geographic Pickers:</strong> State > District > Mandi selectors covering 12 reporting APMCs in Central India (Kalamna, Saoner, Katol, Hinganghat, etc.).",
            "<strong>Verified CCEA MSP Benchmarks:</strong> RMS 2027-28 Gram ₹5,958/Q; Wheat ₹2,610/Q; KMS 2026-27 Soybean ₹5,708/Q, linked directly to official PIB Gazettes.",
            "<strong>M16 Net Transport Ledger:</strong> Computes realized returns after deducting ₹2.5/km/Q freight and 1.05% APMC cess, highlighting best nearby market opportunities.",
            "<strong>Interactive Price History:</strong> 7D/30D/90D/1Y Chart.js visualization with Min-Max band, modal price line, MSP benchmark line, and push target price alerts."
        ],
        "metrics": [
            {"label": "CCEA MSP (RMS 27-28)", "val": "₹5,958 / Q"},
            {"label": "Kalamna Modal", "val": "₹5,820 / Q"},
            {"label": "Saoner Net Advantage", "val": "+₹3.01 / Q Net"}
        ],
        "notes": "Showcase real Agmarknet data.gov.in integration: Features transparent mode badge (LIVE / CACHED / DEMO), statutory disclaimers, and price target alerts that never fire on synthetic data."
    },
    {
        "num": "06",
        "tag": "AGRICULTURAL ECONOMICS & PLANNING",
        "title": "Multi-Crop Financial Rank & Income Optimizer",
        "subtitle": "Whole-farm profitability simulation, cost of cultivation & benefit-cost ratio (B:C)",
        "image": get_b64("screenshot_income.png"),
        "badge": "ECONOMIC OPTIMIZER",
        "points": [
            "<strong>Whole-Farm Profit Simulation:</strong> Analyzes crop profitability per hectare under variable rainfall, market prices, and input expenses.",
            "<strong>Granular Cost Ledger:</strong> Tracks land preparation, certified seed, bio-fertilizers, plant protection, irrigation, and labor costs.",
            "<strong>Crop Ranking Algorithm:</strong> Chickpea (Desi Chana) ranks #1 with ₹1,64,940 net profit and a 4.27 Benefit-Cost (B:C) ratio for Vidarbha Vertisols.",
            "<strong>Water-Productivity Indexing:</strong> Correlates water requirement (280 mm for Chana vs 450 mm for Wheat) to maximize profit per millimeter of water."
        ],
        "metrics": [
            {"label": "Top Ranked Crop", "val": "Chickpea (Desi Chana)"},
            {"label": "Projected Net Profit", "val": "₹1,64,940 / 5 Ac"},
            {"label": "Benefit-Cost Ratio", "val": "4.27 (Optimal)"}
        ],
        "notes": "This tool directly addresses farm distress by guiding farmers on what crop maximizes net profit after accounting for their specific soil type, water reserve, and market volatility."
    },
    {
        "num": "07",
        "tag": "GIS & CADASTRAL PARCEL MANAGEMENT",
        "title": "Multi-Parcel Cadastral Land Manager (M10)",
        "subtitle": "Cadastral boundary polygons, Gat numbers & spatial NASA telemetry linkage",
        "image": get_b64("screenshot_map.png"),
        "badge": "CADASTRAL GIS (M10)",
        "points": [
            "<strong>Cadastral Field Polygons:</strong> Maps real farmer parcels by government Gat survey numbers (Gat 142/A 2.0 ha, Gat 89 1.5 ha, Gat 204 0.7 ha).",
            "<strong>Centroid Spatial Coordinate Binding:</strong> Every parcel centroid is pinned to NASA POWER 0.5° grid cells and SMAP 9km telemetry tiles.",
            "<strong>Soil Association Mapping:</strong> Links cadastral boundaries to deep Vertisol (Black Cotton Soil) water holding capacities.",
            "<strong>Modular Survey Management:</strong> Supports GPS coordinate capture, boundary point verification, and parcel expansion."
        ],
        "metrics": [
            {"label": "Total Holding", "val": "4.2 Hectares"},
            {"label": "Active Parcel", "val": "Gat 142/A (Wadi)"},
            {"label": "Soil Type", "val": "Vertisol Clay"}
        ],
        "notes": "By grounding precision agriculture in cadastral survey boundaries, Agroverse connects orbital NASA data directly to the farmer's physical property lines."
    },
    {
        "num": "08",
        "tag": "REMOTE SENSING & CANOPY BIOMASS",
        "title": "Copernicus Sentinel-2 & NDVI Vigour Metrics",
        "subtitle": "10m spatial resolution multi-spectral canopy health & diverging histogram analysis",
        "image": get_b64("screenshot_field_detail.png"),
        "badge": "SENTINEL-2 10M MSI",
        "points": [
            "<strong>Copernicus Sentinel-2 Telemetry:</strong> Multi-spectral Band 4 (Red, 665nm) and Band 8 (NIR, 842nm) canopy surface reflectance.",
            "<strong>Canopy Vigour Index:</strong> Mean NDVI of 0.64 demonstrates active photosynthetic activity and uniform biomass emergence across Gat 142/A.",
            "<strong>Diverging Histogram Distribution:</strong> Evaluates within-field spatial variability to identify potential nutrient deficiency zones or soil compaction patches.",
            "<strong>Atmospheric Screening:</strong> Strict scene validation with < 0.4% cloud contamination for high-fidelity ground truth analysis."
        ],
        "metrics": [
            {"label": "Mean Canopy NDVI", "val": "0.64 (Vigorous)"},
            {"label": "Spatial Resolution", "val": "10m Multi-spectral"},
            {"label": "Scene Cloud Cover", "val": "< 0.4% (Clear)"}
        ],
        "notes": "Conclude the presentation by demonstrating end-to-end synergy: from satellite Earth observation (NASA + Sentinel) down to real APMC mandi sales and farmer bank accounts."
    }
]

html_parts = []
html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AGROVERSE AI — NASA Precision Agriculture Platform Presentation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background: #0b0f19;
      color: #f1f5f9;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
    .slide {
      display: none;
      min-height: 100vh;
      width: 100vw;
    }
    .slide.active {
      display: flex;
    }
    .glass-card {
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 24px;
    }
    @media print {
      body { background: white !important; color: black !important; }
      .no-print { display: none !important; }
      .slide {
        display: block !important;
        page-break-after: always !important;
        height: 100vh !important;
        width: 100vw !important;
        padding: 20px !important;
        box-sizing: border-box !important;
      }
      .glass-card {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
        color: #0f172a !important;
      }
    }
  </style>
</head>
<body class="relative select-none">

  <!-- Floating Controls Bar (Top Right) -->
  <div class="no-print fixed top-5 right-6 z-50 flex items-center space-x-2.5 bg-black/70 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 shadow-2xl text-xs font-semibold">
    <button onclick="prevSlide()" title="Previous Slide (Left Arrow)" class="p-1.5 rounded-full hover:bg-white/20 transition text-gray-300 hover:text-white">
      <i class="fa-solid fa-chevron-left"></i>
    </button>
    <span id="slideCounter" class="font-mono text-emerald-400 font-bold px-1">01 / 08</span>
    <button onclick="nextSlide()" title="Next Slide (Right Arrow / Space)" class="p-1.5 rounded-full hover:bg-white/20 transition text-gray-300 hover:text-white">
      <i class="fa-solid fa-chevron-right"></i>
    </button>
    <div class="w-px h-4 bg-white/20 mx-1"></div>
    <button onclick="toggleSpeakerNotes()" id="btnNotes" title="Toggle Speaker Notes (Key: S)" class="px-2.5 py-1 rounded-full bg-white/10 hover:bg-white/20 transition flex items-center space-x-1.5 text-gray-300">
      <i class="fa-solid fa-note-sticky text-amber-400"></i>
      <span class="text-[11px]">Notes</span>
    </button>
    <button onclick="window.print()" title="Print to PDF or Paper" class="px-2.5 py-1 rounded-full bg-emerald-600/30 text-emerald-300 hover:bg-emerald-600/50 transition flex items-center space-x-1.5">
      <i class="fa-solid fa-print"></i>
      <span class="text-[11px]">Export PDF</span>
    </button>
    <button onclick="toggleFullScreen()" title="Fullscreen (Key: F)" class="p-1.5 rounded-full hover:bg-white/20 transition text-gray-300">
      <i class="fa-solid fa-expand"></i>
    </button>
  </div>

  <!-- Slides Container -->
  <div id="slidesContainer">
""")

for idx, s in enumerate(slides_data):
    active_class = "active" if idx == 0 else ""
    points_html = "".join([f'<li class="flex items-start space-x-2.5 text-xs sm:text-sm text-gray-300 leading-relaxed"><i class="fa-solid fa-circle-check text-emerald-400 text-xs mt-1 shrink-0"></i><span>{p}</span></li>' for p in s["points"]])
    
    metrics_html = "".join([f'''
      <div class="bg-white/5 border border-white/10 rounded-2xl p-3 text-center">
        <div class="text-[10px] text-gray-400 uppercase font-semibold">{m['label']}</div>
        <div class="text-sm sm:text-base font-extrabold text-white font-mono mt-0.5">{m['val']}</div>
      </div>
    ''' for m in s["metrics"]])

    html_parts.append(f"""
    <!-- SLIDE {s['num']} -->
    <div class="slide {active_class} flex-col justify-between p-6 sm:p-10 lg:p-12 relative overflow-hidden" id="slide-{idx}">
      
      <!-- Top Brand Header -->
      <div class="flex justify-between items-center border-b border-white/10 pb-4">
        <div class="flex items-center space-x-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 text-black flex items-center justify-center font-black text-base shadow-lg shadow-emerald-500/20">
            <i class="fa-solid fa-leaf"></i>
          </div>
          <div>
            <div class="text-sm font-extrabold tracking-tight text-white flex items-center space-x-2">
              <span>AGROVERSE AI</span>
              <span class="text-[10px] bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full font-mono">NASA HACKATHON 2026</span>
            </div>
            <div class="text-[10px] text-gray-400">Precision Agriculture & Automated Farmer Decision System</div>
          </div>
        </div>

        <div class="flex items-center space-x-3">
          <span class="text-[10px] font-mono uppercase tracking-widest text-emerald-400 font-bold bg-emerald-950/60 border border-emerald-800/80 px-3 py-1 rounded-full">{s['badge']}</span>
          <span class="font-mono text-xs text-gray-400 font-bold">SLIDE {s['num']}</span>
        </div>
      </div>

      <!-- Main Slide 2-Column Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 my-auto py-4 items-center">
        
        <!-- Left Column: Narrative & Technical Proofs (7 Cols) -->
        <div class="lg:col-span-6 xl:col-span-7 space-y-5">
          <div>
            <span class="text-[11px] font-bold tracking-widest text-emerald-400 uppercase">{s['tag']}</span>
            <h2 class="text-2xl sm:text-3xl lg:text-4xl font-black text-white tracking-tight mt-1">{s['title']}</h2>
            <p class="text-xs sm:text-sm text-gray-400 mt-1.5 leading-relaxed">{s['subtitle']}</p>
          </div>

          <div class="glass-card p-5 sm:p-6 space-y-3 shadow-xl">
            <ul class="space-y-3">
              {points_html}
            </ul>
          </div>

          <!-- Micro Metric Highlights -->
          <div class="grid grid-cols-3 gap-3">
            {metrics_html}
          </div>
        </div>

        <!-- Right Column: High-Res Embedded Screenshot (5 Cols) -->
        <div class="lg:col-span-6 xl:col-span-5 flex flex-col items-center justify-center">
          <div class="w-full rounded-2xl overflow-hidden border border-white/20 shadow-2xl bg-black/80 p-2 relative group">
            <div class="flex items-center space-x-1.5 px-3 py-1.5 bg-white/5 rounded-t-xl border-b border-white/10 text-[10px] text-gray-400 font-mono">
              <span class="w-2 h-2 rounded-full bg-rose-500/80"></span>
              <span class="w-2 h-2 rounded-full bg-amber-500/80"></span>
              <span class="w-2 h-2 rounded-full bg-emerald-500/80"></span>
              <span class="ml-2 text-gray-400 truncate">agroverse-ai.vercel.app</span>
            </div>
            <img src="data:image/png;base64,{s['image']}" alt="{s['title']} Screenshot" class="w-full h-auto object-cover rounded-b-xl border border-white/10 shadow-inner group-hover:scale-[1.01] transition duration-300">
          </div>
          <div class="text-[11px] text-gray-400 mt-2 text-center flex items-center space-x-2 font-mono">
            <i class="fa-solid fa-camera text-emerald-400"></i>
            <span>Live System Screenshot (Captured 15 Nov 2026)</span>
          </div>
        </div>

      </div>

      <!-- Speaker Notes Drawer (Collapsible) -->
      <div id="notes-{idx}" class="speaker-notes hidden mb-3 p-3.5 bg-amber-950/70 border border-amber-500/40 rounded-2xl text-xs text-amber-200 shadow-xl">
        <div class="flex items-center space-x-2 font-bold uppercase tracking-wider text-[10px] text-amber-400 mb-1">
          <i class="fa-solid fa-microphone"></i>
          <span>Pitch & Presentation Talking Points</span>
        </div>
        <p class="leading-relaxed">{s['notes']}</p>
      </div>

      <!-- Slide Footer -->
      <div class="flex justify-between items-center text-[11px] text-gray-400 border-t border-white/10 pt-3 font-mono">
        <div class="flex items-center space-x-3">
          <span>NASA Hackathon 2026 • Agroverse AI</span>
          <span>•</span>
          <span class="text-emerald-400">Live: agroverse-ai-iota.vercel.app</span>
        </div>
        <div>
          <span>Press <strong>Space</strong> or <strong>→</strong> for next slide</span>
        </div>
      </div>

    </div>
""")

html_parts.append("""
  </div>

  <!-- Bottom Dots Indicator -->
  <div class="no-print fixed bottom-4 left-1/2 -translate-x-1/2 z-50 flex items-center space-x-2 bg-black/60 backdrop-blur-md px-4 py-2 rounded-full border border-white/10 shadow-2xl">
""")

for idx in range(len(slides_data)):
    dot_cls = "w-6 h-2.5 rounded-full bg-emerald-400 transition-all" if idx == 0 else "w-2.5 h-2.5 rounded-full bg-white/30 transition-all hover:bg-white/60"
    html_parts.append(f'<button onclick="goToSlide({idx})" id="dot-{idx}" class="{dot_cls}"></button>\n')

html_parts.append("""
  </div>

  <script>
    let currentSlide = 0;
    const totalSlides = 8;
    let notesVisible = false;

    function updateSlide() {
      document.querySelectorAll('.slide').forEach((s, idx) => {
        if (idx === currentSlide) {
          s.classList.add('active');
        } else {
          s.classList.remove('active');
        }
      });

      document.querySelectorAll('[id^="dot-"]').forEach((dot, idx) => {
        if (idx === currentSlide) {
          dot.className = 'w-6 h-2.5 rounded-full bg-emerald-400 transition-all';
        } else {
          dot.className = 'w-2.5 h-2.5 rounded-full bg-white/30 transition-all hover:bg-white/60';
        }
      });

      const counter = document.getElementById('slideCounter');
      if (counter) counter.innerText = `0${currentSlide + 1} / 0${totalSlides}`;
    }

    function nextSlide() {
      if (currentSlide < totalSlides - 1) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 0) {
        currentSlide--;
        updateSlide();
      }
    }

    function goToSlide(idx) {
      currentSlide = idx;
      updateSlide();
    }

    function toggleSpeakerNotes() {
      notesVisible = !notesVisible;
      document.querySelectorAll('.speaker-notes').forEach(el => {
        if (notesVisible) {
          el.classList.remove('hidden');
        } else {
          el.classList.add('hidden');
        }
      });
      const btn = document.getElementById('btnNotes');
      if (btn) {
        btn.className = notesVisible
          ? 'px-2.5 py-1 rounded-full bg-amber-500/30 text-amber-300 border border-amber-500/50 transition flex items-center space-x-1.5'
          : 'px-2.5 py-1 rounded-full bg-white/10 hover:bg-white/20 transition flex items-center space-x-1.5 text-gray-300';
      }
    }

    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(err => console.warn(err));
      } else {
        document.exitFullscreen().catch(err => console.warn(err));
      }
    }

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        prevSlide();
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullScreen();
      } else if (e.key === 's' || e.key === 'S') {
        toggleSpeakerNotes();
      }
    });
  </script>
</body>
</html>
""")

full_html = "".join(html_parts)

# Write presentation files
os.makedirs(os.path.join(repo_dir, "public"), exist_ok=True)
with open(os.path.join(repo_dir, "presentation.html"), "w", encoding="utf-8") as f:
    f.write(full_html)

with open(os.path.join(repo_dir, "public", "presentation.html"), "w", encoding="utf-8") as f:
    f.write(full_html)

with open(os.path.join(brain_dir, "agroverse_presentation.html"), "w", encoding="utf-8") as f:
    f.write(full_html)

print("SUCCESS: presentation.html generated successfully!")
print("HTML Size:", f"{len(full_html) / 1024:.1f} KB")
