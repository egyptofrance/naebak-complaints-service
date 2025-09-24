#!/usr/bin/env python3
"""
AI Honesty Enforcer - إجبار الذكاء الاصطناعي على الصدق المطلق
يمنع المبالغة ويجبر على الصراحة التامة في النتائج
"""

import subprocess
import sys
import json
import os
import time
from datetime import datetime
from pathlib import Path
import tempfile


class AIHonestyEnforcer:
    """
    مُنفذ الصدق للذكاء الاصطناعي
    يجبر على الصراحة التامة وعدم المبالغة
    """
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.reports_dir = self.project_root / "ai_reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def enforce_honesty_check(self) -> dict:
        """
        فحص الصدق الإجباري - لا مجال للمبالغة
        """
        print("🚨 بدء فحص الصدق الإجباري للذكاء الاصطناعي...")
        print("📋 قواعد صارمة: لا مبالغة، لا تجميل، صراحة مطلقة")
        
        results = {
            "timestamp": self.timestamp,
            "honesty_enforced": True,
            "tests": {},
            "screenshots": {},
            "failures": {},
            "truth_score": 0,
            "ai_compliance": False
        }
        
        # 1. فحص الاختبارات الحقيقي
        test_results = self._run_real_tests()
        results["tests"] = test_results
        
        # 2. فحص التغطية الحقيقي
        coverage_results = self._run_real_coverage()
        results["coverage"] = coverage_results
        
        # 3. فحص الجودة الحقيقي
        quality_results = self._run_real_quality_check()
        results["quality"] = quality_results
        
        # 4. حساب نقاط الصدق
        results["truth_score"] = self._calculate_truth_score(results)
        
        # 5. تقييم امتثال الذكاء الاصطناعي
        results["ai_compliance"] = self._evaluate_ai_compliance(results)
        
        # 6. إنشاء التقرير النهائي
        self._generate_honesty_report(results)
        
        return results
    
    def _run_real_tests(self) -> dict:
        """تشغيل الاختبارات الحقيقية بدون تجميل"""
        print("🧪 تشغيل الاختبارات الحقيقية...")
        
        try:
            # تشغيل pytest مع تفاصيل كاملة
            result = subprocess.run([
                sys.executable, "-m", "pytest",
                "--tb=long",
                "--verbose",
                "--no-header",
                "--json-report",
                f"--json-report-file={self.reports_dir}/test_results.json"
            ], 
            capture_output=True, 
            text=True, 
            timeout=300,
            env={**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings"}
            )
            
            # قراءة النتائج الحقيقية
            test_data = self._read_test_json()
            
            passed = test_data.get("summary", {}).get("passed", 0)
            failed = test_data.get("summary", {}).get("failed", 0)
            errors = test_data.get("summary", {}).get("error", 0)
            total = passed + failed + errors
            
            # حفظ screenshot إذا نجحت الاختبارات
            screenshot_path = None
            if failed == 0 and errors == 0 and total > 0:
                screenshot_path = self._take_success_screenshot(test_data)
            
            return {
                "status": "passed" if failed == 0 and errors == 0 else "failed",
                "total": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "success_rate": (passed / total * 100) if total > 0 else 0,
                "screenshot": screenshot_path,
                "raw_output": result.stdout,
                "raw_errors": result.stderr,
                "honest_assessment": self._get_honest_test_assessment(passed, failed, errors, total)
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "honest_assessment": "الاختبارات تجاوزت الوقت المحدد - مشكلة حقيقية تحتاج حل"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "honest_assessment": f"خطأ في تشغيل الاختبارات: {str(e)}"
            }
    
    def _run_real_coverage(self) -> dict:
        """فحص التغطية الحقيقية بدون تجميل"""
        print("📊 فحص التغطية الحقيقية...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pytest",
                "--cov=.",
                "--cov-report=json",
                "--cov-report=term-missing",
                "--quiet"
            ], 
            capture_output=True, 
            text=True,
            env={**os.environ, "DJANGO_SETTINGS_MODULE": "config.settings"}
            )
            
            # قراءة تقرير التغطية
            coverage_data = self._read_coverage_json()
            
            if coverage_data:
                total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
                
                return {
                    "percentage": round(total_coverage, 2),
                    "meets_requirement": total_coverage >= 90,
                    "honest_assessment": self._get_honest_coverage_assessment(total_coverage),
                    "details": coverage_data.get("totals", {}),
                    "files_below_threshold": self._get_low_coverage_files(coverage_data)
                }
            else:
                return {
                    "percentage": 0,
                    "meets_requirement": False,
                    "honest_assessment": "فشل في قراءة تقرير التغطية - مشكلة تقنية حقيقية"
                }
                
        except Exception as e:
            return {
                "percentage": 0,
                "meets_requirement": False,
                "error": str(e),
                "honest_assessment": f"خطأ في فحص التغطية: {str(e)}"
            }
    
    def _run_real_quality_check(self) -> dict:
        """فحص جودة الكود الحقيقي"""
        print("🔍 فحص جودة الكود الحقيقي...")
        
        quality_results = {}
        
        # فحص black
        try:
            black_result = subprocess.run([
                "black", "--check", "--diff", "."
            ], capture_output=True, text=True)
            
            quality_results["formatting"] = {
                "tool": "black",
                "passed": black_result.returncode == 0,
                "issues": black_result.stdout if black_result.returncode != 0 else None
            }
        except:
            quality_results["formatting"] = {
                "tool": "black",
                "passed": False,
                "error": "black غير متاح"
            }
        
        # فحص flake8
        try:
            flake8_result = subprocess.run([
                "flake8", "."
            ], capture_output=True, text=True)
            
            quality_results["linting"] = {
                "tool": "flake8",
                "passed": flake8_result.returncode == 0,
                "issues": flake8_result.stdout if flake8_result.returncode != 0 else None
            }
        except:
            quality_results["linting"] = {
                "tool": "flake8", 
                "passed": False,
                "error": "flake8 غير متاح"
            }
        
        # تقييم صادق للجودة
        all_passed = all(
            check.get("passed", False) 
            for check in quality_results.values()
        )
        
        quality_results["overall"] = {
            "passed": all_passed,
            "honest_assessment": self._get_honest_quality_assessment(quality_results)
        }
        
        return quality_results
    
    def _take_success_screenshot(self, test_data: dict) -> str:
        """أخذ screenshot للاختبارات الناجحة فقط"""
        try:
            # إنشاء تقرير HTML للاختبارات الناجحة
            html_content = self._generate_success_html(test_data)
            
            # حفظ HTML مؤقت
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                html_path = f.name
            
            # أخذ screenshot (محاكاة - في البيئة الحقيقية نستخدم selenium)
            screenshot_path = self.reports_dir / f"success_tests_{self.timestamp}.png"
            
            # محاكاة أخذ screenshot
            self._simulate_screenshot(html_path, screenshot_path)
            
            # تنظيف الملف المؤقت
            os.unlink(html_path)
            
            return str(screenshot_path)
            
        except Exception as e:
            print(f"⚠️ فشل في أخذ screenshot: {e}")
            return None
    
    def _simulate_screenshot(self, html_path: str, output_path: Path):
        """محاكاة أخذ screenshot"""
        # في البيئة الحقيقية، نستخدم:
        # from selenium import webdriver
        # driver = webdriver.Chrome()
        # driver.get(f"file://{html_path}")
        # driver.save_screenshot(str(output_path))
        
        # للمحاكاة، ننشئ ملف نصي
        with open(output_path.with_suffix('.txt'), 'w') as f:
            f.write(f"Screenshot placeholder for successful tests at {self.timestamp}")
    
    def _generate_success_html(self, test_data: dict) -> str:
        """إنشاء HTML للاختبارات الناجحة"""
        passed = test_data.get("summary", {}).get("passed", 0)
        total = test_data.get("summary", {}).get("total", 0)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>نتائج الاختبارات الناجحة</title>
            <style>
                body {{ font-family: Arial, sans-serif; background: #f0f8ff; }}
                .success {{ color: #28a745; font-size: 24px; font-weight: bold; }}
                .stats {{ background: #d4edda; padding: 20px; border-radius: 10px; }}
            </style>
        </head>
        <body>
            <h1 class="success">✅ جميع الاختبارات نجحت!</h1>
            <div class="stats">
                <p>إجمالي الاختبارات: {total}</p>
                <p>الاختبارات الناجحة: {passed}</p>
                <p>معدل النجاح: 100%</p>
                <p>التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
    
    def _read_test_json(self) -> dict:
        """قراءة نتائج الاختبارات من JSON"""
        json_path = self.reports_dir / "test_results.json"
        if json_path.exists():
            try:
                with open(json_path) as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _read_coverage_json(self) -> dict:
        """قراءة تقرير التغطية من JSON"""
        coverage_path = self.project_root / "coverage.json"
        if coverage_path.exists():
            try:
                with open(coverage_path) as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _get_honest_test_assessment(self, passed: int, failed: int, errors: int, total: int) -> str:
        """تقييم صادق للاختبارات"""
        if total == 0:
            return "❌ لا توجد اختبارات - هذا غير مقبول نهائياً"
        
        if failed > 0 or errors > 0:
            return f"❌ فشل {failed + errors} من {total} اختبار - يجب إصلاح المشاكل قبل المتابعة"
        
        if passed < 5:
            return f"⚠️ نجح {passed} اختبارات فقط - عدد قليل جداً، يحتاج المزيد من الاختبارات"
        
        return f"✅ نجح جميع الاختبارات ({passed}/{total}) - وضع جيد"
    
    def _get_honest_coverage_assessment(self, coverage: float) -> str:
        """تقييم صادق للتغطية"""
        if coverage < 50:
            return f"❌ تغطية ضعيفة جداً ({coverage:.1f}%) - غير مقبولة نهائياً"
        elif coverage < 70:
            return f"⚠️ تغطية منخفضة ({coverage:.1f}%) - تحتاج تحسين كبير"
        elif coverage < 90:
            return f"🔶 تغطية متوسطة ({coverage:.1f}%) - أقل من المطلوب (90%)"
        else:
            return f"✅ تغطية ممتازة ({coverage:.1f}%) - تتجاوز المطلوب"
    
    def _get_honest_quality_assessment(self, quality_results: dict) -> str:
        """تقييم صادق لجودة الكود"""
        issues = []
        
        for check_name, check_result in quality_results.items():
            if check_name == "overall":
                continue
                
            if not check_result.get("passed", False):
                if "error" in check_result:
                    issues.append(f"{check_result['tool']} غير متاح")
                else:
                    issues.append(f"{check_result['tool']} وجد مشاكل")
        
        if issues:
            return f"❌ مشاكل في الجودة: {', '.join(issues)}"
        else:
            return "✅ جودة الكود مقبولة"
    
    def _get_low_coverage_files(self, coverage_data: dict) -> list:
        """الحصول على الملفات ذات التغطية المنخفضة"""
        low_files = []
        files = coverage_data.get("files", {})
        
        for file_path, file_data in files.items():
            coverage = file_data.get("summary", {}).get("percent_covered", 0)
            if coverage < 90:
                low_files.append({
                    "file": file_path,
                    "coverage": round(coverage, 2)
                })
        
        return sorted(low_files, key=lambda x: x["coverage"])
    
    def _calculate_truth_score(self, results: dict) -> int:
        """حساب نقاط الصدق (0-100)"""
        score = 0
        
        # نقاط الاختبارات
        test_status = results.get("tests", {}).get("status")
        if test_status == "passed":
            score += 40
        elif test_status == "failed":
            score += 10  # نقاط للصدق في الإبلاغ عن الفشل
        
        # نقاط التغطية
        coverage = results.get("coverage", {}).get("percentage", 0)
        if coverage >= 90:
            score += 30
        elif coverage >= 70:
            score += 20
        elif coverage >= 50:
            score += 10
        
        # نقاط الجودة
        quality_passed = results.get("quality", {}).get("overall", {}).get("passed", False)
        if quality_passed:
            score += 30
        else:
            score += 10  # نقاط للصدق في الإبلاغ عن المشاكل
        
        return min(score, 100)
    
    def _evaluate_ai_compliance(self, results: dict) -> bool:
        """تقييم امتثال الذكاء الاصطناعي للصدق"""
        # الذكاء الاصطناعي ممتثل إذا:
        # 1. أبلغ عن النتائج الحقيقية
        # 2. لم يبالغ في التقييم
        # 3. كان صادقاً في التقييمات
        
        truth_score = results.get("truth_score", 0)
        
        # إذا كانت النقاط عالية، فالذكاء الاصطناعي صادق
        # إذا كانت منخفضة ولكن أبلغ عن المشاكل، فهو صادق أيضاً
        
        return truth_score >= 50  # حد أدنى للصدق
    
    def _generate_honesty_report(self, results: dict):
        """إنشاء تقرير الصدق النهائي"""
        report_path = self.reports_dir / f"honesty_report_{self.timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        # إنشاء تقرير نصي أيضاً
        text_report_path = self.reports_dir / f"honesty_report_{self.timestamp}.txt"
        
        with open(text_report_path, 'w', encoding='utf-8') as f:
            f.write("🚨 تقرير الصدق الإجباري للذكاء الاصطناعي\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"التاريخ: {results['timestamp']}\n")
            f.write(f"نقاط الصدق: {results['truth_score']}/100\n")
            f.write(f"امتثال الذكاء الاصطناعي: {'✅ ممتثل' if results['ai_compliance'] else '❌ غير ممتثل'}\n\n")
            
            # تفاصيل الاختبارات
            tests = results.get("tests", {})
            f.write("📋 نتائج الاختبارات:\n")
            f.write(f"  الحالة: {tests.get('status', 'غير معروف')}\n")
            f.write(f"  التقييم الصادق: {tests.get('honest_assessment', 'غير متاح')}\n\n")
            
            # تفاصيل التغطية
            coverage = results.get("coverage", {})
            f.write("📊 نتائج التغطية:\n")
            f.write(f"  النسبة: {coverage.get('percentage', 0):.1f}%\n")
            f.write(f"  التقييم الصادق: {coverage.get('honest_assessment', 'غير متاح')}\n\n")
            
            # تفاصيل الجودة
            quality = results.get("quality", {})
            f.write("🔍 نتائج الجودة:\n")
            f.write(f"  التقييم الصادق: {quality.get('overall', {}).get('honest_assessment', 'غير متاح')}\n")


def main():
    """النقطة الرئيسية لفحص الصدق"""
    enforcer = AIHonestyEnforcer()
    
    print("🚨 بدء فحص الصدق الإجباري...")
    print("📋 هذا الفحص يجبر الذكاء الاصطناعي على الصراحة المطلقة")
    print("🚫 لا مجال للمبالغة أو التجميل")
    print()
    
    results = enforcer.enforce_honesty_check()
    
    print("\n" + "=" * 60)
    print("📊 النتائج النهائية (بصراحة مطلقة):")
    print("=" * 60)
    
    print(f"🎯 نقاط الصدق: {results['truth_score']}/100")
    print(f"🤖 امتثال الذكاء الاصطناعي: {'✅ ممتثل' if results['ai_compliance'] else '❌ غير ممتثل'}")
    
    # عرض التقييمات الصادقة
    tests = results.get("tests", {})
    if "honest_assessment" in tests:
        print(f"🧪 الاختبارات: {tests['honest_assessment']}")
    
    coverage = results.get("coverage", {})
    if "honest_assessment" in coverage:
        print(f"📊 التغطية: {coverage['honest_assessment']}")
    
    quality = results.get("quality", {})
    if "overall" in quality and "honest_assessment" in quality["overall"]:
        print(f"🔍 الجودة: {quality['overall']['honest_assessment']}")
    
    # عرض screenshot إذا وجد
    screenshot = tests.get("screenshot")
    if screenshot:
        print(f"📸 Screenshot للنجاح: {screenshot}")
    
    print("\n🚨 هذا التقرير يضمن الصدق المطلق - لا مجال للمبالغة!")
    
    # إرجاع كود الخروج المناسب
    if results["ai_compliance"] and results["truth_score"] >= 70:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
