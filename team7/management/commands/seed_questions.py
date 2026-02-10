"""
Management command to seed TOEFL questions into the database.
Per SRS FR-WR and FR-SP requirements.

Usage:
    python manage.py seed_questions --database=team7
"""
from django.core.management.base import BaseCommand
from team7.models import Question, TaskType, Mode


class Command(BaseCommand):
    help = 'Seeds TOEFL Writing and Speaking questions into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete existing questions before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Question.objects.using('team7').count()
            Question.objects.using('team7').all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing questions'))

        questions_data = [
            # =====================
            # WRITING TASKS
            # =====================
            {
                'task_type': TaskType.WRITING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 2,
                'prompt_text': (
                    "Do you agree or disagree with the following statement? "
                    "Technology has made the world a better place to live. "
                    "Use specific reasons and examples to support your answer."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.WRITING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 3,
                'prompt_text': (
                    "Some people believe that university students should be required to attend classes. "
                    "Others believe that going to classes should be optional for students. "
                    "Which point of view do you agree with? Use specific reasons and details to explain your answer."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.WRITING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 2,
                'prompt_text': (
                    "Do you agree or disagree with the following statement? "
                    "It is better to work in teams than to work alone. "
                    "Use specific reasons and examples to support your position."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.WRITING,
                'mode': Mode.INTEGRATED,
                'difficulty': 4,
                'prompt_text': (
                    "Summarize the points made in the lecture, being sure to explain how they "
                    "challenge the specific points made in the reading passage.\n\n"
                    "[Reading Passage]: The benefits of remote work include increased productivity, "
                    "better work-life balance, and reduced commuting costs. Studies show that employees "
                    "working from home report higher satisfaction levels and companies save on office overhead.\n\n"
                    "[Lecture Summary]: While remote work has advantages, it also has significant drawbacks. "
                    "Studies indicate that isolation can harm mental health, collaborative innovation decreases "
                    "without in-person interaction, and blurred work-home boundaries lead to burnout."
                ),
                'resource_url': 'https://example.com/audio/passage1.mp3'
            },
            {
                'task_type': TaskType.WRITING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 3,
                'prompt_text': (
                    "Do you agree or disagree with the following statement? "
                    "The most important aspect of a job is the money a person earns. "
                    "Use specific reasons and examples to support your answer."
                ),
                'resource_url': None
            },
            # =====================
            # SPEAKING TASKS
            # =====================
            {
                'task_type': TaskType.SPEAKING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 1,
                'prompt_text': (
                    "Describe your favorite place to study. "
                    "Explain why you like this place and how it helps you study effectively."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.SPEAKING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 2,
                'prompt_text': (
                    "Some people prefer to live in a small town. Others prefer to live in a big city. "
                    "Which place would you prefer to live in? Use specific reasons and details to support your answer."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.SPEAKING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 2,
                'prompt_text': (
                    "Do you agree or disagree with the following statement? "
                    "It is important to learn about other cultures. "
                    "Use details and examples to explain your opinion."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.SPEAKING,
                'mode': Mode.INTEGRATED,
                'difficulty': 4,
                'prompt_text': (
                    "The university has announced a new policy requiring all students to take an online course "
                    "before graduation. The woman expresses her opinion about the announcement. "
                    "State her opinion and explain the reasons she gives for holding that opinion.\n\n"
                    "[Context]: Read the announcement and listen to two students discussing it."
                ),
                'resource_url': 'https://example.com/audio/conversation1.mp3'
            },
            {
                'task_type': TaskType.SPEAKING,
                'mode': Mode.INDEPENDENT,
                'difficulty': 3,
                'prompt_text': (
                    "Describe an important decision you made. "
                    "Explain why this decision was important and how it affected your life."
                ),
                'resource_url': None
            },
            {
                'task_type': TaskType.SPEAKING,
                'mode': Mode.INTEGRATED,
                'difficulty': 5,
                'prompt_text': (
                    "Using points and examples from the lecture, explain the two types of social influence: "
                    "normative and informational. Describe how each type affects individual behavior in groups.\n\n"
                    "[Context]: You will read a passage about social psychology, then hear a lecture on the topic."
                ),
                'resource_url': 'https://example.com/audio/lecture1.mp3'
            },
        ]

        created_count = 0
        for q_data in questions_data:
            question, created = Question.objects.using('team7').get_or_create(
                prompt_text=q_data['prompt_text'],
                defaults={
                    'task_type': q_data['task_type'],
                    'mode': q_data['mode'],
                    'difficulty': q_data['difficulty'],
                    'resource_url': q_data['resource_url'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {question.get_task_type_display()} - {question.mode} (Difficulty: {question.difficulty})'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  Already exists: {question.question_id}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Seeding complete! Created {created_count} new questions.')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total questions in database: {Question.objects.using("team7").count()}')
        )
