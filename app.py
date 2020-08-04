from flask import Flask, request, render_template

app = Flask(__name__)


def time_formatting(string):
    ugly_time = string.split(":")
    correct_time = ugly_time[0] + ":" + ugly_time[1] + ":" + str("{0:.1f}".format(float(ugly_time[2])))
    return correct_time


def log_appending(athlete_info):
    logfile = open("log.txt", "a+")
    logfile.write(str(athlete_info) + "\n")
    logfile.close()


@app.route('/', methods=["GET", "POST"])
def home_page():
    athletes = []
    error = ''
    try:

        if request.method == "POST":
            initial_string = request.form['string_entry']
            separator = request.form['separator']
            string_splitted_by_CR = str(initial_string).split("[CR]")

            if len(string_splitted_by_CR) > 2:
                for i in range(len(string_splitted_by_CR) - 1):
                    splitted_string = str(string_splitted_by_CR[i]).split(separator)
                    athlete_info = {"athlete_number": splitted_string[0], "channel_ID": splitted_string[1],
                                    "time": time_formatting(splitted_string[2]), "group_number": splitted_string[3]}
                    athletes.append(athlete_info)
                    log_appending(athlete_info)
            elif len(string_splitted_by_CR) == 2:
                splitted_string = str(string_splitted_by_CR[0]).split(separator)
                athlete_info = {"athlete_number": splitted_string[0], "channel_ID": splitted_string[1],
                                "time": splitted_string[2].split(":"), "group_number": splitted_string[3]}
                athletes.append(athlete_info)
                log_appending(athlete_info)
            else:
                error = "No '[CR]' given. Check your string please!"

            print(athletes)
        else:
            error = "USE post please"
        return render_template("index.html", athletes=athletes, error=error)

    except Exception as e:
        # flash(e)
        return render_template("index.html", error=error)


if __name__ == '__main__':
    app.run()
