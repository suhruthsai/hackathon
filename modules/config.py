SKILLS_LIST = {
    'programming': [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust', 'swift',
        'kotlin', 'php', 'typescript', 'scala', 'perl', 'r', 'matlab', 'bash',
        'shell', 'powershell', 'html', 'css', 'sql', 'plsql', 'mongodb', 'oracle',
        'mysql', 'postgresql', 'sqlite', 'redis', 'elasticsearch', 'docker', 'kubernetes',
        'jenkins', 'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence',
        'aws', 'azure', 'gcp', 'google cloud', 'firebase', 'heroku', 'digitalocean',
        'react', 'angular', 'vue', 'nodejs', 'django', 'flask', 'spring', 'laravel',
        'express', 'fastapi', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'pandas', 'numpy', 'scipy', 'matplotlib', 'seplotly', 'aborn', 'tableau',
        'powerbi', 'excel', 'word', 'powerpoint', 'outlook', 'teams', 'slack',
        'rest api', 'graphql', 'grpc', 'websocket', 'microservices', 'agile', 'scrum',
        'kanban', 'jira', 'confluence', 'linux', 'unix', 'windows', 'macos',
        'networking', 'security', 'cybersecurity', 'penetration testing', 'firewall',
        'vpn', 'tcp/ip', 'dns', 'dhcp', 'load balancing', 'cdn', 'cache',
        'redis', 'memcached', 'rabbitmq', 'kafka', 'activemq', 'spark', 'hadoop',
        'hive', 'pig', 'sqoop', 'flume', 'zookeeper', 'etl', 'data warehouse',
        'data lake', 'snowflake', 'bigquery', 'redshift', 'databricks', 'mlops',
        'ci/cd', 'devops', 'sre', 'iot', 'blockchain', 'ethereum', 'solidity'
    ],
    'soft_skills': [
        'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
        'critical thinking', 'creativity', 'adaptability', 'time management',
        'project management', 'conflict resolution', 'negotiation', 'presentation',
        'writing', 'interpersonal', 'customer service', 'client relations',
        'stakeholder management', 'mentoring', 'coaching', 'collaboration',
        'attention to detail', 'organization', 'planning', 'strategic thinking',
        'decision making', 'initiative', 'self-motivated', 'fast learner'
    ],
    'domain': [
        'finance', 'banking', 'insurance', 'healthcare', 'pharma', 'retail',
        'e-commerce', 'manufacturing', 'logistics', 'supply chain', 'telecom',
        'media', 'entertainment', 'education', 'government', 'non-profit',
        'consulting', 'legal', 'real estate', 'hospitality', 'travel', 'food',
        'automotive', 'aerospace', 'energy', 'utilities', 'mining', 'construction'
    ]
}

ALL_SKILLS = set()
for category in SKILLS_LIST:
    ALL_SKILLS.update([s.lower() for s in SKILLS_LIST[category]])

EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_PATTERN = r'(\+91)?[6-9]\d{9}'
URL_PATTERN = r'https?://[^\s]+'

DEGREE_KEYWORDS = [
    'b.tech', 'b.e', 'b.sc', 'b.com', 'b.a', 'bba', 'bca',
    'm.tech', 'm.e', 'm.sc', 'm.com', 'm.a', 'mba', 'mca',
    'ph.d', 'phd', 'doctorate', 'diploma', 'certificate',
    '10th', '12th', 'ssc', 'hsc', 'cbse', 'icse', 'intermediate'
]

EXPERIENCE_KEYWORDS = [
    'experience', 'work history', 'employment', 'professional background',
    'career', 'internship', 'trainee', 'fresher', 'years', 'months'
]

FRAUD_KEYWORDS = [
    'guarantee job', 'pay fee', 'no interview', 'job without',
    'immediate joining', 'zero interview', 'direct placement',
    'refund money', 'registration fee', 'processing fee'
]

SPACY_MODEL = 'en_core_web_sm'
