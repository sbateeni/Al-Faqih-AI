from typing import Dict, Any

class InheritanceCalculator:
    def __init__(self):
        self.madhab_rules = {
            'hanafi': {
                'name': 'المذهب الحنفي',
                'special_rules': 'يختص المذهب الحنفي بقواعد خاصة في الحجب والعول والرد'
            },
            'maliki': {
                'name': 'المذهب المالكي',
                'special_rules': 'يتميز المذهب المالكي بقواعد خاصة في التعصيب والحجب'
            },
            'shafii': {
                'name': 'المذهب الشافعي',
                'special_rules': 'للمذهب الشافعي قواعد مميزة في ميراث ذوي الأرحام'
            },
            'hanbali': {
                'name': 'المذهب الحنبلي',
                'special_rules': 'يتفرد المذهب الحنبلي بقواعد خاصة في الرد والعول'
            }
        }

    def calculate_shares(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        حساب أنصبة الورثة حسب المذهب المختار
        """
        estate = float(data['total_estate'])  # القيمة الإجمالية بالدولار
        shares = {}
        explanation = []
        total_shares = 0

        # حساب نصيب الزوج/الزوجة
        if data['deceased'] == 'male' and int(data['wives']) > 0:
            wives_share = self._calculate_wives_share(estate, int(data['wives']), 
                                                   bool(int(data['sons']) or int(data['daughters'])))
            shares['الزوجات'] = wives_share
            total_shares += wives_share['amount']
            explanation.append(f"نصيب الزوجات: {wives_share['percentage']}")
        elif data['deceased'] == 'female' and data['husband']:
            husband_share = self._calculate_husband_share(estate, 
                                                       bool(int(data['sons']) or int(data['daughters'])))
            shares['الزوج'] = husband_share
            total_shares += husband_share['amount']
            explanation.append(f"نصيب الزوج: {husband_share['percentage']}")

        # حساب نصيب الأب
        if data['father']:
            father_share = self._calculate_father_share(estate, 
                                                     bool(int(data['sons']) or int(data['daughters'])))
            shares['الأب'] = father_share
            total_shares += father_share['amount']
            explanation.append(f"نصيب الأب: {father_share['percentage']}")

        # حساب نصيب الأم
        if data['mother']:
            mother_share = self._calculate_mother_share(estate, 
                                                     bool(int(data['sons']) or int(data['daughters'])))
            shares['الأم'] = mother_share
            total_shares += mother_share['amount']
            explanation.append(f"نصيب الأم: {mother_share['percentage']}")

        # حساب نصيب الأبناء والبنات
        children_shares = self._calculate_children_shares(estate - total_shares, 
                                                       int(data['sons']), 
                                                       int(data['daughters']))
        shares.update(children_shares['shares'])
        explanation.extend(children_shares['explanation'])

        # إضافة تفاصيل المذهب
        madhab_details = self._get_madhab_details(data['madhab'])

        return {
            'shares': shares,
            'total': estate,
            'explanation': ' '.join(explanation),
            'madhabDetails': madhab_details
        }

    def _calculate_wives_share(self, estate: float, num_wives: int, has_children: bool) -> Dict[str, Any]:
        """حساب نصيب الزوجات"""
        percentage = "1/8" if has_children else "1/4"
        fraction = 1/8 if has_children else 1/4
        amount = (estate * fraction) / num_wives
        return {
            'percentage': percentage,
            'amount': amount * num_wives
        }

    def _calculate_husband_share(self, estate: float, has_children: bool) -> Dict[str, Any]:
        """حساب نصيب الزوج"""
        percentage = "1/4" if has_children else "1/2"
        fraction = 1/4 if has_children else 1/2
        return {
            'percentage': percentage,
            'amount': estate * fraction
        }

    def _calculate_father_share(self, estate: float, has_children: bool) -> Dict[str, Any]:
        """حساب نصيب الأب"""
        percentage = "1/6" if has_children else "الباقي بالتعصيب"
        fraction = 1/6 if has_children else 1
        return {
            'percentage': percentage,
            'amount': estate * fraction
        }

    def _calculate_mother_share(self, estate: float, has_children: bool) -> Dict[str, Any]:
        """حساب نصيب الأم"""
        percentage = "1/6" if has_children else "1/3"
        fraction = 1/6 if has_children else 1/3
        return {
            'percentage': percentage,
            'amount': estate * fraction
        }

    def _calculate_children_shares(self, remaining_estate: float, num_sons: int, num_daughters: int) -> Dict[str, Any]:
        """حساب أنصبة الأبناء والبنات"""
        shares = {}
        explanation = []
        
        if num_sons == 0 and num_daughters == 0:
            return {'shares': shares, 'explanation': explanation}

        total_shares = (num_sons * 2) + num_daughters  # الذكر مثل حظ الأنثيين
        share_value = remaining_estate / total_shares

        if num_sons > 0:
            son_share = share_value * 2
            shares['الأبناء'] = {
                'percentage': f"{num_sons * 2}/{total_shares}",
                'amount': son_share * num_sons
            }
            explanation.append(f"نصيب كل ابن: {son_share}")

        if num_daughters > 0:
            daughter_share = share_value
            shares['البنات'] = {
                'percentage': f"{num_daughters}/{total_shares}",
                'amount': daughter_share * num_daughters
            }
            explanation.append(f"نصيب كل بنت: {daughter_share}")

        return {'shares': shares, 'explanation': explanation}

    def _get_madhab_details(self, madhab: str) -> str:
        """الحصول على تفاصيل المذهب المختار"""
        if madhab == 'all':
            details = []
            for m in self.madhab_rules.values():
                details.append(f"<p><strong>{m['name']}:</strong> {m['special_rules']}</p>")
            return ''.join(details)
        elif madhab in self.madhab_rules:
            m = self.madhab_rules[madhab]
            return f"<p><strong>{m['name']}:</strong> {m['special_rules']}</p>"
        return ""
