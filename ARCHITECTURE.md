# Al-Faqih AI - Modular Architecture Documentation

## 📁 Project Structure

```
Al-Faqih-AI/
├── app.py                      # Main Flask application
├── madhhab_service.py          # Service layer for madhhab operations
├── madhahib/                   # Madhahib package (NEW MODULAR STRUCTURE)
│   ├── __init__.py            # Package initialization & registry
│   ├── base_madhhab.py        # Base class for all madhahib
│   ├── hanafi/                # Hanafi madhhab module
│   │   ├── __init__.py
│   │   └── hanafi_madhhab.py  # Hanafi implementation
│   ├── maliki/                # Maliki madhhab module
│   │   ├── __init__.py
│   │   └── maliki_madhhab.py  # Maliki implementation
│   ├── shafii/                # Shafii madhhab module
│   │   ├── __init__.py
│   │   └── shafii_madhhab.py  # Shafii implementation
│   └── hanbali/               # Hanbali madhhab module
│       ├── __init__.py
│       └── hanbali_madhhab.py # Hanbali implementation
├── templates/                  # HTML templates
├── static/                     # Static assets
└── requirements.txt           # Dependencies
```

## 🏗️ Architecture Overview

### 1. **Modular Madhhab System**

Each Islamic school of jurisprudence (madhhab) now has its own dedicated module with:

- **Separate files and folders** for easy maintenance
- **Specialized knowledge** about methodology, scholars, and geographic influence
- **Custom prompt building** tailored to each madhhab's characteristics
- **Independent response generation** with madhhab-specific context

### 2. **Base Madhhab Class** (`base_madhhab.py`)

```python
class BaseMadhhab(ABC):
    """Base class for all Islamic madhahib"""
    
    # Core attributes
    name: str                    # English name
    arabic_name: str            # Arabic name
    founder: str                # Founder's name
    founding_period: str        # Historical period
    main_sources: List[str]     # Primary sources of jurisprudence
    methodology: str            # Approach to Islamic law
    geographic_influence: List[str]  # Regions of influence
    famous_scholars: List[str]  # Notable scholars
    
    # Abstract methods (must be implemented)
    @abstractmethod
    def get_introduction(self)
    def get_methodology(self)
    def get_famous_scholars(self)
    
    # Common methods
    def build_prompt(self, question)      # Custom prompt for each madhhab
    def get_response(self, question, api_key)  # Generate AI response
```

### 3. **Individual Madhhab Modules**

#### **Hanafi Madhhab** (`madhahib/hanafi/`)
- **Specialty**: Flexibility in application, emphasis on reason and analogy
- **Key Features**: Istihsan (juristic preference), 'Urf (custom)
- **Geographic Influence**: Turkey, Central Asia, India, Pakistan

#### **Maliki Madhhab** (`madhahib/maliki/`)
- **Specialty**: Practice of Medina residents, public interest
- **Key Features**: 'Amal Ahl al-Medina, Maslaha Mursala, Sadd al-Dhara'i
- **Geographic Influence**: North & West Africa

#### **Shafii Madhhab** (`madhahib/shafii/`)
- **Specialty**: Balance between Hadith and Reason, systematic methodology
- **Key Features**: Four sources only, clarity in evidence
- **Geographic Influence**: Egypt, Southeast Asia, East Africa

#### **Hanbali Madhhab** (`madhahib/hanbali/`)
- **Specialty**: Strict adherence to texts, minimal personal opinion
- **Key Features**: Companions' opinions, literal interpretation
- **Geographic Influence**: Saudi Arabia, Gulf countries

### 4. **Service Layer** (`madhhab_service.py`)

The `MadhahibService` class provides:

```python
class MadhahibService:
    # Single madhhab operations
    def get_single_madhhab_response(madhhab_name, question, api_key)
    
    # Multiple madhhab operations  
    def get_all_madhahib_responses(question, api_key)
    def format_combined_response(responses)
    
    # Utility functions
    def get_available_madhahib()
    def get_madhhab_info(madhhab_name)
    def get_madhhab_comparison(madhhab_names)
```

## 🚀 Features

### ✅ **Enhanced User Experience**

1. **Individual Madhhab Responses**: Each madhhab speaks for itself with "أنا المذهب [المذهب]..."
2. **Specialized Knowledge**: Each madhhab provides responses based on its unique methodology
3. **Comparative Analysis**: When selecting "جميع المذاهب", get responses from all four schools
4. **Beautiful Formatting**: Clean, organized display of multiple responses

### ✅ **Maintainability Benefits**

1. **Separation of Concerns**: Each madhhab in its own module
2. **Easy Extension**: Add new madhahib by creating new modules
3. **Independent Development**: Modify one madhhab without affecting others
4. **Clean Code Structure**: Inheritance-based design with clear abstractions
5. **Testability**: Each madhhab can be tested independently

### ✅ **Scalability**

1. **Plugin Architecture**: New Islamic schools can be added easily
2. **Configuration Management**: Each madhhab manages its own configuration
3. **Performance**: Responses can be cached per madhhab
4. **Parallel Processing**: Future enhancement for concurrent responses

## 🛠️ Adding New Madhahib

To add a new madhhab (e.g., Zahiri):

1. **Create the module structure**:
   ```
   madhahib/zahiri/
   ├── __init__.py
   └── zahiri_madhhab.py
   ```

2. **Implement the madhhab class**:
   ```python
   from ..base_madhhab import BaseMadhhab
   
   class ZahiriMadhhab(BaseMadhhab):
       def __init__(self):
           super().__init__()
           self.name = "Zahiri"
           self.arabic_name = "الظاهري"
           # ... other attributes
   ```

3. **Register in the main package**:
   ```python
   # In madhahib/__init__.py
   from .zahiri.zahiri_madhhab import ZahiriMadhhab
   
   MADHAHIB = {
       # ... existing madhahib
       'الظاهري': ZahiriMadhhab
   }
   ```

## 📈 Performance Improvements

1. **Modular Loading**: Only load required madhahib
2. **Specialized Prompts**: Each madhhab has optimized prompts
3. **Better Error Handling**: Isolated error handling per madhhab
4. **Logging**: Detailed logging for each madhhab operation

## 🔧 Technical Benefits

1. **Type Safety**: Full type hints for better IDE support
2. **Abstract Base Classes**: Enforced interface compliance
3. **Service Pattern**: Clean separation between web layer and business logic
4. **Configuration Management**: Each madhhab manages its own settings
5. **Easy Testing**: Mockable service layer and isolated modules

This modular architecture makes the Al-Faqih AI system much more maintainable, scalable, and easier to extend with new Islamic schools of jurisprudence!