# Security Policy

## 🛡️ Supported Versions

We actively maintain and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅ Yes             |
| < 1.0   | ❌ No              |

## 🔒 Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in StrategyDECK, please report it responsibly.

### How to Report

**Do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please report security issues privately using one of these methods:

1. **GitHub Security Advisories** (Recommended)
   - Go to the [Security tab](https://github.com/Jvryan92/StategyDECK/security) in this repository
   - Click "Report a vulnerability"
   - Fill out the vulnerability report form

2. **Email** (Alternative)
   - Send details to the repository maintainers
   - Include "SECURITY" in the subject line
   - Provide detailed information about the vulnerability

### What to Include

When reporting a security vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Impact**: Potential impact and severity of the vulnerability
- **Environment**: 
  - Python version
  - Operating system
  - StrategyDECK version/commit
- **Proof of Concept**: Code or screenshots demonstrating the issue (if applicable)
- **Suggested Fix**: If you have ideas for fixing the issue (optional)

### Response Timeline

We will acknowledge receipt of vulnerability reports within:
- **48 hours** for critical issues
- **1 week** for non-critical issues

Our typical response process:
1. **Acknowledgment**: We confirm receipt of your report
2. **Investigation**: We investigate and validate the vulnerability
3. **Fix Development**: We develop and test a fix
4. **Disclosure**: We coordinate disclosure and release the fix
5. **Credit**: We provide credit to the reporter (if desired)

## 🔍 Security Considerations

### Current Scope

This project primarily handles:
- SVG file processing and generation
- Python script execution for asset generation
- GitHub Actions workflows

### Potential Risk Areas

Areas where security considerations are most relevant:
- **SVG Processing**: Malformed SVG files could potentially cause issues
- **File System Operations**: Script writes files to the assets directory
- **Dependency Chain**: Third-party packages (cairosvg, etc.)
- **GitHub Actions**: Workflow permissions and secrets handling

### Safe Usage

To use StrategyDECK securely:
- **Source Control**: Only run scripts from trusted sources
- **Dependencies**: Keep dependencies updated (Dependabot helps with this)
- **Input Validation**: Be cautious with custom SVG input files
- **File Permissions**: Review generated file locations and permissions

## 🚫 Out of Scope

The following are generally **not** considered security vulnerabilities:
- Issues requiring local file system access beyond the project directory
- Denial of service through resource exhaustion during normal usage
- Issues in third-party dependencies (please report to the respective projects)
- Social engineering attacks
- Issues requiring physical access to the machine

## 🏆 Recognition

We appreciate security researchers who help keep StrategyDECK safe! 

### Hall of Fame

Contributors who responsibly disclose security vulnerabilities will be:
- Listed here (with their permission)
- Credited in release notes
- Given priority for future collaboration opportunities

*No security vulnerabilities have been reported yet.*

## 📚 Additional Resources

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Python Security Guidelines](https://python.org/dev/security/)
- [OWASP Security Practices](https://owasp.org/www-project-top-ten/)

---

Thank you for helping keep StrategyDECK and our users safe! 🙏