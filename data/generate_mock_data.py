import json
import random

first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Laura", "Robert", "Emma", "Daniel", "Olivia", "James", "Sophia", "William", "Isabella"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"]
titles = ["Software Engineer", "Senior Software Engineer", "Data Scientist", "Product Manager", "Frontend Developer", "Backend Developer", "DevOps Engineer", "Machine Learning Engineer", "System Administrator", "UX Designer"]
locations = ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", "Chicago, IL", "Remote", "Boston, MA", "Denver, CO"]
universities = ["MIT", "Stanford University", "Carnegie Mellon", "UC Berkeley", "University of Washington", "NYU", "University of Illinois", "Georgia Tech", "State University"]
all_skills = [
    "Python", "Java", "C++", "JavaScript", "React", "Node.js", "SQL", "NoSQL", 
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "Machine Learning", 
    "Data Analysis", "Project Management", "Agile", "Scrum", "UI/UX", "Figma", 
    "FastAPI", "Django", "Spring Boot", "TensorFlow", "PyTorch", "Redis"
]

candidates = []

for i in range(1, 101):
    candidate = {
        "id": f"CAND{str(i).zfill(3)}",
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "email": f"candidate{i}@example.com",
        "phone": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "location": random.choice(locations),
        "current_title": random.choice(titles),
        "years_experience": random.randint(0, 15),
        "education": {
            "degree": random.choice(["B.S. Computer Science", "M.S. Computer Science", "B.A. Design", "B.S. Information Technology", "Ph.D. Machine Learning"]),
            "university": random.choice(universities),
            "graduation_year": random.randint(2010, 2024)
        },
        "skills": random.sample(all_skills, k=random.randint(5, 12)),
        "source": random.choice(["Career Page", "LinkedIn Integration", "Zoho Recruit", "Greenhouse", "Email Submission"]),
        "open_to_work": random.choice([True, False]),
        "last_updated": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}T10:00:00Z"
    }
    candidates.append(candidate)

with open("mock_candidates.json", "w") as f:
    json.dump(candidates, f, indent=4)

print("Generated 100 candidates in mock_candidates.json")
