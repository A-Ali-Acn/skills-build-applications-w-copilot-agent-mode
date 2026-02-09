from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Create Users

        users = []
        user_data = [
            {'name': 'Spider-Man', 'email': 'spiderman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Iron Man', 'email': 'ironman@marvel.com', 'team': marvel, 'is_superhero': True},
            {'name': 'Wonder Woman', 'email': 'wonderwoman@dc.com', 'team': dc, 'is_superhero': True},
            {'name': 'Batman', 'email': 'batman@dc.com', 'team': dc, 'is_superhero': True},
        ]
        for data in user_data:
            user = User(**data)
            user.save()
            users.append(user)

        # Create Workouts
        workout1 = Workout.objects.create(name='Web Swing', description='Swinging through the city')
        workout2 = Workout.objects.create(name='Flight', description='Flying workout')
        workout1.suggested_for.set([users[0]])
        workout2.suggested_for.set([users[1], users[2]])

        # Create Activities
        Activity.objects.create(user=users[0], activity_type='Swing', duration=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='Fly', duration=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type='Battle', duration=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='Detective Work', duration=90, date=timezone.now().date())

        # Create Leaderboards
        Leaderboard.objects.create(team=marvel, total_points=150)
        Leaderboard.objects.create(team=dc, total_points=200)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully!'))
