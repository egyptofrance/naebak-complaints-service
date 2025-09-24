#!/usr/bin/env python3
"""
فاحص صدق رسائل الـ commit
يمنع المبالغة والتجميل في رسائل الـ commit
"""

import sys
import re
from pathlib import Path


class CommitHonestyChecker:
    """فاحص صدق رسائل الـ commit"""
    
    # كلمات مبالغة محظورة
    EXAGGERATION_WORDS = [
        "perfect", "مثالي", "كامل", "تماماً", "بشكل مثالي",
        "amazing", "رائع", "مذهل", "incredible", "fantastic",
        "flawless", "خالي من العيوب", "بدون أخطاء",
        "100% working", "يعمل 100%", "fully tested", "مختبر بالكامل",
        "bug-free", "خالي من الأخطاء", "production ready", "جاهز للإنتاج",
        "enterprise grade", "مستوى المؤسسات", "world class", "عالمي المستوى",
        "revolutionary", "ثوري", "groundbreaking", "مبتكر",
        "state-of-the-art", "أحدث التقنيات", "cutting edge", "متطور",
        "bulletproof", "محصن", "rock solid", "صلب كالصخر",
        "lightning fast", "سريع كالبرق", "blazing fast", "سريع جداً",
        "ultra", "فائق", "super", "سوبر", "mega", "ضخم",
        "ultimate", "نهائي", "supreme", "أعلى", "premium", "متميز"
    ]
    
    # عبارات مبالغة محظورة
    EXAGGERATION_PHRASES = [
        "works perfectly", "يعمل بشكل مثالي",
        "no issues", "بدون مشاكل", "zero bugs", "صفر أخطاء",
        "completely fixed", "تم إصلاحه بالكامل",
        "fully implemented", "تم تطبيقه بالكامل",
        "ready for production", "جاهز للإنتاج",
        "enterprise ready", "جاهز للمؤسسات",
        "battle tested", "مختبر في المعارك",
        "industry standard", "معيار الصناعة",
        "best practice", "أفضل الممارسات",
        "world class", "مستوى عالمي",
        "next generation", "الجيل القادم",
        "revolutionary approach", "نهج ثوري",
        "game changer", "مغير اللعبة",
        "breakthrough solution", "حل مبتكر"
    ]
    
    # كلمات صادقة مطلوبة
    HONEST_WORDS = [
        "fix", "إصلاح", "improve", "تحسين", "update", "تحديث",
        "add", "إضافة", "remove", "إزالة", "refactor", "إعادة هيكلة",
        "test", "اختبار", "debug", "تصحيح", "patch", "رقعة",
        "partial", "جزئي", "initial", "أولي", "basic", "أساسي",
        "draft", "مسودة", "wip", "work in progress", "قيد العمل",
        "attempt", "محاولة", "try", "تجربة", "experiment", "تجريب"
    ]
    
    def __init__(self, commit_msg_file: str):
        self.commit_msg_file = Path(commit_msg_file)
        
    def check_honesty(self) -> tuple[bool, str]:
        """فحص صدق رسالة الـ commit"""
        
        if not self.commit_msg_file.exists():
            return False, "ملف رسالة الـ commit غير موجود"
        
        with open(self.commit_msg_file, 'r', encoding='utf-8') as f:
            commit_msg = f.read().strip()
        
        if not commit_msg:
            return False, "رسالة الـ commit فارغة"
        
        # تحويل لأحرف صغيرة للفحص
        commit_msg_lower = commit_msg.lower()
        
        # فحص الكلمات المبالغة
        for word in self.EXAGGERATION_WORDS:
            if word.lower() in commit_msg_lower:
                return False, f"❌ كلمة مبالغة محظورة: '{word}'"
        
        # فحص العبارات المبالغة
        for phrase in self.EXAGGERATION_PHRASES:
            if phrase.lower() in commit_msg_lower:
                return False, f"❌ عبارة مبالغة محظورة: '{phrase}'"
        
        # فحص وجود كلمات صادقة
        has_honest_word = any(
            word.lower() in commit_msg_lower 
            for word in self.HONEST_WORDS
        )
        
        if not has_honest_word:
            return False, (
                "⚠️ رسالة الـ commit تفتقر للصدق. "
                "استخدم كلمات صادقة مثل: fix, improve, add, update, test"
            )
        
        # فحص طول الرسالة (رسائل قصيرة جداً مشبوهة)
        if len(commit_msg) < 10:
            return False, "⚠️ رسالة الـ commit قصيرة جداً - كن أكثر وصفاً"
        
        # فحص الرسائل العامة المشبوهة
        generic_messages = [
            "update", "fix", "change", "modify", "improve",
            "تحديث", "إصلاح", "تغيير", "تعديل", "تحسين"
        ]
        
        if commit_msg.strip().lower() in [msg.lower() for msg in generic_messages]:
            return False, (
                "⚠️ رسالة عامة جداً. "
                "كن أكثر تحديداً: ماذا تم إصلاحه/تحديثه بالضبط؟"
            )
        
        return True, "✅ رسالة الـ commit صادقة ومقبولة"
    
    def suggest_honest_message(self, original_msg: str) -> str:
        """اقتراح رسالة صادقة بديلة"""
        suggestions = [
            "Fix issue with authentication logic",
            "Add basic user registration functionality", 
            "Improve error handling in API endpoints",
            "Update database schema for user profiles",
            "Refactor authentication middleware",
            "Add unit tests for user model",
            "Fix Redis connection timeout issue",
            "Improve code coverage for auth module",
            "Update requirements.txt dependencies",
            "Fix linting issues in user views"
        ]
        
        return f"اقتراح رسالة صادقة: '{suggestions[0]}'"


def main():
    """النقطة الرئيسية لفحص صدق الـ commit"""
    
    if len(sys.argv) != 2:
        print("❌ الاستخدام: python check_commit_honesty.py <commit-msg-file>")
        return 1
    
    commit_msg_file = sys.argv[1]
    checker = CommitHonestyChecker(commit_msg_file)
    
    is_honest, message = checker.check_honesty()
    
    print("🚨 فحص صدق رسالة الـ commit:")
    print("=" * 40)
    print(message)
    
    if not is_honest:
        print("\n💡 نصائح للصدق:")
        print("- استخدم كلمات دقيقة: fix, add, improve, update")
        print("- تجنب المبالغة: perfect, amazing, flawless")
        print("- كن محدداً: ماذا تم إصلاحه/إضافته بالضبط؟")
        print("- اعترف بالقيود: 'partial fix', 'initial implementation'")
        
        # قراءة الرسالة الأصلية لاقتراح بديل
        try:
            with open(commit_msg_file, 'r', encoding='utf-8') as f:
                original = f.read().strip()
            print(f"\n{checker.suggest_honest_message(original)}")
        except:
            pass
        
        print("\n🚫 الـ commit مرفوض - عدل الرسالة وحاول مرة أخرى")
        return 1
    
    print("\n✅ رسالة الـ commit مقبولة - يمكن المتابعة")
    return 0


if __name__ == "__main__":
    sys.exit(main())
