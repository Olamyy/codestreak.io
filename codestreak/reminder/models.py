# -*- coding: utf-8 -*-
"""User models."""
import os

from codestreak.database import Column, Model, SurrogatePK, db

from auth0.v2.management import Auth0

# Auth0 API Client
# https://auth0.com/docs/api/management/v2/tokens
auth0_domain = os.environ['AUTH0_DOMAIN']
auth0_token = os.environ['AUTH0_JWT_TOKEN']
auth0 = Auth0(auth0_domain, auth0_token)


class Reminder(SurrogatePK, Model):
    """A settings for a reminder of the app."""

    __tablename__ = 'reminders'
    slug = Column(db.String(255), nullable=False, unique=True, index=True)
    auth_id = Column(db.Text, nullable=False)
    enabled = Column(db.Boolean(), default=True)
    email_enabled = Column(db.Boolean(), default=True)
    time_to_start = Column(db.Integer)

    @classmethod
    def for_username(cls, s):
        return Reminder.query.filter_by(slug=s).first()

    @property
    def email(self):
        # Grab the email address from Auth0.
        return auth0.users.get(self.auth_id)['email']

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Reminder({slug!r})>'.format(slug=self.slug)
