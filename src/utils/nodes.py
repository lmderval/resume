from dataclasses import dataclass

from typing import List, Optional


@dataclass
class Information:
    email: str
    phone: str
    linkedin: Optional[str]
    github: Optional[str]


@dataclass
class School:
    name: str
    short_description: str
    begin: str
    end: Optional[str]
    topics: List[str]


@dataclass
class Certificate:
    name: str
    year: int
    note: Optional[str]


@dataclass
class Task:
    name: str
    subtasks: List[str]


@dataclass
class Experience:
    name: str
    where: str
    begin: str
    end: Optional[str]
    tasks: List[str | Task]


@dataclass
class Project:
    name: str
    description: str
    personal: bool
    ongoing: bool
    languages: List[str]


@dataclass
class Language:
    name: str
    level: int
    note: Optional[str]


@dataclass
class SkillCategory:
    name: str
    skills: List[str]


@dataclass
class Interest:
    name: str
    icon: str


@dataclass
class Resume:
    name: str
    description: str
    profile: str
    information: Information
    education: List[School]
    certificates: List[Certificate]
    experiences: List[Experience]
    projects: List[Project]
    languages: List[Language]
    skill_categories: List[SkillCategory]
    interests: List[Interest]
    variant: Optional[bool] = False
