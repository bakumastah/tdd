import requests
import sys
from accounts.models import ListUser


class PersonaAuthenticationBackend:

    def authenticate(self, assertion):
        # Send the assertion to Mozilla's verifier service.
        data = {'assertion': assertion, 'audience': 'localhost'}
        print >> sys.stderr, 'sending to mozilla', data
        resp = requests.post('https://verifier.login.persona.org/verify', data=data)
        print >> sys.stderr, 'got', resp.content

        if resp.ok:
            # Parse the response
            verification_data = resp.json()

            # Check if the assertion was valid
            if verification_data['status'] == 'okay':
                email = verification_data['email']
                try:
                    return self.get_user(email)
                except ListUser.DoesNotExist:
                    return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)
