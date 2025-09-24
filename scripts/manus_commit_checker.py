#!/usr/bin/env python3
"""
Manus Commit Message Checker
Validates commit messages for exaggerated claims and dishonest statements
"""

import re
import sys
import subprocess
from typing import List, Dict, Any

class ManusCommitChecker:
    """
    Checks commit messages for exaggeration and dishonesty
    """
    
    def __init__(self):
        self.exaggerated_words = [
            'perfect', 'flawless', 'amazing', 'incredible', 'revolutionary',
            'groundbreaking', 'ultimate', 'best', 'greatest', 'fantastic',
            'awesome', 'brilliant', 'genius', 'masterpiece', 'legendary',
            'zero bugs', 'bug-free', 'never fails', 'always works',
            'completely secure', 'totally safe', 'guaranteed', 'absolutely',
            'definitely', 'certainly', 'obviously', 'clearly', 'undoubtedly'
        ]
        
        self.exaggerated_phrases = [
            'works perfectly', 'runs flawlessly', 'zero issues',
            'no problems', 'completely fixed', 'totally resolved',
            'perfectly implemented', 'flawlessly executed',
            'revolutionary solution', 'groundbreaking approach',
            'ultimate fix', 'best solution ever', 'amazing implementation',
            'incredible performance', 'fantastic results'
        ]
        
        self.dishonest_patterns = [
            r'fix.*all.*bug',
            r'solve.*all.*problem',
            r'complete.*implementation',
            r'final.*version',
            r'ready.*production',
            r'fully.*tested',
            r'100%.*working',
            r'no.*more.*issue'
        ]
    
    def get_recent_commits(self, count: int = 10) -> List[str]:
        """
        Get recent commit messages
        """
        try:
            result = subprocess.run(
                ['git', 'log', f'--oneline', f'-{count}', '--pretty=format:%s'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except subprocess.CalledProcessError:
            return []
    
    def check_commit_message(self, message: str) -> Dict[str, Any]:
        """
        Check a single commit message for exaggeration
        """
        violations = []
        message_lower = message.lower()
        
        # Check for exaggerated words
        for word in self.exaggerated_words:
            if word in message_lower:
                violations.append({
                    'type': 'exaggerated_word',
                    'word': word,
                    'message': f"Exaggerated word '{word}' found"
                })
        
        # Check for exaggerated phrases
        for phrase in self.exaggerated_phrases:
            if phrase in message_lower:
                violations.append({
                    'type': 'exaggerated_phrase',
                    'phrase': phrase,
                    'message': f"Exaggerated phrase '{phrase}' found"
                })
        
        # Check for dishonest patterns
        for pattern in self.dishonest_patterns:
            if re.search(pattern, message_lower):
                violations.append({
                    'type': 'dishonest_pattern',
                    'pattern': pattern,
                    'message': f"Potentially dishonest pattern '{pattern}' found"
                })
        
        return {
            'message': message,
            'violations': violations,
            'is_honest': len(violations) == 0,
            'score': max(0, 100 - len(violations) * 20)
        }
    
    def check_all_commits(self) -> Dict[str, Any]:
        """
        Check all recent commits
        """
        commits = self.get_recent_commits()
        results = []
        total_violations = 0
        
        for commit in commits:
            if commit.strip():
                result = self.check_commit_message(commit)
                results.append(result)
                total_violations += len(result['violations'])
        
        return {
            'total_commits': len(results),
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
        report.append("🔍 MANUS COMMIT HONESTY REPORT")
        report.append("=" * 50)
        report.append(f"Total commits checked: {results['total_commits']}")
        report.append(f"Total violations found: {results['total_violations']}")
        report.append(f"Overall honesty: {'✅ PASS' if results['overall_honest'] else '❌ FAIL'}")
        report.append(f"Average honesty score: {results['average_score']:.1f}/100")
        report.append("")
        
        if results['total_violations'] > 0:
            report.append("🚨 VIOLATIONS FOUND:")
            report.append("-" * 30)
            
            for result in results['results']:
                if result['violations']:
                    report.append(f"Commit: {result['message']}")
                    for violation in result['violations']:
                        report.append(f"  ❌ {violation['message']}")
                    report.append("")
        else:
            report.append("✅ No violations found - all commits are honest!")
        
        return "\n".join(report)

def main():
    """
    Main function to run the commit checker
    """
    checker = ManusCommitChecker()
    results = checker.check_all_commits()
    report = checker.generate_report(results)
    
    print(report)
    
    # Exit with error code if violations found
    if not results['overall_honest']:
        print("\n🚨 MANUS HONESTY CHECK FAILED!")
        print("Please revise commit messages to remove exaggerated claims.")
        sys.exit(1)
    else:
        print("\n✅ MANUS HONESTY CHECK PASSED!")
        sys.exit(0)

if __name__ == "__main__":
    main()
