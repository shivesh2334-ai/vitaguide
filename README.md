

"""#💊 VITAguide-AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-url-here)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent, evidence-based web application that provides personalized vitamin, mineral, supplement, and dietary recommendations using AI analysis. Built with Streamlit and aligned with USPSTF (United States Preventive Services Task Force) guidelines.

## 🎯 Key Features

- **Comprehensive Health Profiling**: Analyzes age, sex, medical conditions, dietary preferences, test results, and lifestyle factors
- **Evidence-Based Recommendations**: Follows USPSTF, NIH, and major medical society guidelines
- **Dietary Accommodation**: Supports vegan, vegetarian, halal, kosher, and other religious/cultural preferences
- **Risk Stratification**: Distinguishes between healthy individuals and those at risk for deficiencies
- **Safety First**: Includes toxicity warnings, drug interactions, and monitoring recommendations
- **Regional Adaptations**: Considers geographic factors (sun exposure, food fortification practices)

## 🏥 Clinical Approach

Our application implements the evidence-based approach recommended by major medical organizations:

### For Otherwise Healthy Individuals
> **We suggest NOT taking multivitamin supplementation for primary prevention of chronic diseases** due to insufficient evidence of benefit (USPSTF Grade I recommendation).

- No consistent benefit shown in major trials (PHS II, COSMOS, SELECT)
- Focus on dietary improvement instead
- Do not discourage if personal preference, provided no contraindications

### For At-Risk Individuals
> **Targeted supplementation is appropriate** for those with:
- Documented deficiencies (iron, B12, vitamin D, etc.)
- Malabsorption conditions (celiac, Crohn's, bariatric surgery)
- Restrictive diets (vegan without B12 fortification)
- Specific life stages (pregnancy requiring folate)
- Chronic conditions (CKD, alcohol use disorder)

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/vitaguide-ai.git
cd vitaguide-ai
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# On Windows
venv\\Scripts\\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run vitaguide_app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 📋 Usage Guide

### Step 1: Enter Your Profile
Fill in the sidebar form with:
- **Demographics**: Age, sex, region
- **Diet**: Vegetarian/vegan status, religious preferences
- **Health**: Medical conditions, medications
- **Tests**: Recent lab results (if available)

### Step 2: AI Analysis
The system analyzes your inputs using:
- Risk factor identification
- Evidence-based decision trees
- Drug-nutrient interaction checking
- Cultural/religious accommodation

### Step 3: Review Recommendations
Receive personalized guidance on:
- Specific supplements (dose, duration, priority)
- Dietary modifications
- Safety warnings and contraindications
- Recommended lab monitoring

### Step 4: Export Results
Download your recommendations as JSON to share with your healthcare provider.

## 🧬 Covered Nutrients & Conditions

### Vitamins
- Vitamin D (bone health, deficiency common)
- Vitamin B12 (critical for vegans, elderly)
- Folate/Folic Acid (pregnancy, neural tube defects)
- Vitamin C (scurvy, iron absorption)
- Vitamin E (generally not recommended)
- Vitamin A (caution in smokers)
- B-Complex vitamins (homocysteine, energy metabolism)

### Minerals
- Iron (deficiency anemia, menstruation)
- Calcium (osteoporosis, dairy-free diets)
- Zinc (vegan diets, immunity)
- Magnesium (migraine, diabetes)
- Iodine (thyroid function, vegan diets)

### Special Supplements
- Omega-3 fatty acids (cardiovascular, triglycerides)
- Multivitamins (selective use only)

### Medical Conditions Supported
- Anemia and iron deficiency
- Osteoporosis and bone health
- Cardiovascular disease
- Diabetes and metabolic syndrome
- Gastrointestinal disorders (celiac, IBD)
- Pregnancy and lactation
- Cognitive decline and dementia
- Autoimmune conditions

## 🌍 Dietary & Cultural Support

| Preference | Special Considerations |
|------------|----------------------|
| **Vegan** | B12 (critical), iron, omega-3, zinc, iodine, calcium |
| **Vegetarian** | B12 monitoring, iron optimization |
| **Halal** | Alcohol-free supplements, halal gelatin certification |
| **Kosher** | Kosher certification, no porcine ingredients |
| **Jain** | Strict vegan + no animal-derived excipients |
| **Hindu** | Vegetarian optimization, B12 focus |

## ⚠️ Safety Features

### Toxicity Warnings
- Upper limit alerts for fat-soluble vitamins (A, D, E, K)
- Iron overdose warnings (fatal in overdose)
- Drug-nutrient interaction flags

### Contraindications
- Pregnancy-specific warnings (vitamin A teratogenicity)
- Kidney disease (magnesium, potassium restrictions)
- Bleeding disorders (omega-3, vitamin E)
- Smokers (beta-carotene avoidance)

### Monitoring Recommendations
- Vitamin D levels (target 30-50 ng/mL)
- B12 levels (especially vegans, elderly)
- Iron studies (ferritin, CBC)
- Follow-up timeframes

## 📊 Evidence Base

### Primary Sources
1. **USPSTF Recommendation Statement** (2022): Vitamin, Mineral, and Multivitamin Supplementation
2. **NIH State-of-the-Science Conference** (2006): Multivitamin/Mineral Supplements
3. **COSMOS Trial** (2022): Cocoa Flavanols and Multivitamins
4. **Physicians' Health Study II** (2012): Long-term multivitamin use
5. **SELECT Trial** (2011): Vitamin E and Selenium

### Medical Society Guidelines
- American Heart Association (omega-3 recommendations)
- American College of Obstetricians (prenatal vitamins)
- Endocrine Society (vitamin D guidelines)
- American Gastroenterological Association (malabsorption)

## 🏗️ Architecture

```
vitaguide-ai/
├── vitaguide_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .gitignore              # Git ignore rules
└── assets/                 # Images and documentation
    ├── screenshot.png
    └── architecture.png
```

### Core Components

1. **SupplementKnowledgeBase**: Evidence-based database of nutrients, dosages, and interactions
2. **SupplementRecommender**: AI analysis engine implementing clinical decision logic
3. **Risk Stratification**: USPSTF-aligned healthy vs. at-risk classification
4. **Cultural Adaptation**: Religious and regional dietary considerations

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Connect repository at [share.streamlit.io](https://share.streamlit.io)
3. Deploy with one click

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "vitaguide_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t vitaguide-ai .
docker run -p 8501:8501 vitaguide-ai
```

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit changes** (`git commit -m 'Add amazing feature'`)
4. **Push to branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Areas for Contribution
- Additional medical conditions
- Regional dietary databases
- Drug interaction database expansion
- Multi-language support
- Mobile responsiveness improvements

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚕️ Medical Disclaimer

**IMPORTANT**: This application is for educational and informational purposes only. It does not constitute medical advice, diagnosis, or treatment.

- Always consult with a qualified healthcare provider before starting any supplement regimen
- Do not disregard professional medical advice or delay seeking it because of information from this app
- Individual needs vary based on genetics, medications, and specific health conditions
- Supplement quality varies by manufacturer; choose USP-verified or NSF-certified products when possible

## 🙏 Acknowledgments

- USPSTF for evidence-based guidelines
- NIH Office of Dietary Supplements for nutrient data
- Streamlit team for the amazing framework
- Medical researchers conducting long-term supplementation trials

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/vitaguide-ai/issues)
- **Email**: your.email@example.com
- **Twitter**: [@VitaGuideAI](https://twitter.com/VitaGuideAI)

---

**Made with ❤️ for better health decisions based on science, not marketing.**

*Last updated: March 2025*
"""

with open('/mnt/kimi/output/README.md', 'w') as f:
    f.write(readme)

print("✅ README.md created")



# Create a simple config file for Streamlit
config = """[theme]
primaryColor = "#2E7D32"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
"""

import os
os.makedirs('/mnt/kimi/output/.streamlit', exist_ok=True)
with open('/mnt/kimi/output/.streamlit/config.toml', 'w') as f:
    f.write(config)

print("✅ Streamlit config created")

print("\n" + "="*60)
print("📦 PROJECT STRUCTURE CREATED")
print("="*60)
print("""
/mnt/kimi/output/
├── vitaguide_app.py          (Main application - 44KB)
├── requirements.txt          (Dependencies)
├── README.md                (Comprehensive documentation)
├── .gitignore              (Git ignore rules)
├── .streamlit/
│   └── config.toml         (Streamlit configuration)
└── [GitHub repo ready to push]

TOTAL FILES: 5
""")
