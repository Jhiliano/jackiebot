
from icalendar import Calendar, Event, vCalAddress, vText
from typing import List

from .group import Group
from .course import Course


class EdtCalendar:
    __PERIODID = "-//Google Inc//Google Calendar 70.9054//EN"
    __VERSION = '2.0'
    
    def __init__(self, courses: List[Course], level: str) -> None:
        self.level = level
        self.name = {Group.ALL:f'{level}A', Group.GROUP1:f'{level}G1', Group.GROUP2:f'{level}G2', 'Exam':f'{level}E'}
        self.calendar = {Group.ALL:Calendar(), Group.GROUP1:Calendar(), Group.GROUP2:Calendar(), 'Exam':Calendar()}
        for c in self.calendar:
            self.calendar[c].add('prodid', self.__PERIODID)
            self.calendar[c].add('version', self.__VERSION)
        self.__gen_ics(courses)
    
    def __gen_ics(self, courses: List[Course]) -> None:
         for c in courses:
            event = Event()
            if c.exam:
                call: Calendar = self.calendar['Exam']
            else:
                call: Calendar = self.calendar[c.group]
            event.add('summary',c.name)
            event.add('dtstart',c.begin)
            event.add('dtend', c.end)
            event.add('location', vText(c.location))
            if c.teacher != '':
                event.add('organizer', self.__person(name=c.teacher, mail='prof@stri.fr', role='CHAIR', status='ACCEPTED', group=False), encode=0)
            event.add('attendee', self.__person(name=c.get_group_name(), mail=f'{str(c.group).lower()}@stri.fr', role='REQ-PARTICIPANT', status='ACCEPTED', group=True), encode=0)
            call.add_component(event)
    
    def __person(self, name:str, mail: str, role: str, status: str, group: bool) -> vCalAddress:
        cutype = 'GROUP' if group else 'INDIVIDUAL'
        return vCalAddress(f'CUTYPE={cutype};ROLE={role};PARTSTAT={status};CN={name};MAILTO:{mail}')

    def save(self, directory: str):
        for g, n in self.name.items():
            print(f"{self.level} : Creating {n}.ics")
            with open(f'{directory}/{n}.ics', 'wb') as f:
                f.write(self.calendar[g].to_ical())
    
    def get_files_name(self):
        return [f'{self.name[n]}.ics' for n in self.name]

