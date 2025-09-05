import logging
import logging
from typing import Dict, List, Optional
from madhahib import get_madhhab, get_all_madhahib, MADHAHIB

logger = logging.getLogger(__name__)

class MadhahibService:
    """Service class to handle all madhhab-related operations"""
    
    def __init__(self):
        self.madhahib = MADHAHIB
    
    def get_available_madhahib(self) -> List[str]:
        """Get list of available madhhab names"""
        return list(self.madhahib.keys())
    
    def get_madhhab_info(self, madhhab_name: str) -> Optional[Dict]:
        """Get basic information about a specific madhhab"""
        madhhab = get_madhhab(madhhab_name)
        if madhhab:
            return madhhab.get_basic_info()
        return None
    
    def get_single_madhhab_response(self, madhhab_name: str, question: str, api_key: str) -> str:
        """Get response from a single madhhab"""
        try:
            madhhab = get_madhhab(madhhab_name)
            if not madhhab:
                return f"المذهب {madhhab_name} غير متوفر"
            
            # Use sync method since Gemini API doesn't support async
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
            
            prompt = madhhab.build_prompt(question)
            response = model.generate_content(prompt)
            
            if response and response.text:
                logger.info(f"Successfully received response from {madhhab_name}")
                return response.text
            else:
                logger.warning(f"Empty response from {madhhab_name}")
                return f"عذراً، لم أتمكن من الحصول على إجابة من المذهب {madhhab_name}"
            
        except Exception as e:
            logger.error(f"Error getting response from {madhhab_name}: {str(e)}")
            return f"حدث خطأ أثناء الحصول على إجابة من المذهب {madhhab_name}: {str(e)}"
    
    def get_all_madhahib_responses(self, question: str, api_key: str) -> Dict[str, str]:
        """Get responses from all madhahib sequentially"""
        try:
            all_madhahib = get_all_madhahib()
            results = {}
            
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.0-flash-001')
            
            for madhhab_name, madhhab_instance in all_madhahib.items():
                try:
                    logger.info(f"Getting response from {madhhab_name}...")
                    prompt = madhhab_instance.build_prompt(question)
                    response = model.generate_content(prompt)
                    
                    if response and response.text:
                        results[madhhab_name] = response.text
                        logger.info(f"Successfully received response from {madhhab_name}")
                    else:
                        results[madhhab_name] = f"عذراً، لم أتمكن من الحصول على إجابة من المذهب {madhhab_name}"
                        logger.warning(f"Empty response from {madhhab_name}")
                        
                except Exception as e:
                    logger.error(f"Error getting response from {madhhab_name}: {str(e)}")
                    results[madhhab_name] = f"حدث خطأ أثناء الحصول على إجابة من المذهب {madhhab_name}"
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting responses from all madhahib: {str(e)}")
            return {"error": f"حدث خطأ أثناء الحصول على الإجابات: {str(e)}"}
    
    def format_combined_response(self, responses: Dict[str, str]) -> str:
        """Format multiple madhhab responses into a single combined response"""
        combined_answer = ""
        
        for madhhab_name, answer in responses.items():
            if madhhab_name != "error":
                combined_answer += f"\n\n{'='*50}\n"
                combined_answer += f"إجابة المذهب {madhhab_name}\n"
                combined_answer += f"{'='*50}\n\n"
                combined_answer += answer
        
        if "error" in responses:
            combined_answer += f"\n\n⚠️ تنبيه: {responses['error']}"
        
        return combined_answer
    
    def get_madhhab_comparison(self, madhhab_names: List[str]) -> Dict[str, Dict]:
        """Compare specific madhahib and return their key differences"""
        comparison = {}
        
        for madhhab_name in madhhab_names:
            madhhab = get_madhhab(madhhab_name)
            if madhhab:
                comparison[madhhab_name] = {
                    'methodology': madhhab.get_methodology(),
                    'main_sources': madhhab.main_sources,
                    'famous_scholars': madhhab.famous_scholars[:3],  # Top 3 scholars
                    'geographic_influence': madhhab.geographic_influence[:3]  # Top 3 regions
                }
        
        return comparison