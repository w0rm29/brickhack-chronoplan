import sys
import spacy
from dateutil import parser
from spacy.tokens import DocBin
from dateutil.parser import parse as parse_date
from datetime import datetime, timedelta
import pytz

# Load Spacy with the English language model
nlp = spacy.load("en_core_web_sm")


tags = {
    'work': {'meeting', 'report', 'presentation', 'deadline', 'project', 'client', 'email', 'task', 'conference', 'proposal', 'brainstorm', 'schedule', 'agenda', 'deliverable'},
    'personal': {'call', 'chores', 'organize', 'plan', 'event', 'personal', 'self-care', 'self care', 'journal', 'reflection', 'goal', 'hobby', 'leisure', 'relaxation'},
    'health': {'workout', 'exercise', 'gym', 'yoga', 'run', 'walk', 'fitness', 'activity', 'training', 'cardio', 'strength', 'stretching', 'workout plan', 'exercise routine', 'sports', 'outdoor', 'indoor', 'nutrition', 'diet', 'meditation', 'mindfulness', 'sleep', 'doctor', 'check-up', 'therapy', 'mental health'},
    'shopping': {'groceries', 'shopping', 'list', 'purchase', 'buy', 'household', 'supplies', 'grocery list', 'shopping list', 'household items'},
    'study': {'study', 'read', 'research', 'learn', 'assignment', 'project', 'exam', 'study session', 'class', 'lecture', 'notes', 'textbook', 'study group', 'study guide', 'quiz', 'test', 'paper', 'article', 'tutorial'},
    'home': {'clean', 'organize', 'repair', 'home improvement', 'maintenance', 'decorate', 'house', 'home', 'renovation', 'DIY', 'fix', 'declutter', 'tidy', 'laundry', 'dishes', 'vacuum'},
    'finances': {'budget', 'bills', 'expenses', 'savings', 'investment', 'financial', 'money', 'finance', 'bank', 'account', 'payment', 'debt', 'loan', 'credit card', 'retirement', 'income', 'tax', 'insurance'},
    'social': {'meet', 'event', 'party', 'dinner', 'hangout', 'socialize', 'friend', 'gathering', 'social', 'network', 'community', 'celebrate', 'catch-up', 'reunion', 'date', 'outing', 'fun'},
    'family': {'family', 'parenting', 'children', 'kids', 'baby', 'parent', 'mom', 'dad', 'siblings', 'family event', 'family time', 'family outing', 'family dinner', 'family gathering', 'family vacation'},
    'career': {'career', 'job', 'promotion', 'interview', 'resume', 'networking', 'professional development', 'skill development', 'workshop', 'seminar', 'training', 'mentor', 'career growth', 'career planning'},
    'hobbies': {'hobby', 'interest', 'craft', 'art', 'music', 'dance', 'photography', 'painting', 'cooking', 'baking', 'gardening', 'DIY', 'creative', 'passion', 'hobby project', 'hobby time'},
    'events': {'event', 'party', 'celebration', 'birthday', 'wedding', 'anniversary', 'graduation', 'reunion', 'holiday', 'festival', 'concert', 'performance', 'show', 'exhibition', 'conference'},
    'appointments': {'appointment', 'schedule', 'meeting', 'call', 'doctor', 'dentist', 'check-up', 'check up', 'therapy', 'consultation', 'interview', 'reservation', 'booking'},
}


def check_keywords(sentence, tag_keywords):
    present_keywords = set()
    for word in tag_keywords:
        if word in sentence.lower():
            return True
    return False


from configparser import Error
def generate_tags(input):
  tag_found = ""
    # Check for presence of study-related keywords in the user's sentence
  for tag, values in tags.items():
    found_keywords = check_keywords(input.lower(), values)

    if found_keywords:
      tag_found = tag
      break
    else:
      tag_found = 'Miscellaneous'
  return tag_found


def extract_timestamp(input):
  doc = nlp(input)

  # Extract entities with label TIME
  time_entities = [ent.text for ent in doc.ents if ent.label_ == "TIME"]
  if len(time_entities) > 0:
    # Convert each time entity to HH:MM:SS format
    converted_times = []
    for time_str in time_entities:
        try:
            parsed_time = parser.parse(time_str)
            formatted_time = parsed_time.strftime("%H:%M:%S")
            converted_times.append(formatted_time)
        except ValueError:
            # Handle parsing errors if any
            converted_times.append(None)
            print(f"Unable to extract time")
    return converted_times[0]
  else:
    return None


def extract_date(input):
  doc = nlp(input)

  # Create a DocBin object to store the processed document
  doc_bin = DocBin(docs=[doc])

  # Use spaCy's parser to extract dates
  dates = []
  for ent in doc.ents:
      if ent.label_ == "DATE":
          dates.append(ent.text)

  # Convert extracted dates to DD-MM-YYYY format using dateutil.parser
  formatted_dates = []
  for date_str in dates:
      try:
          parsed_date = parse_date(date_str, fuzzy=True)
      except ValueError:
          if date_str.lower() == "tomorrow":
              # Get current time in local timezone
              local_timezone = pytz.timezone('US/Eastern')  # Replace 'Your/Timezone' with your timezone
              current_time = datetime.now(local_timezone)
              # Add a day to the current date
              parsed_date = current_time + timedelta(days=1)
          else:
              raise
      # formatted_date = parsed_date.strftime("%d-%m-%Y")
      formatted_date = parsed_date.strftime("%Y-%m-%d")
      formatted_dates.append(formatted_date)

  # Print the extracted and formatted dates
#   print("Extracted Dates:")
  # for date in formatted_dates:
      # print(date)

  if len(formatted_dates) > 0:
    return formatted_dates[0]
  else:
    return None


def get_details(task_title):
  task = dict()
  task["title"] = task_title
  task["tag"] = generate_tags(task_title)
  task["date"] = extract_date(task_title)
  task["time"] = extract_timestamp(task_title)
  return task


# if __name__ == "__main__":
#   title = sys.argv[1]
#   task_details = get_details(title)
#   print(task_details)



from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
   return ('chronoplan')

@app.route('/text-ai')
def text_ai():
  title = request.args.get('title') 
  return get_details(title)

app.run()



# source ./venv/scripts/activate
# pip freeze > requirements.txt
# pip install -r requirements.txt
# deactivate