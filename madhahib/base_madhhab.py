from abc import ABC, abstractmethod
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class BaseMadhhab(ABC):
    """Base class for all Islamic madhahib (schools of jurisprudence)"""
    
    def __init__(self):
        self.name = ""
        self.arabic_name = ""
        self.founder = ""
        self.founding_period = ""
        self.main_sources = []
        self.methodology = ""
        self.geographic_influence = []
        self.famous_scholars = []
        
    @abstractmethod
    def get_introduction(self):
        """Return an introduction about this madhhab"""
        pass
    
    @abstractmethod
    def get_methodology(self):
        """Return the methodology of this madhhab"""
        pass
    
    @abstractmethod
    def get_famous_scholars(self):
        """Return famous scholars of this madhhab"""
        pass
    
    def get_basic_info(self):
        """Return basic information about the madhhab"""
        return {
            'name': self.name,
            'arabic_name': self.arabic_name,
            'founder': self.founder,
            'founding_period': self.founding_period,
            'main_sources': self.main_sources,
            'methodology': self.methodology,
            'geographic_influence': self.geographic_influence,
            'famous_scholars': self.famous_scholars
        }
    
    def build_prompt(self, question):
        """Build a specialized prompt for this madhhab"""
        return f"""أنا عالم إسلامي متخصص في المذهب {self.arabic_name}. 
        تحدث باسم المذهب {self.arabic_name} وأجب على السؤال التالي من منظور هذا المذهب:
        
        السؤال: {question}
        
        ابدأ إجابتك بـ: "أنا المذهب {self.arabic_name}..."
        وتحدث بصيغة المتكلم كأنك المذهب نفسه.
        
        يجب أن تتضمن الإجابة:
        1. تعريف بالمذهب ومؤسسه ({self.founder})
        2. الحكم الشرعي حسب هذا المذهب
        3. الدليل من القرآن أو السنة
        4. أقوال علماء هذا المذهب
        5. المنهجية المميزة لهذا المذهب في الاستنباط
        6. التعليل والحكمة"""
    
    def get_response(self, question, api_key):
        """Get a response from this madhhab for the given question"""
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
            
            prompt = self.build_prompt(question)
            response = model.generate_content(prompt)
            
            if response and response.text:
                logger.info(f"Successfully received response from {self.arabic_name}")
                return response.text
            else:
                logger.warning(f"Empty response from {self.arabic_name}")
                return f"عذراً، لم أتمكن من الحصول على إجابة من المذهب {self.arabic_name}"
                
        except Exception as e:
            logger.error(f"Error getting response from {self.arabic_name}: {str(e)}")
            return f"حدث خطأ أثناء الحصول على إجابة من المذهب {self.arabic_name}: {str(e)}"