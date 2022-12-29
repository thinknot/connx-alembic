from datetime import datetime

from .flapp.extension import db
from .model.library import Book
from .model.sites import Project, Site
from .model.sources import Device
from .model.ublog import Note, Person


def rebuild_db():
    db.drop_all()
    db.create_all()

    for data in PEOPLE_NOTES:
        new_person = Person(lname=data.get("lname"), fname=data.get("fname"))
        for content, timestamp in data.get("notes", []):
            new_person.notes.append(
                Note(
                    content=content,
                    timestamp=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                )
            )
        db.session.add(new_person)
    db.session.commit()

    for data in AUTHOR_BOOKS:
        new_author = Person(lname=data.get("lname"), fname=data.get("fname"))
        for content in data.get("books"):
            new_author.books.append(Book(title=content))
        db.session.add(new_author)
    db.session.commit()

    for data in SITE_PROJECT_DEVICES:
        new_project = Project(
            name=data.get("name"), description=data.get("description")
        )
        for content in data.get("sites"):
            new_site = Site(
                summary=content.get("summary"),
                pv_power=content.get("pv_power"),
                timezone=content.get("timezone"),
                address1=content.get("address1"),
                address2=content.get("address2"),
            )
            for dvc in content.get("devices"):
                new_site.devices.append(
                    Device(name=dvc.get("name"), type=dvc.get("type"))
                )
            new_project.sites.append(new_site)
        db.session.add(new_project)
    db.session.commit()


SITE_PROJECT_DEVICES = [
    {
        "name": "mcdonald",
        "description": "McDonald Toyota Greeley CO",
        "sites": [
            {
                "summary": "McDonald Toyota",
                "pv_power": 250000,
                "timezone": "America/Denver",
                "address1": "12484 E Weaver Pl",
                "address2": "Centennial, CO, 80111",
                "devices": [
                    {
                        "name": "egauge63394",
                        "type": "EGAUGE",
                    },
                    {
                        "name": "Ehrlich+Toyota",
                        "type": "EWON",
                    },
                ],
            }
        ],
    },
    {
        "name": "stapp",
        "description": "Stapp Toyota Frederick CO",
        "sites": [
            {
                "summary": "Stapp Interstate Toyota",
                "pv_power": "250000",
                "timezone": "America/Denver",
                "address1": "8019 Raspberry Way",
                "address2": "Frederick, CO",
                "devices": [
                    {
                        "name": "egauge53346",
                        "type": "EGAUGE",
                    },
                    {
                        "name": "Stapp+Toyota",
                        "type": "EWON",
                    },
                ],
            }
        ],
    },
    {
        "name": "loveland",
        "description": "",
        "sites": [
            {
                "summary": "Loveland Elway BMW",
                "pv_power": "250000",
                "timezone": "America/Denver",
                "address1": "4150 Byrd Dr",
                "address2": "Loveland, CO 80538",
                "devices": [
                    {
                        "name": "Elway+BMW",
                        "type": "EWON",
                    }
                ],
            },
            {
                "summary": "Loveland Elway Mini",
                "pv_power": "25000",
                "timezone": "America/Denver",
                "address1": "4055 Byrd Dr",
                "address2": "Loveland, CO 80538",
                "devices": [
                    {
                        "name": "Elway+Mini",
                        "type": "EWON",
                    }
                ],
            },
        ],
    },
    {
        "name": "centennial",
        "description": "Solar canopies at US Citizenship Offices. Centennial, CO",
        "sites": [
            {
                "summary": "Centennial USCIS Field Office",
                "pv_power": "250000",
                "timezone": "America/Denver",
                "address1": "12484 E Weaver Pl",
                "address2": "Centennial, CO, 80111",
                "devices": [
                    {
                        "name": "egauge38888",
                        "type": "EGAUGE",
                    }
                ],
            }
        ],
    },
]

PEOPLE_NOTES = [
    {
        "lname": "Ruprecht",
        "fname": "Knecht",
        "notes": [
            ("I swear, I'll do better this year.", "2022-01-01 09:15:03"),
            ("Really! Only good deeds from now on!", "2022-02-06 13:09:21"),
        ],
    },
    {
        "lname": "Fairy",
        "fname": "Tooth",
        "notes": [
            ("I brush my teeth after each meal.", "2022-01-06 17:10:24"),
            ("The other day a friend said, I have big teeth.", "2022-03-05 22:17:54"),
            ("Do you pay per gram?", "2022-03-05 22:18:10"),
        ],
    },
    {
        "lname": "Jerome",
        "fname": "Powell",
        "notes": [
            ("Please keep the current inflation rate in mind!", "2022-01-07 22:47:54"),
            ("No need to hide the eggs this time.", "2022-04-06 13:03:17"),
        ],
    },
]

AUTHOR_BOOKS = [
    {
        "fname": "Wiz",
        "lname": "Kid",
        "books": [
            "Gathering Moss",
            "Fixing Everything",
        ],
    },
    {
        "name": "Davido",
        "lname": "Opec",
        "books": [
            "How to f up the economy",
            "Starlink plus neuralink inhibitor chip",
        ],
    },
    {"fname": "Burna boy", "books": []},
    {
        "fname": "Robin",
        "lname": " Kimmer",
        "books": [
            "Braiding Sweetgrass",
        ],
    },
    {
        "fname": "Jay",
        "lname": "-Z",
        "books": [
            "How to be feared",
            "How to fumble the bag",
        ],
    },
    {
        "fname": "M.T.",
        "lname": "Richardson",
        "books": ["Practical Blacksmithing", "Practical Carriage Building"],
    },
]

SHIPMENTS = []
