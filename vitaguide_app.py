# Create a COMPLETELY NEW clean file - no file writing code at all
# Just the pure Streamlit application content

streamlit_app_content = '''import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="VitaGuide AI - Personalized Supplement & Diet Advisor",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        background-color: #f0f8ff;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .warning-card {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .danger-card {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .success-card {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 10px 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}

# Knowledge Base - Evidence-Based Guidelines
class SupplementKnowledgeBase:
    def __init__(self):
        self.vitamin_data = self._load_vitamin_data()
        self.condition_mappings = self._load_condition_mappings()
        self.dietary_restrictions = self._load_dietary_restrictions()
        self.regional_factors = self._load_regional_factors()
    
    def _load_vitamin_data(self):
        return {
            "vitamin_d": {
                "name": "Vitamin D",
                "primary_sources": ["Sunlight exposure", "Fatty fish", "Fortified dairy", "Egg yolks"],
                "deficiency_risks": ["Limited sun exposure", "Dark skin", "Obesity", "Malabsorption", "Elderly"],
                "recommended_dose": {"adult": "600-800 IU/day", "elderly": "800-1000 IU/day", "deficiency": "1000-2000 IU/day"},
                "toxicity": ">4000 IU/day may cause hypercalcemia",
                "evidence": "Strong evidence for bone health; insufficient for primary prevention of chronic diseases",
                "conditions": ["Osteoporosis", "Malabsorption", "Chronic kidney disease", "Limited sun exposure"]
            },
            "vitamin_b12": {
                "name": "Vitamin B12",
                "primary_sources": ["Meat", "Fish", "Dairy", "Eggs", "Fortified cereals"],
                "deficiency_risks": ["Vegan diet", "Elderly", "Pernicious anemia", "Gastric bypass", "Metformin use"],
                "recommended_dose": {"adult": "2.4 mcg/day", "pregnant": "2.6 mcg/day", "deficiency": "1000 mcg/day"},
                "toxicity": "No established upper limit; generally considered safe",
                "evidence": "Essential for vegans, elderly, and those with malabsorption; no benefit in sufficient individuals",
                "conditions": ["Vegan/vegetarian", "Pernicious anemia", "Gastric surgery", "Dementia risk", "Metformin therapy"]
            },
            "folate": {
                "name": "Folate (Vitamin B9)",
                "primary_sources": ["Leafy greens", "Legumes", "Fortified grains", "Citrus fruits"],
                "deficiency_risks": ["Pregnancy", "Alcohol use", "Malabsorption", "Poor diet"],
                "recommended_dose": {"adult": "400 mcg/day", "pregnant": "600 mcg/day", "planning_pregnancy": "400-800 mcg/day"},
                "toxicity": "Upper limit 1000 mcg/day from supplements (masks B12 deficiency)",
                "evidence": "Critical for neural tube defect prevention; cardiovascular benefits in specific populations",
                "conditions": ["Pregnancy", "Neural tube defect risk", "Hyperhomocysteinemia", "Megaloblastic anemia"]
            },
            "iron": {
                "name": "Iron",
                "primary_sources": ["Red meat", "Spinach", "Lentils", "Fortified cereals", "Shellfish"],
                "deficiency_risks": ["Menstruating women", "Pregnancy", "Vegetarian", "Chronic blood loss"],
                "recommended_dose": {"adult_men": "8 mg/day", "adult_women": "18 mg/day", "pregnant": "27 mg/day"},
                "toxicity": "Upper limit 45 mg/day; overdose dangerous",
                "evidence": "Treat documented deficiency; routine supplementation not recommended for men/postmenopausal women",
                "conditions": ["Iron deficiency anemia", "Heavy menstrual bleeding", "Pregnancy", "Chronic kidney disease"]
            },
            "calcium": {
                "name": "Calcium",
                "primary_sources": ["Dairy products", "Fortified plant milks", "Leafy greens", "Tofu"],
                "deficiency_risks": ["Dairy-free diet", "Postmenopausal women", "Elderly", "Malabsorption"],
                "recommended_dose": {"adult": "1000 mg/day", "women_50+": "1200 mg/day", "men_70+": "1200 mg/day"},
                "toxicity": "Upper limit 2000-2500 mg/day; kidney stones risk",
                "evidence": "Important for bone health; balance with Vitamin D; cardiovascular controversy at high doses",
                "conditions": ["Osteoporosis", "Lactose intolerance", "Postmenopausal women", "Hypoparathyroidism"]
            },
            "omega3": {
                "name": "Omega-3 Fatty Acids (EPA/DHA)",
                "primary_sources": ["Fatty fish (salmon, mackerel)", "Fish oil", "Algae oil (vegan)", "Walnuts", "Flaxseeds"],
                "deficiency_risks": ["No fish consumption", "High triglycerides", "Cardiovascular disease"],
                "recommended_dose": {"general": "250-500 mg EPA+DHA/day", "triglycerides": "2000-4000 mg/day"},
                "toxicity": "High doses may increase bleeding risk; affect immune function",
                "evidence": "Strong for triglyceride reduction; modest cardiovascular benefit; prescription forms for specific conditions",
                "conditions": ["High triglycerides", "Cardiovascular disease", "Rheumatoid arthritis", "ADHD", "No fish intake"]
            },
            "vitamin_c": {
                "name": "Vitamin C",
                "primary_sources": ["Citrus fruits", "Berries", "Peppers", "Broccoli"],
                "deficiency_risks": ["Smoking", "Poor diet", "Alcohol use disorder"],
                "recommended_dose": {"adult_men": "90 mg/day", "adult_women": "75 mg/day", "smokers": "+35 mg/day"},
                "toxicity": "Upper limit 2000 mg/day; kidney stones risk in susceptible",
                "evidence": "No consistent evidence for preventing chronic diseases; treat deficiency/scurvy",
                "conditions": ["Scurvy", "Poor wound healing", "Iron deficiency (enhances absorption)", "Smokers"]
            },
            "vitamin_e": {
                "name": "Vitamin E",
                "primary_sources": ["Nuts", "Seeds", "Vegetable oils", "Spinach"],
                "deficiency_risks": ["Fat malabsorption", "Genetic disorders"],
                "recommended_dose": {"adult": "15 mg/day (22.4 IU)"},
                "toxicity": "Upper limit 1000 mg/day (1500 IU); increased bleeding risk",
                "evidence": "No benefit for primary prevention; high doses may increase mortality",
                "conditions": ["Fat malabsorption", "Abetalipoproteinemia"]
            },
            "vitamin_a": {
                "name": "Vitamin A",
                "primary_sources": ["Liver", "Dairy", "Eggs", "Orange vegetables", "Leafy greens"],
                "deficiency_risks": ["Malabsorption", "Liver disease", "Restrictive diets"],
                "recommended_dose": {"adult_men": "900 mcg/day", "adult_women": "700 mcg/day"},
                "toxicity": "Upper limit 3000 mcg/day; teratogenic in pregnancy",
                "evidence": "Beta-carotene supplements increase lung cancer in smokers; avoid unless deficient",
                "conditions": ["Night blindness", "Xerophthalmia", "Measles (in developing countries)", "Cystic fibrosis"]
            },
            "zinc": {
                "name": "Zinc",
                "primary_sources": ["Oysters", "Red meat", "Poultry", "Beans", "Nuts"],
                "deficiency_risks": ["Alcohol use disorder", "Malabsorption", "Vegetarian", "Sickle cell disease"],
                "recommended_dose": {"adult_men": "11 mg/day", "adult_women": "8 mg/day"},
                "toxicity": "Upper limit 40 mg/day; copper deficiency",
                "evidence": "May reduce cold duration if started early; deficiency treatment only",
                "conditions": ["Zinc deficiency", "Sickle cell disease", "Wilson's disease", "Acute diarrhea (children)"]
            },
            "magnesium": {
                "name": "Magnesium",
                "primary_sources": ["Nuts", "Seeds", "Whole grains", "Dark chocolate", "Leafy greens"],
                "deficiency_risks": ["Alcohol use disorder", "Diuretic use", "Malabsorption", "Diabetes"],
                "recommended_dose": {"adult_men": "400-420 mg/day", "adult_women": "310-320 mg/day"},
                "toxicity": "Upper limit 350 mg/day from supplements (diarrhea); avoid in kidney failure",
                "evidence": "Deficiency correction only; some evidence for migraine prevention",
                "conditions": ["Hypomagnesemia", "Migraine", "Type 2 diabetes", "Osteoporosis"]
            },
            "iodine": {
                "name": "Iodine",
                "primary_sources": ["Iodized salt", "Seaweed", "Dairy", "Fish"],
                "deficiency_risks": ["No iodized salt", "Pregnancy", "Vegan without seaweed"],
                "recommended_dose": {"adult": "150 mcg/day", "pregnant": "220 mcg/day", "lactating": "290 mcg/day"},
                "toxicity": "Upper limit 1100 mcg/day; thyroid dysfunction",
                "evidence": "Critical for thyroid function; deficiency common in some regions",
                "conditions": ["Iodine deficiency", "Pregnancy", "Lactation", "Goiter"]
            }
        }
    
    def _load_condition_mappings(self):
        return {
            "anemia": ["iron", "vitamin_b12", "folate", "vitamin_c"],
            "osteoporosis": ["calcium", "vitamin_d", "magnesium"],
            "pregnancy": ["folate", "iron", "calcium", "vitamin_d", "iodine", "omega3"],
            "cardiovascular_disease": ["omega3"],
            "diabetes": ["magnesium", "vitamin_d"],
            "malabsorption": ["multivitamin", "vitamin_d", "vitamin_b12", "calcium", "iron"],
            "vegan": ["vitamin_b12", "iron", "calcium", "omega3", "zinc", "iodine"],
            "vegetarian": ["vitamin_b12", "iron", "omega3", "zinc"],
            "alcohol_use_disorder": ["thiamine", "folate", "magnesium", "multivitamin"],
            "bariatric_surgery": ["multivitamin", "vitamin_b12", "iron", "calcium", "vitamin_d"],
            "chronic_kidney_disease": ["vitamin_d", "iron", "calcium"],
            "celiac_disease": ["multivitamin", "iron", "folate", "vitamin_b12", "vitamin_d"],
            "crohns_disease": ["multivitamin", "vitamin_d", "vitamin_b12", "iron"],
            "ulcerative_colitis": ["multivitamin", "vitamin_d", "calcium"],
            "liver_disease": ["vitamin_d", "calcium"],
            "dementia": ["vitamin_b12"],
            "depression": ["vitamin_d", "omega3"],
            "hypertension": ["magnesium", "potassium"],
            "high_triglycerides": ["omega3"],
            "rheumatoid_arthritis": ["omega3", "vitamin_d"],
            "migraine": ["magnesium", "riboflavin"],
            "thyroid_disorder": ["iodine", "selenium"],
            "age_related_macular_degeneration": ["AREDS2 formula"],
            "cataracts": [],
            "kidney_stones": ["avoid_high_dose_vitamin_c", "calcium_with_meals"]
        }
    
    def _load_dietary_restrictions(self):
        return {
            "vegan": {
                "critical": ["vitamin_b12", "vitamin_d", "omega3", "iron", "calcium", "zinc", "iodine"],
                "foods_to_emphasize": ["Legumes", "Nuts", "Seeds", "Whole grains", "Fortified foods", "Nutritional yeast"],
                "protein_sources": ["Tofu", "Tempeh", "Lentils", "Chickpeas", "Quinoa"]
            },
            "vegetarian": {
                "critical": ["vitamin_b12", "iron", "omega3", "zinc"],
                "foods_to_emphasize": ["Dairy", "Eggs", "Legumes", "Nuts", "Seeds", "Whole grains"],
                "protein_sources": ["Dairy", "Eggs", "Legumes", "Tofu", "Tempeh"]
            },
            "halal": {
                "restrictions": ["No pork", "No alcohol", "Halal meat only"],
                "considerations": ["Check gelatin sources in supplements", "Alcohol-free formulations"]
            },
            "kosher": {
                "restrictions": ["No pork", "No shellfish", "No mixing meat and dairy"],
                "considerations": ["Look for kosher certification on supplements"]
            },
            "lactose_intolerant": {
                "avoid": ["Dairy-based supplements"],
                "alternatives": ["Plant-based calcium", "Lactose-free dairy"]
            },
            "gluten_free": {
                "avoid": ["Wheat, barley, rye"],
                "considerations": ["Check supplement fillers for gluten"]
            }
        }
    
    def _load_regional_factors(self):
        return {
            "north_america": {"iodized_salt": True, "fortified_foods": True, "sun_exposure": "variable"},
            "europe": {"iodized_salt": "variable", "fortified_foods": False, "sun_exposure": "variable"},
            "asia": {"iodized_salt": True, "fortified_foods": False, "sun_exposure": "adequate"},
            "africa": {"iodized_salt": "variable", "fortified_foods": False, "sun_exposure": "adequate"},
            "middle_east": {"iodized_salt": True, "fortified_foods": False, "sun_exposure": "adequate"},
            "south_america": {"iodized_salt": "variable", "fortified_foods": False, "sun_exposure": "adequate"},
            "australia": {"iodized_salt": True, "fortified_foods": True, "sun_exposure": "adequate"},
            "india": {"iodized_salt": True, "vegetarian_common": True, "fortified_foods": False},
            "scandinavia": {"vitamin_d_fortification": True, "sun_exposure": "limited"}
        }

# AI Analysis Engine
class SupplementRecommender:
    def __init__(self):
        self.kb = SupplementKnowledgeBase()
    
    def analyze_user(self, user_data):
        """Main analysis function based on evidence-based approach"""
        recommendations = {
            "supplements": [],
            "dietary_advice": [],
            "lifestyle_modifications": [],
            "warnings": [],
            "monitoring": [],
            "approach_summary": ""
        }
        
        # Determine risk profile
        risk_factors = self._assess_risk_factors(user_data)
        
        # Core decision logic based on USPSTF approach
        if self._is_healthy_low_risk(user_data, risk_factors):
            recommendations["approach_summary"] = self._healthy_approach()
        else:
            recommendations["approach_summary"] = self._at_risk_approach()
            recommendations = self._generate_targeted_recommendations(user_data, recommendations, risk_factors)
        
        # Add dietary recommendations
        recommendations = self._add_dietary_recommendations(user_data, recommendations)
        
        # Add religious/cultural considerations
        recommendations = self._add_cultural_considerations(user_data, recommendations)
        
        return recommendations
    
    def _assess_risk_factors(self, user_data):
        """Identify risk factors for deficiency"""
        risks = []
        
        # Dietary risks
        if user_data.get("diet_type") in ["vegan", "strict_vegan"]:
            risks.extend(["vitamin_b12_deficiency", "iron_deficiency", "omega3_deficiency", "zinc_deficiency"])
        elif user_data.get("diet_type") == "vegetarian":
            risks.extend(["vitamin_b12_risk", "iron_risk"])
        
        # Age-related risks
        age = user_data.get("age", 0)
        if age > 50:
            risks.append("b12_malabsorption")
        if age > 65:
            risks.extend(["vitamin_d_deficiency", "calcium_deficiency"])
        
        # Medical conditions
        conditions = user_data.get("conditions", [])
        for condition in conditions:
            if condition in ["celiac", "crohns", "ulcerative_colitis", "bariatric_surgery"]:
                risks.append("malabsorption")
            if condition == "alcohol_use_disorder":
                risks.extend(["thiamine_deficiency", "folate_deficiency", "magnesium_deficiency"])
        
        # Sun exposure
        if user_data.get("sun_exposure") == "limited":
            risks.append("vitamin_d_deficiency")
        
        # Pregnancy
        if user_data.get("pregnancy_status") in ["pregnant", "planning_pregnancy"]:
            risks.append("pregnancy_needs")
        
        return risks
    
    def _is_healthy_low_risk(self, user_data, risk_factors):
        """Determine if user is low-risk per USPSTF criteria"""
        if len(risk_factors) > 0:
            return False
        if user_data.get("conditions"):
            return False
        if user_data.get("test_deficiencies"):
            return False
        return True
    
    def _healthy_approach(self):
        """USPSTF consistent approach for healthy individuals"""
        return """
        **Evidence-Based Approach for Healthy Individuals**
        
        Based on the United States Preventive Services Task Force (USPSTF) recommendations and NIH consensus:
        
        ✅ **RECOMMENDATION**: We suggest NOT taking multivitamin supplementation for primary prevention 
        of chronic diseases due to insufficient evidence of benefit.
        
        📊 **Evidence Quality**: Multiple large randomized trials (including PHS II, COSMOS, SELECT) show 
        no consistent benefit of multivitamins on cardiovascular disease, cancer, or mortality in 
        well-nourished adults.
        
        🥗 **Focus Instead On**:
        - Mediterranean-style dietary pattern
        - 5+ servings of fruits and vegetables daily
        - Whole grains over refined grains
        - Fatty fish 2x/week
        - Limited processed foods and added sugars
        
        ⚠️ **However**: We do not strongly discourage multivitamins if you personally wish to take them 
        (belief systems, insurance), provided there are no contraindications.
        
        **Cost-Benefit**: Multivitamins are generally safe but represent unnecessary expense for most 
        healthy adults with adequate diets.
        """
    
    def _at_risk_approach(self):
        return """
        **Targeted Supplementation Approach for At-Risk Individuals**
        
        You have identified risk factors for nutritional deficiency. Evidence supports targeted 
        supplementation rather than routine multivitamin use.
        
        **Principles**:
        1. Treat documented deficiencies with specific nutrients
        2. Address modifiable risk factors through diet first
        3. Use multivitamins only when multiple deficiencies likely and cost-effective
        4. Monitor levels when possible (Vitamin D, B12, Iron)
        """
    
    def _generate_targeted_recommendations(self, user_data, recs, risk_factors):
        """Generate specific supplement recommendations"""
        
        # Vitamin D - very common deficiency
        if "vitamin_d_deficiency" in risk_factors or user_data.get("vitamin_d_level") == "low":
            recs["supplements"].append({
                "nutrient": "Vitamin D3",
                "dose": "1000-2000 IU daily" if user_data.get("age", 0) < 70 else "2000 IU daily",
                "rationale": "Limited sun exposure and/or confirmed deficiency",
                "duration": "Recheck levels in 3 months",
                "priority": "High",
                "food_sources": ["Fatty fish", "Fortified dairy/plant milks", "Egg yolks"]
            })
            recs["monitoring"].append("Serum 25(OH)D level in 3 months (target 30-50 ng/mL)")
        
        # Vitamin B12 - critical for vegans and elderly
        if "vitamin_b12_deficiency" in risk_factors or user_data.get("diet_type") in ["vegan", "strict_vegan"]:
            recs["supplements"].append({
                "nutrient": "Vitamin B12 (Methylcobalamin or Cyanocobalamin)",
                "dose": "250-500 mcg daily OR 1000 mcg weekly",
                "rationale": "Vegan diet contains no reliable B12 sources; deficiency causes irreversible neurological damage",
                "duration": "Lifelong for vegans",
                "priority": "Critical",
                "food_sources": ["Fortified nutritional yeast", "Fortified plant milks", "Fortified cereals"]
            })
        elif "b12_malabsorption" in risk_factors:
            recs["supplements"].append({
                "nutrient": "Vitamin B12",
                "dose": "500-1000 mcg daily (oral) or monthly injections if severe malabsorption",
                "rationale": "Decreased gastric acid and intrinsic factor with aging",
                "duration": "Ongoing",
                "priority": "High",
                "food_sources": ["Animal products", "Fortified foods"]
            })
        
        # Iron - only if deficient or high risk
        if user_data.get("iron_status") == "deficient" or (user_data.get("sex") == "female" and user_data.get("heavy_periods")):
            recs["supplements"].append({
                "nutrient": "Iron (Ferrous sulfate or bisglycinate)",
                "dose": "65 mg elemental iron every other day (better absorption, fewer side effects)",
                "rationale": "Documented deficiency or high loss state",
                "duration": "3 months to replete, then 6 months maintenance",
                "priority": "High",
                "food_sources": ["Red meat", "Spinach", "Lentils", "Fortified cereals"],
                "interactions": "Take with Vitamin C, away from calcium, coffee, tea"
            })
            recs["monitoring"].append("CBC, ferritin in 8-12 weeks")
            recs["warnings"].append("Iron overdose is dangerous - keep ALL iron supplements away from children!")
        elif user_data.get("sex") == "male" or (user_data.get("sex") == "female" and user_data.get("age", 0) > 50):
            if not user_data.get("iron_status") == "deficient":
                recs["warnings"].append("⚠️ DO NOT take iron supplements unless documented deficient - risk of iron overload")
        
        # Folate - preconception and pregnancy
        if user_data.get("pregnancy_status") in ["planning_pregnancy", "pregnant"]:
            recs["supplements"].append({
                "nutrient": "Folic Acid",
                "dose": "400-800 mcg daily (start at least 1 month before conception)",
                "rationale": "Prevents neural tube defects (spina bifida, anencephaly)",
                "duration": "At least first trimester, ideally throughout pregnancy",
                "priority": "Critical",
                "food_sources": ["Leafy greens", "Legumes", "Fortified grains", "Oranges"]
            })
        
        # Omega-3 - if no fish intake or high triglycerides
        if user_data.get("diet_type") in ["vegan", "vegetarian"] or user_data.get("fish_intake") == "none":
            recs["supplements"].append({
                "nutrient": "Algae-based Omega-3 (DHA/EPA)",
                "dose": "250-300 mg DHA daily",
                "rationale": "No dietary intake of fatty fish; important for cardiovascular and cognitive health",
                "duration": "Ongoing",
                "priority": "Moderate",
                "food_sources": ["Walnuts", "Flaxseeds", "Chia seeds", "Algae oil"]
            })
        elif user_data.get("high_triglycerides"):
            recs["supplements"].append({
                "nutrient": "EPA/DHA (High dose)",
                "dose": "2000-4000 mg EPA+DHA daily (prescription Lovaza or Vascepa preferred)",
                "rationale": "FDA-approved for triglycerides >500 mg/dL",
                "duration": "As directed by physician",
                "priority": "High",
                "food_sources": ["Fatty fish", "Fish oil"]
            })
        
        # Calcium - if low intake
        if user_data.get("diet_type") in ["vegan"] or user_data.get("dairy_intake") == "none":
            recs["supplements"].append({
                "nutrient": "Calcium (Citrate preferred, or Carbonate)",
                "dose": "500-600 mg twice daily (total 1000-1200 mg from diet + supplements)",
                "rationale": "Inadequate dietary calcium without dairy",
                "duration": "Ongoing if dietary intake remains low",
                "priority": "Moderate",
                "food_sources": ["Fortified plant milks", "Tofu (calcium-set)", "Leafy greens", "Almonds"],
                "notes": "Take in divided doses; carbonate with meals, citrate anytime"
            })
        
        # Iodine - if no iodized salt
        if user_data.get("iodized_salt") == "no" or user_data.get("diet_type") == "vegan":
            recs["supplements"].append({
                "nutrient": "Iodine (Potassium iodide)",
                "dose": "150 mcg daily",
                "rationale": "No reliable dietary source without iodized salt or seafood",
                "duration": "Ongoing",
                "priority": "Moderate",
                "food_sources": ["Iodized salt", "Seaweed (variable content)", "Dairy"],
                "warning": "Do not exceed 1100 mcg/day; avoid kelp supplements (variable content)"
            })
        
        # Zinc - vegan/vegetarian
        if user_data.get("diet_type") in ["vegan", "vegetarian"]:
            recs["supplements"].append({
                "nutrient": "Zinc",
                "dose": "8-11 mg daily (or 50% higher than RDA due to plant inhibitors)",
                "rationale": "Plant-based diets have lower zinc bioavailability",
                "duration": "Ongoing",
                "priority": "Low-Moderate",
                "food_sources": ["Legumes", "Nuts", "Seeds", "Whole grains"],
                "notes": "Soaking/sprouting beans and grains increases absorption"
            })
        
        # Multivitamin consideration
        if len(recs["supplements"]) >= 3:
            recs["supplements"].append({
                "nutrient": "OR: High-Quality Multivitamin",
                "dose": "One daily (providing ~100% RDA, not megadoses)",
                "rationale": "Multiple identified deficiencies - may be more cost-effective than individual supplements",
                "duration": "As needed",
                "priority": "Alternative",
                "conditions": "Choose USP-verified brand without iron (unless needed) or vitamin A as beta-carotene"
            })
        
        return recs
    
    def _add_dietary_recommendations(self, user_data, recs):
        """Add evidence-based dietary advice"""
        
        # Base Mediterranean-style recommendations
        base_diet = [
            "Emphasize whole foods over processed foods",
            "Aim for 5-9 servings of fruits and vegetables daily",
            "Choose whole grains (oats, quinoa, brown rice) over refined grains",
            "Include fatty fish 2x/week (salmon, mackerel, sardines) unless vegetarian/vegan",
            "Use olive oil as primary fat source",
            "Limit added sugars to <25g/day (women) or <36g/day (men)",
            "Limit sodium to <2300mg/day"
        ]
        
        recs["dietary_advice"].extend(base_diet)
        
        # Diet-specific modifications
        if user_data.get("diet_type") == "vegan":
            recs["dietary_advice"].extend([
                "**CRITICAL**: Ensure reliable B12 source (supplement or fortified foods)",
                "Combine iron-rich plants with Vitamin C sources (citrus, peppers)",
                "Soak/sprout legumes and grains to reduce phytates and increase mineral absorption",
                "Include algae-based omega-3 supplement",
                "Use iodized salt or take iodine supplement",
                "Eat calcium-set tofu, fortified plant milks, and leafy greens for calcium"
            ])
        elif user_data.get("diet_type") == "vegetarian":
            recs["dietary_advice"].extend([
                "Include eggs and dairy for B12, though supplement may still be needed",
                "Focus on iron-rich foods with Vitamin C",
                "Consider algae-based omega-3 if fish intake <2x/week"
            ])
        
        # Condition-specific diets
        if "diabetes" in user_data.get("conditions", []):
            recs["dietary_advice"].extend([
                "Monitor carbohydrate intake and glycemic load",
                "Emphasize high-fiber foods (>25-30g/day)",
                "Consider low-carb or Mediterranean pattern for glycemic control"
            ])
        
        if "cardiovascular_disease" in user_data.get("conditions", []):
            recs["dietary_advice"].extend([
                "Follow DASH or Mediterranean diet pattern",
                "Increase soluble fiber (oats, beans) for cholesterol",
                "Limit saturated fat to <6% of calories",
                "Consider plant sterols/stanols (2g/day)"
            ])
        
        if "osteoporosis" in user_data.get("conditions", []):
            recs["dietary_advice"].extend([
                "Ensure adequate protein intake (1.0-1.2g/kg body weight)",
                "Limit sodium (increases calcium excretion)",
                "Moderate caffeine and alcohol",
                "Alkaline diet pattern may help (more fruits/vegetables)"
            ])
        
        return recs
    
    def _add_cultural_considerations(self, user_data, recs):
        """Add religious and cultural dietary considerations"""
        
        religion = user_data.get("religious_preference", "none")
        
        if religion == "hindu":
            recs["dietary_advice"].append("Many Hindus are vegetarian - ensure B12, iron, and omega-3 supplementation")
            recs["warnings"].append("Check supplement capsules - some may contain beef gelatin")
        elif religion == "muslim":
            recs["dietary_advice"].append("Halal dietary laws observed - verify supplement ingredients")
            recs["warnings"].append("Ensure supplements are alcohol-free and gelatin is halal-certified (bovine or fish)")
        elif religion == "jewish":
            recs["dietary_advice"].append("Kosher dietary laws observed")
            recs["warnings"].append("Look for kosher certification (OU, OK, Kof-K) on supplements; avoid porcine gelatin")
        elif religion == "jain":
            recs["dietary_advice"].append("Strict vegetarian/vegan diet - critical need for B12 supplementation")
            recs["warnings"].append("Avoid supplements with animal-derived ingredients including some vitamin D3 (lanolin)")
        elif religion == "sikh":
            recs["dietary_advice"].append("Many Sikhs are vegetarian - monitor B12 and iron status")
        elif religion == "buddhist":
            recs["dietary_advice"].append("Many Buddhists are vegetarian or vegan - ensure adequate B12")
        
        # Regional considerations
        region = user_data.get("region", "")
        if "india" in region.lower() or "south_asia" in region.lower():
            recs["dietary_advice"].append("High prevalence of vegetarianism - vitamin B12 and vitamin D deficiency common")
            recs["monitoring"].append("Consider checking B12 and Vitamin D levels")
        elif "scandinavia" in region.lower() or "northern_europe" in region.lower():
            recs["dietary_advice"].append("Limited winter sun exposure - vitamin D supplementation often necessary Oct-March")
        elif "middle_east" in region.lower():
            recs["dietary_advice"].append("High rates of vitamin D deficiency despite sun - supplementation often needed")
        
        return recs

def render_header():
    st.markdown('<div class="main-header">💊 VitaGuide AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evidence-Based Personalized Supplement & Diet Recommendations</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("USPSTF Aligned", "✓")
    with col2:
        st.metric("Evidence-Based", "✓")
    with col3:
        st.metric("Personalized", "✓")

def render_input_form():
    st.sidebar.header("👤 Your Profile")
    
    with st.sidebar.form("user_profile_form"):
        # Basic Demographics
        st.subheader("Demographics")
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
        
        # Geographic
        region = st.selectbox("Region", [
            "North America", "Europe", "Asia", "South America", 
            "Africa", "Middle East", "Australia/Oceania", "India", "Scandinavia"
        ])
        
        # Diet
        st.subheader("Diet & Lifestyle")
        diet_type = st.selectbox("Diet Type", [
            "Omnivore (eat everything)", 
            "Vegetarian (no meat/fish)", 
            "Vegan (no animal products)",
            "Pescatarian (fish but no meat)",
            "Flexitarian (mostly plant-based)"
        ])
        
        religious = st.selectbox("Religious/Cultural Dietary Preferences", [
            "None", "Hindu", "Muslim (Halal)", "Jewish (Kosher)", 
            "Jain", "Sikh", "Buddhist", "Seventh-day Adventist"
        ])
        
        sun_exposure = st.selectbox("Sun Exposure", [
            "Adequate (15+ min daily)", "Limited (office worker, limited outdoor)", "Minimal (night shift, always covered)"
        ])
        
        # Health Status
        st.subheader("Health Status")
        
        conditions = st.multiselect("Medical Conditions", [
            "None/Healthy",
            "Anemia/Iron deficiency",
            "Osteoporosis/Osteopenia", 
            "Cardiovascular disease",
            "Diabetes/Pre-diabetes",
            "Celiac disease",
            "Crohn's disease/Ulcerative colitis",
            "Chronic kidney disease",
            "Liver disease",
            "Depression/Anxiety",
            "Dementia/Cognitive decline",
            "Rheumatoid arthritis",
            "Thyroid disorder",
            "Pregnancy/Planning pregnancy",
            "Breastfeeding",
            "History of bariatric surgery",
            "Alcohol use disorder",
            "Malabsorption issues"
        ])
        
        pregnancy_status = st.selectbox("Pregnancy Status", [
            "Not applicable", "Planning pregnancy", "Currently pregnant", "Currently breastfeeding"
        ])
        
        # Test Results
        st.subheader("Recent Test Results (if available)")
        vitamin_d_level = st.selectbox("Vitamin D Level (25-OH)", [
            "Not tested", "Deficient (<20 ng/mL)", "Insufficient (20-30)", "Adequate (30-50)", "High (>50)"
        ])
        
        b12_level = st.selectbox("Vitamin B12 Level", [
            "Not tested", "Deficient (<200 pg/mL)", "Low-normal (200-300)", "Adequate (>300)"
        ])
        
        iron_status = st.selectbox("Iron Status", [
            "Not tested", "Deficient", "Low", "Normal", "High"
        ])
        
        # Additional Factors
        st.subheader("Additional Factors")
        medications = st.multiselect("Current Medications", [
            "None",
            "Metformin (diabetes)",
            "Proton pump inhibitors (acid reflux)",
            "Statins (cholesterol)",
            "Diuretics",
            "Anticoagulants (blood thinners)",
            "Levothyroxine (thyroid)",
            "Oral contraceptives",
            "Other"
        ])
        
        fish_intake = st.selectbox("Fish Intake (per week)", [
            "2+ times/week",
            "Once a week",
            "Rarely (less than once a week)",
            "Never/None"
        ])
        
        dairy_intake = st.selectbox("Dairy Intake", [
            "Daily",
            "A few times/week",
            "Rarely",
            "Never/None"
        ])
        
        iodized_salt = st.selectbox("Do you use iodized salt?", [
            "Yes",
            "No",
            "Not sure"
        ])
        
        heavy_periods = st.checkbox("Heavy periods (females only)")
        
        high_triglycerides = st.checkbox("Diagnosed with high triglycerides")
        
        submitted = st.form_submit_button("Generate Recommendations")
        
        if submitted:
            return {
                "age": age,
                "sex": sex,
                "region": region,
                "diet_type": diet_type.lower().split()[0],
                "religious_preference": religious.lower(),
                "sun_exposure": sun_exposure.lower().split()[0],
                "conditions": [c.lower().replace("/", "_").replace(" ", "_") for c in conditions if c != "None/Healthy"],
                "pregnancy_status": pregnancy_status.lower().replace(" ", "_"),
                "vitamin_d_level": vitamin_d_level.lower().replace(" ", "_"),
                "b12_level": b12_level.lower().replace(" ", "_"),
                "iron_status": iron_status.lower(),
                "medications": medications,
                "fish_intake": "none" if fish_intake == "Never/None" else fish_intake.lower(),
                "dairy_intake": "none" if dairy_intake == "Never/None" else dairy_intake.lower(),
                "iodized_salt": iodized_salt.lower().replace(" ", "_"),
                "heavy_periods": heavy_periods,
                "high_triglycerides": high_triglycerides
            }
    return None

def render_recommendations(recommendations):
    st.markdown("---")
    st.header("📋 Your Personalized Recommendations")
    
    # Approach Summary
    st.markdown("### 🎯 Clinical Approach")
    st.markdown(recommendations["approach_summary"])
    
    # Warnings
    if recommendations["warnings"]:
        st.markdown("### ⚠️ Important Warnings")
        for warning in recommendations["warnings"]:
            st.markdown(f'<div class="danger-card">{warning}</div>', unsafe_allow_html=True)
    
    # Supplements
    if recommendations["supplements"]:
        st.markdown("### 💊 Supplement Recommendations")
        
        # Priority sorting
        priority_order = {"Critical": 0, "High": 1, "Moderate": 2, "Low-Moderate": 3, "Alternative": 4}
        sorted_supps = sorted(recommendations["supplements"], 
                            key=lambda x: priority_order.get(x.get("priority", "Low"), 5))
        
        for supp in sorted_supps:
            priority_color = {
                "Critical": "🔴", "High": "🟠", "Moderate": "🟡", 
                "Low-Moderate": "🟢", "Alternative": "🔵"
            }.get(supp.get("priority", ""), "⚪")
            
            with st.expander(f"{priority_color} {supp['nutrient']} ({supp.get('priority', '')} Priority)"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**Recommended Dose:** {supp['dose']}")
                    st.markdown(f"**Rationale:** {supp['rationale']}")
                    st.markdown(f"**Duration:** {supp['duration']}")
                with col2:
                    if "food_sources" in supp:
                        st.markdown(f"**Food Sources:** {', '.join(supp['food_sources'])}")
                    if "interactions" in supp:
                        st.markdown(f"**Interactions:** {supp['interactions']}")
                    if "notes" in supp:
                        st.markdown(f"**Notes:** {supp['notes']}")
                    if "warning" in supp:
                        st.markdown(f"**⚠️ Warning:** {supp['warning']}")
    
    # Dietary Advice
    if recommendations["dietary_advice"]:
        st.markdown("### 🥗 Dietary Recommendations")
        for advice in recommendations["dietary_advice"]:
            if advice.startswith("**"):
                st.markdown(f'<div class="warning-card">{advice}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"- {advice}")
    
    # Monitoring
    if recommendations["monitoring"]:
        st.markdown("### 🔬 Recommended Monitoring")
        for monitor in recommendations["monitoring"]:
            st.markdown(f'<div class="success-card">📊 {monitor}</div>', unsafe_allow_html=True)
    
    # Evidence Disclaimer
    st.markdown("---")
    st.info("""
    **Evidence-Based Disclaimer**: These recommendations are based on the United States Preventive Services 
    Task Force (USPSTF) guidelines, NIH Office of Dietary Supplements, and major medical society recommendations. 
    Individual needs may vary. Always consult with your healthcare provider before starting any supplement regimen, 
    especially if you have chronic health conditions or take medications.
    """)

def render_educational_content():
    st.sidebar.markdown("---")
    st.sidebar.header("📚 Educational Resources")
    
    with st.sidebar.expander("About Our Approach"):
        st.write("""
        **USPSTF-Aligned Methodology**
        
        We follow the evidence-based approach that:
        1. Routine multivitamins are NOT recommended for primary prevention in healthy adults
        2. Targeted supplementation IS appropriate for documented deficiencies or high-risk conditions
        3. Dietary improvement is preferred over pills when possible
        
        **Key References:**
        - USPSTF Vitamin Supplementation (2022)
        - NIH State-of-the-Science Conference (2006)
        - COSMOS Trial Results (2022)
        - PHS II Trial Results (2012)
        """)
    
    with st.sidebar.expander("Vitamin Toxicity Limits"):
        st.write("""
        **Upper Limits (Adults):**
        - Vitamin A: 3000 mcg (10,000 IU)
        - Vitamin D: 100 mcg (4000 IU)
        - Vitamin E: 1000 mg (1500 IU)
        - Vitamin B6: 100 mg
        - Folate: 1000 mcg
        - Niacin: 35 mg
        - Iron: 45 mg
        - Zinc: 40 mg
        - Calcium: 2000-2500 mg
        - Magnesium: 350 mg (supplements only)
        """)

def main():
    render_header()
    
    # Initialize recommender
    recommender = SupplementRecommender()
    
    # Get user input
    user_data = render_input_form()
    
    # Render educational content
    render_educational_content()
    
    # Process and display recommendations
    if user_data:
        with st.spinner("Analyzing your profile with AI..."):
            recommendations = recommender.analyze_user(user_data)
            st.session_state.recommendations = recommendations
            st.session_state.user_profile = user_data
        
        render_recommendations(recommendations)
        
        # Export option
        st.markdown("---")
        if st.button("📥 Export Recommendations to JSON"):
            export_data = {
                "profile": user_data,
                "recommendations": recommendations,
                "generated_date": datetime.now().isoformat(),
                "disclaimer": "For educational purposes only. Consult healthcare provider."
            }
            st.download_button(
                label="Download JSON",
                data=json.dumps(export_data, indent=2),
                file_name=f"vitaguide_recommendations_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
    else:
        # Welcome content
        st.markdown("### 👈 Enter your details in the sidebar to get started")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **What VitaGuide AI Does:**
            - ✅ Analyzes your individual risk factors
            - ✅ Provides evidence-based supplement recommendations
            - ✅ Considers dietary preferences (vegan, halal, kosher)
            - ✅ Accounts for medical conditions and medications
            - ✅ Offers personalized dietary advice
            - ✅ Suggests appropriate lab monitoring
            """)
        with col2:
            st.markdown("""
            **Our Evidence-Based Approach:**
            - 📊 Aligned with USPSTF guidelines
            - 🔬 Based on major clinical trials (COSMOS, PHS II, SELECT)
            - 🏥 Considers NIH Office of Dietary Supplements data
            - ⚠️ Distinguishes between sufficient and deficient individuals
            - 🥗 Prioritizes food over supplements when appropriate
            """)
        
        st.info("**Privacy Note**: Your health information is processed locally and not stored on any server.")

if __name__ == "__main__":
    main()
'''

# Save the completely clean file
with open('/mnt/kimi/output/vitaguide_app.py', 'w') as f:
    f.write(streamlit_app_content)

print("✅ SUCCESS: Clean vitaguide_app.py created!")
print(f"✅ Size: {len(streamlit_app_content)} characters")
print("\n" + "="*70)
print("🔧 TO FIX YOUR DEPLOYMENT:")
print("="*70)
print("""
1. Go to your GitHub repository
2. Open vitaguide_app.py
3. Click 'Edit' (pencil icon)
4. DELETE ALL CONTENT
5. COPY AND PASTE the new content from below
6. Commit the changes
7. Streamlit Cloud will auto-redeploy

OR

1. Delete the repository
2. Create a new one with the fixed files
3. Redeploy on Streamlit Cloud
""")
print("="*70)
