from collections import namedtuple

GameCreated = namedtuple("GameCreated", "chat code")
GameJoinedPrivate = namedtuple("GameJoinedPrivate", "chat joined_user")
GameJoined = namedtuple("GameJoined", "chat joined_user")
GameNotEnoughParticipants = namedtuple("GameNotEnoughParticipants", "chat participants")

RoundStarted = namedtuple("RoundStarted", "chat participants giving_problem")
RoundDemandProblem = namedtuple("RoundDemandProblem", "chat user reply_context")
RoundAcceptProblem = namedtuple("RoundAcceptProblem", "chat")
RoundNotifyProblem = namedtuple("RoundNotifyProblem", "chat problem")
RoundDemandSolutions = namedtuple("RoundDemandSolutions", "chat problem giving_problem solution_order reply_context")
SolutionAlreadySubmitted = namedtuple("SolutionAlreadySubmitted", "chat solution")
RoundNotFinishedYet = namedtuple("RoundNotFinishedYet", "chat missing_solutions")
RoundSummary = namedtuple("RoundSummary", "chat problem solutions")
RoundRevealed = namedtuple("RoundRevealed", "chat elon_musk")
