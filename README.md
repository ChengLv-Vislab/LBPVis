# LBPVis Visual Analytics System

## Overview  
The **LBPVis visual analytics system** provides five interactive views to support learner behavior analysis:  
1. **Learner Profile View**  
2. **Abnormal Detection View**  
3. **Pattern Overview**  
4. **Pattern Explore View**  
5. **Pattern Compare View**  

To protect learners’ privacy, the original dataset has been replaced with randomly generated sample data.

The system adopts a **frontend–backend architecture**, where:  
- **Backend** is implemented with **Django**  
- **Frontend** is implemented with **Vue**  

---

## System Requirements  

- **Frontend**  
  - Vue: `2.5.2`  
  - Axios: `0.24.0`  
  - Node.js: `>= 6.0.0`  
  - Webpack: `3.6.0`  
  - npm: `>= 3.0.0`  

- **Backend**  
  - Python: `3.7.9`  
  - Django: `3.2.12`  

---

## Installation and Running  

### Backend (Django)  
```bash
# Navigate to backend folder
cd <backend-folder>

# Run Django server
python manage.py runserver
```

### Frontend (Vue)

```bash
# Navigate to frontend folder
cd <frontend-folder>

# Install dependencies
npm install

# Run development server
npm run dev
```
 





