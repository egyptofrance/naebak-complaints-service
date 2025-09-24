#!/usr/bin/env python3
"""
Manus Documentation Validator
Validates documentation files for honest and accurate claims
"""

import os
import re
import sys
from typing import List, Dict, Any

class ManusDocsValidator:
    """
    Validates documentation for honesty and accuracy
    """
    
    def __init__(self):
        self.exaggerated_claims = [
            'perfect solution', 'flawless implementation', 'amazing performance',
            'incredible speed', 'revolutionary approach', 'groundbreaking technology',
            'ultimate solution', 'best in class', 'world-class', 'industry-leading',
            'cutting-edge', 'state-of-the-art', 'next-generation', 'advanced',
            'sophisticated', 'enterprise-grade', 'military-grade', 'bank-level',
            'zero downtime', 'never fails', 'always works', 'guaranteed uptime',
            'bug-free', 'error-free', 'completely secure', 'totally safe',
            'absolutely reliable', 'definitely works', 'certainly effective'
        ]
        
        self.unsupported_claims = [
            'fastest', 'slowest', 'biggest', 'smallest', 'most secure',
            'least secure', 'most reliable', 'most efficient', 'best performance',
            'worst performance', 'highest quality', 'lowest cost', 'cheapest',
            'most expensive', 'most popular', 'least popular', 'most used',
            'most trusted', 'most advanced', 'most innovative', 'most scalable'
        ]
        
        self.doc_extensions = ['.md', '.rst', '.txt', '.doc', '.docx']
        
        self.exclude_files = ['CHANGELOG.md', 'LICENSE', 'CONTRIBUTORS.md']
    
    def should_validate_file(self, filepath: str) -> bool:
        """
        Determine if a file should be validated
        """
        # Check file extension
        if not any(filepath.endswith(ext) for ext in self.doc_extensions):
            return False
        
        # Check if in excluded files
        filename = os.path.basename(filepath)
        if filename in self.exclude_files:
            return False
        
        return True
    
    def validate_file(self, filepath: str) -> Dict[str, Any]:
        """
        Validate a single documentation file
        """
        violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                
                # Skip empty lines and very short lines
                if len(line.strip()) < 5:
                    continue
                
                # Check for exaggerated claims
                for claim in self.exaggerated_claims:
                    if claim in line_lower:
                        violations.append({
                            'type': 'exaggerated_claim',
                            'line': line_num,
                            'content': line.strip(),
                            'claim': claim,
                            'message': f"Exaggerated claim '{claim}' found",
                            'severity': 'high'
                        })
                
                # Check for unsupported superlative claims
                for claim in self.unsupported_claims:
                    if claim in line_lower:
                        violations.append({
                            'type': 'unsupported_claim',
                            'line': line_num,
                            'content': line.strip(),
                            'claim': claim,
                            'message': f"Unsupported superlative '{claim}' found - needs evidence",
                            'severity': 'medium'
                        })
                
                # Check for specific dishonest patterns
                dishonest_patterns = [
                    (r'100%\s+(secure|safe|reliable|working)', 'Absolute percentage claims are rarely accurate'),
                    (r'never\s+(fails|breaks|crashes)', 'Absolute negative claims are unrealistic'),
                    (r'always\s+(works|succeeds|performs)', 'Absolute positive claims are unrealistic'),
                    (r'guaranteed\s+to\s+work', 'Guarantees in software are rarely possible'),
                    (r'impossible\s+to\s+(hack|break|fail)', 'Absolute security claims are dangerous'),
                    (r'zero\s+(bugs|errors|issues)', 'Zero defect claims are unrealistic')
                ]
                
                for pattern, message in dishonest_patterns:
                    if re.search(pattern, line_lower):
                        violations.append({
                            'type': 'dishonest_pattern',
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern,
                            'message': message,
                            'severity': 'high'
                        })
        
        except Exception as e:
            violations.append({
                'type': 'validation_error',
                'line': 0,
                'content': '',
                'message': f"Error validating file: {str(e)}",
                'severity': 'low'
            })
        
        return {
            'filepath': filepath,
            'violations': violations,
            'is_honest': len(violations) == 0,
            'score': max(0, 100 - len(violations) * 15)
        }
    
    def validate_directory(self, directory: str = '.') -> Dict[str, Any]:
        """
        Validate all documentation files in a directory
        """
        results = []
        total_violations = 0
        total_files = 0
        
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories and common build directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for file in files:
                filepath = os.path.join(root, file)
                
                if self.should_validate_file(filepath):
                    result = self.validate_file(filepath)
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
        Generate a detailed validation report
        """
        report = []
        report.append("📚 MANUS DOCUMENTATION HONESTY REPORT")
        report.append("=" * 55)
        report.append(f"Total documentation files: {results['total_files']}")
        report.append(f"Total violations found: {results['total_violations']}")
        report.append(f"Overall honesty: {'✅ PASS' if results['overall_honest'] else '❌ FAIL'}")
        report.append(f"Average honesty score: {results['average_score']:.1f}/100")
        report.append("")
        
        if results['total_violations'] > 0:
            report.append("🚨 VIOLATIONS FOUND:")
            report.append("-" * 30)
            
            # Group violations by severity
            high_severity = []
            medium_severity = []
            low_severity = []
            
            for result in results['results']:
                for violation in result['violations']:
                    violation['filepath'] = result['filepath']
                    if violation.get('severity') == 'high':
                        high_severity.append(violation)
                    elif violation.get('severity') == 'medium':
                        medium_severity.append(violation)
                    else:
                        low_severity.append(violation)
            
            if high_severity:
                report.append("🔴 HIGH SEVERITY VIOLATIONS:")
                for violation in high_severity:
                    report.append(f"  File: {violation['filepath']}")
                    report.append(f"  Line {violation['line']}: {violation['message']}")
                    report.append(f"    Content: {violation['content']}")
                    report.append("")
            
            if medium_severity:
                report.append("🟡 MEDIUM SEVERITY VIOLATIONS:")
                for violation in medium_severity:
                    report.append(f"  File: {violation['filepath']}")
                    report.append(f"  Line {violation['line']}: {violation['message']}")
                    report.append(f"    Content: {violation['content']}")
                    report.append("")
            
            if low_severity:
                report.append("🟢 LOW SEVERITY VIOLATIONS:")
                for violation in low_severity:
                    report.append(f"  File: {violation['filepath']}")
                    report.append(f"  Line {violation['line']}: {violation['message']}")
                    report.append("")
        else:
            report.append("✅ No violations found - all documentation is honest!")
        
        return "\n".join(report)
    
    def get_improvement_suggestions(self) -> List[str]:
        """
        Get suggestions for improving documentation honesty
        """
        return [
            "🔧 DOCUMENTATION IMPROVEMENT SUGGESTIONS:",
            "-" * 45,
            "• Replace superlatives with specific, measurable claims",
            "• Provide evidence or benchmarks for performance claims",
            "• Use 'designed to' instead of 'guaranteed to'",
            "• Replace 'never fails' with 'handles errors gracefully'",
            "• Use 'tested' instead of 'perfect' or 'flawless'",
            "• Specify conditions under which claims are true",
            "• Include limitations and known issues",
            "• Use comparative language with context",
            "• Cite sources for third-party claims",
            "• Include version information for claims"
        ]

def main():
    """
    Main function to run the documentation validator
    """
    validator = ManusDocsValidator()
    results = validator.validate_directory()
    report = validator.generate_report(results)
    
    print(report)
    
    if not results['overall_honest']:
        suggestions = validator.get_improvement_suggestions()
        print("\n" + "\n".join(suggestions))
        
        print("\n🚨 MANUS DOCUMENTATION HONESTY CHECK FAILED!")
        print("Please revise documentation to remove exaggerated and unsupported claims.")
        sys.exit(1)
    else:
        print("\n✅ MANUS DOCUMENTATION HONESTY CHECK PASSED!")
        sys.exit(0)

if __name__ == "__main__":
    main()
