from apps.common.views.iommi_prototype import Page, Table, Form, html
from apps.event.models import AbstractEvent as Event

class EventPage(Page):
    # title = html.h1('Events')
    # subtitle_text = 'This is subtitle text'

    sources = Table(auto__model=Event, page_size=10)
    create_source = Form.create(auto__model=Event)
