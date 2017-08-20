from models import Question, Answer


for n in Question.select():
    print("Question {}:{}".format(n.id,n.text))
    a = input("Delete it?")
    if a == "Y" or a == 'y':
        n.delete_instance()


for n in Answer.select():
    print("Answer {}:{} to question {}".format(n.id,n.text,n.question.text))
    a = input("Delete it?")
    if a == "Y" or a =='y':
        n.delete_instance()
