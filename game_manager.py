
# manages the game flow, including the memory phase, building phase and scoring

from direct.showbase.ShowBaseGlobal import globalClock
from generator import Generator


class GameManager:
    def __init__(self, app):
        self.app = app
        self.island = app.island
        self.block_manager = self.island.block_manager
        self.ui = app.ui

        self.generator = Generator(self.block_manager)

        # these are the durations of the two game phases, in seconds
        self.memory_duration = 20
        self.build_duration = 40

        # the current phase determines whether the player can interact with blocks
        self.phase = "memory"
        self.can_build = False

        # this dictionary stores the correct structure independently of the visible blocks
        self.solution = {}

        # the score is filled in after the building phase ends
        self.score = None

        # these attributes are used to calculate the remaining time
        self.phase_start_time = 0
        self.phase_duration = 0

        self.createStructure()

        # display the initial phase and start its countdown
        self.ui.updatePhase("memorize")
        self.startCountdown(self.memory_duration)

        # schedule the end of the memory phase
        self.app.taskMgr.doMethodLater(
            self.memory_duration,
            self.startBuildPhase,
            "memory_phase_end"
        )

    def createStructure(self):
        # generate returns a dictionary containing positions and colors
        self.solution = self.generator.generate()

        # display the generated structure so the player can memorize it
        self.generator.build(self.solution)

    def startCountdown(self, duration):
        # remember when this phase started and how long it lasts
        self.phase_start_time = globalClock.getFrameTime()
        self.phase_duration = duration

        # show the full duration immediately
        self.ui.updateTimer(duration)

        # update the displayed time while the phase is running
        self.app.taskMgr.add(
            self.updateCountdown,
            "game_countdown"
        )

    def updateCountdown(self, task):
        # calculate how many seconds have passed since the phase started
        elapsed = globalClock.getFrameTime() - self.phase_start_time

        # round up so the display shows the remaining whole seconds
        remaining = max(0, int(self.phase_duration - elapsed + 0.999))

        self.ui.updateTimer(remaining)

        return task.cont

    def startBuildPhase(self, task):
        # stop the previous phase's countdown
        self.app.taskMgr.remove("game_countdown")

        # remove the visible structure, but keep the solution dictionary
        self.block_manager.removeAllBlocks()

        self.phase = "build"
        self.can_build = True

        # update the UI for the building phase
        self.ui.updatePhase("rebuild")
        self.startCountdown(self.build_duration)

        # schedule the end of the building phase
        self.app.taskMgr.doMethodLater(
            self.build_duration,
            self.finishBuildPhase,
            "build_phase_end"
        )

        return task.done

    def finishBuildPhase(self, task):
        # stop the countdown and prevent further changes
        self.app.taskMgr.remove("game_countdown")

        self.can_build = False
        self.phase = "finished"

        # show that the round has ended and the timer has run out
        self.ui.updatePhase("score")
        self.ui.updateTimer(0)

        # calculate the score and pass it to the UI for display
        self.score = self.evaluate()
        self.ui.showScore(self.score)

        return task.done

    def evaluate(self):
        score = 0

        # check every block the player actually placed
        for pos, block in self.block_manager.blocks.items():

            # blocks outside the solution receive a penalty
            if pos not in self.solution:
                score -= 0.5
                continue

            # a correct position awards one point
            score += 1

            # the color point is only awarded at the correct position
            if block.color == self.solution[pos]:
                score += 1

        # missing blocks receive no points and no direct penalty
        return score

