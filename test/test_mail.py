# -*- coding: utf-8 -*-
import json
import unittest

try:
    from email.message import EmailMessage
except ImportError:
    # Python2
    from email import message
    EmailMessage = message.Message

from sendgrid.helpers.mail import (
    Asm,
    ApiKeyIncludedException,
    Attachment,
    BccSettings,
    BypassListManagement,
    Category,
    ClickTracking,
    Content,
    CustomArg,
    Email,
    FooterSettings,
    Ganalytics,
    Header,
    Mail,
    MailSettings,
    OpenTracking,
    Personalization,
    SandBoxMode,
    Section,
    SendGridException,
    SpamCheck,
    SubscriptionTracking,
    Substitution,
    TrackingSettings,
    ValidateApiKey
)


class UnitTests(unittest.TestCase):

    def test_sendgrid_api_key(self):
        """Tests if including SendGrid API will throw an Exception"""

        # Minimum required to send an email
        self.max_diff = None
        mail = Mail()

        mail.from_email = Email("test@example.com")

        mail.subject = "Hello World from the SendGrid Python Library"

        personalization = Personalization()
        personalization.add_to(Email("test@example.com"))
        mail.add_personalization(personalization)

        # Try to include SendGrid API key
        try:
            mail.add_content(Content("text/plain", "some SG.2123b1B.1212lBaC here"))
            mail.add_content(
                Content(
                    "text/html",
                    "<html><body>some SG.Ba2BlJSDba.232Ln2 here</body></html>"))

            self.assertEqual(
                json.dumps(
                    mail.get(),
                    sort_keys=True),
                '{"content": [{"type": "text/plain", "value": "some text here"}, '
                '{"type": "text/html", '
                '"value": "<html><body>some text here</body></html>"}], '
                '"from": {"email": "test@example.com"}, "personalizations": '
                '[{"to": [{"email": "test@example.com"}]}], '
                '"subject": "Hello World from the SendGrid Python Library"}'
            )

        # Exception should be thrown
        except Exception as e:
            pass

        # Exception not thrown
        else:
            self.fail("Should have failed as SendGrid API key included")

    # Send a Single Email to a Single Recipient
    def test_single_email_to_a_single_recipient(self):
        from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent
        self.maxDiff = None
        message = Mail(from_email=From('test+from@example.com', 'Example From Name'),
               to_emails=To('test+to@example.com', 'Example To Name'),
               subject=Subject('Sending with SendGrid is Fun'),
               plain_text_content=PlainTextContent('and easy to do anywhere, even with Python'),
               html_content=HtmlContent('<strong>and easy to do anywhere, even with Python</strong>'))

        self.assertEqual(
            message.get(),
            json.loads(r'''{
                "content": [
                    {
                        "type": "text/plain", 
                        "value": "and easy to do anywhere, even with Python"
                    }, 
                    {
                        "type": "text/html", 
                        "value": "<strong>and easy to do anywhere, even with Python</strong>"
                    }
                ], 
                "from": {
                    "email": "test+from@example.com", 
                    "name": "Example From Name"
                }, 
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": "test+to@example.com", 
                                "name": "Example To Name"
                            }
                        ]
                    }
                ], 
                "subject": "Sending with SendGrid is Fun"
            }''')
        )

    def test_single_email_to_a_single_recipient_content_reversed(self):
        """Tests bug found in Issue-451 with Content ordering causing a crash"""
        from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent
        self.maxDiff = None
        message = Mail()
        message.from_email = From('test+from@example.com', 'Example From Name')
        message.to = To('test+to@example.com', 'Example To Name')
        message.subject = Subject('Sending with SendGrid is Fun')
        message.content = HtmlContent('<strong>and easy to do anywhere, even with Python</strong>')
        message.content = PlainTextContent('and easy to do anywhere, even with Python')

        self.assertEqual(
            message.get(),
            json.loads(r'''{
                "content": [
                    {
                        "type": "text/plain", 
                        "value": "and easy to do anywhere, even with Python"
                    }, 
                    {
                        "type": "text/html", 
                        "value": "<strong>and easy to do anywhere, even with Python</strong>"
                    }
                ], 
                "from": {
                    "email": "test+from@example.com", 
                    "name": "Example From Name"
                }, 
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": "test+to@example.com", 
                                "name": "Example To Name"
                            }
                        ]
                    }
                ], 
                "subject": "Sending with SendGrid is Fun"
            }''')
        )

    def test_send_a_single_email_to_multiple_recipients(self):
        from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent
        self.maxDiff = None
        to_emails = [
            To('test+to0@example.com', 'Example To Name 0'),
            To('test+to1@example.com', 'Example To Name 1')
        ]
        message = Mail(from_email=From('test+from@example.com', 'Example From Name'),
                    to_emails=to_emails,
                    subject=Subject('Sending with SendGrid is Fun'),
                    plain_text_content=PlainTextContent('and easy to do anywhere, even with Python'),
                    html_content=HtmlContent('<strong>and easy to do anywhere, even with Python</strong>'))

        self.assertEqual(
            message.get(),
            json.loads(r'''{
                "content": [
                    {
                        "type": "text/plain", 
                        "value": "and easy to do anywhere, even with Python"
                    }, 
                    {
                        "type": "text/html", 
                        "value": "<strong>and easy to do anywhere, even with Python</strong>"
                    }
                ], 
                "from": {
                    "email": "test+from@example.com", 
                    "name": "Example From Name"
                }, 
                "personalizations": [
                    {
                        "to": [
                            {
                                "email": "test+to0@example.com", 
                                "name": "Example To Name 0"
                            }, 
                            {
                                "email": "test+to1@example.com", 
                                "name": "Example To Name 1"
                            }
                        ]
                    }
                ], 
                "subject": "Sending with SendGrid is Fun"
            }''')
        )
    
    def test_multiple_emails_to_multiple_recipients(self):
        from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException, Substitution
        self.maxDiff = None

        to_emails = [
            To(email='test+to0@example.com',
            name='Example Name 0',
            substitutions={
                Substitution('-name-', 'Example Name Substitution 0'),
                Substitution('-github-', 'https://example.com/test0'),
            },
            subject=Subject('Override Global Subject')),
            To(email='test+to1@example.com',
            name='Example Name 1',
            substitutions={
                Substitution('-name-', 'Example Name Substitution 1'),
                Substitution('-github-', 'https://example.com/test1'),
            })
        ]
        global_substitutions = Substitution('-time-', '2019-01-01 00:00:00')
        message = Mail(from_email=From('test+from@example.com', 'Example From Name'),
                    to_emails=to_emails,
                    subject=Subject('Hi -name-'),
                    plain_text_content=PlainTextContent('Hello -name-, your URL is -github-, email sent at -time-'),
                    html_content=HtmlContent('<strong>Hello -name-, your URL is <a href=\"-github-\">here</a></strong> email sent at -time-'),
                    global_substitutions=global_substitutions,
                    is_multiple=True)
    
        self.assertEqual(
            message.get(),
            json.loads(r'''{
                "content": [
                    {
                        "type": "text/plain", 
                        "value": "Hello -name-, your URL is -github-, email sent at -time-"
                    }, 
                    {
                        "type": "text/html", 
                        "value": "<strong>Hello -name-, your URL is <a href=\"-github-\">here</a></strong> email sent at -time-"
                    }
                ], 
                "from": {
                    "email": "test+from@example.com", 
                    "name": "Example From Name"
                }, 
                "personalizations": [
                    {
                        "substitutions": {
                            "-github-": "https://example.com/test1", 
                            "-name-": "Example Name Substitution 1", 
                            "-time-": "2019-01-01 00:00:00"
                        }, 
                        "to": [
                            {
                                "email": "test+to1@example.com", 
                                "name": "Example Name 1"
                            }
                        ]
                    }, 
                    {
                        "substitutions": {
                            "-github-": "https://example.com/test0", 
                            "-name-": "Example Name Substitution 0", 
                            "-time-": "2019-01-01 00:00:00"
                        }, 
                        "to": [
                            {
                                "email": "test+to0@example.com", 
                                "name": "Example Name 0"
                            }
                        ]
                    }
                ], 
                "subject": "Hi -name-"
            }''')
        )

    def test_kitchen_sink(self):
        from sendgrid.helpers.mail import (
            Mail, From, To, Cc, Bcc, Subject, PlainTextContent, 
            HtmlContent, SendGridException, Substitution, 
            Header, CustomArg, SendAt, Content, MimeType, Attachment,
            FileName, FileContent, FileType, Disposition, ContentId,
            TemplateId, Section, ReplyTo, Category, BatchId, Asm,
            GroupId, GroupsToDisplay, IpPoolName, MailSettings,
            BccSettings, BccSettingsEmail, BypassListManagement,
            FooterSettings, FooterText, FooterHtml, SandBoxMode,
            SpamCheck, SpamThreshold, SpamUrl, TrackingSettings,
            ClickTracking, SubscriptionTracking, SubscriptionText,
            SubscriptionHtml, SubscriptionSubstitutionTag,
            OpenTracking, OpenTrackingSubstitutionTag, Ganalytics,
            UtmSource, UtmMedium, UtmTerm, UtmContent, UtmCampaign)
        import time
        import datetime
        self.maxDiff = None

        message = Mail()

        # Define Personalizations 

        message.to = To('test1@sendgrid.com', 'Example User1', p=0)
        message.to = [ 
            To('test2@sendgrid.com', 'Example User2', p=0),
            To('test3@sendgrid.com', 'Example User3', p=0)
        ]

        message.cc = Cc('test4@example.com', 'Example User4', p=0)
        message.cc = [ 
            Cc('test5@example.com', 'Example User5', p=0),
            Cc('test6@example.com', 'Example User6', p=0)
        ]

        message.bcc = Bcc('test7@example.com', 'Example User7', p=0)
        message.bcc = [ 
            Bcc('test8@example.com', 'Example User8', p=0),
            Bcc('test9@example.com', 'Example User9', p=0)
        ]

        message.subject = Subject('Sending with SendGrid is Fun 0', p=0)

        message.header = Header('X-Test1', 'Test1', p=0)
        message.header = Header('X-Test2', 'Test2', p=0)
        message.header = [
            Header('X-Test3', 'Test3', p=0),
            Header('X-Test4', 'Test4', p=0)
        ]

        message.substitution = Substitution('%name1%', 'Example Name 1', p=0)
        message.substitution = Substitution('%city1%', 'Example City 1', p=0)
        message.substitution = [
            Substitution('%name2%', 'Example Name 2', p=0),
            Substitution('%city2%', 'Example City 2', p=0)
        ]

        message.custom_arg = CustomArg('marketing1', 'true', p=0)
        message.custom_arg = CustomArg('transactional1', 'false', p=0)
        message.custom_arg = [
            CustomArg('marketing2', 'false', p=0),
            CustomArg('transactional2', 'true', p=0)
        ]

        message.send_at = SendAt(1461775051, p=0)

        message.to = To('test10@example.com', 'Example User10', p=1)
        message.to = [ 
            To('test11@example.com', 'Example User11', p=1),
            To('test12@example.com', 'Example User12', p=1)
        ]

        message.cc = Cc('test13@example.com', 'Example User13', p=1)
        message.cc = [ 
            Cc('test14@example.com', 'Example User14', p=1),
            Cc('test15@example.com', 'Example User15', p=1)
        ]

        message.bcc = Bcc('test16@example.com', 'Example User16', p=1)
        message.bcc = [ 
            Bcc('test17@example.com', 'Example User17', p=1),
            Bcc('test18@example.com', 'Example User18', p=1)
        ]

        message.header = Header('X-Test5', 'Test5', p=1)
        message.header = Header('X-Test6', 'Test6', p=1)
        message.header = [
            Header('X-Test7', 'Test7', p=1),
            Header('X-Test8', 'Test8', p=1)
        ]

        message.substitution = Substitution('%name3%', 'Example Name 3', p=1)
        message.substitution = Substitution('%city3%', 'Example City 3', p=1)
        message.substitution = [
            Substitution('%name4%', 'Example Name 4', p=1),
            Substitution('%city4%', 'Example City 4', p=1)
        ]

        message.custom_arg = CustomArg('marketing3', 'true', p=1)
        message.custom_arg = CustomArg('transactional3', 'false', p=1)
        message.custom_arg = [
            CustomArg('marketing4', 'false', p=1),
            CustomArg('transactional4', 'true', p=1)
        ]

        message.send_at = SendAt(1461775052, p=1)

        message.subject = Subject('Sending with SendGrid is Fun 1', p=1)

        # The values below this comment are global to entire message

        message.from_email = From('dx@sendgrid.com', 'DX')

        message.reply_to = ReplyTo('dx_reply@sendgrid.com', 'DX Reply')

        message.subject = Subject('Sending with SendGrid is Fun 2')

        message.content = Content(MimeType.text, 'and easy to do anywhere, even with Python')
        message.content = Content(MimeType.html, '<strong>and easy to do anywhere, even with Python</strong>')
        message.content = [
            Content('text/calendar', 'Party Time!!'),
            Content('text/custom', 'Party Time 2!!')
        ]

        message.attachment = Attachment(FileContent('base64 encoded content 1'),
                                        FileType('application/pdf'),
                                        FileName('balance_001.pdf'),
                                        Disposition('attachment'),
                                        ContentId('Content ID 1'))
        message.attachment = [
            Attachment(FileContent('base64 encoded content 2'),
                    FileType('image/png'),
                    FileName('banner.png'),
                    Disposition('inline'),
                    ContentId('Content ID 2')),
            Attachment(FileContent('base64 encoded content 3'),
                    FileType('image/png'),
                    FileName('banner2.png'),
                    Disposition('inline'),
                    ContentId('Content ID 3'))
        ]

        message.template_id = TemplateId('13b8f94f-bcae-4ec6-b752-70d6cb59f932')

        message.section = Section('%section1%', 'Substitution for Section 1 Tag')
        message.section = [
            Section('%section2%', 'Substitution for Section 2 Tag'),
            Section('%section3%', 'Substitution for Section 3 Tag')    
        ]

        message.header = Header('X-Test9', 'Test9')
        message.header = Header('X-Test10', 'Test10')
        message.header = [
            Header('X-Test11', 'Test11'),
            Header('X-Test12', 'Test12')
        ]

        message.category = Category('Category 1')
        message.category = Category('Category 2')
        message.category = [
            Category('Category 1'),
            Category('Category 2')
        ]

        message.custom_arg = CustomArg('marketing5', 'false')
        message.custom_arg = CustomArg('transactional5', 'true')
        message.custom_arg = [
            CustomArg('marketing6', 'true'),
            CustomArg('transactional6', 'false')
        ]

        message.send_at = SendAt(1461775053)

        message.batch_id = BatchId("HkJ5yLYULb7Rj8GKSx7u025ouWVlMgAi")

        message.asm = Asm(GroupId(1), GroupsToDisplay([1,2,3,4]))

        message.ip_pool_name = IpPoolName("IP Pool Name")

        mail_settings = MailSettings()
        mail_settings.bcc_settings = BccSettings(False, BccSettingsEmail("bcc@twilio.com"))
        mail_settings.bypass_list_management = BypassListManagement(False)
        mail_settings.footer_settings = FooterSettings(True, FooterText("w00t"), FooterHtml("<string>w00t!<strong>"))
        mail_settings.sandbox_mode = SandBoxMode(True)
        mail_settings.spam_check = SpamCheck(True, SpamThreshold(5), SpamUrl("https://example.com"))
        message.mail_settings = mail_settings

        tracking_settings = TrackingSettings()
        tracking_settings.click_tracking = ClickTracking(True, False)
        tracking_settings.open_tracking = OpenTracking(True, OpenTrackingSubstitutionTag("open_tracking"))
        tracking_settings.subscription_tracking = SubscriptionTracking(
            True, 
            SubscriptionText("Goodbye"),
            SubscriptionHtml("<strong>Goodbye!</strong>"),
            SubscriptionSubstitutionTag("unsubscribe"))
        tracking_settings.ganalytics = Ganalytics(
            True,
            UtmSource("utm_source"),
            UtmMedium("utm_medium"),
            UtmTerm("utm_term"),
            UtmContent("utm_content"),
            UtmCampaign("utm_campaign"))
        message.tracking_settings = tracking_settings
        self.assertEqual(
            message.get(),
            json.loads(r'''{
                "asm": {
                    "group_id": 1, 
                    "groups_to_display": [
                        1, 
                        2, 
                        3, 
                        4
                    ]
                }, 
                "attachments": [
                    {
                        "content": "base64 encoded content 3", 
                        "content_id": "Content ID 3", 
                        "disposition": "inline", 
                        "filename": "banner2.png", 
                        "type": "image/png"
                    }, 
                    {
                        "content": "base64 encoded content 2", 
                        "content_id": "Content ID 2", 
                        "disposition": "inline", 
                        "filename": "banner.png", 
                        "type": "image/png"
                    }, 
                    {
                        "content": "base64 encoded content 1", 
                        "content_id": "Content ID 1", 
                        "disposition": "attachment", 
                        "filename": "balance_001.pdf", 
                        "type": "application/pdf"
                    }
                ], 
                "batch_id": "HkJ5yLYULb7Rj8GKSx7u025ouWVlMgAi", 
                "categories": [
                    "Category 2", 
                    "Category 1", 
                    "Category 2", 
                    "Category 1"
                ], 
                "content": [
                    {
                        "type": "text/plain", 
                        "value": "and easy to do anywhere, even with Python"
                    }, 
                    {
                        "type": "text/html", 
                        "value": "<strong>and easy to do anywhere, even with Python</strong>"
                    }, 
                    {
                        "type": "text/calendar", 
                        "value": "Party Time!!"
                    }, 
                    {
                        "type": "text/custom", 
                        "value": "Party Time 2!!"
                    }
                ], 
                "custom_args": {
                    "marketing5": "false", 
                    "marketing6": "true", 
                    "transactional5": "true", 
                    "transactional6": "false"
                }, 
                "from": {
                    "email": "dx@sendgrid.com", 
                    "name": "DX"
                }, 
                "headers": {
                    "X-Test10": "Test10", 
                    "X-Test11": "Test11", 
                    "X-Test12": "Test12", 
                    "X-Test9": "Test9"
                }, 
                "ip_pool_name": "IP Pool Name", 
                "mail_settings": {
                    "bcc": {
                        "email": "bcc@twilio.com", 
                        "enable": false
                    }, 
                    "bypass_list_management": {
                        "enable": false
                    }, 
                    "footer": {
                        "enable": true, 
                        "html": "<string>w00t!<strong>", 
                        "text": "w00t"
                    }, 
                    "sandbox_mode": {
                        "enable": true
                    }, 
                    "spam_check": {
                        "enable": true, 
                        "post_to_url": "https://example.com", 
                        "threshold": 5
                    }
                }, 
                "personalizations": [
                    {
                        "bcc": [
                            {
                                "email": "test7@example.com", 
                                "name": "Example User7"
                            }, 
                            {
                                "email": "test8@example.com", 
                                "name": "Example User8"
                            }, 
                            {
                                "email": "test9@example.com", 
                                "name": "Example User9"
                            }
                        ], 
                        "cc": [
                            {
                                "email": "test4@example.com", 
                                "name": "Example User4"
                            }, 
                            {
                                "email": "test5@example.com", 
                                "name": "Example User5"
                            }, 
                            {
                                "email": "test6@example.com", 
                                "name": "Example User6"
                            }
                        ], 
                        "custom_args": {
                            "marketing1": "true", 
                            "marketing2": "false", 
                            "transactional1": "false", 
                            "transactional2": "true"
                        }, 
                        "headers": {
                            "X-Test1": "Test1", 
                            "X-Test2": "Test2", 
                            "X-Test3": "Test3", 
                            "X-Test4": "Test4"
                        }, 
                        "send_at": 1461775051, 
                        "subject": "Sending with SendGrid is Fun 0", 
                        "substitutions": {
                            "%city1%": "Example City 1", 
                            "%city2%": "Example City 2", 
                            "%name1%": "Example Name 1", 
                            "%name2%": "Example Name 2"
                        }, 
                        "to": [
                            {
                                "email": "test1@sendgrid.com", 
                                "name": "Example User1"
                            }, 
                            {
                                "email": "test2@sendgrid.com", 
                                "name": "Example User2"
                            }, 
                            {
                                "email": "test3@sendgrid.com", 
                                "name": "Example User3"
                            }
                        ]
                    }, 
                    {
                        "bcc": [
                            {
                                "email": "test16@example.com", 
                                "name": "Example User16"
                            }, 
                            {
                                "email": "test17@example.com", 
                                "name": "Example User17"
                            }, 
                            {
                                "email": "test18@example.com", 
                                "name": "Example User18"
                            }
                        ], 
                        "cc": [
                            {
                                "email": "test13@example.com", 
                                "name": "Example User13"
                            }, 
                            {
                                "email": "test14@example.com", 
                                "name": "Example User14"
                            }, 
                            {
                                "email": "test15@example.com", 
                                "name": "Example User15"
                            }
                        ], 
                        "custom_args": {
                            "marketing3": "true", 
                            "marketing4": "false", 
                            "transactional3": "false", 
                            "transactional4": "true"
                        }, 
                        "headers": {
                            "X-Test5": "Test5", 
                            "X-Test6": "Test6", 
                            "X-Test7": "Test7", 
                            "X-Test8": "Test8"
                        }, 
                        "send_at": 1461775052, 
                        "subject": "Sending with SendGrid is Fun 1", 
                        "substitutions": {
                            "%city3%": "Example City 3", 
                            "%city4%": "Example City 4", 
                            "%name3%": "Example Name 3", 
                            "%name4%": "Example Name 4"
                        }, 
                        "to": [
                            {
                                "email": "test10@example.com", 
                                "name": "Example User10"
                            }, 
                            {
                                "email": "test11@example.com", 
                                "name": "Example User11"
                            }, 
                            {
                                "email": "test12@example.com", 
                                "name": "Example User12"
                            }
                        ]
                    }
                ], 
                "reply_to": {
                    "email": "dx_reply@sendgrid.com", 
                    "name": "DX Reply"
                }, 
                "sections": {
                    "%section1%": "Substitution for Section 1 Tag", 
                    "%section2%": "Substitution for Section 2 Tag", 
                    "%section3%": "Substitution for Section 3 Tag"
                }, 
                "send_at": 1461775053, 
                "subject": "Sending with SendGrid is Fun 2", 
                "template_id": "13b8f94f-bcae-4ec6-b752-70d6cb59f932", 
                "tracking_settings": {
                    "click_tracking": {
                        "enable": true, 
                        "enable_text": false
                    }, 
                    "ganalytics": {
                        "enable": true, 
                        "utm_campaign": "utm_campaign", 
                        "utm_content": "utm_content", 
                        "utm_medium": "utm_medium", 
                        "utm_source": "utm_source", 
                        "utm_term": "utm_term"
                    }, 
                    "open_tracking": {
                        "enable": true, 
                        "substitution_tag": "open_tracking"
                    }, 
                    "subscription_tracking": {
                        "enable": true, 
                        "html": "<strong>Goodbye!</strong>", 
                        "substitution_tag": "unsubscribe", 
                        "text": "Goodbye"
                    }
                }
            }''')
        )

    def test_unicode_values_in_substitutions_helper(self):
        return
        # """ Test that the Substitutions helper accepts unicode values """

        # self.max_diff = None

        # """Minimum required to send an email"""
        # mail = Mail()

        # mail.from_email = Email("test@example.com")

        # mail.subject = "Testing unicode substitutions with the SendGrid Python Library"

        # personalization = Personalization()
        # personalization.add_to(Email("test@example.com"))
        # personalization.add_substitution(Substitution("%city%", u"Αθήνα"))
        # mail.add_personalization(personalization)

        # mail.add_content(Content("text/plain", "some text here"))
        # mail.add_content(
        #     Content(
        #         "text/html",
        #         "<html><body>some text here</body></html>"))

        # expected_result = {
        #     "content": [
        #         {
        #             "type": "text/plain",
        #             "value": "some text here"
        #         },
        #         {
        #             "type": "text/html",
        #             "value": "<html><body>some text here</body></html>"
        #         }
        #     ],
        #     "from": {
        #         "email": "test@example.com"
        #     },
        #     "personalizations": [
        #         {
        #             "substitutions": {
        #                 "%city%": u"Αθήνα"
        #             },
        #             "to": [
        #                 {
        #                     "email": "test@example.com"
        #                 }
        #             ]
        #         }
        #     ],
        #     "subject": "Testing unicode substitutions with the SendGrid Python Library",
        # }

        # self.assertEqual(
        #     json.dumps(mail.get(), sort_keys=True),
        #     json.dumps(expected_result, sort_keys=True)
        # )

    def test_asm_display_group_limit(self):
        return
        # self.assertRaises(ValueError, Asm, 1, list(range(26)))

    def test_disable_tracking(self):
        return
        # tracking_settings = TrackingSettings()
        # tracking_settings.click_tracking = ClickTracking(False, False)

        # self.assertEqual(
        #     tracking_settings.get(),
        #     {'click_tracking': {'enable': False, 'enable_text': False}}
        # )

    def test_directly_setting_substitutions(self):
        return
        # personalization = Personalization()
        # personalization.substitutions = [{'a': 0}]

    def test_from_emailmessage(self):
        return
        # message = EmailMessage()
        # body = 'message that is not urgent'
        # try:
        #     message.set_content(body)
        # except AttributeError:
        #     # Python2
        #     message.set_payload(body)
        # message.set_default_type('text/plain')
        # message['Subject'] = 'URGENT TITLE'
        # message['From'] = 'test@example.com'
        # message['To'] = 'test@sendgrid.com'
        # mail = Mail.from_EmailMessage(message)
        # self.assertEqual(mail.subject.get(), 'URGENT TITLE')
        # self.assertEqual(mail.from_email.email, 'test@example.com')
        # self.assertEqual(len(mail.personalizations), 1)
        # self.assertEqual(len(mail.personalizations[0].tos), 1)
        # self.assertEqual(mail.personalizations[0].tos[0], {'email': 'test@sendgrid.com'})
        # self.assertEqual(len(mail.contents), 1)
        # content = mail.contents[0]
        # self.assertEqual(content.type, 'text/plain')
        # self.assertEqual(content.value, 'message that is not urgent')
