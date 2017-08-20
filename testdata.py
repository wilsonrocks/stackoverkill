from models import Question, Answer
from time import sleep

q1 = Question.create(text="Should I irrigate my alpine trooper?")
Answer.create(question=q1, text= "You haven't already?")
Answer.create(question=q1, text= "Never!")
Answer.create(question=q1, text= "Just Testing here")
q2 = Question.create(text="Are Cruise Missiles worth it?")
Answer.create(question=q2, text="Unless we gimp them in the ruleset")
Answer.create(question=q2, text="So worth it!")

