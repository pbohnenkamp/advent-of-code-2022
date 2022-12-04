from dataclasses import dataclass
from sys import stdin


class RockPaperScissorsMove:
    def selection_score(self):
        pass

    def wins_against(self):
        pass

    def will_win(self, opponent_move):
        return opponent_move == self.wins_against()

    def ties_against(self):
        return self

    def will_tie(self, opponent_move):
        return opponent_move == self.ties_against()

    def loses_against(self):
        pass

    def will_lose(self, opponent_move):
        return opponent_move == self.loses_against()

    @staticmethod
    def create_from_strategy_guide_symbol(symbol):
        if symbol.lower() == 'a' or symbol.lower() == 'x':
            return RockMove()
        elif symbol.lower() == 'b' or symbol.lower() == 'y':
            return PaperMove()
        elif symbol.lower() == 'c' or symbol.lower() == 'z':
            return ScissorsMove()
        else:
            raise Exception(f'Unrecognized move symbol: ${symbol}')

    def create_from_desired_outcome_symbol(self, symbol):
        pass

@dataclass(frozen=True)
class RockMove(RockPaperScissorsMove):

    def wins_against(self):
        return ScissorsMove()

    def loses_against(self):
        return PaperMove()

    def selection_score(self):
        return 1

    def __str__(self):
        return "RockMove"


@dataclass(frozen=True)
class PaperMove(RockPaperScissorsMove):

    def wins_against(self):
        return RockMove()

    def loses_against(self):
        return ScissorsMove()

    def selection_score(self):
        return 2

    def __str__(self):
        return "PaperMove"


@dataclass(frozen=True)
class ScissorsMove(RockPaperScissorsMove):

    def wins_against(self):
        return PaperMove()

    def loses_against(self):
        return RockMove()

    def selection_score(self):
        return 3

    def __str__(self):
        return "ScissorsMove"


class StrategyGuideBaseScorer:
    def __init__(self) -> None:
        self._win_outcome_points = 6
        self._tie_outcome_points = 3
        self._loss_outcome_points = 0
        self._total_score = 0
        self._total_rounds = 0

    def total_score(self):
        return self._total_score

    def total_rounds(self):
        return self._total_rounds

    def score_round_from_symbols(self, opponent_move_symbol, scoring_player_move_symbol):
        pass

    def score_round(self, opponent_move, scoring_player_move):
        round_score = 0
        round_score += scoring_player_move.selection_score()
        round_score += self._points_from_outcome(opponent_move, scoring_player_move)
        # print(f'Scored {opponent_move} vs {scoring_player_move} as {round_score}')
        self._total_score += round_score
        self._total_rounds += 1

    @staticmethod
    def _points_from_outcome(opponent_move_symbol, scoring_player_move_symbol):
        if scoring_player_move_symbol.will_win(opponent_move_symbol):
            return 6
        elif scoring_player_move_symbol.will_tie(opponent_move_symbol):
            return 3
        else:
            return 0


class StrategyGuideRecommendedMoveScorer(StrategyGuideBaseScorer):
    def score_round_from_symbols(self, opponent_move_symbol, scoring_player_move_symbol):
        self.score_round(RockPaperScissorsMove.create_from_strategy_guide_symbol(opponent_move_symbol),
                         RockPaperScissorsMove.create_from_strategy_guide_symbol(scoring_player_move_symbol))


class StrategyGuideDesiredOutcomeScorer(StrategyGuideBaseScorer):
    def score_round_from_symbols(self, opponent_move_symbol, desired_outcome_symbol):
        opponent_move = RockPaperScissorsMove.create_from_strategy_guide_symbol(opponent_move_symbol)
        self.score_round(opponent_move,
                         self._map_desired_outcome_to_move(opponent_move, desired_outcome_symbol))

    @staticmethod
    def _map_desired_outcome_to_move(opponent_move, desired_outcome_symbol):
        if desired_outcome_symbol.lower() == 'x':
            return opponent_move.wins_against()
        elif desired_outcome_symbol.lower() == 'y':
            return opponent_move.ties_against()
        else:
            return opponent_move.loses_against()


def score_strategy_guide():
    strategy_guide_recommended_move_scorer = StrategyGuideRecommendedMoveScorer()
    strategy_guide_desired_outcome_scorer = StrategyGuideDesiredOutcomeScorer()
    for line in stdin:
        strategy_guide_recommended_move_scorer.score_round_from_symbols(*line.split())
        strategy_guide_desired_outcome_scorer.score_round_from_symbols(*line.split())

    print('Recommended Move Strategy:')
    print(f'There were {strategy_guide_recommended_move_scorer.total_rounds()} rounds')
    print(f'Your final score would have been {strategy_guide_recommended_move_scorer.total_score()}')
    print('Recommended Move Strategy:')
    print(f'There were {strategy_guide_desired_outcome_scorer.total_rounds()} rounds')
    print(f'Your final score would have been {strategy_guide_desired_outcome_scorer.total_score()}')


if __name__ == '__main__':
    score_strategy_guide()
