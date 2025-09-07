#!/usr/bin/env python3
"""
Dependency checker for Estima - Medical Document Data Extraction System
Run this script to verify all required dependencies are properly installed.
"""

import sys
import importlib
from typing import List, Tuple

def check_dependency(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """
    Check if a dependency is installed and importable.
    
    Args:
        module_name: The module name to import
        package_name: The package name for display (defaults to module_name)
    
    Returns:
        Tuple of (success, message)
    """
    if package_name is None:
        package_name = module_name
    
    try:
        importlib.import_module(module_name)
        return True, f"✅ {package_name}"
    except ImportError as e:
        return False, f"❌ {package_name} - {str(e)}"

def check_version(module_name: str, min_version: str = None) -> Tuple[bool, str]:
    """
    Check if a module has the required minimum version.
    
    Args:
        module_name: The module name to check
        min_version: Minimum required version (e.g., "0.2.0")
    
    Returns:
        Tuple of (success, message)
    """
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, '__version__'):
            version = module.__version__
            if min_version:
                from packaging import version as pkg_version
                if pkg_version.parse(version) >= pkg_version.parse(min_version):
                    return True, f"✅ {module_name} v{version} (>= {min_version})"
                else:
                    return False, f"❌ {module_name} v{version} (requires >= {min_version})"
            else:
                return True, f"✅ {module_name} v{version}"
        else:
            return True, f"✅ {module_name} (version unknown)"
    except ImportError:
        return False, f"❌ {module_name} - not installed"
    except Exception as e:
        return False, f"❌ {module_name} - error checking version: {str(e)}"

def main():
    """Run dependency checks."""
    print("🔍 Estima Dependency Checker")
    print("=" * 50)
    
    # Core dependencies to check
    dependencies = [
        # Core LangChain
        ("langchain", "langchain"),
        ("langchain_community", "langchain-community"),
        ("langchain_core", "langchain-core"),
        
        # Vector database
        ("chromadb", "chromadb"),
        
        # AI providers
        ("ollama", "ollama"),
        ("openai", "openai"),
        
        # Data processing
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        
        # Document processing
        ("pdfplumber", "pdfplumber"),
        
        # Environment
        ("dotenv", "python-dotenv"),
    ]
    
    # Version-specific checks
    version_checks = [
        ("langchain", "0.2.0"),
        ("pandas", "2.0.0"),
        ("numpy", "1.24.0"),
    ]
    
    print("\n📦 Checking Core Dependencies...")
    core_results = []
    for module, package in dependencies:
        success, message = check_dependency(module, package)
        core_results.append(success)
        print(f"   {message}")
    
    print("\n🔢 Checking Version Requirements...")
    version_results = []
    for module, min_ver in version_checks:
        success, message = check_version(module, min_ver)
        version_results.append(success)
        print(f"   {message}")
    
    print("\n🧪 Testing Imports...")
    import_tests = [
        ("langchain.text_splitter", "RecursiveCharacterTextSplitter"),
        ("langchain.schema", "Document"),
        ("langchain.vectorstores", "Chroma"),
        ("langchain.embeddings", "OllamaEmbeddings"),
        ("langchain.embeddings", "OpenAIEmbeddings"),
    ]
    
    import_results = []
    for module, component in import_tests:
        try:
            mod = importlib.import_module(module)
            if hasattr(mod, component):
                print(f"   ✅ {module}.{component}")
                import_results.append(True)
            else:
                print(f"   ❌ {module}.{component} - not found")
                import_results.append(False)
        except ImportError as e:
            print(f"   ❌ {module}.{component} - import error: {str(e)}")
            import_results.append(False)
    
    # Summary
    print("\n" + "=" * 50)
    total_checks = len(core_results) + len(version_results) + len(import_results)
    passed_checks = sum(core_results) + sum(version_results) + sum(import_results)
    
    print(f"📊 Dependency Check Results: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("🎉 All dependencies are properly installed!")
        print("\n✅ You can now run:")
        print("   python test_config.py  # Test your configuration")
        print("   python runExtraction.py  # Run the extraction workflow")
        return 0
    else:
        print("⚠️  Some dependencies are missing or have issues.")
        print("\n🔧 To fix missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\n📚 For detailed installation instructions, see README.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
