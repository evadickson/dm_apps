from dm_apps.emails import Email
generic_email = "DFO.PAC.SGCM-MSCS.PAC.MPO@dfo-mpo.gc.ca"


class FeedBackEmail(Email):
    email_template_path = 'spot/emails/email_template.html'

    def get_recipient_list(self):
        return [generic_email]

    def get_subject_en(self):
        return self.instance.subject

    def get_from_email(self):
        return self.instance.sent_by.username

    def get_message_en(self):
        return self.instance.comment
