from tests.unit_tests.server.fixtures import client, test_club, test_comp


class TestShowSummary:

    club = test_club()[0]
    past_comp = test_comp()[0]

    def test_valid_email_should_return_welcome_page(self, client):
        """
        As we dont have means to assert used templates, we check if our posted email is in response
        """
        valid_email = self.club["email"]
        response = client.post('/showSummary', data={'email': valid_email})
        assert response.status_code == 200
        assert valid_email in response.data.decode()

    def test_invalid_email_should_return_index_page_with_error(self, client):
        """
        As we dont have means to assert used templates, we check if the error message is in response
        """
        invalid_email = 'invalid@simplylift.com'
        response = client.post('/showSummary', data={'email': invalid_email}, follow_redirects=True)
        assert response.status_code == 200
        assert "GUDLFT Registration" in response.data.decode()
        assert 'error' in response.data.decode()

    def test_past_competition_should_not_be_bookable(self, client):
        """
        Check if past competition is unbookable. "Past competition" should be written instead of Booking link
        """
        response = client.post('/showSummary', data={'email': self.club['email']})
        assert response.status_code == 200
        assert "Past competition" in response.data.decode()
        assert self.past_comp['name'] in response.data.decode()


