import os
import json
import re

def list_all_files(path='.'):
    """Lists all files and directories recursively, ignoring .git."""
    file_list = []
    for root, dirs, files in os.walk(path):
        if '.git' in dirs:
            dirs.remove('.git')  # Don't descend into .git directories

        for name in files:
            file_list.append(os.path.join(root, name))
        for name in dirs:
            file_list.append(os.path.join(root, name) + '/')

    return file_list

def identify_ddd(files):
    """Identifies evidence of Domain-Driven Design."""
    evidence = []
    bounded_contexts = {}

    # Regex to find patterns like '.../context_name/domain/'
    context_pattern = re.compile(r'(.+)/((?:application|domain|infrastructure)/)$')

    for f in files:
        if 'ubiquitous-language.md' in f.lower() or 'ubiquitous_language.md' in f.lower():
            evidence.append({'type': 'Ubiquitous Language Document', 'file': f})

        match = context_pattern.search(f)
        if match:
            path_prefix = match.group(1)
            layer = match.group(2).strip('/')

            # Heuristic: the parent of the layer is the bounded context
            context_name = os.path.basename(path_prefix)

            if context_name not in bounded_contexts:
                bounded_contexts[context_name] = {'path': path_prefix, 'layers': set()}
            bounded_contexts[context_name]['layers'].add(layer)

    for context, data in bounded_contexts.items():
        # A strong indicator is the presence of at least two of the canonical layers
        if len(data['layers']) >= 2:
            evidence.append({
                'type': 'Bounded Context Detected',
                'context_name': context,
                'path': data['path'],
                'found_layers': list(data['layers'])
            })

    return evidence

def identify_tdd_xp(files):
    """Identifies evidence of Test-Driven Development or Extreme Programming."""
    evidence = []
    source_files = 0
    test_files = 0
    test_file_examples = []

    test_patterns = [
        r'test_.*\.py$',
        r'.*\.test\.js$',
        r'.*\.spec\.js$',
        r'.*Test\.java$',
        r'.*Tests\.cs$'
    ]

    source_patterns = [
        r'\.py$',
        r'\.js$',
        r'\.java$',
        r'\.cs$',
        r'\.go$',
        r'\.rs$'
    ]

    for f in files:
        if any(re.search(p, f) for p in test_patterns):
            if not any(f.endswith(d) for d in ['__init__.py']): # Exclude common non-test files
                test_files += 1
                if len(test_file_examples) < 3:
                    test_file_examples.append(f)
        elif any(re.search(p, f) for p in source_patterns):
             if not any(f.endswith(d) for d in ['__init__.py']):
                source_files += 1

    if source_files > 0 and test_files > 0:
        ratio = test_files / source_files
        evidence.append({
            'type': 'Test to Source Ratio',
            'test_files': test_files,
            'source_files': source_files,
            'ratio': round(ratio, 2),
            'test_file_examples': test_file_examples
        })
        # A ratio > 0.8 is a moderate indicator of a test-heavy culture
        if ratio > 0.8:
            evidence.append({
                'type': 'Conclusion',
                'finding': 'High test-to-source ratio suggests a TDD/XP culture.'
            })

    return evidence

def identify_devops(files):
    """Identifies evidence of DevOps practices."""
    evidence = []
    iac_files = [f for f in files if f.endswith('.tf') or 'terraform' in f]
    docker_files = [f for f in files if 'Dockerfile' in f or 'docker-compose.yml' in f]
    ci_cd_files = [f for f in files if '.github/workflows' in f or '.gitlab-ci.yml' in f]

    if iac_files:
        evidence.append({'type': 'Infrastructure-as-Code', 'files': iac_files[:3]})
    if docker_files:
        evidence.append({'type': 'Containerization', 'files': docker_files[:3]})
    if ci_cd_files:
        evidence.append({'type': 'CI/CD Pipeline', 'files': ci_cd_files[:3]})

    return evidence

def analyze_repository(path='.'):
    """Analyzes the repository to identify methodologies."""
    all_files = list_all_files(path)

    detected_methodologies = {}

    ddd_evidence = identify_ddd(all_files)
    if ddd_evidence:
        detected_methodologies['domain_driven_design'] = ddd_evidence

    tdd_evidence = identify_tdd_xp(all_files)
    if tdd_evidence:
        detected_methodologies['test_driven_development_xp'] = tdd_evidence

    devops_evidence = identify_devops(all_files)
    if devops_evidence:
        detected_methodologies['devops'] = devops_evidence

    return detected_methodologies

if __name__ == "__main__":
    results = analyze_repository()
    print(json.dumps(results, indent=2))
