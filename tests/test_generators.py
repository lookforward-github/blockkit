import pytest
from blockkit.generators import CodeGenerationError, eval_components, generate


def test_generates_section_plain_text():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "This is a plain text section block.",
                    "emoji": True,
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Message, PlainText, Section; Message(blocks=[Section(text=PlainText(text="This is a plain text section block.", emoji=True))])'  # noqa
    )


def test_generates_section_markdown_text():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        "This is a mrkdwn section "
                        "block :ghost: *this is bold*, "
                        "and ~this is crossed out~, "
                        "and <https://google.com|this is a link>"
                    ),
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, Section; Message(blocks=[Section(text=MarkdownText(text="This is a mrkdwn section block :ghost: *this is bold*, and ~this is crossed out~, and <https://google.com|this is a link>"))])'  # noqa
    )


def test_generates_section_text_fields():
    payload = {
        "blocks": [
            {
                "type": "section",
                "fields": [
                    {
                        "type": "plain_text",
                        "text": "*this is plain_text text*",
                        "emoji": True,
                    }
                ],
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Message, PlainText, Section; Message(blocks=[Section(fields=[PlainText(text="*this is plain_text text*", emoji=True)])])'  # noqa
    )


def test_generates_section_static_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick an item from the dropdown list",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                        "emoji": True,
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-0",
                        }
                    ],
                    "action_id": "static_select-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, Option, PlainText, Section, StaticSelect; Message(blocks=[Section(text=MarkdownText(text="Pick an item from the dropdown list"), accessory=StaticSelect(placeholder=PlainText(text="Select an item", emoji=True), options=[Option(text=PlainText(text="*this is plain_text text*", emoji=True), value="value-0")], action_id="static_select-action"))])'  # noqa
    )


def test_generates_section_static_select_option_groups():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Available options",
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Manage",
                    },
                    "action_id": "static_select-action",
                    "option_groups": [
                        {
                            "label": {"type": "plain_text", "text": "Group 1"},
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "*this is plain_text text*",
                                    },
                                    "value": "value-0",
                                }
                            ],
                        },
                        {
                            "label": {"type": "plain_text", "text": "Group 2"},
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "*this is plain_text text*",
                                    },
                                    "value": "value-3",
                                }
                            ],
                        },
                    ],
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, Option, OptionGroup, PlainText, Section, StaticSelect; Message(blocks=[Section(text=MarkdownText(text="Available options"), accessory=StaticSelect(placeholder=PlainText(emoji=True, text="Manage"), action_id="static_select-action", option_groups=[OptionGroup(label=PlainText(text="Group 1"), options=[Option(text=PlainText(text="*this is plain_text text*"), value="value-0")]), OptionGroup(label=PlainText(text="Group 2"), options=[Option(text=PlainText(text="*this is plain_text text*"), value="value-3")])]))])'  # noqa
    )


def test_generates_section_users_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Test block with users select",
                },
                "accessory": {
                    "type": "users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                        "emoji": True,
                    },
                    "action_id": "users_select-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, PlainText, Section, UsersSelect; Message(blocks=[Section(text=MarkdownText(text="Test block with users select"), accessory=UsersSelect(placeholder=PlainText(text="Select a user", emoji=True), action_id="users_select-action"))])'  # noqa
    )


def test_generates_section_channels_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick a channel from the dropdown list",
                },
                "accessory": {
                    "action_id": "text1234",
                    "type": "channels_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                    },
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import ChannelsSelect, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick a channel from the dropdown list"), accessory=ChannelsSelect(action_id="text1234", placeholder=PlainText(text="Select an item")))])'  # noqa
    )


def test_generates_section_conversations():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick a conversation from the dropdown list",
                },
                "accessory": {
                    "action_id": "text1234",
                    "type": "conversations_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                    },
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import ConversationsSelect, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick a conversation from the dropdown list"), accessory=ConversationsSelect(action_id="text1234", placeholder=PlainText(text="Select an item")))])'  # noqa
    )


def test_generates_section_external_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick an item from the dropdown list",
                },
                "accessory": {
                    "action_id": "text1234",
                    "type": "external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item",
                    },
                    "min_query_length": 3,
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import ExternalSelect, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick an item from the dropdown list"), accessory=ExternalSelect(action_id="text1234", placeholder=PlainText(text="Select an item"), min_query_length=3))])'  # noqa
    )


def test_generates_section_multi_static():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {"type": "mrkdwn", "text": "Pick items from the list"},
                "accessory": {
                    "action_id": "text1234",
                    "type": "multi_static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select items",
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                            },
                            "value": "value-0",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                            },
                            "value": "value-1",
                        },
                    ],
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, MultiStaticSelect, Option, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick items from the list"), accessory=MultiStaticSelect(action_id="text1234", placeholder=PlainText(text="Select items"), options=[Option(text=PlainText(text="*this is plain_text text*"), value="value-0"), Option(text=PlainText(text="*this is plain_text text*"), value="value-1")]))])'  # noqa
    )


def test_generates_section_multi_users_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {"type": "mrkdwn", "text": "Pick users from the list"},
                "accessory": {
                    "action_id": "text1234",
                    "type": "multi_users_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select users",
                    },
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, MultiUsersSelect, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick users from the list"), accessory=MultiUsersSelect(action_id="text1234", placeholder=PlainText(text="Select users")))])'  # noqa
    )


def test_generates_section_multi_channels_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick channels from the list",
                },
                "accessory": {
                    "action_id": "text1234",
                    "type": "multi_channels_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select channels",
                    },
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, MultiChannelsSelect, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick channels from the list"), accessory=MultiChannelsSelect(action_id="text1234", placeholder=PlainText(text="Select channels")))])'  # noqa
    )


def test_generates_section_multi_conversations():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Test block with multi conversations select",
                },
                "accessory": {
                    "type": "multi_conversations_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select conversations",
                        "emoji": True,
                    },
                    "action_id": "multi_conversations_select-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, MultiConversationsSelect, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="Test block with multi conversations select"), accessory=MultiConversationsSelect(placeholder=PlainText(text="Select conversations", emoji=True), action_id="multi_conversations_select-action"))])'  # noqa
    )


def test_generates_section_multi_external_select():
    payload = {
        "blocks": [
            {
                "type": "section",
                "block_id": "section678",
                "text": {"type": "mrkdwn", "text": "Pick items from the list"},
                "accessory": {
                    "action_id": "text1234",
                    "type": "multi_external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select items",
                    },
                    "min_query_length": 3,
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, MultiExternalSelect, PlainText, Section; Message(blocks=[Section(block_id="section678", text=MarkdownText(text="Pick items from the list"), accessory=MultiExternalSelect(action_id="text1234", placeholder=PlainText(text="Select items"), min_query_length=3))])'  # noqa
    )


def test_generates_section_button():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with a button.",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "action_id": "button-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Button, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with a button."), accessory=Button(text=PlainText(text="Click Me", emoji=True), value="click_me_123", action_id="button-action"))])'  # noqa
    )


def test_generates_section_button_confirm():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with a button.",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "action_id": "button-action",
                    "confirm": {
                        "title": {
                            "type": "plain_text",
                            "text": "Are you sure?",
                        },
                        "text": {
                            "type": "mrkdwn",
                            "text": "Wouldn't you prefer a good game of _chess_?",
                        },
                        "confirm": {"type": "plain_text", "text": "Do it"},
                        "deny": {
                            "type": "plain_text",
                            "text": "Stop, I've changed my mind!",
                        },
                    },
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Button, Confirm, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with a button."), accessory=Button(text=PlainText(text="Click Me", emoji=True), value="click_me_123", action_id="button-action", confirm=Confirm(title=PlainText(text="Are you sure?"), text=MarkdownText(text="Wouldn\'t you prefer a good game of _chess_?"), confirm=PlainText(text="Do it"), deny=PlainText(text="Stop, I\'ve changed my mind!"))))])'  # noqa
    )


def test_generates_section_link_button():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with a button.",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "url": "https://google.com",
                    "action_id": "button-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Button, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with a button."), accessory=Button(text=PlainText(text="Click Me", emoji=True), value="click_me_123", url="https://google.com", action_id="button-action"))])'  # noqa
    )


def test_generates_section_image():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with a button.",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Click Me",
                        "emoji": True,
                    },
                    "value": "click_me_123",
                    "url": "https://google.com",
                    "action_id": "button-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Button, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with a button."), accessory=Button(text=PlainText(text="Click Me", emoji=True), value="click_me_123", url="https://google.com", action_id="button-action"))])'  # noqa
    )


def test_generates_section_image():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with an accessory image.",
                },
                "accessory": {
                    "type": "image",
                    "image_url": (
                        "https://pbs.twimg.com/profile_images/"
                        "625633822235693056/lNGUneLX_400x400.jpg"
                    ),
                    "alt_text": "cute cat",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Image, MarkdownText, Message, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with an accessory image."), accessory=Image(image_url="https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg", alt_text="cute cat"))])'  # noqa
    )


def test_generates_section_overflow():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with an overflow menu.",
                },
                "accessory": {
                    "type": "overflow",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-0",
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-1",
                        },
                    ],
                    "action_id": "overflow-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, Option, Overflow, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with an overflow menu."), accessory=Overflow(options=[Option(text=PlainText(text="*this is plain_text text*", emoji=True), value="value-0"), Option(text=PlainText(text="*this is plain_text text*", emoji=True), value="value-1")], action_id="overflow-action"))])'  # noqa
    )


def test_generates_section_datepicker():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Pick a date for the deadline.",
                },
                "accessory": {
                    "type": "datepicker",
                    "initial_date": "1990-04-28",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True,
                    },
                    "action_id": "datepicker-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import DatePicker, MarkdownText, Message, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="Pick a date for the deadline."), accessory=DatePicker(initial_date="1990-04-28", placeholder=PlainText(text="Select a date", emoji=True), action_id="datepicker-action"))])'  # noqa
    )


def test_generates_section_checkboxes():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with checkboxes.",
                },
                "accessory": {
                    "type": "checkboxes",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "this is plain text",
                            },
                            "description": {
                                "type": "plain_text",
                                "text": "this is plain text",
                            },
                            "value": "value-0",
                        }
                    ],
                    "action_id": "checkboxes-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Checkboxes, MarkdownText, Message, Option, PlainText, Section; Message(blocks=[Section(text=MarkdownText(text="This is a section block with checkboxes."), accessory=Checkboxes(options=[Option(text=PlainText(text="this is plain text"), description=PlainText(text="this is plain text"), value="value-0")], action_id="checkboxes-action"))])'  # noqa
    )


def test_generates_section_radio_buttons():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Section block with radio buttons",
                },
                "accessory": {
                    "type": "radio_buttons",
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "*this is plain_text text*",
                                "emoji": True,
                            },
                            "value": "value-0",
                        }
                    ],
                    "action_id": "radio_buttons-action",
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import MarkdownText, Message, Option, PlainText, RadioButtons, Section; Message(blocks=[Section(text=MarkdownText(text="Section block with radio buttons"), accessory=RadioButtons(options=[Option(text=PlainText(text="*this is plain_text text*", emoji=True), value="value-0")], action_id="radio_buttons-action"))])'  # noqa
    )


def test_generates_actions_all_selects():
    payload = {
        "blocks": [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a conversation",
                            "emoji": True,
                        },
                        "action_id": "actionId-0",
                    },
                    {
                        "type": "channels_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a channel",
                            "emoji": True,
                        },
                        "action_id": "actionId-1",
                    },
                    {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True,
                        },
                        "action_id": "actionId-2",
                    },
                    {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an item",
                            "emoji": True,
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "*this is plain_text text*",
                                    "emoji": True,
                                },
                                "value": "value-0",
                            }
                        ],
                        "action_id": "actionId-3",
                    },
                ],
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Actions, ChannelsSelect, ConversationsSelect, Message, Option, PlainText, StaticSelect, UsersSelect; Message(blocks=[Actions(elements=[ConversationsSelect(placeholder=PlainText(text="Select a conversation", emoji=True), action_id="actionId-0"), ChannelsSelect(placeholder=PlainText(text="Select a channel", emoji=True), action_id="actionId-1"), UsersSelect(placeholder=PlainText(text="Select a user", emoji=True), action_id="actionId-2"), StaticSelect(placeholder=PlainText(text="Select an item", emoji=True), options=[Option(text=PlainText(text="*this is plain_text text*", emoji=True), value="value-0")], action_id="actionId-3")])])'  # noqa
    )


def test_generates_actions_filtered_conversations_select():
    payload = {
        "blocks": [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select private conversation",
                            "emoji": True,
                        },
                        "filter": {"include": ["private"]},
                        "action_id": "actionId-0",
                    }
                ],
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Actions, ConversationsSelect, Filter, Message, PlainText; Message(blocks=[Actions(elements=[ConversationsSelect(placeholder=PlainText(text="Select private conversation", emoji=True), filter=Filter(include=["private"]), action_id="actionId-0")])])'  # noqa
    )


def test_generates_actions_selects_with_initial():
    payload = {
        "blocks": [
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "conversations_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a conversation",
                            "emoji": True,
                        },
                        "initial_conversation": "G12345678",
                        "action_id": "actionId-0",
                    },
                    {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True,
                        },
                        "initial_user": "U12345678",
                        "action_id": "actionId-1",
                    },
                    {
                        "type": "channels_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a channel",
                            "emoji": True,
                        },
                        "initial_channel": "C12345678",
                        "action_id": "actionId-2",
                    },
                ],
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Actions, ChannelsSelect, ConversationsSelect, Message, PlainText, UsersSelect; Message(blocks=[Actions(elements=[ConversationsSelect(placeholder=PlainText(text="Select a conversation", emoji=True), initial_conversation="G12345678", action_id="actionId-0"), UsersSelect(placeholder=PlainText(text="Select a user", emoji=True), initial_user="U12345678", action_id="actionId-1"), ChannelsSelect(placeholder=PlainText(text="Select a channel", emoji=True), initial_channel="C12345678", action_id="actionId-2")])])'  # noqa
    )


def test_generates_divider():
    assert (
        generate({"blocks": [{"type": "divider"}]})
        == "from blockkit import Divider, Message; Message(blocks=[Divider()])"
    )


def test_generates_image_title():
    payload = {
        "blocks": [
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": "I Need a Marg",
                    "emoji": True,
                },
                "image_url": (
                    "https://assets3.thrillist.com/v1/image/"
                    "1682388/size/tl-horizontal_main.jpg"
                ),
                "alt_text": "marg",
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import ImageBlock, Message, PlainText; Message(blocks=[ImageBlock(title=PlainText(text="I Need a Marg", emoji=True), image_url="https://assets3.thrillist.com/v1/image/1682388/size/tl-horizontal_main.jpg", alt_text="marg")])'  # noqa
    )


def test_generates_image_no_title():
    payload = {
        "blocks": [
            {
                "type": "image",
                "image_url": (
                    "https://i1.wp.com/thetempest.co/wp-content/uploads/2017/08/"
                    "The-wise-words-of-Michael-Scott-Imgur-2.jpg?w=1024&ssl=1"
                ),
                "alt_text": "inspiration",
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import ImageBlock, Message; Message(blocks=[ImageBlock(image_url="https://i1.wp.com/thetempest.co/wp-content/uploads/2017/08/The-wise-words-of-Michael-Scott-Imgur-2.jpg?w=1024&ssl=1", alt_text="inspiration")])'  # noqa
    )


def test_generates_context_plain_text():
    payload = {
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Author: K A Applegate",
                        "emoji": True,
                    }
                ],
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Context, Message, PlainText; Message(blocks=[Context(elements=[PlainText(text="Author: K A Applegate", emoji=True)])])'  # noqa
    )


def test_generates_context_mrkdwn():
    payload = {
        "blocks": [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": (
                            "https://pbs.twimg.com/profile_images/"
                            "625633822235693056/lNGUneLX_400x400.jpg"
                        ),
                        "alt_text": "cute cat",
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Cat* has approved this message.",
                    },
                ],
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Context, Image, MarkdownText, Message; Message(blocks=[Context(elements=[Image(image_url="https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg", alt_text="cute cat"), MarkdownText(text="*Cat* has approved this message.")])])'  # noqa
    )


def test_generates_input_dispatches_actions():
    payload = {
        "blocks": [
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Input, Message, PlainText, PlainTextInput; Message(blocks=[Input(dispatch_action=True, element=PlainTextInput(action_id="plain_text_input-action"), label=PlainText(text="Label", emoji=True))])'  # noqa
    )


def test_generates_input_dispatches_custom_actions():
    payload = {
        "blocks": [
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "dispatch_action_config": {
                        "trigger_actions_on": ["on_character_entered"]
                    },
                    "action_id": "plain_text_input-action",
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import DispatchActionConfig, Input, Message, PlainText, PlainTextInput; Message(blocks=[Input(dispatch_action=True, element=PlainTextInput(dispatch_action_config=DispatchActionConfig(trigger_actions_on=["on_character_entered"]), action_id="plain_text_input-action"), label=PlainText(text="Label", emoji=True))])'  # noqa
    )


def test_generates_input_multiline_plain_text():
    payload = {
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "plain_text_input-action",
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Input, Message, PlainText, PlainTextInput; Message(blocks=[Input(element=PlainTextInput(multiline=True, action_id="plain_text_input-action"), label=PlainText(text="Label", emoji=True))])'  # noqa
    )


def test_generates_input_plain_text():
    payload = {
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action",
                },
                "label": {"type": "plain_text", "text": "Label", "emoji": True},
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Input, Message, PlainText, PlainTextInput; Message(blocks=[Input(element=PlainTextInput(action_id="plain_text_input-action"), label=PlainText(text="Label", emoji=True))])'  # noqa
    )


def test_generates_header():
    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "This is a header block",
                    "emoji": True,
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Header, Message, PlainText; Message(blocks=[Header(text=PlainText(text="This is a header block", emoji=True))])'  # noqa
    )


def test_generates_modal():
    payload = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "My App", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "This is a plain text section block.",
                    "emoji": True,
                },
            }
        ],
    }
    assert (
        generate(payload)
        == 'from blockkit import Modal, PlainText, Section; Modal(title=PlainText(text="My App", emoji=True), submit=PlainText(text="Submit", emoji=True), close=PlainText(text="Cancel", emoji=True), blocks=[Section(text=PlainText(text="This is a plain text section block.", emoji=True))])'  # noqa
    )


def test_generates_app_home():
    payload = {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "This is a plain text section block.",
                    "emoji": True,
                },
            }
        ],
    }
    assert (
        generate(payload)
        == 'from blockkit import Home, PlainText, Section; Home(blocks=[Section(text=PlainText(text="This is a plain text section block.", emoji=True))])'  # noqa
    )


def test_generates_escape():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "This is a plain\n\ttext section block.",
                    "emoji": True,
                },
            }
        ]
    }
    assert (
        generate(payload)
        == 'from blockkit import Message, PlainText, Section; Message(blocks=[Section(text=PlainText(text="This is a plain\\n\\ttext section block.", emoji=True))])'  # noqa
    )


def test_raises_exception_on_incorrect_block_type():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "incorrect",
                    "text": "This is a mrkdwn section block :ghost: *this is bold*",
                },
            }
        ]
    }
    with pytest.raises(CodeGenerationError):
        generate(payload)


def test_raises_exception_on_empty_accessory():
    payload = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "This is a section block with a button.",
                },
                "accessory": {},
            }
        ]
    }
    with pytest.raises(CodeGenerationError):
        generate(payload)


def test_raises_exception_on_validation():
    with pytest.raises(TypeError):
        eval_components(
            'Message(blocks=[Section(text=MarkdownText(text="This is a plain text section block.", emoji="True"))])'  # noqa
        )
