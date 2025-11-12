import csv
def get_name():
    name_list = list(input("input: ").upper().strip())
    score = input("Score;")
    try:
        name = name_list[0] + name_list[1] + name_list[2]
    except IndexError:
        print("f u, try again")
        get_name()
    else: check_zwerg_file(name, score)

def check_zwerg_file(name, score):
    try:
        with open('zwerg_score_ex.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if int(row[1]) >= int(score):
                    print(f"High Score: {row[0], row[1]}")
                else:
                    print("New High Score!")
                    print(f"Old: {row[0]} {row[1]} -> New: {name} {score}")
                    with open('zwerg_score_ex.csv', 'w', newline= "") as n_file:
                        writer = csv.writer(n_file)
                        writer.writerow([name, score])

            # find the highest score, check to see who is higher you or them
            # if the high score is more, show that, else show New high score {your score} Old Score {they score}
            # write your score
    except FileNotFoundError:
        with open('zwerg_score_ex.csv', 'w', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([name, score])
            print("New High Score!")
            print(f"Old: N/A 0 -> New: {name} {score}")
            # add title
            # write your crap in, show your crap as new high score


get_name()