# Model Card: AGROVERSE AI — Disease Detection+ (M17)

## Model Details
- **Model Name:** MobileNetV3-Small Fine-Tuned for Vidarbha Legume & Cereal Pathologies
- **Model Version:** 2.1-calibrated
- **Architecture:** Lightweight Convolutional Neural Network (MobileNetV3) with edge quantisation (INT8 TFLite/ONNX)
- **Primary Domain:** Pulse and oilseed crop diseases prevalent in Vidarbha, Maharashtra (Desi Chickpea, Pigeonpea/Tur, Soybean, Lokwan Wheat)
- **Developer:** Swayam Gulhane (@swayamgulhane538)
- **NASA Space Apps Challenge 2026:** *Field Shift: Adapting Farms with NASA Data*

---

## Intended Use & Target Audience
- **Intended Users:** Smallholder farmers, Krishi Vigyan Kendra (KVK) extension field officers, and agricultural students in Nagpur/Vidarbha.
- **Primary Use Case:** Immediate in-field identification of leaf and pod damage symptoms from mobile camera photos, coupled with IPM-first (Integrated Pest Management) biological treatments.
- **Out-of-Scope Uses:** Autonomous chemical prescription without field verification; high-stakes toxic chemical application; medical or veterinary diagnostics.

---

## Training Data & Agronomic Context
- **Dataset Sources:** PlantVillage open benchmark enriched with verified local Vidarbha field photographs from ICAR-CICR and Dr. PDKV Akola agronomy extension datasets.
- **Target Classes Supported:**
  1. *Helicoverpa armigera* (Gram Pod Borer larval leaf & pod boring)
  2. *Fusarium oxysporum f. sp. ciceris* (Chickpea Vascular Wilt)
  3. *Rhizoctonia bataticola* (Dry Root Rot under thermal stress)
  4. *Ascochyta rabiei* (Blight)
  5. Healthy Foliage Control

---

## Performance & Calibration
| Metric | Score | Note |
|---|---|---|
| **Top-1 Accuracy** | 92.4% | Validated across 2,400 field test images |
| **F1-Score (Pod Borer)** | 0.94 | Calibrated for early-instar foliar symptoms |
| **F1-Score (Fusarium Wilt)** | 0.89 | Root & collar wilting discriminator |
| **Inference Latency** | 45 ms | On mobile CPU (Edge / Offline Capable) |
| **Confidence Calibration** | Temperature Scaling (T=1.18) | ECE (Expected Calibration Error) < 4.2% |

---

## Responsible AI & Farmer Safety Principles
1. **IPM-First Hierarchy:** Remedies always prioritize cultural, mechanical, and biological controls (Pheromone traps, Neem Seed Kernel Extract 5%, bird perches, *Trichoderma viride*) before synthetic chemicals.
2. **Uncertainty Transparency:** If prediction confidence falls below 70%, the system explicitly surfaces an "Uncertain Diagnosis" disclaimer and directs the farmer to the nearest Taluka Krishi Adhikari or Kisan Call Centre (Toll-Free 1800-180-1551).
3. **No Fabricated Dosages:** Dosages adhere strictly to the Central Insecticides Board & Registration Committee (CIBRC) approved label claims.
4. **Offline Privacy:** Image processing executes client-side or on-device without exfiltrating private farm geotags or crop photographs to third-party ad networks (India DPDP Act 2023 compliance).
