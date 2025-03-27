from django.core.management.base import BaseCommand
from decouple import config
from django.utils import termcolors
import redis

class Command(BaseCommand):
    help = "Completely clears the Redis database"
    
    def handle(self, *args, **kwargs):        
        REDIS_HOST = config('REDIS_HOST')
        REDIS_PORT = config('REDIS_PORT')
        REDIS_PASSWORD = config('REDIS_PASSWORD')
        REDIS_DB = config('REDIS_DB')
        
        try:
            r = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                socket_timeout=5
            )

            # Connection test
            r.ping()
            
            # Clearing operation
            r.flushdb()
            self.stdout.write(termcolors.make_style(fg="green")('✓ Redis flushed'))
             
        except redis.AuthenticationError:
            self.stdout.write(termcolors.make_style(fg="red")('✘ Redis password is incorrect'))
        except redis.ConnectionError:
            self.stdout.write(termcolors.make_style(fg="red")('✘ Could not connect to Redis server'))
        except Exception as e:
            self.stdout.write(termcolors.make_style(fg="red")(f'✘ Unknown error: {str(e)}'))