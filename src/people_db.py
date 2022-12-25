# people.py


from datetime import datetime

from flask import abort, make_response


def get_timestamp():
    # string representation of the current timestamp
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# dictionary data structure, fake a proper database
PEOPLE = {
    # A person’s last name must be unique
    "Fairy": {
        "fname": "Tooth",
        "lname": "Fairy",
        "timestamp": get_timestamp(),
    },
    "Ruprecht": {
        "fname": "Knecht",
        "lname": "Ruprecht",
        "timestamp": get_timestamp(),
    },
    "Bunny": {
        "fname": "Easter",
        "lname": "Bunny",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    # runs when server receives an HTTP request to GET /api/people
    return list(PEOPLE.values())


def read_one(lname):
    if lname in PEOPLE:
        return PEOPLE[lname]
    else:
        abort(404, f"Person with last name {lname} not found")


def create(person):
    # request body must contain a last name
    lname = person.get("lname")

    fname = person.get("fname", "")

    if lname and lname not in PEOPLE:

        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        # respond with the new object and a 201 HTTP code
        return PEOPLE[lname], 201

    else:

        abort(
            406,
            f"Person with last name {lname} already exists",
        )


def update(lname, person):
    # When a person with the provided last name exists
    if lname in PEOPLE:
        # update the person data
        PEOPLE[lname]["fname"] = person.get("fname", PEOPLE[lname]["fname"])
        PEOPLE[lname]["timestamp"] = get_timestamp()
        return PEOPLE[lname]
    else:
        abort(404, f"Person with last name {lname} not found")


def delete(lname):
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(f"{lname} successfully deleted", 200)
    else:
        abort(404, f"Person with last name {lname} not found")
