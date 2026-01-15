# OCEGS Presentation PPT Prompt Plan

> **Project Name**: OCEGS (Online Consultation and Emergency Guidance System)  
> **Presentation Duration**: 30 minutes (8-10 min PPT + 10-12 min Demo + 8-10 min Q&A)  
> **Team Size**: 4 members  
> **Course**: CPC354W

---

## Overall Design Requirements

- **Style**: Modern, clean, professional medical/healthcare theme
- **Color Palette**: Blue/Teal primary (#0ea5e9, #14b8a6) with white backgrounds and subtle gradients
- **Typography**: Clean sans-serif fonts (e.g., Inter, Roboto, or system fonts)
- **Icons**: Use healthcare-related icons (heart rate, stethoscope, emergency, AI brain)
- **Animations**: Subtle fade-in transitions, professional and minimal

---

## Slide-by-Slide Content

---

### Slide 1: Cover Page

**Title**: OCEGS  
**Subtitle**: Online Consultation and Emergency Guidance System

**Content**:
- Project Logo (AI + Medical Cross combined icon)
- Team Members: [Ma,Jiajun], [Zhang,Yunfan], [Chen,Xiangtong], [Wei,Shengwei]
- Course: CPC354W
- Date: January 2026

**Visual Elements**:
- Large, centered project name
- Subtle medical/tech background pattern
- University logo (if applicable)

---

### Slide 2: Problem Background

**Title**: Why Do We Need This System?

**Content (Bullet Points)**:
1. **Limited Access in Malaysia**: Lack of free, intelligent online medical consultation systems
2. **Traditional Solutions Are Costly**: Existing services are paid online doctor consultations with high barriers
3. **Time Constraints**: Difficult to get medical advice outside of working hours
4. **Geographic & Economic Inequality**: Rural areas and low-income populations struggle to access healthcare resources

**Visual Elements**:
- Icon: Clock with "24/7" crossed out
- Icon: Dollar sign / wallet with restriction
- Icon: Map pin with question mark
- Simple infographic or statistics (if available)

---

### Slide 3: Our Solution & SDG Alignment

**Title**: OCEGS - Healthcare for Everyone, Anytime, Anywhere

**Content**:

| SDG Goal | Target | How OCEGS Achieves It |
|----------|--------|----------------------|
| 🎯 **SDG 3** | Good Health and Well-being | 24/7 AI-powered triage, professional consultation, emergency guidance |
| 🤝 **SDG 10** | Reduced Inequalities | Free access, no time/location restrictions, equal healthcare support for all |

**Core Philosophy**:
> *"Providing relatively professional medical support to anyone, anytime, anywhere."*

**Visual Elements**:
- SDG 3 and SDG 10 official icons/badges
- World map or globe with connection lines
- Equality symbol with medical cross

---

### Slide 4: System Overview

**Title**: Core Features at a Glance

**Content (4 Feature Cards)**:

1. **🏥 AI Triage System**
   - Automatic severity classification (Level 1-5)
   - Smart department recommendations

2. **👨‍⚕️ AI Expert Panel**
   - 12 specialized AI doctors
   - Multi-round collaborative discussions

3. **🚨 Emergency Guidance**
   - Real-time rescue instructions
   - Auto-matched local emergency numbers (911, 120, 999)

4. **⚙️ Admin Dashboard**
   - AI provider configuration
   - Doctor team management

**Visual Elements**:
- 4 cards layout with icons
- Color-coded severity badges
- Flow arrows connecting features

---

### Slide 5: System Architecture

**Title**: Technical Architecture

**Content (Architecture Diagram)**:

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│              Vue 3 + Vite + Pinia + Ant Design               │
└─────────────────────────┬───────────────────────────────────┘
                          │ REST API / WebSocket
┌─────────────────────────▼───────────────────────────────────┐
│                        BACKEND                               │
│                  Python FastAPI (Async)                      │
│  ┌─────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐  │
│  │  Auth   │  │  AI Doctor  │  │  Emergency  │  │ Admin  │  │
│  │  JWT    │  │   Module    │  │   Module    │  │ Panel  │  │
│  └─────────┘  └─────────────┘  └─────────────┘  └────────┘  │
└─────────────────────────┬───────────────────────────────────┘
            │                         │
            ▼                         ▼
   ┌─────────────────┐    ┌─────────────────────────┐
   │   PostgreSQL    │    │     AI Services         │
   │    Database     │    │  ┌──────────────────┐   │
   └─────────────────┘    │  │   SiliconFlow    │   │
                          │  │   OpenAI         │   │
                          │  │   Anthropic      │   │
                          │  │   Gemini         │   │
                          │  └──────────────────┘   │
                          └─────────────────────────┘
```

**Tech Stack Summary**:
| Layer | Technologies |
|-------|-------------|
| Frontend | Vue 3, Vite, Pinia, Ant Design Vue |
| Backend | Python 3.11+, FastAPI, SQLAlchemy 2.0 |
| Database | PostgreSQL 15+ |
| AI Integration | OpenAI-compatible API (SiliconFlow, OpenAI, etc.) |
| Security | JWT Authentication, bcrypt |

---

### Slide 6: Core Feature 1 - AI Triage

**Title**: Intelligent Triage System

**Content**:

**How It Works**:
1. User inputs chief complaint (symptoms)
2. AI analyzes severity level (1-5)
3. System provides preliminary diagnosis suggestions
4. Recommends appropriate medical departments

**Severity Levels**:
| Level | Priority | Example | Action |
|-------|----------|---------|--------|
| 1 | Non-urgent | Minor cold | Standard consultation |
| 2 | Low | Mild allergies | AI consultation |
| 3 | Medium | Persistent pain | AI + Doctor visit suggested |
| 4 | High | Severe symptoms | Priority handling |
| 5 | Emergency | Chest pain, breathing difficulty | **Red Alert + Emergency Guidance** |

**Visual Elements**:
- Severity color gradient (green → yellow → orange → red → dark red)
- Flow diagram showing triage process
- Sample UI screenshot (if available)

---

### Slide 7: Core Feature 2 - AI Expert Panel

**Title**: Multi-Specialist AI Consultation

**Content**:

**12 Specialized AI Doctors**:
| Category | Specialties |
|----------|-------------|
| Cardiology | Heart & cardiovascular issues |
| Neurology | Brain & nervous system |
| Pediatrics | Children's health |
| Dermatology | Skin conditions |
| Orthopedics | Bone & joint problems |
| Gastroenterology | Digestive system |
| Pulmonology | Respiratory issues |
| Endocrinology | Hormonal disorders |
| Urology | Urinary system |
| Ophthalmology | Eye conditions |
| ENT | Ear, nose, throat |
| General Medicine | Overall health |

**Multi-Round Discussion Process**:
1. **Symptom Analysis**: Initial assessment by matched specialists
2. **Cross-Consultation**: Specialists discuss and share perspectives
3. **Consensus Building**: Multi-round discussions to refine diagnosis

**Visual Elements**:
- Grid of doctor avatars with specialty icons
- Discussion flow diagram
- Sample chat interface screenshot

---

### Slide 8: Core Feature 3 - Emergency Guidance

**Title**: Emergency Response Module

**Content**:

**When Severity = 5 (Emergency)**:

1. **🚨 Immediate Alert**
   - Red warning interface activates
   - Clear, calm emergency instructions displayed

2. **📍 Location-Based Emergency Numbers**
   - Auto-detects user location via IP
   - Displays local emergency numbers:
     - Malaysia: 999 / 112
     - China: 120
     - US/International: 911

3. **📞 One-Click Call**
   - Direct call button for emergency services
   - Quick access to emergency contacts

4. **📋 First Aid Instructions**
   - Step-by-step rescue guidance
   - Large fonts, clear visuals for stress situations

**Visual Elements**:
- Emergency alert UI mockup
- World map with emergency number pins
- One-click call button design

---

### Slide 9: Security & Admin System

**Title**: Security & Administration

**Content**:

**Security Features**:
- **JWT Authentication**: Secure token-based user sessions
- **Password Encryption**: bcrypt hashing for all passwords
- **Role-Based Access Control**: Patient / Admin roles
- **API Protection**: Protected endpoints with token validation

**Admin Dashboard Features**:
| Function | Description |
|----------|-------------|
| System Status | View total users, consultations, active sessions |
| AI Provider Config | Configure API Keys (OpenAI / Anthropic / Gemini / SiliconFlow) |
| Default Model Settings | Select default AI provider and model |
| Doctor Team Management | Enable/disable AI doctors, configure individual models |

**Visual Elements**:
- Security flow diagram (JWT token lifecycle)
- Admin panel screenshot
- Lock/shield icons for security points

---

### Slide 10: Team Contributions

**Title**: Team Division of Work

**Content**:

| Member | Role | Responsibilities |
|--------|------|-----------------|
| **Member 1** | [Role] | [Specific modules/features developed] |
| **Member 2** | [Role] | [Specific modules/features developed] |
| **Member 3** | [Role] | [Specific modules/features developed] |
| **Member 4** | [Role] | [Specific modules/features developed] |

**Collaboration Highlights**:
- Code version control with Git
- Regular team meetings and code reviews
- Modular development approach

**Visual Elements**:
- Team member photos or avatars
- Responsibility diagram/matrix
- GitHub contribution graph (optional)

---

### Slide 11: Project Achievements & Future

**Title**: Achievements & Future Roadmap

**Content**:

**✅ What We Achieved**:
- Complete user authentication system
- AI-powered triage with 5-level severity
- Multi-specialist AI consultation panel
- Emergency guidance with location-based support
- Fully functional admin dashboard
- Secure, scalable architecture

**📚 What We Learned**:
- Full-stack development with Vue 3 + FastAPI
- AI integration and prompt engineering
- Healthcare system design considerations
- Team collaboration and project management

**🚀 Future Improvements**:
- Mobile app version (iOS/Android)
- Voice/video consultation support
- Multi-language support (Malay, Chinese, Tamil)
- Integration with real hospital systems

**Visual Elements**:
- Checkmark list for achievements
- Learning icons (books, lightbulb)
- Roadmap timeline for future plans

---

### Slide 12: Live Demo

**Title**: Live Demonstration

**Content**:
- Large "DEMO" text or icon
- Brief demo outline:
  1. User registration & login
  2. Normal consultation flow ("Slight cold, sore throat")
  3. Emergency case ("Sudden severe chest pain, breathing difficulty")
  4. Admin panel walkthrough

**Visual Elements**:
- Play button icon
- Demo flow diagram
- "Now let's see it in action!" tagline

---

### Slide 13: Q&A

**Title**: Questions & Answers

**Content**:
- Large "Q&A" or question mark icon
- "Thank you for listening!"
- Contact information (optional)
- GitHub repository link (optional)

**Visual Elements**:
- Question mark icons
- Team email or contact info
- "We're happy to answer your questions"

---

## Demo Script Suggestions

### Demo Case 1: Normal Flow
```
Input: "I have a slight cold and sore throat"
Expected: 
- Triage Level: 1-2 (Non-urgent)
- Recommendation: General Medicine
- AI consultation proceeds normally
```

### Demo Case 2: Emergency Flow
```
Input: "Sudden severe chest pain just now, having trouble breathing"
Expected:
- Triage Level: 5 (Emergency)
- Red alert warning triggered
- Emergency guidance displayed
- Local emergency number shown
```

---

## Q&A Preparation Topics

1. **SDG Alignment**: How specifically does OCEGS contribute to SDG 3 and SDG 10?
2. **AI Accuracy**: How do you ensure the AI provides accurate medical advice?
3. **Liability**: Who is responsible if the AI gives wrong advice?
4. **Data Privacy**: How is patient medical data protected?
5. **Scalability**: Can this system handle many concurrent users?
6. **Monetization**: What is the business model if it's free?
7. **Differentiation**: What makes OCEGS different from existing solutions?
8. **Testing**: How was the system tested and validated?

---

## Presentation Time Allocation

| Section | Time | Presenter |
|---------|------|-----------|
| Slides 1-4 (Intro & Problem) | 3 min | Member 1 |
| Slides 5-6 (Architecture & Triage) | 2 min | Member 2 |
| Slides 7-8 (AI Panel & Emergency) | 2 min | Member 3 |
| Slides 9-11 (Security & Summary) | 2 min | Member 4 |
| Slide 12: Live Demo | 10-12 min | All (rotate) |
| Slide 13: Q&A | 8-10 min | All |

---

## Notes for PPT Generator

1. Use consistent color theme throughout (medical blue/teal)
2. Include presenter notes for each slide
3. Add subtle animations (fade-in preferred)
4. Ensure text is large enough for presentation (min 24pt)
5. Use high-quality icons from medical/tech icon packs
6. Include slide numbers
7. Add a progress bar or section indicator if possible
