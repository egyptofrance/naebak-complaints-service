#!/usr/bin/env python3
"""
Manus Code Scanner
Scans source code for exaggerated claims and dishonest comments
"""

import os
import re
import sys
from typing import List, Dict, Any, Tuple

class ManusCodeScanner:
    """
    Scans code files for exaggerated claims and dishonest statements
    """
    
    def __init__(self):
        self.exaggerated_words = [
            'perfect', 'flawless', 'amazing', 'incredible', 'revolutionary',
            'groundbreaking', 'ultimate', 'best', 'greatest', 'fantastic',
            'awesome', 'brilliant', 'genius', 'masterpiece', 'legendary',
            'zero bugs', 'bug-free', 'never fails', 'always works',
            'completely secure', 'totally safe', 'guaranteed', 'absolutely',
            'definitely works', 'never breaks', 'impossible to fail'
        ]
        
        self.exaggerated_phrases = [
            'works perfectly', 'runs flawlessly', 'zero issues',
            'no problems', 'completely secure', 'totally safe',
            'perfectly implemented', 'flawlessly executed',
            'revolutionary algorithm', 'groundbreaking solution',
            'ultimate performance', 'best code ever', 'amazing speed',
            'incredible efficiency', 'fantastic results', 'never fails',
            'always successful', 'guaranteed to work', 'bug-free code'
        ]
        
        self.file_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go']
        
        self.exclude_dirs = [
            '.git', '__pycache__', 'node_modules', '.pytest_cache',
            'venv', 'env', '.env', 'build', 'dist', '.tox'
        ]
    
    def should_scan_file(self, filepath: str) -> bool:
        """
        Determine if a file should be scanned
        """
        # Check file extension
        if not any(filepath.endswith(ext) for ext in self.file_extensions):
            return False
        
        # Check if in excluded directory
        path_parts = filepath.split(os.sep)
        if any(excluded in path_parts for excluded in self.exclude_dirs):
            return False
        
        return True
    
    def scan_file(self, filepath: str) -> Dict[str, Any]:
        """
        Scan a single file for exaggerated claims
        """
        violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # Skip if line is too short or doesn't contain comments/strings
                if len(line.strip()) < 10:
                    continue
                
                # Check for exaggerated words
                for word in self.exaggerated_words:
                    if word in line_lower:
                        violations.append({
                            'type': 'exaggerated_word',
                            'line': line_num,
                            'content': line.strip(),
                            'word': word,
                            'message': f"Exaggerated word '{word}' found"
                        })
                
                # Check for exaggerated phrases
                for phrase in self.exaggerated_phrases:
                    if phrase in line_lower:
                        violations.append({
                            'type': 'exaggerated_phrase',
                            'line': line_num,
                            'content': line.strip(),
                            'phrase': phrase,
                            'message': f"Exaggerated phrase '{phrase}' found"
                        })
        
        except Exception as e:
            violations.append({
                'type': 'scan_error',
                'line': 0,
                'content': '',
                'message': f"Error scanning file: {str(e)}"
            })
        
        return {
            'filepath': filepath,
            'violations': violations,
            'is_honest': len(violations) == 0,
            'score': max(0, 100 - len(violations) * 10)
        }
    
    def scan_directory(self, directory: str = '.') -> Dict[str, Any]:
        """
        Scan all files in a directory
        """
        results = []
        total_violations = 0
        total_files = 0
        
        for root, dirs, files in os.walk(directory):
            # Remove excluded directories from dirs list
            dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
            
            for file in files:
                filepath = os.path.join(root, file)
                
                if self.should_scan_file(filepath):
                    result = self.scan_file(filepath)
                    results.append(result)
                    total_violations += len(result['violations'])
                    total_files += 1
        
        return {
            'total_files': total_files,
            'total_violations': total_violations,
            'results': results,
            'overall_honest': total_violations == 0,
            'average_score': sum(r['score'] for r in results) / len(results) if results else 100
        }
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a detailed report
        """
        report = []
        report.append("🔍 MANUS CODE HONESTY REPORT")
        report.append("=" * 50)
        report.append(f"Total files scanned: {results['total_files']}")
        report.append(f"Total violations found: {results['total_violations']}")
        report.append(f"Overall honesty: {'✅ PASS' if results['overall_honest'] else '❌ FAIL'}")
        report.append(f"Average honesty score: {results['average_score']:.1f}/100")
        report.append("")
        
        if results['total_violations'] > 0:
            report.append("🚨 VIOLATIONS FOUND:")
            report.append("-" * 30)
            
            for result in results['results']:
                if result['violations']:
                    report.append(f"File: {result['filepath']}")
                    for violation in result['violations']:
                        report.append(f"  Line {violation['line']}: {violation['message']}")
                        report.append(f"    Content: {violation['content']}")
                    report.append("")
        else:
            report.append("✅ No violations found - all code is honest!")
        
        return "\n".join(report)
    
    def get_suggestions(self, violations: List[Dict[str, Any]]) -> List[str]:
        """
        Get suggestions for fixing violations
        """
        suggestions = []
        
        if violations:
            suggestions.append("🔧 SUGGESTIONS FOR FIXING VIOLATIONS:")
            suggestions.append("-" * 40)
            suggestions.append("• Replace 'perfect' with 'functional' or 'working'")
            suggestions.append("• Replace 'flawless' with 'tested' or 'reviewed'")
            suggestions.append("• Replace 'amazing' with 'effective' or 'efficient'")
            suggestions.append("• Replace 'never fails' with 'handles errors gracefully'")
            suggestions.append("• Replace 'guaranteed' with 'expected to' or 'designed to'")
            suggestions.append("• Replace 'completely secure' with 'follows security best practices'")
            suggestions.append("• Replace 'zero bugs' with 'tested and reviewed'")
            suggestions.append("• Use specific, measurable claims instead of superlatives")
        
        return suggestions

def main():
    """
    Main function to run the code scanner
    """
    scanner = ManusCodeScanner()
    results = scanner.scan_directory()
    report = scanner.generate_report(results)
    
    print(report)
    
    if not results['overall_honest']:
        suggestions = scanner.get_suggestions([v for r in results['results'] for v in r['violations']])
        print("\n" + "\n".join(suggestions))
        
        print("\n🚨 MANUS CODE HONESTY CHECK FAILED!")
        print("Please revise code comments and strings to remove exaggerated claims.")
        sys.exit(1)
    else:
        print("\n✅ MANUS CODE HONESTY CHECK PASSED!")
        sys.exit(0)

if __name__ == "__main__":
    main()
