from models import Famq

s=""

while s != 'Q':

    q = input("Question:\n")
    a = input("Answer:\n")

    print("Okay...\nQuestion:\n{}\n\nAnswer:\n{}\n\n Is this alright? 'Y' to commit to the database, 'Q' to quit, anything else to reject and enter a new one.".format(q,a))
    s = input()
    if s == 'Y':
        print("Committing...\n\n\n\n")
        Famq.create(question=q, answer=a)

