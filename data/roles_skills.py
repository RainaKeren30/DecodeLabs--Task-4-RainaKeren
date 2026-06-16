ROLES_DATA = {
    "Data Scientist": {
        "required_skills": [
            "python", "machine learning", "statistics", "sql", "data analysis",
            "pandas", "numpy", "scikit-learn", "data visualization", "deep learning",
            "tensorflow", "pytorch", "feature engineering", "model evaluation",
            "hypothesis testing", "regression", "classification", "clustering",
            "nlp", "time series", "big data", "spark", "tableau", "matplotlib",
            "seaborn", "jupyter", "git", "r", "probability"
        ],
        "weights": {
            "python": 10, "machine learning": 10, "statistics": 9, "sql": 8,
            "data analysis": 9, "pandas": 8, "numpy": 7, "scikit-learn": 8,
            "deep learning": 7, "tensorflow": 6, "pytorch": 6, "feature engineering": 8,
            "model evaluation": 8, "hypothesis testing": 7, "regression": 7,
            "classification": 7, "clustering": 6, "nlp": 6, "time series": 6,
            "big data": 5, "spark": 5, "tableau": 5, "matplotlib": 6,
            "seaborn": 5, "jupyter": 7, "git": 7, "r": 5, "probability": 7,
            "data visualization": 7
        },
        "learning_paths": {
            "python": {"resource": "Python for Data Science (Coursera)", "duration": "4 weeks", "priority": "Critical"},
            "machine learning": {"resource": "ML Specialization – Andrew Ng (Coursera)", "duration": "8 weeks", "priority": "Critical"},
            "statistics": {"resource": "Statistics with Python (edX)", "duration": "5 weeks", "priority": "High"},
            "sql": {"resource": "SQL for Data Analysis (Mode Analytics)", "duration": "3 weeks", "priority": "High"},
            "deep learning": {"resource": "Deep Learning Specialization (Coursera)", "duration": "10 weeks", "priority": "Medium"},
            "tensorflow": {"resource": "TensorFlow Developer Certificate (Google)", "duration": "8 weeks", "priority": "Medium"},
            "spark": {"resource": "Apache Spark with Python (Databricks)", "duration": "4 weeks", "priority": "Low"},
            "tableau": {"resource": "Tableau Desktop Specialist (Tableau Learning)", "duration": "3 weeks", "priority": "Low"},
            "nlp": {"resource": "NLP with Transformers (Hugging Face)", "duration": "6 weeks", "priority": "Medium"},
            "time series": {"resource": "Time Series Analysis (Kaggle)", "duration": "3 weeks", "priority": "Medium"},
        }
    },

    "Machine Learning Engineer": {
        "required_skills": [
            "python", "machine learning", "deep learning", "tensorflow", "pytorch",
            "mlops", "docker", "kubernetes", "aws", "gcp", "model deployment",
            "api development", "fastapi", "flask", "sql", "nosql", "git",
            "ci/cd", "feature engineering", "data pipelines", "airflow",
            "spark", "kafka", "monitoring", "a/b testing", "statistics",
            "computer vision", "nlp", "transformers", "scikit-learn"
        ],
        "weights": {
            "python": 10, "machine learning": 10, "deep learning": 9, "tensorflow": 8,
            "pytorch": 8, "mlops": 9, "docker": 8, "kubernetes": 7, "aws": 7,
            "gcp": 6, "model deployment": 10, "api development": 8, "fastapi": 7,
            "flask": 6, "sql": 7, "nosql": 6, "git": 8, "ci/cd": 7,
            "feature engineering": 8, "data pipelines": 8, "airflow": 6,
            "spark": 6, "kafka": 5, "monitoring": 7, "a/b testing": 6,
            "statistics": 7, "computer vision": 6, "nlp": 6, "transformers": 7,
            "scikit-learn": 7
        },
        "learning_paths": {
            "mlops": {"resource": "MLOps Specialization (Coursera)", "duration": "8 weeks", "priority": "Critical"},
            "docker": {"resource": "Docker Mastery (Udemy)", "duration": "3 weeks", "priority": "High"},
            "kubernetes": {"resource": "Kubernetes for Developers (Linux Foundation)", "duration": "5 weeks", "priority": "High"},
            "aws": {"resource": "AWS Machine Learning Specialty (AWS Training)", "duration": "8 weeks", "priority": "High"},
            "model deployment": {"resource": "Deploying ML Models (Fast.ai)", "duration": "4 weeks", "priority": "Critical"},
            "fastapi": {"resource": "FastAPI Official Tutorial (fastapi.tiangolo.com)", "duration": "2 weeks", "priority": "Medium"},
            "airflow": {"resource": "Apache Airflow Fundamentals (Astronomer)", "duration": "3 weeks", "priority": "Medium"},
            "kafka": {"resource": "Apache Kafka for Developers (Confluent)", "duration": "4 weeks", "priority": "Low"},
            "transformers": {"resource": "NLP with Transformers (Hugging Face)", "duration": "6 weeks", "priority": "Medium"},
        }
    },

    "Full Stack Developer": {
        "required_skills": [
            "javascript", "typescript", "react", "node.js", "python", "html",
            "css", "sql", "nosql", "mongodb", "postgresql", "rest api",
            "graphql", "docker", "git", "aws", "ci/cd", "testing",
            "redux", "next.js", "express.js", "authentication", "websockets",
            "microservices", "system design", "agile", "linux", "nginx"
        ],
        "weights": {
            "javascript": 10, "typescript": 8, "react": 9, "node.js": 9,
            "python": 6, "html": 8, "css": 8, "sql": 8, "nosql": 7,
            "mongodb": 7, "postgresql": 7, "rest api": 9, "graphql": 6,
            "docker": 7, "git": 9, "aws": 6, "ci/cd": 7, "testing": 8,
            "redux": 6, "next.js": 7, "express.js": 8, "authentication": 8,
            "websockets": 5, "microservices": 7, "system design": 8,
            "agile": 6, "linux": 6, "nginx": 5
        },
        "learning_paths": {
            "typescript": {"resource": "TypeScript Handbook (typescriptlang.org)", "duration": "3 weeks", "priority": "High"},
            "react": {"resource": "React – The Complete Guide (Udemy)", "duration": "6 weeks", "priority": "Critical"},
            "node.js": {"resource": "Node.js Developer Course (Udemy)", "duration": "5 weeks", "priority": "Critical"},
            "graphql": {"resource": "GraphQL with React (Udemy)", "duration": "3 weeks", "priority": "Medium"},
            "docker": {"resource": "Docker and Kubernetes (Udemy)", "duration": "4 weeks", "priority": "High"},
            "testing": {"resource": "JavaScript Testing (Testing Library Docs)", "duration": "2 weeks", "priority": "High"},
            "microservices": {"resource": "Microservices with Node.js (Udemy)", "duration": "6 weeks", "priority": "Medium"},
            "system design": {"resource": "System Design Interview (Grokking)", "duration": "5 weeks", "priority": "High"},
            "next.js": {"resource": "Next.js Official Tutorial (nextjs.org)", "duration": "2 weeks", "priority": "Medium"},
        }
    },

    "DevOps Engineer": {
        "required_skills": [
            "linux", "docker", "kubernetes", "aws", "gcp", "azure", "terraform",
            "ansible", "ci/cd", "jenkins", "git", "python", "bash", "monitoring",
            "prometheus", "grafana", "elk stack", "networking", "security",
            "nginx", "apache", "kafka", "helm", "cloud architecture",
            "incident management", "agile", "microservices", "load balancing"
        ],
        "weights": {
            "linux": 10, "docker": 10, "kubernetes": 10, "aws": 9, "gcp": 7,
            "azure": 7, "terraform": 9, "ansible": 8, "ci/cd": 10, "jenkins": 7,
            "git": 8, "python": 7, "bash": 8, "monitoring": 9, "prometheus": 7,
            "grafana": 7, "elk stack": 6, "networking": 8, "security": 8,
            "nginx": 6, "apache": 5, "kafka": 6, "helm": 7, "cloud architecture": 9,
            "incident management": 7, "agile": 6, "microservices": 8, "load balancing": 7
        },
        "learning_paths": {
            "kubernetes": {"resource": "Certified Kubernetes Admin (Linux Foundation)", "duration": "8 weeks", "priority": "Critical"},
            "terraform": {"resource": "HashiCorp Terraform Associate (HashiCorp)", "duration": "4 weeks", "priority": "Critical"},
            "aws": {"resource": "AWS Solutions Architect Associate (AWS)", "duration": "8 weeks", "priority": "High"},
            "ansible": {"resource": "Ansible for Automation (Red Hat)", "duration": "3 weeks", "priority": "High"},
            "prometheus": {"resource": "Prometheus & Grafana (Udemy)", "duration": "2 weeks", "priority": "Medium"},
            "elk stack": {"resource": "Elastic Stack (elastic.co)", "duration": "3 weeks", "priority": "Medium"},
            "helm": {"resource": "Helm Charts (helm.sh docs)", "duration": "2 weeks", "priority": "Medium"},
            "security": {"resource": "DevSecOps Fundamentals (SANS)", "duration": "4 weeks", "priority": "High"},
        }
    },

    "Product Manager": {
        "required_skills": [
            "product strategy", "roadmapping", "user research", "agile", "scrum",
            "data analysis", "sql", "ab testing", "wireframing", "figma",
            "stakeholder management", "go-to-market", "metrics", "okrs",
            "competitive analysis", "customer interviews", "jira", "confluence",
            "communication", "leadership", "prioritization", "market research",
            "product analytics", "growth hacking", "revenue modeling"
        ],
        "weights": {
            "product strategy": 10, "roadmapping": 9, "user research": 9,
            "agile": 8, "scrum": 7, "data analysis": 8, "sql": 6, "ab testing": 7,
            "wireframing": 6, "figma": 6, "stakeholder management": 9,
            "go-to-market": 8, "metrics": 9, "okrs": 8, "competitive analysis": 8,
            "customer interviews": 8, "jira": 6, "confluence": 5, "communication": 9,
            "leadership": 9, "prioritization": 9, "market research": 8,
            "product analytics": 8, "growth hacking": 6, "revenue modeling": 7
        },
        "learning_paths": {
            "product strategy": {"resource": "Product Management (Reforge)", "duration": "6 weeks", "priority": "Critical"},
            "user research": {"resource": "User Research Methods (Nielsen Norman)", "duration": "4 weeks", "priority": "High"},
            "sql": {"resource": "SQL for Product Managers (Mode Analytics)", "duration": "3 weeks", "priority": "High"},
            "figma": {"resource": "Figma for Beginners (Figma Academy)", "duration": "2 weeks", "priority": "Medium"},
            "ab testing": {"resource": "Experimentation for PMs (Udemy)", "duration": "3 weeks", "priority": "High"},
            "okrs": {"resource": "OKR Framework (What Matters)", "duration": "1 week", "priority": "Medium"},
            "go-to-market": {"resource": "GTM Strategy (HBS Online)", "duration": "4 weeks", "priority": "High"},
            "revenue modeling": {"resource": "Financial Modeling for PMs (CFI)", "duration": "3 weeks", "priority": "Medium"},
        }
    },

    "Cybersecurity Analyst": {
        "required_skills": [
            "network security", "penetration testing", "vulnerability assessment",
            "siem", "incident response", "python", "linux", "firewall",
            "cryptography", "ethical hacking", "threat intelligence",
            "digital forensics", "cloud security", "compliance", "nist",
            "iso 27001", "owasp", "malware analysis", "security auditing",
            "scripting", "wireshark", "nmap", "metasploit", "risk management"
        ],
        "weights": {
            "network security": 10, "penetration testing": 9, "vulnerability assessment": 9,
            "siem": 8, "incident response": 9, "python": 7, "linux": 9, "firewall": 8,
            "cryptography": 7, "ethical hacking": 8, "threat intelligence": 8,
            "digital forensics": 7, "cloud security": 8, "compliance": 7, "nist": 7,
            "iso 27001": 6, "owasp": 8, "malware analysis": 7, "security auditing": 8,
            "scripting": 7, "wireshark": 8, "nmap": 8, "metasploit": 7, "risk management": 8
        },
        "learning_paths": {
            "penetration testing": {"resource": "CEH – Certified Ethical Hacker (EC-Council)", "duration": "8 weeks", "priority": "Critical"},
            "siem": {"resource": "Splunk Fundamentals (Splunk Training)", "duration": "3 weeks", "priority": "High"},
            "incident response": {"resource": "GCIH Certification (SANS)", "duration": "6 weeks", "priority": "Critical"},
            "cloud security": {"resource": "CCSP – Cloud Security (ISC2)", "duration": "8 weeks", "priority": "High"},
            "owasp": {"resource": "OWASP Top 10 (owasp.org)", "duration": "2 weeks", "priority": "High"},
            "malware analysis": {"resource": "Practical Malware Analysis (NoStarch)", "duration": "5 weeks", "priority": "Medium"},
            "cryptography": {"resource": "Cryptography I (Coursera – Stanford)", "duration": "4 weeks", "priority": "Medium"},
            "nist": {"resource": "NIST Cybersecurity Framework (NIST)", "duration": "2 weeks", "priority": "Medium"},
        }
    },

    "Cloud Architect": {
        "required_skills": [
            "aws", "gcp", "azure", "terraform", "kubernetes", "docker",
            "networking", "security", "cost optimization", "cloud architecture",
            "microservices", "serverless", "devops", "ci/cd", "python",
            "infrastructure as code", "load balancing", "auto scaling",
            "databases", "storage", "monitoring", "compliance", "multi-cloud",
            "disaster recovery", "linux"
        ],
        "weights": {
            "aws": 10, "gcp": 8, "azure": 8, "terraform": 9, "kubernetes": 9,
            "docker": 8, "networking": 9, "security": 9, "cost optimization": 8,
            "cloud architecture": 10, "microservices": 8, "serverless": 7,
            "devops": 8, "ci/cd": 7, "python": 7, "infrastructure as code": 9,
            "load balancing": 8, "auto scaling": 8, "databases": 7, "storage": 7,
            "monitoring": 8, "compliance": 7, "multi-cloud": 7, "disaster recovery": 8,
            "linux": 8
        },
        "learning_paths": {
            "aws": {"resource": "AWS Solutions Architect Professional (AWS)", "duration": "10 weeks", "priority": "Critical"},
            "terraform": {"resource": "Terraform Associate Certification (HashiCorp)", "duration": "4 weeks", "priority": "Critical"},
            "kubernetes": {"resource": "CKA – Kubernetes Admin (CNCF)", "duration": "8 weeks", "priority": "High"},
            "cloud architecture": {"resource": "Google Cloud Professional Architect (Google)", "duration": "10 weeks", "priority": "Critical"},
            "serverless": {"resource": "Serverless Architectures (AWS Lambda docs)", "duration": "3 weeks", "priority": "Medium"},
            "disaster recovery": {"resource": "AWS Disaster Recovery (AWS Well-Architected)", "duration": "2 weeks", "priority": "High"},
            "compliance": {"resource": "Cloud Compliance Frameworks (Coursera)", "duration": "3 weeks", "priority": "Medium"},
            "multi-cloud": {"resource": "Multi-Cloud Strategy (Google Cloud)", "duration": "4 weeks", "priority": "Medium"},
        }
    },

    "Data Engineer": {
        "required_skills": [
            "python", "sql", "spark", "hadoop", "kafka", "airflow", "dbt",
            "aws", "gcp", "data warehousing", "etl", "data modeling",
            "postgresql", "nosql", "snowflake", "redshift", "bigquery",
            "docker", "git", "linux", "scala", "data quality",
            "data governance", "stream processing", "batch processing"
        ],
        "weights": {
            "python": 10, "sql": 10, "spark": 9, "hadoop": 7, "kafka": 8,
            "airflow": 9, "dbt": 8, "aws": 7, "gcp": 6, "data warehousing": 9,
            "etl": 10, "data modeling": 9, "postgresql": 8, "nosql": 7,
            "snowflake": 7, "redshift": 6, "bigquery": 6, "docker": 7,
            "git": 8, "linux": 7, "scala": 6, "data quality": 8,
            "data governance": 7, "stream processing": 8, "batch processing": 8
        },
        "learning_paths": {
            "spark": {"resource": "Apache Spark with Python (Databricks)", "duration": "5 weeks", "priority": "Critical"},
            "airflow": {"resource": "Apache Airflow Fundamentals (Astronomer)", "duration": "3 weeks", "priority": "Critical"},
            "kafka": {"resource": "Apache Kafka for Developers (Confluent)", "duration": "4 weeks", "priority": "High"},
            "dbt": {"resource": "dbt Fundamentals (dbt Learn)", "duration": "2 weeks", "priority": "High"},
            "data modeling": {"resource": "Data Modeling Fundamentals (Udemy)", "duration": "3 weeks", "priority": "Critical"},
            "snowflake": {"resource": "Snowflake SnowPro Core (Snowflake)", "duration": "3 weeks", "priority": "Medium"},
            "data governance": {"resource": "Data Governance Fundamentals (DAMA)", "duration": "3 weeks", "priority": "Medium"},
            "scala": {"resource": "Scala for Data Engineers (Rock the JVM)", "duration": "5 weeks", "priority": "Low"},
        }
    }
}

EXPERIENCE_MULTIPLIERS = {
    "Beginner (0–1 years)": 0.7,
    "Intermediate (1–3 years)": 1.0,
    "Experienced (3–6 years)": 1.2,
    "Senior (6+ years)": 1.4
}
