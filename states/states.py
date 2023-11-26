from aiogram.fsm.state import StatesGroup, State

class MenuStates(StatesGroup):
    menu = State()
    choosing_language = State()

class StartStates(StatesGroup):
    start_choosing_language = State()

class AdminMenuStates(StatesGroup):
    menu = State()
    clubs = State()
    event = State()
    announce = State()

class ClubsStates(StatesGroup):
    #add new club
    enterClubName = State()
    enterClubDescription = State()
    sendClubImage = State()
    enterResidentName = State()
    enterResidentNumber = State()
    enterInstagram = State()

    #delete existent club
    choose_club_to_delete = State()

class EventsStates(StatesGroup):
    enterEventName = State()
    enterEventDescription = State()
    enterEventPlace = State()
    enterEventDate = State()
    enterEventLink = State()
    enterEventIMG = State()
    notifyAllUsers = State()

class AnnounceStates(StatesGroup):
    waiting_for_confirmation = State()

class SuggestSongStates(StatesGroup):
    writingSong = State()