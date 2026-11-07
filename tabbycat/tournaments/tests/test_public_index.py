from django.test import TestCase

from tournaments.models import Round
from utils.misc import reverse_tournament
from utils.tests import CompletedTournamentTestMixin


class PublicCurrentDrawVisibilityTests(CompletedTournamentTestMixin, TestCase):
    view_name = 'tournament-public-index'

    def setUp(self):
        super().setUp()
        self.tournament.preferences['tab_release__team_tab_released'] = True
        self.tournament.preferences['public_features__public_draw'] = 'current'

    def test_current_draw_remains_available_with_released_team_tab(self):
        round = self.tournament.round_set.filter(stage=Round.Stage.PRELIMINARY).order_by('seq').first()
        round.completed = False
        round.draw_status = Round.Status.RELEASED
        round.save(update_fields=['completed', 'draw_status'])

        response = self.get_response(self.view_name)

        self.assertResponseOK(response)
        self.assertContains(response, reverse_tournament('draw-public-current-rounds', self.tournament))

    def test_current_draw_is_not_linked_after_all_rounds_are_complete(self):
        self.tournament.round_set.update(completed=True)

        response = self.get_response(self.view_name)

        self.assertResponseOK(response)
        self.assertNotContains(response, reverse_tournament('draw-public-current-rounds', self.tournament))
