from unittest import TestCase
from .strategy_scoring import StrategyGuideRecommendedMoveScorer, RockMove, ScissorsMove, PaperMove, \
    StrategyGuideDesiredOutcomeScorer


class TestRockMove(TestCase):
    def test_equality(self):
        self.assertEqual(RockMove(), RockMove())

    def test_selection_score(self):
        self.assertEqual(1, RockMove().selection_score())

    def test_will_win(self):
        self.assertTrue(RockMove().will_win(ScissorsMove()))
        self.assertFalse(RockMove().will_win(PaperMove()))
        self.assertFalse(RockMove().will_win(RockMove()))

    def test_ties(self):
        self.assertTrue(RockMove().will_tie(RockMove()))
        self.assertFalse(RockMove().will_tie(ScissorsMove()))
        self.assertFalse(RockMove().will_tie(PaperMove()))

    def test_will_lose(self):
        self.assertTrue(RockMove().will_lose(PaperMove()))
        self.assertFalse(RockMove().will_lose(ScissorsMove()))
        self.assertFalse(RockMove().will_lose(RockMove()))


class TestPaperMove(TestCase):
    def test_equality(self):
        self.assertEqual(PaperMove(), PaperMove())

    def test_selection_score(self):
        self.assertEqual(2, PaperMove().selection_score())

    def test_will_win(self):
        self.assertTrue(PaperMove().will_win(RockMove()))
        self.assertFalse(PaperMove().will_win(PaperMove()))
        self.assertFalse(PaperMove().will_win(ScissorsMove()))

    def test_will_tie(self):
        self.assertTrue(PaperMove().will_tie(PaperMove()))
        self.assertFalse(PaperMove().will_tie(ScissorsMove()))
        self.assertFalse(PaperMove().will_tie(RockMove()))

    def test_will_lose(self):
        self.assertTrue(PaperMove().will_lose(ScissorsMove()))
        self.assertFalse(PaperMove().will_lose(RockMove()))
        self.assertFalse(PaperMove().will_lose(PaperMove()))


class TestScissorsMove(TestCase):
    def test_equality(self):
        self.assertEqual(ScissorsMove(), ScissorsMove())

    def test_selection_score(self):
        self.assertEqual(3, ScissorsMove().selection_score())

    def test_will_win(self):
        self.assertTrue(ScissorsMove().will_win(PaperMove()))
        self.assertFalse(ScissorsMove().will_win(ScissorsMove()))
        self.assertFalse(ScissorsMove().will_win(RockMove()))

    def test_will_tie(self):
        self.assertTrue(ScissorsMove().will_tie(ScissorsMove()))
        self.assertFalse(ScissorsMove().will_tie(PaperMove()))
        self.assertFalse(ScissorsMove().will_tie(RockMove()))

    def test_will_lose(self):
        self.assertTrue(ScissorsMove().will_lose(RockMove()))
        self.assertFalse(ScissorsMove().will_lose(PaperMove()))
        self.assertFalse(ScissorsMove().will_lose(ScissorsMove()))


class TestStrategyGuideBaseeScorer(TestCase):
    def test_construction(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        self.assertEqual(0, strategy_guide_scorer.total_score())
        self.assertEqual(0, strategy_guide_scorer.total_rounds())

    def test_score_round_rock_vs_rock(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(RockMove(), RockMove())
        self.assertEqual(4, strategy_guide_scorer.total_score(), '1 point for choosing rock, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_rock_vs_paper(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(RockMove(), PaperMove())
        self.assertEqual(8, strategy_guide_scorer.total_score(), '2 points for choosing paper, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_rock_vs_scissors(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(RockMove(), ScissorsMove())
        self.assertEqual(3, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 0 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_rock(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(PaperMove(), RockMove())
        self.assertEqual(1, strategy_guide_scorer.total_score(), '1 point for choosing rock, 0 points for loss')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_paper(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(PaperMove(), PaperMove())
        self.assertEqual(5, strategy_guide_scorer.total_score(), '2 points for choosing paper, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_scissors(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(PaperMove(), ScissorsMove())
        self.assertEqual(9, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_rock(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(ScissorsMove(), RockMove())
        self.assertEqual(7, strategy_guide_scorer.total_score(), '1 point for choosing rock, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_paper(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(ScissorsMove(), PaperMove())
        self.assertEqual(2, strategy_guide_scorer.total_score(), '2 points for choosing paper, 0 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_scissors(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(ScissorsMove(), ScissorsMove())
        self.assertEqual(6, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 3 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_accumulation(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round(RockMove(), RockMove())
        strategy_guide_scorer.score_round(PaperMove(), RockMove())
        strategy_guide_scorer.score_round(ScissorsMove(), RockMove())
        self.assertEqual(12, strategy_guide_scorer.total_score(),
                         '4 points for rock vs rock, 1 point for paper vs rock, 7 points for scissors vs rock')
        self.assertEqual(3, strategy_guide_scorer.total_rounds())


class TestStrategyGuideRecommendedMoveScorer(TestCase):
    def test_score_round_rock_vs_rock(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('A', 'X')
        self.assertEqual(4, strategy_guide_scorer.total_score(), '1 point for choosing rock, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_rock_vs_paper(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('a', 'Y')
        self.assertEqual(8, strategy_guide_scorer.total_score(), '2 points for choosing paper, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_rock_vs_scissors(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('A', 'Z')
        self.assertEqual(3, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 0 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_rock(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('B', 'x')
        self.assertEqual(1, strategy_guide_scorer.total_score(), '1 point for choosing rock, 0 points for loss')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_paper(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('b', 'y')
        self.assertEqual(5, strategy_guide_scorer.total_score(), '2 points for choosing paper, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_scissors(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('B', 'z')
        self.assertEqual(9, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_rock(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('C', 'X')
        self.assertEqual(7, strategy_guide_scorer.total_score(), '1 point for choosing rock, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_paper(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('c', 'Y')
        self.assertEqual(2, strategy_guide_scorer.total_score(), '2 points for choosing paper, 0 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_scissors(self):
        strategy_guide_scorer = StrategyGuideRecommendedMoveScorer()
        strategy_guide_scorer.score_round_from_symbols('C', 'Z')
        self.assertEqual(6, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 3 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())


class TestStrategyGuideDesiredOutcomeScorer(TestCase):
    def test_score_round_rock_vs_lose(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('A', 'X')
        self.assertEqual(3, strategy_guide_scorer.total_score(), '3 point for choosing scissors, 0 points for loss')

    def test_score_round_rock_vs_tie(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('a', 'Y')
        self.assertEqual(4, strategy_guide_scorer.total_score(), '1 points for choosing rock, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_rock_vs_win(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('A', 'Z')
        self.assertEqual(8, strategy_guide_scorer.total_score(), '2 points for choosing paper, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_lose(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('B', 'X')
        self.assertEqual(1, strategy_guide_scorer.total_score(), '1 point for choosing rock, 0 points for loss')

    def test_score_round_paper_vs_tie(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('b', 'Y')
        self.assertEqual(5, strategy_guide_scorer.total_score(), '2 points for choosing paper, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_paper_vs_win(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('B', 'Z')
        self.assertEqual(9, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_lose(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('C', 'X')
        self.assertEqual(2, strategy_guide_scorer.total_score(), '2 points for choosing paper, 0 points for loss')

    def test_score_round_scissors_vs_tie(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('c', 'Y')
        self.assertEqual(6, strategy_guide_scorer.total_score(), '3 points for choosing scissors, 3 points for tie')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())

    def test_score_round_scissors_vs_win(self):
        strategy_guide_scorer = StrategyGuideDesiredOutcomeScorer()
        strategy_guide_scorer.score_round_from_symbols('C', 'Z')
        self.assertEqual(7, strategy_guide_scorer.total_score(), '1 point for choosing rock, 6 points for win')
        self.assertEqual(1, strategy_guide_scorer.total_rounds())
